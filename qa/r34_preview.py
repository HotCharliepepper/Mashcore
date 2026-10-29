"""R3.4 IA preview browser checks, no real submission."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

URL=os.environ.get("R34_URL","http://127.0.0.1:8333/r34-review/")
OUT=Path("qa/r34-evidence")
OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok,detail=None):
    checks.append(dict(check=name,status="PASS" if ok else "FAIL",detail=detail))
    print(checks[-1],flush=True)
with sync_playwright() as p:
    for engine in ("chromium","webkit"):
        browser=getattr(p,engine).launch()
        for w,h in ((1440,900),(390,844),(320,760)):
            if engine=="webkit" and w!=390: continue
            page=browser.new_page(viewport={"width":w,"height":h})
            errors=[]
            page.on("pageerror",lambda error:errors.append(str(error)))
            page.goto(URL,wait_until="load",timeout=20000)
            label=f"{engine}-{w}x{h}"
            check(label+" title visible",page.locator("#view-home .hero-title").is_visible())
            check(label+" one active heading",page.locator("h1:visible").count()==1)
            check(label+" no overflow",page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"))
            check(label+" image loaded",page.locator(".hero-photo img").first.evaluate("(el)=>el.naturalWidth>0"))
            check(label+" no runtime error",not errors,errors)
            check(label+" no private name","LEDGER" not in page.content())
            page.screenshot(path=str(OUT/(label+"-main.png")))
            page.locator('button[data-review-go="lab"]').click()
            check(label+" lab",page.locator("#view-lab").is_visible() and page.locator("#view-lab .detail-title").is_visible())
            page.locator('button[data-review-go="notes"]').click()
            check(label+" notes",page.locator("#view-notes").is_visible())
            page.locator('button[data-review-go="studio"]').click()
            check(label+" studio",page.locator("#view-studio").is_visible())
            page.locator('button[data-review-go="home"]').click()
            page.locator('button[data-obs="alternative"]').click()
            check(label+" research tab",page.locator('[data-obs-panel="alternative"]').is_visible())
            page.locator('button[data-proof="after"]').click()
            check(label+" comparison",page.locator(".proof-card").get_attribute("data-state")=="after")
            if w<821:check(label+" mobile menu",page.locator(".mobilemenu summary").is_visible())
            page.close()
        browser.close()
(OUT/"results.json").write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding="utf-8")
failed=[x for x in checks if x["status"]=="FAIL"]
print(json.dumps({"pass":len(checks)-len(failed),"fail":len(failed)}),flush=True)
if failed:raise SystemExit(1)
