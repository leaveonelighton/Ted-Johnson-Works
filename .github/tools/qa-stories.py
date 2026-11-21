"""Scoped Stories/RSS verification. Requires beautifulsoup4 and feedparser.

Run from the repository root: python .github/tools/qa-stories.py
Preservation compares against the pre-assignment main commit (or --baseline).
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
import feedparser

ROOT = Path(__file__).resolve().parents[2]
ORIGIN = 'https://tedjohnsonworks.com/'
BASELINE = '3dcae4506186675c081c020884782de13ed41626'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--baseline', default=BASELINE)
args = parser.parse_args()
errors = []
checks = Counter()


def check(condition, message):
    checks['assertions'] += 1
    if not condition:
        errors.append(message)


def original(path):
    return subprocess.check_output(['git', 'show', f'{args.baseline}:{path}'], cwd=ROOT).decode()


records = json.loads((ROOT / '.github/tools/stories.json').read_text())
feed = ET.parse(ROOT / 'feed.xml').getroot()
check(feed.tag == 'rss' and feed.get('version') == '2.0', 'RSS version')
channel = feed.find('channel')
for required in ['title', 'link', 'description']:
    check(bool(channel.findtext(required)), f'Missing channel {required}')
items = channel.findall('item')
check(len(items) == len(records), 'Feed inventory count')
check(len({i.findtext('guid') for i in items}) == len(items), 'Duplicate GUIDs')
check(len({i.findtext('link') for i in items}) == len(items), 'Duplicate links')
reader = feedparser.parse((ROOT / 'feed.xml').read_bytes())
check(not reader.bozo and reader.version == 'rss20', 'Independent RSS reader failed')
hub = BeautifulSoup((ROOT / 'stories.html').read_text(), 'html.parser')
sitemap = ET.parse(ROOT / 'sitemap.xml')
locations = [n.text for n in sitemap.findall('.//{*}loc')]
check(len(locations) == len(set(locations)), 'Duplicate sitemap URLs')
old_locations = [n.text for n in ET.fromstring(original('sitemap.xml')).findall('.//{*}loc')]
check(set(old_locations) <= set(locations), 'Historical sitemap URLs removed')
for record, item in zip(records, items):
    path = record['path']
    source = (ROOT / path).read_text()
    soup = BeautifulSoup(source, 'html.parser')
    previous = BeautifulSoup(original(path), 'html.parser')
    canonical = soup.select_one('link[rel="canonical"]')['href']
    check(item.findtext('link') == item.findtext('guid') == canonical == ORIGIN + path, f'{path}: canonical/GUID')
    check(item.findtext('description') == soup.select_one('meta[name="description"]')['content'], f'{path}: description')
    check(item.findtext('title') == record['title'], f'{path}: title')
    check(canonical in locations, f'{path}: not in sitemap')
    links = hub.select(f'.story-card h3 a[href="{path}"]')
    check(len(links) == 1, f'{path}: missing/duplicate hub listing')
    check(not soup.select('meta[name="robots"][content*="noindex"]'), f'{path}: noindex')
    for data in soup.select('script[type="application/ld+json"]'):
        json.loads(data.string)
        checks['structured_data_blocks'] += 1
    # Exact body bytes protect text, pictures, offers and all existing links.
    check(source.split('</head>', 1)[1] == original(path).split('</head>', 1)[1], f'{path}: article body changed')
    discovery = soup.select('link[rel="alternate"][type="application/rss+xml"]')
    check(len(discovery) == 1 and discovery[0]['href'] == ORIGIN + 'feed.xml', f'{path}: discovery')
    for selector in ['title', 'meta', 'link[rel="canonical"]', 'script', 'style']:
        check([str(n) for n in soup.select(selector)] == [str(n) for n in previous.select(selector)], f'{path}: historical metadata/script/style changed')

pages = ['index.html', 'stories.html', 'learnn-as-we-go.html'] + [r['path'] for r in records]
for path in pages:
    soup = BeautifulSoup((ROOT / path).read_text(), 'html.parser')
    previous = BeautifulSoup(original(path), 'html.parser')
    check([str(n) for n in soup.select('script')] == [str(n) for n in previous.select('script')], f'{path}: scripts altered')
    check([str(n) for n in soup.select('header, footer, form')] == [str(n) for n in previous.select('header, footer, form')], f'{path}: navigation/footer/forms changed')
    check([str(n) for n in soup.select('link[rel="canonical"], meta, title')] == [str(n) for n in previous.select('link[rel="canonical"], meta, title')], f'{path}: original SEO changed')
    check(len(soup.select('link[rel="alternate"][type="application/rss+xml"]')) == 1, f'{path}: feed discovery count')
    check(not any(c > 1 for c in Counter(n['id'] for n in soup.select('[id]')).values()), f'{path}: duplicate ID')
    for element in soup.select('[src], [href]'):
        url = element.get('src', element.get('href'))
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not url:
            continue
        target = (ROOT / path).parent / unquote(parsed.path) if parsed.path else ROOT / path
        check(target.exists(), f'{path}: broken reference {url}')
        if parsed.fragment and target.suffix == '.html':
            check(bool(BeautifulSoup(target.read_text(), 'html.parser').find(id=unquote(parsed.fragment))), f'{path}: broken fragment {url}')
        checks['local_references'] += 1
    for image in soup.select('img'):
        check(bool(image.get('alt', '').strip()), f'{path}: missing image alt')
        checks['images_with_alt'] += 1

# All tracked files outside this small allowlist must remain byte-identical.
allowed = set(pages + ['sitemap.xml'])
for path in subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', args.baseline], cwd=ROOT, text=True).splitlines():
    if path not in allowed:
        check((ROOT / path).is_file() and (ROOT / path).read_bytes() == subprocess.check_output(['git', 'show', f'{args.baseline}:{path}'], cwd=ROOT), f'Protected file changed: {path}')
        checks['protected_files'] += 1
for path in ['index.html', 'learnn-as-we-go.html']:
    check((ROOT / path).read_text().split('</head>', 1)[1] == original(path).split('</head>', 1)[1], f'{path}: body changed')
for identifier in ['from-student-to-teacher']:
    check(str(hub.find(id=identifier)) == str(BeautifulSoup(original('stories.html'), 'html.parser').find(id=identifier)), f'{identifier}: external story changed')
print(json.dumps({'checks': dict(checks), 'feed_items': len(items), 'errors': errors}, indent=2))
raise SystemExit(bool(errors))
