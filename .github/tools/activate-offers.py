"""Render authorized offer copy into static pages. Does not change external services.

Run only after Ted approves and the supplied checkout links have matching prices:
python .github/tools/activate-offers.py --payments-verified \
  --clarity-url https://... --checkup-url https://...
Requires BeautifulSoup: python -m pip install beautifulsoup4
"""
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--payments-verified', action='store_true', required=True)
parser.add_argument('--clarity-url', required=True)
parser.add_argument('--checkup-url', required=True)
args = parser.parse_args()
urls = {'clarity': args.clarity_url, 'checkup': args.checkup_url}
for name, url in urls.items():
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
        parser.error(f'{name} must be a public HTTPS checkout URL')
config = json.loads((root / '.github/tools/offers.json').read_text())
changed = 0
for path in root.rglob('*.html'):
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    targets = soup.select('[data-offer][data-field]')
    if not targets:
        continue
    for element in targets:
        name, field = element['data-offer'], element['data-field']
        if field == 'checkout':
            element['href'] = urls[name]
        else:
            element.string = config['planned'][name][field]
        changed += 1
    path.write_text(str(soup))
print(f'Updated {changed} offer fields. Review the diff, run QA, then obtain publishing authorization.')
