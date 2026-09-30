"""Check static references, offer fields, and deployment boundaries before publishing.
Requires BeautifulSoup: python -m pip install beautifulsoup4
Run from any directory: python .github/tools/qa-static.py
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import Counter
import json
import re
import subprocess
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[2]
errors = []
references = 0
fields = []
external = set()
for path in root.rglob('*.html'):
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    for identifier, count in Counter(el['id'] for el in soup.select('[id]')).items():
        if count > 1:
            errors.append(f'{path.name}: duplicate ID {identifier}')
    for element in soup.select('[href],[src]'):
        url = element.get('href', element.get('src'))
        parsed = urlsplit(url)
        if parsed.scheme in ('https', 'http'):
            if element.name == 'a' and parsed.hostname != 'tedjohnsonworks.com':
                external.add(url)
            continue
        if parsed.scheme or not url:
            continue
        target = path.parent / unquote(parsed.path) if parsed.path else path
        references += 1
        if not target.exists():
            errors.append(f'{path.relative_to(root)}: missing {url}')
        elif parsed.fragment and target.suffix == '.html':
            destination = BeautifulSoup(target.read_text(), 'html.parser')
            if not destination.find(id=unquote(parsed.fragment)):
                errors.append(f'{path.relative_to(root)}: missing anchor {url}')
    for element in soup.select('[data-offer][data-field]'):
        fields.append({'file':path.relative_to(root).as_posix(), 'offer':element['data-offer'],
                       'field':element['data-field'], 'value':element.get('href') if element['data-field']=='checkout' else element.get_text()})
    # Catch the old triage prices, even when embedded inside JavaScript.
    if '$35' in path.read_text():
        errors.append(f'{path.name}: obsolete $35 price')
    if soup.select('a[href^="https://amzn.to/"]') and 'As an Amazon Associate I earn from qualifying purchases.' not in soup.get_text():
        errors.append(f'{path.name}: Amazon disclosure missing')

tracked = subprocess.check_output(['git','-C',str(root),'ls-files'], text=True).splitlines()
for name in tracked:
    if '.tjw-private' in Path(name).parts or Path(name).name.startswith('.env'):
        errors.append(f'Private file tracked: {name}')
    path = root / name
    if path.is_file() and path.suffix in ('.html','.js','.php','.json','.yml','.yaml','.md'):
        text = path.read_text(errors='replace')
        for pattern in [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'\bsk_live_[A-Za-z0-9]{16,}', r'\bghp_[A-Za-z0-9]{30,}', r'\bAKIA[A-Z0-9]{16}\b']:
            if re.search(pattern,text): errors.append(f'Possible credential: {name}')
for required in ['submit-checkup.php','lib/phpmailer/PHPMailer.php','lib/phpmailer/SMTP.php','.github/workflows/deploy-hostinger.yml']:
    if not (root/required).is_file(): errors.append(f'Required file absent: {required}')
summary = {'html_pages':len(list(root.rglob('*.html'))),'internal_references':references,
           'external_link_destinations':len(external),'offer_fields':fields,'errors':errors}
print(json.dumps(summary,indent=2))
raise SystemExit(bool(errors))
