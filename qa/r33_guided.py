"""Measured sequence, escape and native scroll checks; no submissions."""
import json, os
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('PREVIEW_URL','http://localhost:8333/').rstrip('/')+'/'
OUT=Path('qa/r33-evidence'); OUT.mkdir(exist_ok=True,parents=True)
rows=[]
def check(name, value, detail=None):
    rows.append(dict(check=name,status='PASS' if value else 'FAIL',detail=detail))
    print(rows[-1],flush=True)
with sync_playwright() as p:
    for engine in ('chromium','webkit'):
        browser=getattr(p,engine).launch()
        page=browser.new_page(viewport={'width':1440,'height':900})
        for mode,duration,gap in [('slow',2.2,.9),('calm',1.85,.7)]:
            page.goto(BASE+'?motion='+mode)
            page.wait_for_function("document.querySelector('#opening-title').dataset.wordMotionState==='playing'")
            data=page.evaluate("""() => {
                const el=document.querySelector('#opening-title');
                const words=[...el.querySelectorAll('.r32-word')];
                const timeline=gsap.globalTimeline.getChildren().find(t=>t.getChildren && t.getChildren().some(c=>c.targets?.().includes(words[0])));
                return {words:words.map(w=>w.textContent),duration:timeline.duration(),tweens:timeline.getChildren().filter(t=>t.vars.y===0).map(t=>({start:t.startTime(),end:t.endTime(),duration:t.duration()}))};
            }""")
            check(engine+mode+' three meaning units', data['words']==['그 사람은,','왜 잠시','멈췄을까요?'],data)
            check(engine+mode+' original accessible name', page.locator('#opening-title').get_attribute('aria-label')=='그 사람은, 왜 잠시 멈췄을까요?')
            check(engine+mode+' sequence duration',abs(data['duration']-(duration+2*gap))<.01,data)
            page.screenshot(path=str(OUT/(engine+mode+'-frame.png')))
            page.locator('.r31-primary').click()
            page.wait_for_url('**/services/')
            check(engine+mode+' immediate CTA during animation',page.url.endswith('/services/'))
        page.goto(BASE+'?scroll=free#invitation')
        page.wait_for_timeout(250)
        check(engine+' direct invitation free',page.evaluate("getComputedStyle(document.documentElement).scrollSnapType==='none'"))
        check(engine+' field invitation no snap',page.evaluate("['field','invitation'].every(id=>getComputedStyle(document.getElementById(id)).scrollSnapAlign==='none')"))
        page.goto(BASE)
        page.wait_for_function("document.querySelector('#opening-title').dataset.wordMotionState==='playing'")
        page.locator('.r32-review summary').click()
        page.locator('[data-r33-skip]').click()
        check(engine+' skip restores original',page.locator('#opening-title .r32-word').count()==0)
        page.locator('[data-r32-replay]').click()
        page.wait_for_function("document.querySelector('#opening-title').dataset.wordMotionState==='playing'")
        page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
        page.wait_for_function("document.querySelectorAll('#opening-title .r32-word').length===0",timeout=1500)
        check(engine+' scroll interrupts and escapes',page.locator('#opening-title .r32-word').count()==0 and page.evaluate('scrollY>600'))
        page.goto(BASE+'?motion=still')
        page.evaluate("document.documentElement.style.zoom='2'")
        page.wait_for_timeout(250)
        check(engine+' 200 percent no overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'))
        page.screenshot(path=str(OUT/(engine+'-zoom200.png')))
        page.set_viewport_size({'width':390,'height':667})
        page.goto(BASE+'?motion=still')
        page.evaluate("document.documentElement.style.zoom='2'")
        page.wait_for_timeout(250)
        check(engine+' mobile 200 percent no overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'))
        page.screenshot(path=str(OUT/(engine+'-mobile200.png')))
        browser.close()
(OUT/'guided-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
assert all(r['status']=='PASS' for r in rows)
