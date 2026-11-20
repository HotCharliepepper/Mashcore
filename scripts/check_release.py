#!/usr/bin/env python3
"""Strict current release gate: sealed bytes, current scenes, search and public boundary."""
from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
import argparse,json,re,sys,xml.etree.ElementTree as ET
from urllib.parse import urlsplit,unquote
from prepare_public import ROOT, OUT, manifest, DENIED_EXTS, DENIED_ROOTS, ALLOWED_CONTEXTS
from release_lock import validate_source_lock, validate_output_lock

BUSINESS=['247-02-04104','최규현','weplacehyun@naver.com']
SEARCH_TAGS=['naver-site-verification','msvalidate.01']
CANON='https://mashcore.co.kr/'
META_NOINDEX_ROUTES={'mobile/index.html','research/method/index.html'}
ASSET_RE=re.compile(r'(?<![\w/])/?assets/[\w./%-]+(?:\.(?:js|css|svg|png|jpeg|jpg|webp|mp4|woff2|woff|ttf|map|txt))?',re.I)
CSS_RE=re.compile(r'url\(\s*["\']?([^"\')]+)',re.I)
LITERAL_ASSET_RE=re.compile(r'''["'](/?assets/[\w./%-]+\.(?:js|css|svg|png|jpeg|jpg|webp|mp4|woff2|woff|ttf|txt|ico))(?:\?[^"'\s]*)?["']''',re.I)
CURRENT_MODULES={
 'assets/home-a23-Byn7jaxj.js':'809d860b53397148e7e378b64df706d00acb725de8ee0bbf56592d934e7f7dd7',
 'assets/interlude-r1-D7l2aCxP.js':'96f56f1763a8d88269039125eceaa171e7c0c4e34f6161fe09cd082b3ba4747f',
 'assets/value-flow-r1-CNEfV0ww.js':'c373b60e9f06b35b33e52f25bf420c2f422aa8d599e8438e9ec550a212c9ce52'
}
CURRENT_ORDER=['origin','question','break-frame','from-ash-to-core','value-flow','research','ai-dialogue','field','capabilities','field-working-tools','linen','invitation']
EXPECTED_PAGES={'index.html','mobile/index.html','about/index.html','contact/index.html','explore/index.html',
 'market-notes/index.html','research/index.html','services/index.html','signal-studio/index.html',
 'work/index.html','work/weplace/index.html','research/archive/index.html','research/chore-to-play/index.html',
 'research/lab/index.html','research/log/index.html','research/market-interpretation/index.html',
 'research/method/index.html','research/notes/index.html','policies/refund/index.html'}

class Inspect(HTMLParser):
    def __init__(self,source):
        super().__init__(convert_charrefs=True)
        self.tags=[];self.refs=[];self.ids=[];self.h1=0;self.titles=0;self.description=[];self.canonical=[];self.robots=[]
        self.title_text=[];self.in_title=False;self.in_body=False;self.body_count=0;self.h1_in_body=0;self.legal_in_body=False;self.business_in_body=False
        self.feed(source)
    def handle_starttag(self,t,attrs):
        d=dict(attrs);self.tags.append((t,d))
        if t=='body':self.in_body=True;self.body_count+=1
        if t=='title':self.in_title=True
        if 'id' in d:self.ids.append(d['id'])
        if t=='h1':self.h1+=1;self.h1_in_body+=int(self.in_body)
        if t=='title':self.titles+=1
        classes=d.get('class','').split()
        if self.in_body and 'footer-legal' in classes:self.legal_in_body=True
        if self.in_body and 'business-info' in classes:self.business_in_body=True
        if t=='meta' and d.get('name')=='description':self.description.append(d.get('content',''))
        if t=='meta' and d.get('name')=='robots':self.robots.append(d.get('content',''))
        if t=='link' and d.get('rel')=='canonical':self.canonical.append(d.get('href',''))
        if t=='img' and 'alt' not in d:raise AssertionError('Image missing alt')
        for attr in ('href','src','poster','data-src'):
            if d.get(attr):self.refs.append(d[attr])
        if d.get('srcset'):
            for item in d['srcset'].split(','):
                if item.strip():self.refs.append(item.strip().split()[0])
    def handle_endtag(self,t):
        if t=='title':self.in_title=False
        if t=='body':self.in_body=False
    def handle_data(self,data):
        if self.in_title:self.title_text.append(data)

def assert_link(ref,source,paths,pages=None):
    if not ref or ref.startswith(('mailto:','tel:','data:','blob:')):return
    url=urlsplit(ref)
    assert url.scheme!='javascript',(source,'script URL is not a public link')
    assert url.hostname not in ('localhost','127.0.0.1','0.0.0.0','::1'),(source,'Local-only link',ref)
    if url.scheme or url.netloc:return
    raw=unquote(url.path)
    if not raw:
        target=source
    elif raw.startswith('/'):
        target=raw.lstrip('/')
    else:
        target=str((PurePosixPath(source).parent/PurePosixPath(raw)))
    from posixpath import normpath
    trailing=target.endswith('/')
    target=normpath(target)
    assert not target.startswith('../') and target!='..',(source,'Link escapes public root',ref)
    if trailing:target+='/'
    if target=='.':target=''
    # URL directory paths resolve to index.html.
    if not target or target.endswith('/'):
        target=target+'index.html'
    if target not in paths and target+'/index.html' in paths:target=target+'/index.html'
    if target not in paths:
        raise AssertionError(f'Missing/case-mismatch local link in {source}: {ref} -> {target}')
    if pages is not None and url.fragment and target.endswith('.html'):
        assert unquote(url.fragment) in pages[target].ids,(source,'Missing target anchor',ref,target)

def check(context):
    if context not in ALLOWED_CONTEXTS:raise ValueError('Unknown context')
    source_manifest=set(manifest())
    lock=validate_source_lock(sorted(source_manifest))
    output_digest=validate_output_lock(context,lock)
    out={x.relative_to(OUT).as_posix() for x in OUT.rglob('*') if x.is_file()}
    if out!=source_manifest|{'_headers'}:raise AssertionError(f'Public allowlist differs: extra={out-source_manifest}, missing={source_manifest-out}')
    pages=sorted(p for p in source_manifest if p.endswith('.html'))
    assert set(pages)==EXPECTED_PAGES,('Official route set changed',set(pages)^EXPECTED_PAGES)
    parsed={path:Inspect((OUT/path).read_text(encoding='utf8')) for path in pages}
    indexed_titles=[];indexed_descriptions=[]
    for path in pages:
        s=(OUT/path).read_text(encoding='utf8');p=parsed[path]
        assert p.h1==1 and p.h1_in_body==1 and p.body_count==1,(path,p.h1,'Expected one body and body H1')
        assert p.titles==1 and len(p.description)==1 and p.description[0],(path,'title/description')
        assert ''.join(p.title_text).strip(),(path,'Empty title')
        assert len(p.ids)==len(set(p.ids)),(path,'duplicate IDs')
        expected=(CANON if path=='mobile/index.html' else CANON+'research/' if path=='research/method/index.html' else CANON+(path[:-10] if path!='index.html' else ''))
        assert p.canonical==[expected],(path,'canonical',p.canonical,expected)
        for field in BUSINESS:assert field in s,(path,'missing business detail',field)
        assert p.legal_in_body and p.business_in_body,(path,'legal footer must be inside body')
        if path not in META_NOINDEX_ROUTES:
            indexed_titles.append(''.join(p.title_text).strip())
            indexed_descriptions.append(p.description[0].strip())
        if context=='production':
            if path in META_NOINDEX_ROUTES:
                assert len(p.robots)==1 and 'noindex' in p.robots[0].lower(),(path,'dedicated noindex missing')
            else:assert not any('noindex' in v.lower() for v in p.robots),(path,'Unexpected production noindex')
        else:assert len(p.robots)==1 and 'noindex' in p.robots[0].lower(),(path,'Preview noindex missing')
        if path=='index.html':
            for name in SEARCH_TAGS:assert s.count('name="'+name+'"')==1,('ownership tag',name)
        for ref in p.refs:
            assert_link(ref,path,source_manifest,parsed)
    assert len(indexed_titles)==len(set(indexed_titles)), 'Indexed page titles must be distinct'
    assert len(indexed_descriptions)==len(set(indexed_descriptions)), 'Indexed descriptions must be distinct'
    # Preserve CSS/JS references as case-sensitive paths.
    checked_refs=0
    for path in source_manifest:
        if not path.endswith(('.css','.js','.html')):continue
        data=(OUT/path).read_text(encoding='utf8',errors='replace')
        for ref in LITERAL_ASSET_RE.findall(data):
            assert ref.lstrip('/') in source_manifest,(path,'Missing literal asset',ref)
        assert not re.search(r'(?:https?:)?//(?:localhost|127\.0\.0\.1|0\.0\.0\.0)(?::\d+)?',data,re.I),(path,'Local review URL in public text')
        assert not re.search(r'sourceMappingURL\s*=',data),(path,'Source map reference in public output')
        for ref in ASSET_RE.findall(data):
            item=ref.lstrip('/').split('?')[0]
            # Only a literal recognized file path, not a partial JS template string.
            if item.lower() in {x.lower() for x in source_manifest if x.startswith('assets/')}:
                assert item in source_manifest,(path,'asset case mismatch',item)
                checked_refs+=1
        if path.endswith('.css'):
            for ref in CSS_RE.findall(data):
                ref=ref.strip();url=urlsplit(ref)
                if ref.startswith(('data:','//','#')) or url.scheme or url.netloc:continue
                # Relative CSS url() assets are only checked when the named extension is present.
                item=ref.split('#')[0].split('?')[0]
                if not item:continue
                from posixpath import normpath,dirname,join
                loc=normpath(join(dirname(path),item.lstrip('/'))) if not item.startswith('/') else item.lstrip('/')
                assert loc in source_manifest,(path,'missing CSS url()',ref,loc)
    allowed_videos={'assets/columbus-b9bvurhk.mp4','assets/scene02-thread-desktop-bpvij5sp.mp4'}
    video_set={x.lower() for x in source_manifest if x.lower().endswith('.mp4')}
    assert video_set==allowed_videos,('Video allowlist mismatch',video_set)
    assert all((OUT/x).stat().st_size < 5_000_000 for x in source_manifest if x.lower().endswith('.mp4'))
    for p in out:
        part=PurePosixPath(p)
        assert not any(seg in DENIED_ROOTS or seg.startswith('.') for seg in part.parts)
        assert part.suffix.lower() not in DENIED_EXTS
    # Pin the actual current modules and scene flow; an A20-only smoke test cannot substitute.
    import hashlib
    home=(OUT/'index.html').read_text(encoding='utf8')
    home_scan=parsed['index.html']
    positions=[home_scan.ids.index(name) for name in CURRENT_ORDER]
    assert positions==sorted(positions),('Current scene order changed',CURRENT_ORDER)
    assert not {'hero-10.html','hero-30.html','question-a0.html'} & source_manifest,'Review alternative leaked'
    for path,digest in CURRENT_MODULES.items():
        assert path in source_manifest and '/'+path in home_scan.refs,('Current module missing',path)
        assert hashlib.sha256((OUT/path).read_bytes()).hexdigest()==digest,('Reviewed generated module changed',path)
    choices=[d.get('data-value-choice') for t,d in home_scan.tags if 'data-value-choice' in d]
    panels=[d.get('data-value-panel') for t,d in home_scan.tags if 'data-value-panel' in d]
    expected_choices=['consulting','marketing','design','space','experience','reservation']
    assert choices==expected_choices and set(panels)==set(expected_choices) and len(panels)==6,'VALUE FLOW six models missing'
    assert '#ai-dialogue' in home_scan.refs and '#capabilities' in home_scan.refs,'Current handoff missing'
    assert '설명을 위한 가상 시각 모델' in home and '운영 데이터와 현장 반응' in home,'VALUE FLOW evidence limits missing'
    sitemap=ET.parse(OUT/'sitemap.xml');urls=[x.text for x in sitemap.iter() if x.tag.endswith('loc')]
    headers=(OUT/'_headers').read_text(encoding='utf8')
    if context=='production':
        assert len(urls)==17,('Expected 17 indexed sitemap URLs',len(urls))
        expected_urls={CANON+(p[:-10] if p!='index.html' else '') for p in pages if p not in META_NOINDEX_ROUTES}
        assert len(set(urls))==17 and set(urls)==expected_urls,'Sitemap must match all 17 indexable routes exactly'
        assert all('Sitemap: '+CANON+'sitemap.xml' in (OUT/'robots.txt').read_text(encoding='utf8') for _ in [0])
        assert not re.search(r'^\s*Disallow:\s*/\s*$',(OUT/'robots.txt').read_text(encoding='utf8'),re.M),'Production crawl blocked'
        assert 'X-Robots-Tag: noindex, nofollow' not in headers
        assert '/mobile/*' in headers and '/research/method/*' in headers
    else:
        assert not urls,('Preview sitemap must be empty',urls)
        assert 'X-Robots-Tag: noindex, nofollow' in headers
    result={'result':'PASS','release':'VALUE FLOW R1 / R070','context':context,'public_files':len(source_manifest),'pages':len(pages),'asset_references_checked':checked_refs,'sitemap_urls':len(urls),'current_scenes':len(CURRENT_ORDER),'value_flow_models':len(panels),'source_tree_sha256':lock['source']['tree_sha256'],'output_tree_sha256':output_digest}
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    pa=argparse.ArgumentParser();pa.add_argument('--context',required=True,choices=sorted(ALLOWED_CONTEXTS));a=pa.parse_args()
    try:check(a.context)
    except Exception as ex:print('RELEASE CHECK FAILED:',repr(ex),file=sys.stderr);sys.exit(1)
