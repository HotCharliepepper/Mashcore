"""Zero-dependency link, asset, semantic-reference and JSON-LD regression check."""
from html.parser import HTMLParser
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path=path; self.ids=[]; self.refs=[]; self.links=[]; self.errors=[]
        self.h1=0; self.title=0; self.description=False; self.json=False; self.data=''
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='html' and a.get('lang')!='ko': self.errors.append('Expected lang=ko')
        if tag=='h1': self.h1+=1
        if tag=='title': self.title+=1
        if tag=='meta' and a.get('name')=='description': self.description=bool(a.get('content'))
        if tag=='img' and 'alt' not in a: self.errors.append('Missing image alt')
        for attr in ('aria-controls','aria-labelledby','aria-describedby'):
            self.refs.extend(a.get(attr,'').split())
        if tag=='label' and a.get('for'): self.refs.append(a['for'])
        if tag in ('a','script','link','img'):
            url=a.get('href',a.get('src'))
            if url is not None: self.links.append(url)
        if tag=='script' and a.get('type')=='application/ld+json': self.json=True; self.data=''
    def handle_data(self, data):
        if self.json: self.data+=data
    def handle_endtag(self, tag):
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
