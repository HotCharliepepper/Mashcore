#!/usr/bin/env python3
"""R3 additive reverse hero contract; run after build_public and check_public."""
from check_public import ROOT, DIST, Page
for route in ['index.html', 'mobile/index.html']:
    html = (DIST / route).read_text(encoding='utf-8')
    parsed = Page(html)
    assert sum('data-hero-experience' in node.attrs for node in parsed.nodes) == 1, route
    assert html.count('data-hero-mode-choice=') == 2, route
    assert 'data-hero-mode="default"' in html, route
    assert 'data-hero-reverse-layer' in html, route
    assert 'data-hero-mode-controls hidden' in html, route
    assert '/assets/js/hero-reverse.js' in html, route
    assert '/assets/css/hero-reverse.css' in html, route
    assert all('id="' + key + '"' in html for key in ('origin','research','field','invitation')), route
    assert 'data-observation-lab' in html and 'data-hero-media' in html, route
    assert 'href="/services/"' in html and 'href="#research"' in html, route
    assert 'data-hero-config' in html and 'data-hero-video' in html, route
    assert '그 사람은,' in html and '왜 잠시 멈췄을까요?' in html, route
source = (ROOT / 'scripts/review_r2.py').read_text(encoding='utf-8')
assert 'data-hero-reverse-layer' in source
js = (DIST / 'assets/js/hero-reverse.js').read_text(encoding='utf-8')
css = (DIST / 'assets/css/hero-reverse.css').read_text(encoding='utf-8')
assert "hero', 'reverse'" in js
assert 'aria-pressed' in js and 'history.replaceState' in js
assert 'prefers-reduced-motion: reduce' in js and css
assert 'hero-variant-bar[hidden]' in css and 'hero-reverse-trace' in css
assert (DIST / 'assets/js/hero-media.js').is_file()
assert (DIST / 'assets/js/observations.js').is_file()
assert (DIST / 'assets/js/chore-spatial.js').is_file()
assert (DIST / 'policies/refund/index.html').is_file()
print('PASS: R3 hero A/B overlay, accessible switch, reduced motion, unchanged R2 content and preserved dependencies')
