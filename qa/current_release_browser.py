#!/usr/bin/env python3
"""Behavior gate for the current Interlude/VALUE FLOW release, not only A20.

Uses a local built dist by default; --base-url can verify the same deployed build.
No submission is sent: every POST is blocked and recorded as a failure.
"""
from pathlib import Path
import argparse, contextlib, functools, http.server, json, os, socketserver, threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
KEYS = ['consulting', 'marketing', 'design', 'space', 'experience', 'reservation']

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

@contextlib.contextmanager
def serve(base):
    if base:
        yield base.rstrip('/') + '/'
        return
    handler = functools.partial(QuietHandler, directory=str(ROOT / 'dist'))
    with socketserver.TCPServer(('127.0.0.1', 0), handler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            yield f'http://127.0.0.1:{server.server_address[1]}/'
        finally:
            server.shutdown()

def test(base):
    checks, failures, errors, posts = [], [], [], []
    def check(name, condition):
        (checks if condition else failures).append(name)
    with sync_playwright() as engine:
        browser = engine.chromium.launch(headless=True, args=['--no-sandbox'], executable_path=os.environ.get('CHROMIUM_PATH') or None)
        def open_page(width=390, mode='normal'):
            context = browser.new_context(viewport={'width': width, 'height': 900 if width == 1440 else 844}, has_touch=width < 500, is_mobile=width < 500, java_script_enabled=mode != 'no-js', reduced_motion='reduce' if mode == 'reduced' else 'no-preference', permissions=['clipboard-read','clipboard-write'], accept_downloads=True)
            page = context.new_page()
            page.set_default_timeout(20000)
            page.on('pageerror', lambda error: errors.append(str(error)))
            def route_request(route):
                if route.request.method == 'POST':
                    posts.append(route.request.url)
                    route.abort()
                elif mode == 'media-failure' and route.request.resource_type in ('font', 'image', 'media'):
                    route.abort()
                else:
                    route.continue_()
            page.route('**/*', route_request)
            page.goto(base, wait_until='domcontentloaded')
            page.evaluate('document.fonts.ready')
            if mode != 'no-js':
                page.wait_for_function("document.querySelector('#value-flow')?.dataset.valueEnhanced === 'true'")
            return context, page
        try:
            for width in [1440, 768, 390, 360, 320]:
                context, page = open_page(width)
                order = page.evaluate("""() => {const ids=[...document.querySelector('main').children].map(e=>e.id);return {ids,order:ids.indexOf('from-ash-to-core')<ids.indexOf('value-flow')&&ids.indexOf('value-flow')<ids.indexOf('research'),aliases:['origin','research','field','invitation','ash-to-core','ai-dialogue'].every(id=>document.querySelectorAll('#'+id).length===1)};}""")
                check(f'{width}: preserved scene order and anchors', order['order'] and order['aliases'])
                check(f'{width}: Interlude has three static explanations', all(text in page.locator('#from-ash-to-core').inner_text() for text in ['그냥 지나쳤던 장면.', '무엇을 먼저 확인해야 할까요?', '먼저 보여줄 한 가지를 정합니다.']))
                models = []
                for key in KEYS:
                    button = page.locator(f'[data-value-choice="{key}"]')
                    button.tap() if width < 500 else button.click()
                    current = page.locator('#value-flow').evaluate("""e => {const panel=[...e.querySelectorAll('[data-value-panel]')].filter(p=>!p.hidden);const model=panel[0]?.querySelector('[data-value-model]');return {selected:e.dataset.valueSelected,count:panel.length,key:panel[0]?.dataset.valuePanel,model:model?.innerHTML,text:model?.innerText,overflow:document.documentElement.scrollWidth-innerWidth};} """)
                    check(f'{width}: {key} actual result', current['selected'] == key and current['key'] == key and current['count'] == 1 and bool(current['text']) and current['overflow'] <= 1)
                    models.append(current['model'])
                check(f'{width}: six authored model structures', len(set(models)) == 6)
                page.locator('#value-flow a[href="#ai-dialogue"]').click()
                page.wait_for_function("location.hash === '#ai-dialogue'")
                for key in ['observe', 'reframe', 'verify', 'observe']:
                    page.locator(f'[data-r092-choice="{key}"]').click()
                    check(f'{width}: HUMAN {key}', page.evaluate('window.mashcoreR092Dialogue.getState().selected') == key)
                page.locator('#value-flow a[href="#capabilities"]').click()
                page.wait_for_function("location.hash === '#capabilities'")
                for mode in ['before', 'after', 'both']:
                    page.locator(f'[data-field-mode="{mode}"]').click()
                    check(f'{width}: FIELD {mode}', page.locator('[data-field-compare]').get_attribute('data-field-view') == mode)
                context.close()
            context, page = open_page(1440)
            page.locator('[data-value-choice]').first.focus()
            for i, key in enumerate(KEYS):
                if i:
                    page.keyboard.press('Tab')
                page.keyboard.press('Space' if i % 2 else 'Enter')
                check('Keyboard ' + key, page.evaluate('document.activeElement.dataset.valueChoice') == key and page.locator('#value-flow').get_attribute('data-value-selected') == key)
            context.close()
            for mode in ['reduced', 'no-js', 'media-failure']:
                context, page = open_page(390, mode)
                for scene in ['from-ash-to-core','value-flow','ai-dialogue','capabilities','invitation']:
                    check(mode + ' readable ' + scene, len(page.locator('#'+scene).inner_text().strip()) > 20)
                if mode == 'no-js':
                    check('No-JS all six explanations', all(page.locator('[data-value-fallback]').inner_text().find(label) >= 0 for label in ['컨설팅','온라인 마케팅','디자인','공간 경험 설계','고객 경험 개선','예약 동선 개선']))
                else:
                    page.locator('[data-value-choice="reservation"]').tap()
                    check(mode + ' immediate selection', page.locator('#value-flow').get_attribute('data-value-selected') == 'reservation')
                    if mode == 'reduced':
                        check('Reduced no result animation', page.locator('#value-flow').evaluate("e=>e.getAnimations({subtree:true}).filter(a=>a.playState==='running').length") == 0)
                page.locator('#value-flow a[href="#ai-dialogue"]').click()
                check(mode + ' next link', page.url.endswith('#ai-dialogue'))
                context.close()
            context, page = open_page(390)
            page.locator('input[name="mini-intent"][value="website"]').tap()
            page.locator('[data-mini-contact]').tap()
            page.wait_for_url('**/contact/**')
            check('Inquiry choice reaches editable draft', '홈페이지' in page.locator('#situation').input_value())
            page.locator('#situation').fill('릴리스 QA 로컬 초안입니다. 실제 발송하지 않습니다.')
            page.locator('button[type="submit"]').click()
            draft = page.locator('[data-inquiry-output]').input_value()
            page.locator('[data-inquiry-copy]').click()
            page.wait_for_function("document.querySelector('[data-inquiry-status]').textContent.includes('복사')")
            clipboard = page.evaluate('navigator.clipboard.readText()')
            check('Actual clipboard with native Windows line ending normalization', draft.replace('\r\n','\n') == clipboard.replace('\r\n','\n'))
            with page.expect_download() as download_info:
                page.locator('[data-inquiry-download]').click()
            downloaded = Path(download_info.value.path()).read_text(encoding='utf-8-sig')
            check('Actual text download', downloaded.replace('\r\n','\n') == draft.replace('\r\n','\n'))
            check('No false sent state', '전송되지 않았습니다' in page.locator('[data-inquiry-status]').inner_text())
            check('Explicit direct mail route', page.locator('.contact-direct a').get_attribute('href').startswith('mailto:'))
            context.close()
        except Exception as exc:
            failures.append(f'Exception: {exc}')
        finally:
            browser.close()
    check('No page JavaScript errors', not errors)
    check('No POST or submission', not posts)
    result={'result':'PASS' if not failures else 'FAIL','base':base,'passed':len(checks),'failed':len(failures),'failures':failures,'errors':errors,'posts':posts}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url')
    args=parser.parse_args()
    with serve(args.base_url) as base:
        result=test(base)
    raise SystemExit(0 if result['result']=='PASS' else 1)
