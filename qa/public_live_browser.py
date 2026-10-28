#!/usr/bin/env python3
"""Read-only browser QA for PR #10 live-safe static release.

Screenshots and JSON are kept as CI artifacts (never copied into the public dist).
The runner never clicks a mailto action, sends a form, enters customer data,
changes billing, or edits a remote account.
"""
import json
import os
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE=os.environ.get("PREVIEW_URL","https://deploy-preview-10--mashcore.netlify.app/").rstrip("/")+"/"
OUT=Path("qa/public-evidence")
OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def record(name,okay,detail=""):
    row={"check":name,"status":"PASS" if okay else "FAIL","detail":detail}
    checks.append(row)
    print(f"{row['status']}: {name}" + (f" — {str(detail)[:160]}" if detail else ""),flush=True)

def visit(page,path="/"):
    url=urljoin(BASE,path.lstrip("/"))
    last=""
    for i in range(18):
        try:
            res=page.goto(url,wait_until="domcontentloaded",timeout=18000)
            if res and res.status==200 and (path!="/" or "왜 잠시 멈췄을까요?" in page.content()):
                return res
            last=f"HTTP {res.status if res else 'none'} or older preview"
        except Exception as e:
            last=str(e)[:170]
        page.wait_for_timeout(2500)
    raise RuntimeError(f"Preview not ready: {url} ({last})")

def overflow(page):
    return page.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")

def visible(page,selector):
    x=page.locator(selector)
    return x.count()>=1 and x.first.is_visible()

def screen(browser,w,h):
    page=browser.new_page(viewport={"width":w,"height":h},device_scale_factor=1)
    errors=[]
    page.on("pageerror",lambda x:errors.append(str(x)))
    try:
        res=visit(page)
        record(f"{w} homepage HTTP",res.status==200)
        record(f"{w} unique H1",page.locator("h1").count()==1)
        record(f"{w} question is readable","왜 잠시 멈췄을까요?" in page.locator("h1").inner_text())
        record(f"{w} hero CTA visible",visible(page,'a.mc-hero-action[href="/services/"]'))
        if visible(page,'a.mc-hero-action[href="/services/"]'):
            box=page.locator("a.mc-hero-action").bounding_box()
            record(f"{w} hero CTA above fold",bool(box and box["y"]+box["height"]<=h+2),box)
        record(f"{w} four original scene IDs",[page.locator(f'#{id}[data-chapter]').count() for id in ("origin","research","field","invitation")]==[1,1,1,1])
        record(f"{w} LAB NOTES Studio routes",all(page.locator(f'a[href="{x}"]').count()>0 for x in ("/research/lab/","/research/notes/","/signal-studio/")))
        record(f"{w} no horizontal scroll",overflow(page)<=2,overflow(page))
        record(f"{w} no uncaught JS errors",not errors,errors)
        menu=page.locator(".menu-btn")
        if menu.count() and menu.is_visible():
            menu.click()
            record(f"{w} menu open",menu.get_attribute("aria-expanded")=="true")
            page.keyboard.press("Escape")
            record(f"{w} menu close Escape",menu.get_attribute("aria-expanded")=="false")
        else:
            record(f"{w} desktop nav visible",visible(page,"#main-nav"))
        page.screenshot(path=str(OUT/f"home-{w}-fold.png"),full_page=False,animations="disabled")
        if w in (390,1440):
            page.screenshot(path=str(OUT/f"home-{w}-full.png"),full_page=True,animations="disabled",timeout=35000)
    except Exception as e:
        record(f"{w} home scenario complete",False,str(e))
        try:page.screenshot(path=str(OUT/f"home-{w}-error.png"),full_page=False)
        except:pass
    finally:page.close()

def details(browser):
    page=browser.new_page(viewport={"width":390,"height":844})
    routes={
      "research/lab/":("관찰","/#invitation"),
      "research/notes/":("2026.05.11","/#invitation"),
      "signal-studio/":("Gate 0","/#invitation"),
      "work/weplace/":("독립","/#invitation"),
      "research/":("익숙한 장면","/research/lab/"),
      "services/":("서비스","/#invitation"),
      "about/":("Mashcore","/research/"),
      "policies/refund/":("환불","/services/")
    }
    try:
        for path,(word,link) in routes.items():
            try:
                r=visit(page,path)
                body=page.locator("body").inner_text()
                record(f"{path} HTTP + H1",r.status==200 and page.locator("h1").count()==1)
                record(f"{path} readable content",word in body)
                record(f"{path} intended next route",page.locator(f'a[href="{link}"]').count()>0)
                expected="https://mashcore.co.kr/"+path
                record(f"{path} canonical",page.locator('link[rel="canonical"]').first.get_attribute("href")==expected)
                tags=page.locator('meta[name="robots"]')
                record(f"{path} noindex on preview",tags.count()==1 and "noindex" in tags.first.get_attribute("content").lower() and "noindex" in r.headers.get("x-robots-tag","").lower())
                record(f"{path} no overflow",overflow(page)<=2,overflow(page))
                if path in ("research/lab/","research/notes/","signal-studio/","work/weplace/"):
                    page.screenshot(path=str(OUT/f"{path.strip('/').replace('/','-')}.png"),full_page=True,animations="disabled",timeout=35000)
            except Exception as e:record(f"{path} detail scenario complete",False,str(e))
        visit(page,"research/notes/")
        record("Market original URL preserved",page.locator('a[href="https://mashcore-market-notes.netlify.app/"]').count()==1)
        visit(page,"signal-studio/")
        s=page.locator("body").inner_text()
        record("Studio local/Mock boundaries",all(x in s for x in ("Gate 0","Mock","미검증")))
        visit(page,"research/chore-to-play/")
        buttons=page.locator("[data-spatial-select]")
        record("Chore-to-Play six perspectives",buttons.count()==6)
        if buttons.count()==6:
            buttons.nth(2).click()
            record("Chore-to-Play selection",buttons.nth(2).get_attribute("aria-pressed")=="true")
        res=visit(page,"robots.txt")
        record("Preview robots allows reading noindex","Allow: /" in res.text() and "Disallow: /" not in res.text())
        res=visit(page,"sitemap.xml")
        record("Preview sitemap excludes draft URLs","<url>" not in res.text())
    finally:page.close()

def alternatives(browser):
    context=browser.new_context(viewport={"width":390,"height":844},java_script_enabled=False)
    page=context.new_page()
    try:
        visit(page)
        record("JS disabled: H1 & service CTA",visible(page,"#opening-title") and visible(page,".mc-hero-action"))
    except Exception as e:record("JS disabled scenario",False,str(e))
    finally:context.close()

    context=browser.new_context(viewport={"width":390,"height":844},reduced_motion="reduce")
    page=context.new_page()
    try:
        visit(page)
        record("reduced motion: visible question/CTA",visible(page,"#opening-title") and visible(page,".mc-hero-action"))
    except Exception as e:record("reduced motion scenario",False,str(e))
    finally:context.close()

    context=browser.new_context(viewport={"width":400,"height":460},device_scale_factor=2)
    page=context.new_page()
    try:
        visit(page)
        record("200% reflow proxy: no horizontal scroll",overflow(page)<=2,overflow(page))
        record("200% reflow proxy: CTA visible",visible(page,".mc-hero-action"))
    except Exception as e:record("200% reflow proxy scenario",False,str(e))
    finally:context.close()

    context=browser.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True)
    page=context.new_page()
    try:
        visit(page)
        record("mobile touch CTA",visible(page,".mc-hero-action"))
        btn=page.locator(".menu-btn")
        if btn.count() and btn.is_visible():
            btn.tap()
            record("mobile touch menu open",btn.get_attribute("aria-expanded")=="true")
    except Exception as e:record("mobile touch scenario",False,str(e))
    finally:context.close()

    page=browser.new_page(viewport={"width":390,"height":844})
    try:
        visit(page)
        question=page.locator("#question")
        question.fill("홈페이지 정보 흐름을 확인하고 싶습니다.")
        link=page.locator("#email-question").get_attribute("href") or ""
        record("Inquiry opens mail draft only","mailto:" in link and "body=" in link,link[:130])
        record("Inquiry has no form submission button",page.locator('button[type="submit"]').count()==0)
        record("Inquiry text remains in field",question.input_value().startswith("홈페이지"))
    except Exception as e:record("inquiry scenario",False,str(e))
    finally:page.close()

def main():
    meta={"url":BASE,"sha":os.environ.get("QA_COMMIT",""),"environment":"GitHub Actions / Chromium",
          "not_run":["physical devices","native browser 200% zoom","assistive-technology human test","customer comprehension","mail delivery","production RUM"]}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
            for w,h in ((320,700),(390,844),(768,1024),(1440,900)):screen(browser,w,h)
            details(browser)
            alternatives(browser)
            browser.close()
    except Exception as e:record("browser runner failed",False,str(e))
    failed=[x for x in checks if x["status"]=="FAIL"]
    meta.update({"checks":len(checks),"passed":len(checks)-len(failed),"failed":len(failed),"result":"PASS" if not failed else "FAIL","rows":checks})
    (OUT/"results.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:meta[k] for k in ("sha","checks","passed","failed","result")},ensure_ascii=False),flush=True)
    raise SystemExit(bool(failed))

if __name__=="__main__":main()
