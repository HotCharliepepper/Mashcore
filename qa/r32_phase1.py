"""Exact-commit Deploy Preview checks. Screenshots/JSON remain CI artifacts.

No mailto click, form submission, customer input, payment or account mutation.
Real-device testing, Lighthouse scores and field Core Web Vitals are not implied.
"""
import json
import os
import time
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import quote
from playwright.sync_api import sync_playwright

BASE = os.environ['PREVIEW_URL'].rstrip('/') + '/'
SHA = os.environ['QA_COMMIT']
OUT = Path('qa/r33-evidence')
OUT.mkdir(parents=True, exist_ok=True)
ROWS = []
METRICS = []
PROBE = r"""(() => {
  window.__wordQA = {cls:0, shifts:[], longTasks:[], starts:{origin:0,research:0}};
  try { new PerformanceObserver(list => list.getEntries().forEach(e => {
    if(!e.hadRecentInput) { __wordQA.cls += e.value; __wordQA.shifts.push({value:e.value,sources:e.sources.map(s=>({tag:s.node?.tagName,cls:String(s.node?.className||''),from:s.previousRect.y,to:s.currentRect.y}))}); }
  })).observe({type:'layout-shift',buffered:true}); } catch(_) {}
  try { new PerformanceObserver(list => list.getEntries().forEach(e => __wordQA.longTasks.push(e.duration)))
    .observe({type:'longtask',buffered:true}); } catch(_) {}
  new MutationObserver(list => {
    for(const change of list) if(change.type === 'attributes' && change.target.dataset.wordMotionState === 'playing')
      __wordQA.starts[change.target.dataset.wordMotion]++;
    if(!__wordQA.first && document.querySelector('.r31-primary')) requestAnimationFrame(() => {
      if(!__wordQA.first) __wordQA.first = [...document.querySelectorAll('#opening-title,.r31-role,.r31-primary')].map(e => {
        const s=getComputedStyle(e),r=e.getBoundingClientRect();
        return {text:e.textContent,visible:r.width>0 && r.height>0 && Number(s.opacity)===1 && s.visibility==='visible'};
      });
    });
  }).observe(document,{subtree:true,childList:true,attributes:true,attributeFilter:['data-word-motion-state']});
})()"""


def record(name, ok, detail=''):
    row = {'check': name, 'status': 'PASS' if ok else 'FAIL', 'detail': detail}
    ROWS.append(row)
    print(f"{row['status']}: {name} {str(detail)[:170]}", flush=True)


def ready():
    for attempt in range(48):
        try:
            with urlopen(BASE + '?qa_revision=' + SHA, timeout=15) as response:
                if f'name="r31-commit" content="{SHA}"' in response.read().decode('utf-8'):
                    return
        except Exception:
            pass
        if attempt % 6 == 0:
            print('Waiting for exact Netlify preview ' + SHA, flush=True)
        time.sleep(5)
    raise RuntimeError('Exact source commit is not ready on Deploy Preview')


def visit(page, route=''):
    response = page.goto(BASE + route, wait_until='domcontentloaded', timeout=45000)
    if not response or response.status != 200:
        raise RuntimeError('HTTP failure ' + route)
    page.wait_for_function('document.querySelector(\'meta[name="r31-commit"]\')')
    marker = page.locator('meta[name="r31-commit"]').get_attribute('content')
    if marker != SHA:
        raise RuntimeError('Wrong commit: ' + str(marker))


def snapshot(page):
    return page.evaluate(r"""(() => {
      const box = e => {const r=e.getBoundingClientRect(),s=getComputedStyle(e); return {
        x:r.x,y:r.y,width:r.width,height:r.height,visible:r.width>0&&r.height>0&&s.visibility==='visible'&&Number(s.opacity)===1};};
      return {width:innerWidth,overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,
        h1:box(document.querySelector('#opening-title')),cta:box(document.querySelector('.r31-primary')),
        scene:box(document.querySelector('.r31-media')),poster:box(document.querySelector('.r31-poster')),
        duration:document.documentElement.dataset.wordMotionDuration,
        preset:document.documentElement.dataset.wordMotionPreset,
        layout:document.documentElement.dataset.r32Layout,
        role:box(document.querySelector('.r31-role')),words:document.querySelectorAll('.r32-word').length,
        first:window.__wordQA?.first,cls:window.__wordQA?.cls,starts:window.__wordQA?.starts,
        shifts:window.__wordQA?.shifts,
        longTasks:window.__wordQA?.longTasks,
        fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),
        wordRequests:performance.getEntriesByType('resource').filter(e=>/word-motion|SplitText|ScrollTrigger/.test(e.name))
          .map(e=>({url:e.name,bytes:e.transferSize,duration:e.duration})),
        h1Text:document.querySelector('#opening-title').textContent,
        researchText:document.querySelector('#r31-research-title').textContent,
        origin:document.querySelector('#opening-title').dataset.wordMotionState,
        research:document.querySelector('#r31-research-title').dataset.wordMotionState};
    })()""")


def readable(page, name):
    shot = snapshot(page)
    record(name + ' copy/role/CTA readable', all(shot[k]['visible'] for k in ['h1', 'role', 'cta']))
    record(name + ' Korean copy preserved', '그 사람은,' in shot['h1Text'] and '멈췄을까요?' in shot['h1Text'] and '다르게 읽는 일.' in shot['researchText'])
    record(name + ' no horizontal overflow', shot['overflow'] <= 2, shot['overflow'])
    return shot


def research_regression(page, name):
    for step in ['alternative', 'next', 'observation']:
        button = page.locator(f'[data-research-step="{step}"]')
        button.focus()
        page.keyboard.press('Enter')
        record(name + ' research ' + step, button.get_attribute('aria-pressed') == 'true' and page.locator(f'[data-step-panel="{step}"]').is_visible())
    record(name + ' one research panel', page.locator('[data-step-panel]:visible').count() == 1)


def screen(browser, width, height, route='', engine='chromium'):
    name = f'{engine}-{width}x{height}-' + ('mobile-route' if route else 'home')
    context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=1,
                                  is_mobile=width <= 390, has_touch=width <= 390)
    context.add_init_script(PROBE)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    try:
        visit(page, route + '?layout=before')
        page.evaluate('document.fonts.ready.then(()=>true)')
        page.wait_for_timeout(500)
        page.evaluate("document.querySelector('#origin-video').pause()")
        before = snapshot(page)
        page.screenshot(path=str(OUT / (name + '-before.png')))
        record(name + ' R3.1 before mode', before['layout'] == 'before' and page.locator('.r32-word').count() == 0)
        visit(page, route)
        initial = readable(page, name + ' initial')
        page.wait_for_function("document.querySelector('#opening-title').dataset.wordMotionState === 'complete'", timeout=12000)
        record(name + ' matching GSAP plugins', page.evaluate("[gsap.version,SplitText.version,ScrollTrigger.version].every(v=>v==='3.15.0')"))
        record(name + ' exactly one core request', page.evaluate("performance.getEntriesByType('resource').filter(e=>e.name.endsWith('/assets/r31/gsap.min.js')).length") == 1)
        complete = readable(page, name + ' complete')
        record(name + ' default duration 2.2s', complete['duration'] == '2.2')
        if width <= 820 and height >= 760:
            record(name + ' entire observation frame above fold', complete['scene']['y'] >= 0 and complete['scene']['y'] + complete['scene']['height'] <= height, complete['scene'])
            record(name + ' scene before question', complete['scene']['y'] + complete['scene']['height'] <= complete['h1']['y'])
            record(name + ' question and CTA above fold', complete['h1']['y'] + complete['h1']['height'] <= height and complete['cta']['y'] + complete['cta']['height'] <= height)
        record(name + ' first frame readable', bool(complete['first']) and all(x['visible'] for x in complete['first']), complete['first'])
        record(name + ' CTA reachable', complete['cta']['height'] >= 44 and complete['cta']['visible'], complete['cta'])
        record(name + ' Origin wrappers reverted', page.locator('#opening-title .r32-word').count() == 0)
        page.evaluate("document.querySelector('#origin-video').pause()")
        page.screenshot(path=str(OUT / (name + '-after.png')))
        page.locator('#r31-research-title').evaluate("e=>e.scrollIntoView({block:'center',behavior:'instant'})")
        page.wait_for_function("document.querySelector('#r31-research-title').dataset.wordMotionState === 'complete'", timeout=10000)
        page.screenshot(path=str(OUT / (name + '-research.png')))
        count = page.evaluate('__wordQA.starts.research')
        page.evaluate('scrollTo(0,0)')
        page.wait_for_timeout(200)
        page.locator('#r31-research-title').evaluate("e=>e.scrollIntoView({block:'center',behavior:'instant'})")
        page.wait_for_timeout(300)
        record(name + ' Research runs once', count == 1 and page.evaluate('__wordQA.starts.research') == 1, count)
        record(name + ' Research wrappers reverted', page.locator('#r31-research-title .r32-word').count() == 0)
        research_regression(page, name)
        page.locator('#question').fill('QA local text only')
        record(name + ' inquiry count', page.locator('#question-count').inner_text().startswith('18'))
        record(name + ' inquiry mail draft', quote('QA local text only') in page.locator('#email-question').get_attribute('href'))
        record(name + ' word wrappers not tabbable', page.locator('.r32-word[tabindex]').count() == 0)
        page.evaluate('scrollTo(0,0)')
        menu = page.locator('.menu-btn')
        if menu.is_visible():
            menu.click()
            record(name + ' mobile menu opens', menu.get_attribute('aria-expanded') == 'true')
            page.keyboard.press('Escape')
            record(name + ' Escape returns menu focus', menu.get_attribute('aria-expanded') == 'false' and menu.evaluate('(e)=>e===document.activeElement'))
        # Existing video UI must stay consistent with the actual media state.
        record(name + ' video state preserved', page.evaluate("(() => {const v=document.querySelector('#origin-video');return document.querySelector('#video-toggle').getAttribute('aria-pressed')===String(!v.paused&&!v.ended&&v.classList.contains('is-playing'));})()"))
        final = snapshot(page)
        record(name + ' CLS under .1 (includes fonts)', final['cls'] < .1, final['cls'])
        record(name + ' no page exceptions', not errors, errors)
        METRICS.append({'scenario': name, 'before': before, 'initial': initial, 'complete': complete, 'final': final})
    except Exception as error:
        record(name + ' scenario', False, str(error))
        try:
            page.screenshot(path=str(OUT / (name + '-error.png')))
        except Exception:
            pass
    finally:
        context.close()


def fallback(browser, mode):
    context = browser.new_context(viewport={'width': 390, 'height': 844},
        java_script_enabled=mode != 'no-js', reduced_motion='reduce' if mode == 'reduced' else 'no-preference')
    requests = []
    if mode == 'saveData':
        context.add_init_script("const c=new EventTarget();c.saveData=true;Object.defineProperty(navigator,'connection',{value:c,configurable:true})")
    blocks = {'core-fail': '**/gsap.min.js', 'split-fail': '**/SplitText.min.js',
              'trigger-fail': '**/ScrollTrigger.min.js', 'module-fail': '**/word-motion.js', 'video-fail': '**/origin.mp4'}
    if mode in blocks:
        context.route(blocks[mode], lambda route: route.abort())
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('request', lambda request: requests.append(request.url))
    try:
        visit(page, '?motion=still' if mode == 'still' else '')
        if mode == 'video-fail':
            page.locator('#video-toggle').click()
            page.wait_for_function("document.querySelector('#video-toggle').disabled")
            record('video-fail poster remains visible', page.locator('.r31-poster').is_visible() and not page.locator('#origin-video').evaluate('(v)=>v.classList.contains("is-playing")'))
            page.wait_for_function("document.querySelector('#opening-title').dataset.wordMotionState === 'complete'", timeout=12000)
        else:
            page.wait_for_timeout(700)
        readable(page, mode)
        record(mode + ' no leftover word wrappers', page.locator('.r32-word').count() == 0)
        page.screenshot(path=str(OUT / (mode + '-origin.png')))
        if mode in ['saveData', 'reduced', 'still', 'core-fail', 'no-js']:
            record(mode + ' no additional plugin requests', not any('SplitText.min.js' in x or 'ScrollTrigger.min.js' in x for x in requests), requests)
        if mode == 'no-js':
            record('no-js all research explanations readable', page.locator('[data-step-panel]:visible').count() == 3)
            page.locator('.r32-native-menu summary').click()
            record('no-js native navigation usable', page.locator('.r32-native-menu[open] a[href="/services/"]').is_visible())
            page.locator('.r32-native-menu summary').click()
        else:
            research_regression(page, mode)
        record(mode + ' no page exceptions', not errors, errors)
        page.screenshot(path=str(OUT / (mode + '.png')))
    except Exception as error:
        record(mode + ' scenario', False, str(error))
    finally:
        context.close()


def preference_and_resize(browser):
    for change in ['reduce', 'resize', 'saveData']:
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        if change == 'saveData':
            context.add_init_script("const c=new EventTarget();c.saveData=false;Object.defineProperty(navigator,'connection',{value:c,configurable:true})")
        page = context.new_page()
        try:
            visit(page)
            page.wait_for_function("document.querySelector('#opening-title').dataset.wordMotionState==='playing'", timeout=12000)
            if change == 'reduce':
                page.emulate_media(reduced_motion='reduce')
            elif change == 'resize':
                page.set_viewport_size({'width': 320, 'height': 760})
            else:
                page.evaluate("navigator.connection.saveData=true;navigator.connection.dispatchEvent(new Event('change'))")
            page.wait_for_timeout(150)
            record(change + ' active wrappers reverted', page.locator('.r32-word').count() == 0)
            readable(page, change + ' mid-motion')
        except Exception as error:
            record(change + ' mid-motion scenario', False, str(error))
        finally:
            context.close()


def baseline(browser):
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    context.route('**/word-motion.js', lambda route: route.abort())
    page = context.new_page()
    try:
        context.add_init_script(PROBE)
        visit(page)
        page.wait_for_timeout(2000)
        data = snapshot(page)
        METRICS.append({'scenario': 'baseline-without-word-module', 'final': data})
        normal = next((m for m in METRICS if m['scenario'] == 'chromium-1440-home'), None)
        if normal:
            delta = normal['complete']['cta']['y'] - data['cta']['y']
            record('CTA position equals non-word baseline', abs(delta) <= 1, delta)
            record('word-motion CLS delta <= .01', normal['final']['cls'] - data['cls'] <= .01,
                   {'with': normal['final']['cls'], 'without': data['cls']})
    finally:
        context.close()


def motion_comparison(browser):
    for mode, duration in [('calm','1.85'),('slow','2.2')]:
        context = browser.new_context(viewport={'width':390,'height':844})
        page = context.new_page()
        try:
            visit(page, '?motion=' + mode)
            page.wait_for_function("document.querySelector('#opening-title').dataset.wordMotionState==='playing'", timeout=12000)
            page.wait_for_timeout(250)
            data = page.locator('#opening-title .r32-word').evaluate_all("words=>words.map(w=>({y:new DOMMatrixReadOnly(getComputedStyle(w).transform).m42,opacity:getComputedStyle(w).opacity,color:getComputedStyle(w).color}))")
            record(mode + ' exact duration', page.evaluate('document.documentElement.dataset.wordMotionDuration') == duration)
            record(mode + ' stagger has sequential positions', len(data)>1 and max(d['y'] for d in data)-min(d['y'] for d in data)>.1, data)
            record(mode + ' words always readable', all(d['opacity']=='1' and 0<=d['y']<=14 for d in data))
            record(mode + ' sequential color variation', len(set(d['color'] for d in data))>1)
            page.screenshot(path=str(OUT/(mode+'-during-motion.png')))
            page.wait_for_function("document.querySelector('#opening-title').dataset.wordMotionState==='complete'", timeout=10000)
            page.locator('.r32-review summary').click()
            record(mode + ' active comparison link', page.locator(f'[data-r32-motion-choice="{mode}"]').get_attribute('aria-current')=='page')
            page.screenshot(path=str(OUT/(mode+'-comparison-controls.png')))
        except Exception as error:
            record(mode + ' comparison scenario', False, str(error))
        finally:
            context.close()


def video_and_cta(browser):
    context = browser.new_context(viewport={'width':390,'height':844})
    page = context.new_page()
    try:
        visit(page)
        page.locator('#video-toggle').click()
        page.wait_for_function("document.querySelector('#origin-video').currentTime>.2", timeout=12000)
        record('mobile video actually advances', page.locator('#video-toggle').get_attribute('aria-pressed')=='true')
        page.locator('#video-toggle').click()
        record('mobile pause restores still poster', page.locator('#video-toggle').get_attribute('aria-pressed')=='false' and not page.locator('#origin-video').evaluate('(v)=>v.classList.contains("is-playing")'))
        page.locator('.r31-primary').click()
        page.wait_for_url('**/services/')
        record('service CTA reaches real local route', page.locator('h1').count()==1 and page.url.endswith('/services/'))
    except Exception as error:
        record('video/CTA real action scenario', False, str(error))
    finally:
        context.close()


try:
    ready()
    with sync_playwright() as p:
        chromium = p.chromium.launch()
        for route in ['', 'mobile/']:
            for width, height in [(320, 760), (390, 844), (390, 667), (844, 390), (768, 1024), (1440, 900)]:
                screen(chromium, width, height, route)
        for mode in ['reduced', 'still', 'saveData', 'no-js', 'core-fail', 'split-fail', 'trigger-fail', 'module-fail', 'video-fail']:
            fallback(chromium, mode)
        motion_comparison(chromium)
        video_and_cta(chromium)
        preference_and_resize(chromium)
        baseline(chromium)
        chromium.close()
        webkit = p.webkit.launch()
        screen(webkit, 390, 844, engine='webkit')
        webkit.close()
except Exception as error:
    record('browser suite completion', False, str(error))
finally:
    result = {'commit': SHA, 'preview': BASE, 'checks': ROWS, 'metrics': METRICS,
              'not_run': ['physical iOS/Android', 'screen-reader user session', 'field Core Web Vitals', 'Lighthouse/throttled-lab score']}
    (OUT/'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    failed = [r for r in ROWS if r['status'] == 'FAIL']
    (OUT/'summary.md').write_text(f'# R3.2 Word Motion QA\n\nCommit: {SHA}\n\nPreview: {BASE}\n\nPASS: {len(ROWS)-len(failed)} / FAIL: {len(failed)}\n\n' + '\n'.join(f"- {r['check']}: {r['detail']}" for r in failed), encoding='utf-8')
    print(json.dumps({'commit': SHA, 'pass': len(ROWS)-len(failed), 'fail': len(failed), 'output': str(OUT)}), flush=True)
    if failed:
        raise SystemExit(1)
