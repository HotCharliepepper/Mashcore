"""Source and publish invariants for the additive R3.1 word motion."""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = '614a7351525e5b8bad00e4bfbea621be1352389f775830e46a3d3cb441c74d71'
CORE = 'dd7dc87e023b3480f9707296342565ca2e361c8393cabb30f9557e06eb1bed4d'
TITLE = '그 사람은,<br><em>왜 잠시<br class="r31-break"> 멈췄을까요?</em>'
RESEARCH = '같은 장면을,<br><em>다르게 읽는 일.</em>'
ROLE = '현장과 고객을 살펴, 사업의 방향과 브랜드의 말,<br class="r31-wide"> 홈페이지와 상담의 흐름을 설계합니다.'
CTA = '<a class="mc-hero-action r31-primary" href="/services/">함께할 수 있는 일 보기 <span aria-hidden="true">↗</span></a>'
for file, digest in [('app.js', APP), ('gsap.min.js', CORE)]:
    assert hashlib.sha256((ROOT/'assets/r31'/file).read_bytes()).hexdigest() == digest, file + ' changed'
for file in ['gsap.min.js', 'SplitText.min.js', 'ScrollTrigger.min.js']:
    text = (ROOT/'assets/r31'/file).read_text(encoding='utf-8')
    assert '3.15.0' in text[:120] and '@license' in text[:500], 'Version/license: ' + file

def check(html):
    assert re.search(r'<h1\b[^>]*id="opening-title"[^>]*>(.*?)</h1>', html, re.S)[1] == TITLE
    assert re.search(r'<h2\b[^>]*id="r31-research-title"[^>]*>(.*?)</h2>', html, re.S)[1] == RESEARCH
    assert f'<p class="r31-role">{ROLE}</p>' in html and CTA in html
    assert html.count('data-word-motion="origin"') == html.count('data-word-motion="research"') == 1
    for name in ['word-motion.js', 'word-motion.css']:
        assert html.count('/assets/r31/' + name) == 1
    assert html.count('/assets/r31/gsap.min.js') == 1
    assert html.index('/assets/r31/app.js') < html.index('/assets/r31/word-motion.js')
    assert 'SplitText.min.js' not in html and 'ScrollTrigger.min.js' not in html, 'Plugins must be preference-aware'

home = (ROOT/'index.html').read_text(encoding='utf-8')
mobile = (ROOT/'mobile/index.html').read_text(encoding='utf-8')
assert home == mobile.replace('<title>Mashcore 모바일 —', '<title>Mashcore —').replace('landing-page mobile-edition', 'landing-page')
for source in ['index.html', 'mobile/index.html']:
    check((ROOT/source).read_text(encoding='utf-8'))
    if (ROOT/'dist'/source).exists():
        check((ROOT/'dist'/source).read_text(encoding='utf-8'))
print('PASS: immutable app/core, unchanged copy/CTA, synchronized mobile, plugin versions, source/dist hooks')
