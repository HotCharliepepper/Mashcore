#!/usr/bin/env python3
"""Read-only R3.1 Deploy Preview browser checks; screenshots stay in CI artifacts.

No customer data, submissions, mailbox launches or account mutations. Run in CI,
not through a local browser-control substitute in the managed Work environment.
"""
import json
import os
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

BASE = os.environ['PREVIEW_URL'].rstrip('/') + '/'
SHA = os.environ['QA_COMMIT']
OUT = Path('qa/r31-evidence')
OUT.mkdir(parents=True, exist_ok=True)
ROWS = []


def record(name, okay, detail=''):
    row = {'check': name, 'status': 'PASS' if okay else 'FAIL', 'detail': detail}
    ROWS.append(row)
    print(f"{row['status']}: {name}" + (f' — {str(detail)[:180]}' if detail else ''), flush=True)


def ready():
    """Wait for this exact PR revision, never accept a prior successful deploy."""
    last = ''
    for attempt in range(48):
        try:
            with urlopen(BASE + '?qa_revision=' + SHA, timeout=15) as response:
                html = response.read().decode('utf-8')
                if f'name="r31-commit" content="{SHA}"' in html:
                    return
                last = f'HTTP {response.status}; expected revision marker absent'
        except Exception as error:
            last = str(error)[:180]
        if attempt % 4 == 0:
            print(f'Waiting for exact Preview {SHA[:12]}: {last}', flush=True)
        time.sleep(10)
    raise RuntimeError(f'Preview revision not ready: {last}')


def visit(page, wait_until='load'):
    response = page.goto(BASE, wait_until=wait_until, timeout=45000)
    if not response or response.status != 200:
        raise RuntimeError('Preview HTTP failure')
    marker = page.locator('meta[name="r31-commit"]').get_attribute('content')
    if marker != SHA:
        raise RuntimeError(f'Wrong Preview revision: {marker}')
    return response


def visible(page, selector):
    element = page.locator(selector)
    return element.count() > 0 and element.first.is_visible()


def overflow(page):
    return page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')


def poster_ready(page):
    # The browser's requestAnimationFrame polling may not advance with page JS
    # disabled. Read the DOM from Python instead; this also tests the no-JS case.
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        state = page.locator('.r31-poster').evaluate('(img) => ({complete: img.complete, width: img.naturalWidth})')
        if state['complete']:
            return state['width'] > 0
        time.sleep(.05)
    return False


def screenshot(page, filename, full=False):
    page.screenshot(path=str(OUT / filename), full_page=full, animations='disabled', timeout=45000)



def section_contrast(page, section, label):
    """Check computed foreground against composited solid ancestor backgrounds.

    Scoped regression guard for the retained field/invitation headings, including
    differently colored emphasis. This is not a full-page accessibility audit.
    """
    rows = page.locator(f'#{section} h2, #{section} h2 em').evaluate_all(r"""elements => {
      const rgba = value => {
        const parts = value.match(/[\d.]+/g).map(Number);
        return [parts[0], parts[1], parts[2], parts.length > 3 ? parts[3] : 1];
      };
      const over = (fg, bg) => [0,1,2].map(i => fg[i] * fg[3] + bg[i] * (1-fg[3]));
      const luminance = rgb => rgb.map(v => {
        v /= 255;
        return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4);
      }).reduce((sum, v, i) => sum + v * [.2126, .7152, .0722][i], 0);
      return elements.map(el => {
        const chain = [];
        for (let node = el; node; node = node.parentElement) chain.unshift(node);
        let background = [255,255,255];
        let solid = true;
        for (const node of chain) {
          const css = getComputedStyle(node);
          if (css.backgroundImage !== 'none') solid = false;
          background = over(rgba(css.backgroundColor), background);
        }
        const css = getComputedStyle(el);
        const foreground = over(rgba(css.color), background);
        const a = luminance(foreground), b = luminance(background);
        const ratio = (Math.max(a,b)+.05) / (Math.min(a,b)+.05);
        const large = parseFloat(css.fontSize) >= 24 ||
          (parseFloat(css.fontSize) >= 18.6667 && Number(css.fontWeight) >= 700);
        return {text: el.textContent.trim(), foreground: css.color, background,
          ratio, required: large ? 3 : 4.5, solid};
      });
    }""")
    for index, row in enumerate(rows):
        record(f'{label}: {section} heading contrast {index+1}',
               row['solid'] and row['ratio'] >= row['required'], row)


def common(page, label):
    record(label + ': question visible', visible(page, '#opening-title') and '왜 잠시 멈췄을까요?' in ' '.join(page.locator('#opening-title').inner_text().split()))
    record(label + ': service CTA usable', visible(page, '.mc-hero-action[href="/services/"]'))
    record(label + ': inquiry usable', visible(page, '#email-question') and page.locator('#email-question').get_attribute('href').startswith('mailto:'))
    record(label + ': no horizontal overflow', overflow(page) <= 2, overflow(page))


def viewports(browser):
    for width, height in ((320, 700), (390, 844), (768, 1024), (1440, 900)):
        context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=1)
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        try:
            response = visit(page)
            common(page, str(width))
            page.locator('.header-cta').click()
            page.wait_for_function('Math.abs(document.getElementById("invitation").getBoundingClientRect().top) < 100', timeout=8000)
            record(f'{width}: inquiry anchor reaches destination', True)
            page.goto(BASE, wait_until='load')
            record(f'{width}: one H1', page.locator('h1').count() == 1)
            record(f'{width}: original scene IDs', all(page.locator(f'#{item}[data-chapter]').count() == 1 for item in ('origin', 'research', 'field', 'invitation')))
            record(f'{width}: original routes retained', all(page.locator(f'a[href="{path}"]').count() for path in ('/services/', '/research/lab/', '/research/notes/', '/signal-studio/', '/work/weplace/', '/research/chore-to-play/')))
            record(f'{width}: six independent Chore to Play perspectives', page.locator('[data-spatial-select]').count() == 6)
            record(f'{width}: noindex meta and HTTP', 'noindex' in page.locator('meta[name="robots"]').get_attribute('content').lower() and 'noindex' in response.headers.get('x-robots-tag', '').lower())
            record(f'{width}: canonical remains public homepage', page.locator('link[rel="canonical"]').get_attribute('href') == 'https://mashcore.co.kr/')
            cta = page.locator('.mc-hero-action').bounding_box()
            record(f'{width}: CTA above initial fold', bool(cta and cta['y'] + cta['height'] <= height + 2), cta)
            if width <= 820:
                media = page.locator('#origin-video').bounding_box()
                record(f'{width}: copy and CTA precede media', bool(cta and media and cta['y'] + cta['height'] <= media['y'] + 2))
                record(f'{width}: no automatic video playback', page.locator('#origin-video').evaluate('(v) => v.paused && v.currentTime === 0'))
                record(f'{width}: poster loaded', poster_ready(page))
            record(f'{width}: no uncaught JS errors', not errors, errors)
            screenshot(page, f'r31-{width}-fold.png')
            if width in (390, 1440):
                screenshot(page, f'r31-{width}-full.png', full=True)
            page.locator('#research').scroll_into_view_if_needed()
            buttons = page.locator('[data-research-step]')
            record(f'{width}: three research controls', buttons.count() == 3)
            for step in ('observation', 'alternative', 'next'):
                button = page.locator(f'[data-research-step="{step}"]')
                button.click()
                record(f'{width}: research {step} selection', button.get_attribute('aria-pressed') == 'true' and visible(page, f'[data-step-panel="{step}"]') and page.locator('[data-research-step][aria-pressed="true"]').count() == 1)
            screenshot(page, f'r31-{width}-research.png')
            if width == 390:
                page.locator('[data-spatial-select="economy"]').click()
                record('Existing six-lens interaction works', page.locator('[data-spatial-select="economy"]').get_attribute('aria-pressed') == 'true')
            for section in ('field', 'invitation'):
                page.locator('#' + section).scroll_into_view_if_needed()
                section_contrast(page, section, str(width))
                if width in (390, 1440):
                    screenshot(page, f'r31-{width}-{section}.png')
        except Exception as error:
            record(f'{width}: viewport scenario', False, str(error))
            try:
                screenshot(page, f'r31-{width}-error.png')
            except Exception:
                pass
        finally:
            context.close()


def keyboard(browser):
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    try:
        visit(page)
        page.keyboard.press('Tab')
        record('Keyboard: skip link first', page.locator('.skip').evaluate('(el) => el === document.activeElement'))
        page.keyboard.press('Enter')
        record('Keyboard: skip reaches main', page.evaluate('location.hash === "#main"'))
        # Locate by sequential Tab traversal, not pointer activation.
        found = False
        for _ in range(35):
            page.keyboard.press('Tab')
            if page.evaluate('document.activeElement?.dataset.researchStep === "alternative"'):
                found = True
                break
        record('Keyboard: research is in tab order', found)
        if found:
            page.keyboard.press('Enter')
            record('Keyboard: Enter selects research', page.locator('[data-research-step="alternative"]').get_attribute('aria-pressed') == 'true')
            page.keyboard.press('Tab')
            page.keyboard.press('Space')
            record('Keyboard: Space selects next step', page.locator('[data-research-step="next"]').get_attribute('aria-pressed') == 'true')
            record('Keyboard: visible focus styling', page.evaluate('getComputedStyle(document.activeElement).outlineStyle !== "none"'))
        record('Research live announcement container', page.locator('#research-reading').get_attribute('aria-live') == 'polite')
        screenshot(page, 'r31-keyboard.png')
    except Exception as error:
        record('Keyboard scenario', False, str(error))
    finally:
        page.close()


def media_and_motion(browser):
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    # Observe rendered signal styles while the short, finite GSAP timeline runs.
    # Checking the timeline later can miss a correctly completed one-shot motion.
    page.add_init_script("""
      window.__r31SignalSamples = [];
      addEventListener('DOMContentLoaded', () => {
        let remaining = 100;
        const sample = () => {
          const signal = document.querySelector('.r31-focus');
          if (signal) {
            const css = getComputedStyle(signal);
            window.__r31SignalSamples.push(css.transform + '|' + css.opacity);
          }
          if (--remaining) setTimeout(sample, 25);
        };
        sample();
      });
    """)
    try:
        visit(page, wait_until='domcontentloaded')
        video = page.locator('#origin-video')
        record('Video: muted, inline, never loops', video.evaluate('(v) => v.muted && v.playsInline && !v.loop'))
        page.wait_for_function('document.querySelector("#origin-video").readyState >= 2', timeout=20000)
        record('Video: real 1920x1080 asset decoded', video.evaluate('(v) => v.videoWidth === 1920 && v.videoHeight === 1080'))
        record('Video: approximately six seconds', video.evaluate('(v) => v.duration > 5 && v.duration < 7'))
        record('Desktop: GSAP 3.15.0 available', page.evaluate('window.gsap?.version === "3.15.0"'))
        page.wait_for_function('new Set(window.__r31SignalSamples).size > 1', timeout=6000)
        samples = page.evaluate('new Set(window.__r31SignalSamples).size')
        record('Desktop: rendered GSAP signal styles actually change', samples > 1, samples)
        if video.evaluate('(v) => v.paused'):
            page.locator('#video-toggle').click()
        before = video.evaluate('(v) => v.currentTime')
        page.wait_for_timeout(650)
        after = video.evaluate('(v) => v.currentTime')
        record('Video: actual playback time advances', after > before, {'before': before, 'after': after})
        page.locator('#video-toggle').click()
        record('Video: user pause works', video.evaluate('(v) => v.paused'))
        page.locator('#video-toggle').click()
        record('Video: user resume works', not video.evaluate('(v) => v.paused'))
        page.locator('#field').scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        record('Video: pauses outside viewport', video.evaluate('(v) => v.paused'))
        page.locator('#origin').scroll_into_view_if_needed()
        if video.evaluate('(v) => v.paused'):
            page.locator('#video-toggle').click()
        page.wait_for_function('document.querySelector("#origin-video").ended', timeout=15000)
        record('Video: finishes once, does not loop', video.evaluate('(v) => v.ended && v.paused && !v.loop'))
        screenshot(page, 'r31-video-ended.png')
        page.locator('#video-toggle').click()
        page.wait_for_timeout(300)
        record('Video: explicit replay', video.evaluate('(v) => !v.paused && v.currentTime < 2'))
    except Exception as error:
        record('Media and GSAP scenario', False, str(error))
    finally:
        page.close()


def alternatives(browser):
    scenarios = (
        ('no-js', {'java_script_enabled': False}, None),
        ('reduced-motion', {'reduced_motion': 'reduce'}, None),
        ('video-failed', {}, '**/origin.mp4*'),
        ('gsap-failed', {}, '**/gsap.min.js*'),
        ('image-failed', {}, '**/origin.webp*'),
        ('save-data', {}, None),
    )
    for name, options, blocked in scenarios:
        context = browser.new_context(viewport={'width': 1440, 'height': 900}, **options)
        if name == 'save-data':
            context.add_init_script('Object.defineProperty(navigator, "connection", {value: {saveData: true, addEventListener() {}}, configurable: true})')
        if blocked:
            context.route(blocked, lambda route: route.abort())
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        try:
            visit(page)
            common(page, name)
            if name in ('no-js', 'reduced-motion', 'save-data'):
                record(name + ': video remains still', page.locator('#origin-video').evaluate('(v) => v.paused && v.currentTime === 0'))
            if name != 'image-failed':
                record(name + ': valid poster retained', poster_ready(page))
            if name == 'no-js':
                record('No JS: all research explanations readable', all(visible(page, f'[data-step-panel="{step}"]') for step in ('observation', 'alternative', 'next')))
            else:
                button = page.locator('[data-research-step="alternative"]')
                button.click()
                record(name + ': research still works', button.get_attribute('aria-pressed') == 'true' and visible(page, '[data-step-panel="alternative"]'))
                record(name + ': no uncaught JS errors', not errors, errors)
            if name == 'gsap-failed':
                record('GSAP failure actually simulated', page.evaluate('typeof window.gsap === "undefined"'))
            if name == 'video-failed':
                page.locator('#origin').scroll_into_view_if_needed()
                page.wait_for_timeout(400)
                record('Video failure actually simulated', page.locator('#origin-video').evaluate('(v) => !!v.error || v.readyState === 0'))
            if name in ('reduced-motion', 'save-data'):
                record(name + ': no active GSAP animation', page.evaluate('!window.gsap || !window.gsap.globalTimeline.getChildren(true, true, true).some(x => x.isActive())'))
            page.locator('#origin').scroll_into_view_if_needed()
            screenshot(page, f'r31-{name}.png')
        except Exception as error:
            record(name + ': fallback scenario', False, str(error))
        finally:
            context.close()


def mobile_touch(browser):
    context = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    page = context.new_page()
    try:
        visit(page)
        page.locator('#video-toggle').tap()
        page.wait_for_function('document.querySelector("#origin-video").currentTime > 0', timeout=20000)
        record('Mobile touch: explicit video play works', not page.locator('#origin-video').evaluate('(v) => v.paused'))
        page.locator('#video-toggle').tap()
        record('Mobile touch: pause works', page.locator('#origin-video').evaluate('(v) => v.paused'))
        page.locator('[data-research-step="next"]').tap()
        record('Mobile touch: research selection works', page.locator('[data-research-step="next"]').get_attribute('aria-pressed') == 'true')
        menu = page.locator('.menu-btn')
        if menu.count() and menu.is_visible():
            menu.tap()
            record('Mobile touch: menu opens', menu.get_attribute('aria-expanded') == 'true')
            page.keyboard.press('Escape')
            record('Mobile: Escape closes menu', menu.get_attribute('aria-expanded') == 'false')
    except Exception as error:
        record('Mobile touch scenario', False, str(error))
    finally:
        context.close()


def preserved_routes(browser):
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    try:
        visit(page)
        page.locator('#question').fill('정보 흐름을 함께 살펴보고 싶습니다.')
        href = page.locator('#email-question').get_attribute('href')
        record('Inquiry: mail draft is prepared, never sent', href.startswith('mailto:weplacehyun@naver.com') and 'body=' in href)
        record('Inquiry: does not claim automatic submission', '자동 저장·전송하지 않습니다.' in page.locator('body').inner_text())
        for path in ('services/', 'research/lab/', 'research/notes/', 'research/chore-to-play/', 'signal-studio/', 'work/weplace/'):
            response = page.goto(urljoin(BASE, '/' + path), wait_until='domcontentloaded')
            record(f'Existing /{path}: HTTP 200 + H1', response.status == 200 and page.locator('h1').count() == 1)
        response = page.goto(urljoin(BASE, '/sitemap.xml'))
        record('Preview sitemap excludes review route', 'r31-review' not in response.text() and '<url>' not in response.text())
        response = page.goto(urljoin(BASE, '/robots.txt'))
        record('Preview permits crawling noindex', 'Allow: /' in response.text() and 'Disallow: /' not in response.text())
    except Exception as error:
        record('Preserved route scenario', False, str(error))
    finally:
        page.close()


def main():
    meta = {'url': BASE, 'sha': SHA, 'environment': 'GitHub Actions / Chromium / Playwright 1.57.0',
            'not_run': ['physical iOS/Android devices', 'Safari and Firefox', 'screen reader listening', 'browser native 200% zoom', 'customer comprehension', 'real inquiry delivery', 'production Core Web Vitals']}
    try:
        ready()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            viewports(browser)
            keyboard(browser)
            media_and_motion(browser)
            alternatives(browser)
            mobile_touch(browser)
            preserved_routes(browser)
            browser.close()
    except Exception as error:
        record('Browser runner', False, str(error))
    failures = sum(row['status'] == 'FAIL' for row in ROWS)
    meta.update({'checks': len(ROWS), 'passed': len(ROWS) - failures, 'failed': failures, 'result': 'FAIL' if failures else 'PASS', 'rows': ROWS})
    (OUT / 'results.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({key: meta[key] for key in ('sha', 'checks', 'passed', 'failed', 'result')}), flush=True)
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    main()
