"""Render authorized offer copy into static pages. Does not change external services.

Run only after Ted approves and the supplied checkout links have matching prices:
python .github/tools/activate-offers.py --payments-verified \
  --clarity-url https://... --checkup-url https://...
Both links must also have fresh, successful checkout observations recorded in
.github/review/checkout-verification.json. A flag alone cannot activate pricing.
Requires BeautifulSoup: python -m pip install beautifulsoup4
"""
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--payments-verified', action='store_true', required=True)
parser.add_argument('--clarity-url', required=True)
parser.add_argument('--checkup-url', required=True)
parser.add_argument('--verification-file', type=Path,
                    default=root / '.github/review/checkout-verification.json')
args = parser.parse_args()
urls = {'clarity': args.clarity_url, 'checkup': args.checkup_url}
for name, url in urls.items():
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
        parser.error(f'{name} must be a public HTTPS checkout URL')
config = json.loads((root / '.github/tools/offers.json').read_text())
try:
    verification = json.loads(args.verification_file.read_text())
    for name, url in urls.items():
        evidence = verification[name]
        expected = config['planned'][name]
        if (evidence.get('verified') is not True or evidence.get('live_mode') is not True
                or evidence.get('url') != url or evidence.get('currency') != 'usd'
                or evidence.get('amount_minor') != expected['amount_minor']):
            parser.error(f'{name}: a verified live checkout matching the approved amount and URL is required')
        observed = datetime.fromisoformat(evidence['verified_at'].replace('Z', '+00:00'))
        if observed.tzinfo is None or not timedelta(0) <= datetime.now(timezone.utc) - observed <= timedelta(hours=24):
            parser.error(f'{name}: verify the checkout again; observation must be within the last 24 hours')
except (OSError, KeyError, TypeError, ValueError) as error:
    parser.error(f'Checkout verification is missing or incomplete: {error}')
changed = 0
prepared = []
for path in root.rglob('*.html'):
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    targets = soup.select('[data-offer][data-field]')
    if not targets:
        continue
    for element in targets:
        name, field = element['data-offer'], element['data-field']
        if field == 'checkout':
            element['href'] = urls[name]
        elif field == 'price':
            # Keep the amount machine-readable while displaying the exact launch label.
            if element.name == 'p':
                amount = soup.new_tag('span')
                amount['data-offer'], amount['data-field'] = name, 'price'
                amount.string = config['planned'][name]['price']
                label = soup.new_tag('span', attrs={'class': 'launch-rate-label'})
                label['data-offer'], label['data-field'] = name, 'label'
                label.string = config['planned'][name]['label']
                element.attrs.pop('data-offer', None)
                element.attrs.pop('data-field', None)
                element.clear()
                element.append(label)
                element.append(' ')
                element.append(amount)
                price_block = element
            else:
                element.string = config['planned'][name]['price']
                if not element.parent.select_one(f'[data-offer="{name}"][data-field="label"]'):
                    label = soup.new_tag('span', attrs={'class': 'launch-rate-label'})
                    label['data-offer'], label['data-field'] = name, 'label'
                    label.string = config['planned'][name]['label']
                    element.insert_before(label)
                    element.insert_before(' ')
                price_block = element.find_parent(['p', 'h3'])
            if not price_block.find_next_sibling(attrs={'data-offer': name, 'data-field': 'regular_price'}):
                regular = soup.new_tag('p', attrs={'class': 'regular-price'})
                regular['data-offer'], regular['data-field'] = name, 'regular_price'
                regular.string = config['planned'][name]['regular_price']
                price_block.insert_after(regular)
        else:
            element.string = config['planned'][name][field]
        changed += 1
    prepared.append((path, str(soup).rstrip() + '\n'))
for path, contents in prepared:
    path.write_text(contents)
print(f'Updated {changed} offer fields. Review the diff, run QA, then obtain publishing authorization.')
