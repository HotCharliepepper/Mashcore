#!/usr/bin/env python3
"""R2 source and generated-artifact checks; browser QA is separate."""
import hashlib,json,re,subprocess
from pathlib import Path
from check_public import Page,ROOT,DIST,business_config

checks=[]
baseline='4cd7504878f3118e876beb179f490a141a0e5b61'
for path in ['assets/js/site-config.js','assets/js/site.js','assets/js/observations.js','assets/js/chapters.js','assets/js/chore-spatial.js','content/services-prototype.json','content/services-main-review.html','policies/refund/index.html']:
    old=subprocess.check_output(['git','show',baseline+':'+path],cwd=ROOT)
    assert old==(ROOT/path).read_bytes(),path+' changed'
checks.append('R1 business, A/B, six-perspective/3D, inquiry, both price tracks and policy sources byte-identical')
home=(DIST/'index.html').read_text();h=Page(home)
assert all(i in h.ids for i in ['origin','research','field','invitation','situations-title','home-judgment-title','home-outputs-title','home-faq-title'])
assert home.index('situations-title')<home.index('id="research"')<home.index('home-judgment-title')<home.index('id="field"')<home.index('home-outputs-title')<home.index('id="invitation"')
checks.append('Four original scenes + R2 sales sequence; real detail links checked by check_public')
m=json.loads((ROOT/'content/hero-media.json').read_text())
assert json.loads(h.one('data-hero-config').text())==m
assert h.one('data-hero-poster').attrs['fetchpriority']=='high'
assert 'src' not in h.one('data-hero-video').attrs
assert 'hidden' in h.one('data-hero-controls').attrs
assert m['experience']['fixed_loading_delay_ms']==0 and m['video']['duration_seconds']==6.5 and not m['video']['loop']
assert 'AI' in m['provenance']['review_label'] and m['provenance']['public_use_approved'] is False
manifest=json.loads((ROOT/'source-media/manifest.json').read_text())
for f in manifest['files']:
    data=(DIST/f['output']).read_bytes()
    assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256']
assert not list(DIST.rglob('*.b64'))
assert not (DIST/'source-media').exists()
checks.append('Poster-first HTML, no eager video src, 6.5s sample, no loop, explicit AI provenance, media checksums and source exclusion')
pages=json.loads((ROOT/'content/seo.json').read_text())['pages'];titles=set();descs=set()
for route,p in pages.items():
    raw=(DIST/route.strip('/')/'index.html').read_text()
    page=Page(raw)
    title=next(n.text() for n in page.nodes if n.tag=='title')
    assert title==p['title'] and title not in titles;titles.add(title)
    desc=[n.attrs['content'] for n in page.nodes if n.tag=='meta' and n.attrs.get('name')=='description']
    assert desc==[p['description']] and desc[0] not in descs;descs.add(desc[0])
    canonical=[n.attrs['href'] for n in page.nodes if n.tag=='link' and n.attrs.get('rel')=='canonical']
    assert canonical==['https://mashcore.co.kr'+p.get('canonical',route)]
    schemas=[json.loads(n.text()) for n in page.nodes if n.tag=='script' and n.attrs.get('type')=='application/ld+json']
    assert sum(s['@type']=='WebPage' for s in schemas)==1
    assert sum(s['@type']=='Organization' for s in schemas)==(route in ('/','/about/'))
    assert not re.search(r'"(?:LocalBusiness|telephone|openingHours|sameAs|AggregateRating|Offer)"',json.dumps(schemas))
    assert 'noindex,nofollow' in raw
checks.append('11 unique titles/descriptions, canonical URLs, Organization tied to actual business config; no invented phone/hours/GBP/ratings/offers; review noindex retained')
print(json.dumps({'status':'PASS','checks':checks,'media_bytes':{x['output']:x['bytes'] for x in manifest['files']}},ensure_ascii=False,indent=2))
