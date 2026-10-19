#!/usr/bin/env python3
"""Check the actual Netlify publish directory, not the historical v5 templates."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote, parse_qs
import json
import re
import os
import hashlib
from build_public import catalog_guard, read_json

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.refs=[];self.aria=[];self.h1=0;self.blocks=[];self.block=None;self.product_links=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        for key in ('href','src'):
            if a.get(key):self.refs.append(a[key])
        for key in ('aria-controls','aria-labelledby','aria-describedby'):
            if a.get(key):self.aria.extend(a[key].split())
        if 'data-product-contact' in a:self.product_links.append(a.get('href',''))
        if tag=='script' and a.get('type')=='application/ld+json':self.block=''
    def handle_data(self,text):
        if self.block is not None:self.block+=text
    def handle_endtag(self,tag):
        if tag=='script' and self.block is not None:
            self.blocks.append(self.block);self.block=None


def main():
    paths=sorted(DIST.rglob('*.html'))
    assert len(paths)==11,f'Expected the 10 existing routes plus /services/: {len(paths)}'
    parsed={p:Page(p.read_text(encoding='utf-8')) for p in paths}
    references=0;footers=0
    for path,page in parsed.items():
        rel=path.relative_to(DIST).as_posix();text=path.read_text(encoding='utf-8')
        assert len(page.ids)==len(set(page.ids)),f'Duplicate ID: {rel}'
        if rel!='preview/index.html':assert page.h1==1,f'H1: {rel}'
        for ident in page.aria:assert ident in page.ids,f'Broken ARIA ref: {rel} #{ident}'
        for block in page.blocks:
            data=json.loads(block)
            assert not re.search(r'"@type"\s*:\s*"(?:Offer|AggregateOffer)"',block),'Draft offers must not be purchase metadata.'
        for ref in page.refs:
            parts=urlparse(ref)
            if parts.scheme or ref.startswith('//'):continue
            resolved=urlparse(urljoin('https://local/'+rel,ref))
            target=DIST/unquote(resolved.path).lstrip('/')
            if target.is_dir():target=target/'index.html'
            assert target.is_file(),f'Missing asset/route: {rel} {ref}'
            references+=1
            if resolved.fragment and target.suffix=='.html':
                assert unquote(resolved.fragment) in parsed[target].ids,f'Broken anchor: {rel} {ref}'
        if 'data-business-info' in text:
            footers+=1
            assert all(x in text for x in ('247-02-04104','최규현','선유로9길 10')),f'Business details: {rel}'
        if os.environ.get('CONTEXT')!='production':
            assert re.search(r'<meta\b[^>]*name=[\'"]robots[\'"][^>]*>',text),f'Robots: {rel}'
    catalog=read_json(ROOT/'content/services-prototype.json')
    for name in ('index.html','mobile/index.html','services/index.html'):
        path=DIST/name;text=path.read_text(encoding='utf-8');p=parsed[path]
        assert len(p.product_links)==4
        for price in ('400만원','250만원','150만원','50만원'):assert price in text
        assert '부가세 포함 여부 미정' in text and '1회 프로젝트 기준 제안' in text
        for i,href in enumerate(p.product_links):
            uri=urlparse(href);query=parse_qs(uri.query)
            assert uri.scheme=='mailto' and uri.path=='weplace25@gmail.com'
            assert catalog['products'][i]['name'] in query['subject'][0]
            assert '부가세 포함 여부 미정' in query['body'][0]
    home=(DIST/'index.html').read_text(encoding='utf-8');mobile=(DIST/'mobile/index.html').read_text(encoding='utf-8')
    assert mobile.replace('class="landing-page core-page mobile-edition"','class="landing-page core-page"',1).replace('<title>Mashcore 모바일 —','<title>Mashcore —',1)==home
    assert home.count('data-chapter=""')==4
    before=(ROOT/'index.html').read_text(encoding='utf-8')
    pattern=r'<div class="observation-lab".*?<p class="observation-principle">'
    assert re.search(pattern,before,re.S).group()==re.search(pattern,home,re.S).group(),'Preserve the demo content.'
    assert footers==10
    assert not any((DIST/name).exists() for name in ('docs','content','scripts','.git','node_modules','qa','README.md','DESIGN.md','netlify.toml'))
    # Explicit negative test. This does not deploy or modify production.
    try:catalog_guard(catalog,'production')
    except ValueError:guard='blocked as expected'
    else:raise AssertionError('Unapproved production must be blocked during prototype review.')
    result={'static_validation':'PASS','html_pages':len(paths),'local_references':references,'business_footers':footers,'prototype_products':4,'production_guard':guard,'baseline_observation_unchanged':True,'mobile_sync_exact':True,'runtime_js_sha256':{name:hashlib.sha256((DIST/'assets/js'/name).read_bytes()).hexdigest() for name in ('site.js','observations.js','chapters.js')}}
    print(json.dumps(result,ensure_ascii=False))
    # Safe review-only evidence: counts/hashes, never source data, keys or customer input.
    if os.environ.get('CONTEXT')!='production':
        (DIST/'__review').mkdir(exist_ok=True)
        (DIST/'__review/build.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
