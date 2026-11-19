#!/usr/bin/env python3
"""Strict A20 release check: business info, search, file case, public boundary."""
from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
import argparse,json,re,sys,xml.etree.ElementTree as ET
from urllib.parse import urlsplit,unquote
from prepare_public import ROOT, OUT, manifest, DENIED_EXTS, DENIED_ROOTS, ALLOWED_CONTEXTS

BUSINESS=['247-02-04104','최규현','weplacehyun@naver.com']
SEARCH_TAGS=['naver-site-verification','msvalidate.01']
CANON='https://mashcore.co.kr/'
META_NOINDEX_ROUTES={'mobile/index.html','research/method/index.html'}
ASSET_RE=re.compile(r'(?<![\w/])/?assets/[\w./%-]+(?:\.(?:js|css|svg|png|jpeg|jpg|webp|mp4|woff2|woff|ttf|map|txt))?',re.I)
CSS_RE=re.compile(r'url\(\s*["\']?([^"\')]+)',re.I)

class Inspect(HTMLParser):
    def __init__(self,source):
        super().__init__(convert_charrefs=True)
        self.tags=[];self.refs=[];self.ids=[];self.h1=0;self.titles=0;self.description=[];self.canonical=[];self.robots=[]
        self.feed(source)
    def handle_starttag(self,t,attrs):
        d=dict(attrs);self.tags.append((t,d))
        if 'id' in d:self.ids.append(d['id'])
        if t=='h1':self.h1+=1
        if t=='title':self.titles+=1
        if t=='meta' and d.get('name')=='description':self.description.append(d.get('content',''))
        if t=='meta' and d.get('name')=='robots':self.robots.append(d.get('content',''))
        if t=='link' and d.get('rel')=='canonical':self.canonical.append(d.get('href',''))
        if t=='img' and 'alt' not in d:raise AssertionError('Image missing alt')
        for attr in ('href','src','poster','data-src'):
            if d.get(attr):self.refs.append(d[attr])
        if d.get('srcset'):
            for item in d['srcset'].split(','):
                if item.strip():self.refs.append(item.strip().split()[0])

def assert_link(ref,source,paths):
    if not ref or ref.startswith(('mailto:','tel:','data:','blob:','javascript:','#','//')):return
    url=urlsplit(ref)
    if url.scheme or url.netloc:return
    raw=unquote(url.path)
    if not raw:return
    if raw.startswith('/'):
        target=raw.lstrip('/')
    else:
        target=str((PurePosixPath(source).parent/PurePosixPath(raw)))
    # URL directory paths resolve to index.html.
    if not target or target.endswith('/'):
        target=target+'index.html'
    if target not in paths and target+'/index.html' in paths:target=target+'/index.html'
    if target not in paths:
        raise AssertionError(f'Missing/case-mismatch local link in {source}: {ref} -> {target}')

def check(context):
    if context not in ALLOWED_CONTEXTS:raise ValueError('Unknown context')
    source_manifest=set(manifest())
    out={x.relative_to(OUT).as_posix() for x in OUT.rglob('*') if x.is_file()}
    if out!=source_manifest|{'_headers'}:raise AssertionError(f'Public allowlist differs: extra={out-source_manifest}, missing={source_manifest-out}')
    pages=sorted(p for p in source_manifest if p.endswith('.html'))
    assert len(pages)==19,(len(pages),'Expected 19 HTML pages')
    for path in pages:
        s=(OUT/path).read_text(encoding='utf8');p=Inspect(s)
        assert p.h1==1,(path,p.h1,'Expected one H1')
        assert p.titles==1 and len(p.description)==1 and p.description[0],(path,'title/description')
        assert len(p.ids)==len(set(p.ids)),(path,'duplicate IDs')
        expected=(CANON if path=='mobile/index.html' else CANON+'research/' if path=='research/method/index.html' else CANON+(path[:-10] if path!='index.html' else ''))
        assert p.canonical==[expected],(path,'canonical',p.canonical,expected)
        for field in BUSINESS:assert field in s,(path,'missing business detail',field)
        assert 'footer-legal' in s and 'business-info' in s,(path,'legal footer tokens missing')
        if context=='production':
            if path in META_NOINDEX_ROUTES:
                assert len(p.robots)==1 and 'noindex' in p.robots[0].lower(),(path,'dedicated noindex missing')
            else:assert not any('noindex' in v.lower() for v in p.robots),(path,'Unexpected production noindex')
        else:assert len(p.robots)==1 and 'noindex' in p.robots[0].lower(),(path,'Preview noindex missing')
        if path=='index.html':
            for name in SEARCH_TAGS:assert s.count('name="'+name+'"')==1,('ownership tag',name)
        for ref in p.refs:
            assert_link(ref,path,source_manifest)
    # Preserve CSS/JS references as case-sensitive paths.
    checked_refs=0
    for path in source_manifest:
        if not path.endswith(('.css','.js','.html')):continue
        data=(OUT/path).read_text(encoding='utf8',errors='replace')
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
        assert part.suffix not in DENIED_EXTS
    sitemap=ET.parse(OUT/'sitemap.xml');urls=[x.text for x in sitemap.iter() if x.tag.endswith('loc')]
    headers=(OUT/'_headers').read_text(encoding='utf8')
    if context=='production':
        assert len(urls)==17,('Expected 17 indexed sitemap URLs',len(urls))
        assert all(u.startswith(CANON) for u in urls)
        assert all('Sitemap: '+CANON+'sitemap.xml' in (OUT/'robots.txt').read_text(encoding='utf8') for _ in [0])
        assert 'X-Robots-Tag: noindex, nofollow' not in headers
        assert '/mobile/*' in headers and '/research/method/*' in headers
    else:
        assert not urls,('Preview sitemap must be empty',urls)
        assert 'X-Robots-Tag: noindex, nofollow' in headers
    result={'result':'PASS','context':context,'public_files':len(source_manifest),'pages':len(pages),'asset_references_checked':checked_refs,'sitemap_urls':len(urls)}
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    pa=argparse.ArgumentParser();pa.add_argument('--context',required=True,choices=sorted(ALLOWED_CONTEXTS));a=pa.parse_args()
    try:check(a.context)
    except Exception as ex:print('RELEASE CHECK FAILED:',repr(ex),file=sys.stderr);sys.exit(1)
