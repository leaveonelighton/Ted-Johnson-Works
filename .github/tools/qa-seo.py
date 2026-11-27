"""Check all published TJW HTML canonicals against the XML sitemap."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ORIGIN = 'https://tedjohnsonworks.com/'

class Signals(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.canonicals = []; self.noindex = False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and 'canonical' in a.get('rel', '').split():
            self.canonicals.append(a.get('href'))
        if tag == 'meta' and a.get('name', '').lower() in ('robots', 'googlebot'):
            self.noindex |= 'noindex' in a.get('content', '').lower()

urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')]
assert len(urls) == len(set(urls)), 'Duplicate sitemap URL'
indexable = set()
for path in ROOT.rglob('*.html'):
    if path.relative_to(ROOT).parts[0] in ('.git', '.github'):
        continue
    signals = Signals(path.read_text())
    assert len(signals.canonicals) == 1, f'{path}: expected one canonical'
    canonical = signals.canonicals[0]
    if signals.noindex:
        assert canonical not in urls, f'{path}: noindex page in sitemap'
        continue
    assert canonical.startswith(ORIGIN), f'{path}: unexpected canonical host'
    indexable.add(canonical)
    assert canonical in urls, f'{path}: canonical missing from sitemap'
for url in urls:
    assert url in indexable, f'{url}: not an indexable canonical'
    route = urlsplit(url).path.lstrip('/') or 'index.html'
    assert (ROOT / route).is_file(), f'{url}: missing source'
print(f'PASS: {len(indexable)} public canonicals; {len(urls)} sitemap URLs; no duplicates or noindex entries.')
