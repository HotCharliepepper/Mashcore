"""R1-specific static invariants on actual dist (not a browser assertion)."""
from pathlib import Path
import json,hashlib,subprocess
from check_public import Page,compact
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'content/strategy.json').read_text());m=json.loads((root/'content/hero-media.json').read_text())
h=Page((root/'dist/index.html').read_text());checks=[]
assert compact(h.one('id','opening-title').text())==compact(''.join(s['hero_title']))
assert compact(s['hero_description']) in compact(h.root.text())
checks.append('Strategy is the rendered hero copy source; obsolete hardcoded hero removed')
p=h.one('data-hero-poster');assert p.attrs['loading']=='eager' and p.attrs['fetchpriority']=='high'
for key in ['desktop','mobile']:assert (root/'dist'/m['poster'][key].lstrip('/')).is_file()
assert m['video']['desktop'] is None and m['video']['mobile'] is None
assert not h.where('data-hero-video') and 'hidden' in h.one('data-hero-controls').attrs
assert h.one('data-hero-media').attrs['data-media-state']=='poster_only'
assert h.one('data-hero-config').text() and json.loads(h.one('data-hero-config').text())==m
checks.append('Eager real SVG poster; null sources emit no video; controls hidden; runtime receives exact configuration')
assert m['provenance']['public_use_approved'] is False
assert '히어로 구도 시안 · 실제 촬영 아님' in h.root.text()
assert len([n for n in h.nodes if n.tag=='details' and n.attrs.get('class')=='study-question'])==3
assert not any(n.tag=='details' and '전환율' in n.text() for n in h.nodes)
checks.append('Asset status visible; three hypotheses collapsed, experiment limits always outside disclosure')
for n in h.where('class','origin-next'):assert n.attrs['href']=='#research'
services=Page((root/'dist/services/index.html').read_text())
assert all(services.one('id','axis-'+str(i)) for i in range(1,7))
assert len([n for n in services.nodes if n.tag=='details' and n.attrs.get('class')=='service-faq'])==3
assert 'PR #2' not in services.root.text() and 'main 가격' not in services.root.text()
checks.append('Situation choices target six existing service axes; FAQ works without JS; no visitor-facing Git labels')
for name in ['site.js','observations.js','chore-spatial.js','chapters.js','site-config.js']:
 old=subprocess.check_output(['git','show','a3c81d821f4bcbe542bb0aee332a1803fd8ae8a4:assets/js/'+name],cwd=root)
 assert old==(root/'assets/js'/name).read_bytes(),name+' runtime unexpectedly changed'
assert subprocess.check_output(['git','show','a3c81d821f4bcbe542bb0aee332a1803fd8ae8a4:content/services-prototype.json'],cwd=root)==(root/'content/services-prototype.json').read_bytes()
checks.append('Inquiry/A-B/3D/chapter/business runtimes and product catalog byte-identical to baseline')
for name in ['qa','docs','scripts','content']:assert not (root/'dist'/name).exists()
assert not list((root/'dist').rglob('fixture.webm'))
checks.append('Local QA runner/test media absent from public output')
print(json.dumps({'status':'PASS','checks':checks,'poster_bytes':{k:(root/'dist'/m['poster'][k].lstrip('/')).stat().st_size for k in ['desktop','mobile']}},ensure_ascii=False,indent=2))
