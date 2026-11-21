"""Write/check the static RSS feed. Python 3 standard library; no site build.

Run: python .github/tools/stories-feed.py [--check]
The reviewed inventory is in stories.json. Dates with no verified publication
time stay in the inventory/hub, not a fabricated RFC 822 pubDate.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ORIGIN = 'https://tedjohnsonworks.com/'
ATOM = 'http://www.w3.org/2005/Atom'
ET.register_namespace('atom', ATOM)


def render():
    records = json.loads((ROOT / '.github/tools/stories.json').read_text())
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    for name, value in [('title', 'Ted’s Stories | Ted Johnson Works'),
                        ('link', ORIGIN + 'stories.html'),
                        ('description', 'Practical articles, personal stories, and lessons from Ted Johnson’s work and life.'),
                        ('language', 'en-us')]:
        ET.SubElement(channel, name).text = value
    ET.SubElement(channel, f'{{{ATOM}}}link', href=ORIGIN + 'feed.xml',
                  rel='self', type='application/rss+xml')
    seen = set()
    for record in records:
        path = record['path']
        assert not path.startswith('/') and '..' not in Path(path).parts
        assert (ROOT / path).is_file() and path.endswith('.html')
        url = ORIGIN + path
        assert url not in seen, f'Duplicate article: {url}'
        seen.add(url)
        item = ET.SubElement(channel, 'item')
        for name, value in [('title', record['title']), ('link', url),
                            ('description', record['description']),
                            ('category', record['category'])]:
            assert value.strip(), f'Empty {name}: {path}'
            ET.SubElement(item, name).text = value
        ET.SubElement(item, 'guid', isPermaLink='true').text = url
    ET.indent(rss, space='  ')
    return ET.tostring(rss, encoding='utf-8', xml_declaration=True) + b'\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = render()
    feed = ROOT / 'feed.xml'
    if args.check:
        if not feed.exists() or feed.read_bytes() != expected:
            raise SystemExit('Feed differs from reviewed inventory. Run stories-feed.py.')
        print('PASS: RSS matches reviewed inventory; XML parsed successfully.')
    else:
        feed.write_bytes(expected)
        print('Wrote feed.xml. Review it with the article hub before release.')
