"""Zero-dependency link, asset, semantic-reference and JSON-LD regression check."""
from html.parser import HTMLParser
from html import escape
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CONFIG_TEXT = (ROOT/'assets/js/site-config.js').read_text(encoding='utf-8')
BUSINESS_FIELDS = ('companyName', 'representative', 'registrationNumber', 'address', 'phone', 'email')
PUBLIC_BUSINESS = {}
for key in BUSINESS_FIELDS:
    found = re.search(r'\b' + key + r"\s*:\s*'([^']*)'", CONFIG_TEXT)
    PUBLIC_BUSINESS[key] = found.group(1).strip() if found else ''
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path=path; self.ids=[]; self.refs=[]; self.links=[]; self.errors=[]
        self.h1=0; self.title=0; self.description=False; self.json=False; self.data=''; self.in_head=False
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='head': self.in_head=True
        if 'id' in a: self.ids.append(a['id'])
        if tag=='html' and a.get('lang')!='ko': self.errors.append('Expected lang=ko')
        if tag=='h1': self.h1+=1
        if tag=='title' and self.in_head: self.title+=1
        if tag=='meta' and a.get('name')=='description': self.description=bool(a.get('content'))
        if tag=='img' and 'alt' not in a: self.errors.append('Missing image alt')
        for attr in ('aria-controls','aria-labelledby','aria-describedby'):
            self.refs.extend(a.get(attr,'').split())
        if tag=='label' and a.get('for'): self.refs.append(a['for'])
        if tag in ('a','script','link','img','iframe'):
            url=a.get('href',a.get('src'))
            if url is not None: self.links.append(url)
        if tag=='script' and a.get('type')=='application/ld+json': self.json=True; self.data=''
    def handle_data(self, data):
        if self.json: self.data+=data
    def handle_endtag(self, tag):
        if tag=='head': self.in_head=False
        if tag=='script' and self.json:
            try: json.loads(self.data)
            except ValueError as e: self.errors.append(f'Invalid JSON-LD: {e}')
            self.json=False

pages={p.resolve():Page(p) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
errors=[]
for path,page in pages.items():
    label=str(path.relative_to(ROOT))
    errors.extend(f'{label}: {e}' for e in page.errors)
    if page.h1!=1 or page.title!=1 or not page.description: errors.append(f'{label}: missing/duplicate heading or metadata')
    # A successful deploy is not enough if required business information is
    # visually buried or only hydrated by JavaScript. Keep its full-width panel
    # and the legal details in the static HTML of every customer-facing footer.
    source=path.read_text(encoding='utf-8')
    if '<footer class="footer">' in source:
        if '<section class="footer-legal"' not in source or '<h2 id="footer-business-title">사업자 정보</h2>' not in source:
            errors.append(f'{label}: missing labelled business info panel')
        if '<dl class="business-info" data-business-info="">' not in source:
            errors.append(f'{label}: business info must be visible without JavaScript')
        legal_section = re.search(r'<section class="footer-legal"[^>]*>[\s\S]*?</section>', source)
        if legal_section:
            for key, value in PUBLIC_BUSINESS.items():
                if value and escape(value) not in legal_section.group(0):
                    errors.append(f'{label}: business detail {key} differs from site-config.js')
        footer=source[source.index('<footer class="footer">'):]
        footer_grid_end=footer.find('</nav></div>')
        legal_start=footer.find('<section class="footer-legal"')
        if footer_grid_end<0 or legal_start<=footer_grid_end:
            errors.append(f'{label}: business info must be outside the narrow footer grid')
    for id,count in Counter(page.ids).items():
        if count>1: errors.append(f'{label}: duplicate id {id}')
    for id in page.refs:
        if id not in page.ids: errors.append(f'{label}: missing ARIA/label target {id}')
    for link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        if link=='#': errors.append(f'{label}: empty anchor'); continue
        target=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else (path.parent/unquote(u.path) if u.path else path)
        target=target.resolve()
        if target.is_dir(): target=target/'index.html'
        if not target.exists(): errors.append(f'{label}: missing file {link}'); continue
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids: errors.append(f'{label}: missing anchor {link}')
print(json.dumps({'pages':len(pages),'local_links_and_assets':'passed' if not errors else 'failed','errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
