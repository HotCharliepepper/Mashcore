"""Make an isolated local browser harness. Never copied into public dist."""
from pathlib import Path
import shutil,json,subprocess
root=Path(__file__).resolve().parents[1]
site=root/'qa/r1/site'
if site.exists():shutil.rmtree(site)
shutil.copytree(root/'dist',site)
(site/'qa').mkdir()
for name in ['browser.html','browser.js']:
 shutil.copy2(root/'qa/r1'/name,site/'qa'/name)
subprocess.run(['ffmpeg','-y','-f','lavfi','-i','testsrc2=size=320x180:rate=12','-t','2.5','-c:v','libvpx-vp9','-b:v','180k','-an',str(site/'qa/fixture.webm')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
(root/'.openai/hosting.json').write_text(json.dumps({'static':{'directory':'qa/r1/site'}}))
print('Isolated QA at qa/r1/site; dist is unchanged. TEST FIXTURE: color bars, not brand media.')
