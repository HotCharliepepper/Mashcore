"""Compare a ready Netlify review deploy with the locally tested dist."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse, urllib.request, urllib.error, re, json, hashlib
p=argparse.ArgumentParser();p.add_argument('--url',required=True);p.add_argument('--deploy-id',required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[2];base=a.url.rstrip('/')
paths=['/'+str(x.relative_to(root/'dist')).removesuffix('index.html') for x in sorted((root/'dist').rglob('index.html'))]
paths+=['/assets/js/hero-media.js','/assets/js/site.js','/assets/js/observations.js','/assets/js/chore-spatial.js','/assets/css/renewal.css','/assets/media/origin-threshold-desktop.svg','/assets/media/origin-threshold-mobile.svg']
excluded=['/content/hero-media.json','/docs/qa/r1/deploy.json','/scripts/build_public.py','/qa/browser.html','/.git/config']
toolbar=re.compile(rb'<div data-netlify-deploy-id="'+re.escape(a.deploy_id.encode())+rb'" data-netlify-site-id="0aca3b54-9691-4381-b853-61c09ab620e5" data-vcs="github" style="position:fixed">\s*<script async src="/\.netlify/scripts/cdp"></script>\s*</div>\s*')
def inspect(path):
 try:
  with urllib.request.urlopen(base+path,timeout=20) as r: data=r.read();code=r.status;robots=r.headers.get('X-Robots-Tag');url=r.url
 except urllib.error.HTTPError as e:
  return {'path':path,'http':e.code,'pass':path in excluded and e.code==404}
 except Exception as e:return {'path':path,'pass':False,'error':str(e)}
 if path in excluded:return {'path':path,'http':code,'pass':False}
 local=(root/'dist'/path.lstrip('/'))
 if path.endswith('/'):local=local/'index.html'
 normalized,count=toolbar.subn(b'',data)
 same=normalized==local.read_bytes()
 return {'path':path,'url':url,'http':code,'robots':robots,'raw_sha256':hashlib.sha256(data).hexdigest(),'toolbar_blocks_removed':count,'matches_after_only_toolbar_removal':same,'pass':code==200 and same and 'noindex' in (robots or '')}
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(inspect,paths+excluded))
report={'deploy_id':a.deploy_id,'url':base,'environment':'HTTP bytes, separate from rendered-browser QA','pass':all(r['pass'] for r in results),'results':results}
(root/'docs/qa/r1/remote-http.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'pass':report['pass'],'checked':len(results),'failed':[r for r in results if not r['pass']]},ensure_ascii=False))
raise SystemExit(0 if report['pass'] else 1)
