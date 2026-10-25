"""Prepare isolated local QA surface; never included in dist/deploy."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[2]
site=root/'qa/r2/site'
fixture=(root/'qa/r2/fixture.webm').read_bytes()
if site.exists():shutil.rmtree(site)
shutil.copytree(root/'dist',site)
(site/'qa').mkdir()
for name in ['browser.html','browser.js','performance.js']:
    shutil.copy2(root/'qa/r2'/name,site/'qa'/name)
(site/'qa/fixture.webm').write_bytes(fixture)
home=(site/'index.html').read_text()
(site/'qa/performance.html').write_text(home.replace('</head>','<script src="/qa/performance.js"></script></head>',1))

preview=site/'preview/index.html'
preview.write_text(preview.read_text().replace('<option value="/">홈</option>','<option value="/">홈</option><option value="/qa/performance.html">로컬 성능 샘플</option><option value="/qa/before/">R1 변경 전</option>'))
before=root/'qa/r2/before-dist'
if before.exists():
    shutil.copytree(before,site/'qa/before')
    for page in (site/'qa/before').rglob('*.html'):
        page.write_text(page.read_text().replace('="/','="/qa/before/'))
