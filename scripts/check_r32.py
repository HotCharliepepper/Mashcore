"""R3.2 source/SEO/GEO invariants and preview packaging checks."""
import hashlib
import re
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = 'eef90b6e470e1af7a1c72c444208589c4033cf64095a848d4a4f4de4c18b6bc8'
CORE = '92bb9a96476f983d212a2bc4f54c889039c1696dd4461d40a736860938570fbb'
TITLE = '그 사람은,<br><em>왜 잠시<br class="r31-break"> 멈췄을까요?</em>'
RESEARCH = '같은 장면을,<br><em>다르게 읽는 일.</em>'
ROLE = '현장과 고객을 살펴, 사업의 방향과 브랜드의 말,<br class="r31-wide"> 홈페이지와 상담의 흐름을 설계합니다.'
CTA = '<a class="mc-hero-action r31-primary" href="/services/">함께할 수 있는 일 보기 <span aria-hidden="true">↗</span></a>'
for file, digest in [('app.js', APP), ('gsap.min.js', CORE)]:
    # Git stores LF; Windows autocrlf checkouts must compare the same source bytes.
    canonical = (ROOT/'assets/r31'/file).read_text(encoding='utf-8').encode('utf-8')
    assert hashlib.sha256(canonical).hexdigest() == digest, file + ' changed'
for file in ['assets/r31/gsap.min.js', 'assets/r32/SplitText.min.js', 'assets/r32/ScrollTrigger.min.js']:
    text = (ROOT/file).read_text(encoding='utf-8')
    assert '3.15.0' in text[:120] and '@license' in text[:500], 'Version/license: ' + file

def check(html):
    assert re.search(r'<h1\b[^>]*id="opening-title"[^>]*>(.*?)</h1>', html, re.S)[1] == TITLE
    assert re.search(r'<h2\b[^>]*id="r31-research-title"[^>]*>(.*?)</h2>', html, re.S)[1] == RESEARCH
    assert f'<p class="r31-role">{ROLE}</p>' in html and CTA in html
    assert html.count('data-word-motion="origin"') == html.count('data-word-motion="research"') == 1
    for name in ['word-motion.js', 'styles.css']:
        assert html.count('/assets/r32/' + name) == 1
    assert html.count('/assets/r31/gsap.min.js') == 1
    assert html.index('/assets/r31/app.js') < html.index('/assets/r32/word-motion.js')
    assert 'SplitText.min.js' not in html and 'ScrollTrigger.min.js' not in html, 'Plugins must be preference-aware'

home = (ROOT/'index.html').read_text(encoding='utf-8')
mobile = (ROOT/'mobile/index.html').read_text(encoding='utf-8')
assert home == mobile.replace('<title>Mashcore 모바일 —', '<title>Mashcore —').replace('landing-page mobile-edition', 'landing-page')
for source in ['index.html', 'mobile/index.html']:
    check((ROOT/source).read_text(encoding='utf-8'))
    if (ROOT/'dist'/source).exists():
        check((ROOT/'dist'/source).read_text(encoding='utf-8'))
BASE = 'a8dae1c4b6e69cd02e24b5e28bc9600f5a756fcf'
def original(relative):
    return subprocess.check_output(['git','show',BASE+':'+relative], cwd=ROOT).decode('utf-8')
assert (ROOT/'assets/r31/styles.css').read_text(encoding='utf-8') == original('assets/r31/styles.css')
for relative in ['index.html','mobile/index.html']:
    old = original(relative)
    current = (ROOT/relative).read_text(encoding='utf-8')
    for pattern in [r'<title>.*?</title>', r'<script type="application/ld\+json">(.*?)</script>']:
        assert re.findall(pattern,current,re.S) == re.findall(pattern,old,re.S), 'SEO/schema changed: '+relative
    for attr in ['canonical', 'og:title', 'og:description', 'og:url']:
        assert [s for s in re.findall(r'<(?:link|meta)\b[^>]*>',current) if attr in s] == [s for s in re.findall(r'<(?:link|meta)\b[^>]*>',old) if attr in s], attr
    assert re.search(r'<section class="footer-legal".*?</section>',current,re.S)[0] == re.search(r'<section class="footer-legal".*?</section>',old,re.S)[0]
for directory in ['research','services','about','explore','policies','signal-studio','work']:
    for file in (ROOT/directory).rglob('*.html'):
        assert file.read_text(encoding='utf-8') == original(file.relative_to(ROOT).as_posix()), 'Unrelated page changed: '+str(file)
assert '1.85' in (ROOT/'assets/r32/word-motion.js').read_text() and '2.2' in (ROOT/'assets/r32/word-motion.js').read_text()
print('PASS: R3.1 app/style/core, copy/CTA, all detail pages, SEO/schema/GEO, mobile sync and R3.2 source/dist hooks')
