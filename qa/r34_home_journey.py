"""R3.4 public home journey checks on Netlify Draft Preview; never submit customer data."""
import json
import os
import time
from pathlib import Path
from urllib.request import Request, urlopen
from playwright.sync_api import sync_playwright

BASE=os.environ.get("PREVIEW_URL","http://127.0.0.1:8333/").rstrip("/")+"/"
SHA=os.environ.get("QA_COMMIT")
OUT=Path("qa/r34-home-evidence")
OUT.mkdir(parents=True,exist_ok=True)
checks=[]

def check(name,ok,detail=None):
    checks.append({"check":name,"status":"PASS" if ok else "FAIL","detail":detail})
    print(checks[-1],flush=True)

def exact_preview():
    if not SHA:
        return
    for attempt in range(30):
        try:
            req=Request(BASE,headers={"Cache-Control":"no-cache"})
            with urlopen(req,timeout=10) as response:
                text=response.read().decode("utf-8")
            if 'name="r31-commit" content="'+SHA+'"' in text:
                return
        except Exception as exc:
            print("preview retry",attempt,str(exc),flush=True)
        time.sleep(4)
    raise RuntimeError("Netlify Preview does not reflect exact PR head: "+SHA)

exact_preview()
with sync_playwright() as p:
    for browser_name in ("chromium","webkit"):
        engine=getattr(p,browser_name)
        browser=engine.launch()
        viewports=[(1440,900),(768,1024),(390,844),(320,760)] if browser_name=="chromium" else [(390,844)]
        for width,height in viewports:
            for route in ("","mobile/"):
                label=f"{browser_name}-{width}x{height}-{route or 'home'}"
                context=browser.new_context(viewport={"width":width,"height":height},reduced_motion="reduce")
                page=context.new_page()
                errors=[]
                page.on("pageerror",lambda e: errors.append(str(e)))
                response=page.goto(BASE+route,wait_until="domcontentloaded",timeout=25000)
                page.wait_for_timeout(200)
                check(label+" page ready",response is not None and response.status==200)
                check(label+" content identity",page.locator("meta[name='r31-commit']").get_attribute("content")==SHA if SHA else True)
                check(label+" four chapters",page.locator("section[data-chapter]").count()==4)
                check(label+" original hero CTA",page.locator("a.r31-primary[href='/services/']").count()==1)
                check(label+" three public entries",page.locator("a.r34-door").count()==3)
                routes=page.locator("a.r34-door").evaluate_all("(els)=>els.map(e=>e.getAttribute('href'))")
                check(label+" links to source details",routes==["/research/lab/","/research/notes/","/signal-studio/"],routes)
                check(label+" Ledger absent","LEDGER" not in page.content())
                check(label+" no horizontal overflow",page.evaluate("document.documentElement.scrollWidth <= innerWidth+2"))
                check(label+" JS no errors",not errors,errors)
                page.locator(".r34-doors").screenshot(path=str(OUT/(label+"-doors.png")))
                check(label+" synthetic before default",page.locator(".r34-before").is_visible() and not page.locator(".r34-after").is_visible())
                page.locator('input[name="r34-information-order"][value="after"]').check()
                check(label+" after radio works",page.locator(".r34-after").is_visible() and not page.locator(".r34-before").is_visible())
                page.locator(".r34-field-proof").screenshot(path=str(OUT/(label+"-proof.png")))
                detail=page.locator("details#chore-research")
                check(label+" deep study opt-in",detail.get_attribute("open") is None)
                detail.locator("summary").click()
                check(label+" six lenses still present",detail.get_attribute("open") is not None and detail.locator("[data-spatial-select]").count()==6)
                page.locator('[data-spatial-select="meaning"]').click()
                check(label+" retained spatial selection",page.locator("[data-spatial]").get_attribute("data-spatial-selected")=="meaning")
                if browser_name=="chromium":
                    page.evaluate("document.documentElement.style.zoom='2'")
                    page.wait_for_timeout(180)
                    check(label+" 200% CSS zoom reflow",page.evaluate("document.documentElement.scrollWidth <= innerWidth+2"),
                          page.evaluate("({scroll:document.documentElement.scrollWidth,width:innerWidth})"))
                    page.evaluate("document.documentElement.style.zoom=''")
                context.close()
        browser.close()
    # No-JavaScript fallback: native details, radio and links still work.
    browser=p.chromium.launch()
    context=browser.new_context(viewport={"width":390,"height":844},java_script_enabled=False)
    page=context.new_page()
    page.goto(BASE,wait_until="domcontentloaded",timeout=25000)
    check("no-js source links",page.locator("a.r34-door").count()==3)
    page.locator("details#chore-research > summary").click()
    check("no-js research detail open",page.locator("details#chore-research").get_attribute("open") is not None)
    page.locator('input[name="r34-information-order"][value="after"]').check()
    check("no-js comparison switch",page.locator(".r34-after").is_visible())
    context.close()
    browser.close()

OUT.joinpath("results.json").write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding="utf-8")
fails=[c for c in checks if c["status"]=="FAIL"]
print(json.dumps({"total":len(checks),"pass":len(checks)-len(fails),"fail":len(fails),"sha":SHA},ensure_ascii=False),flush=True)
if fails: raise SystemExit(1)
