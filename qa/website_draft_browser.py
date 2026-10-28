#!/usr/bin/env python3
"""Browser QA for the isolated MASHCORE Draft PR #9 preview.

Run: PREVIEW_URL=https://deploy-preview-9--mashcore.netlify.app \
     python3 qa/website_draft_browser.py
Only reads public review pages. Never sends inquiry, billing or customer data.
Browser screenshots and JSON evidence go to qa/browser-evidence/ (not dist).
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE = os.environ.get("PREVIEW_URL", "https://deploy-preview-9--mashcore.netlify.app/").rstrip("/") + "/"
OUT = Path(os.environ.get("QA_OUTPUT", "qa/browser-evidence"))
OUT.mkdir(parents=True, exist_ok=True)
results = []
failures = []


def check(name, ok, detail=None):
    entry = {"test": name, "result": "PASS" if ok else "FAIL", "detail": detail}
    results.append(entry)
    print(f"{entry['result']}: {name}" + (f" — {str(detail)[:180]}" if detail else ""), flush=True)
    if not ok:
        failures.append(entry)


def load(page, path="/", retries=3):
    url = urljoin(BASE, path.lstrip("/"))
    error = None
    for attempt in range(retries):
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=25000)
            if response and response.status < 500:
                return response
            error = f"HTTP {response.status if response else 'none'}"
        except Exception as exc:
            error = str(exc)[:250]
        page.wait_for_timeout(900 * (attempt + 1))
    raise RuntimeError(f"Could not load {url}: {error}")


def overflow(page):
    return page.evaluate("""() => {
      const w = document.documentElement.clientWidth;
      const items = [...document.querySelectorAll('body *')].filter(el => {
        if (getComputedStyle(el).position === 'fixed') return false;
        const r = el.getBoundingClientRect();
        return r.width > 0 && (r.right > w + 2 || r.left < -2);
      }).slice(0, 8).map(el => ({tag:el.tagName.toLowerCase(), cls:String(el.className).slice(0,100), right:Math.round(el.getBoundingClientRect().right)}));
      return { viewport: w, scroll: document.documentElement.scrollWidth,
               excess: document.documentElement.scrollWidth - w, candidates:items};
    }""")


def visible(page, selector):
    loc = page.locator(selector)
    return loc.count() >= 1 and loc.first.is_visible()


def scenario(browser, width, height):
    page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
    try:
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)[:200]))
        response = load(page, "?hero=reverse&motion=still")
        check(f"{width}: home HTTP", response.status == 200, response.status)
        check(f"{width}: single H1", page.locator("h1").count() == 1)
        check(f"{width}: hero H1 readable", visible(page, "#opening-title"))
        check(f"{width}: services CTA readable", visible(page, 'a.hero-primary[href="/services/"]'))
        check(f"{width}: four scenes", [page.locator(f"#{x}[data-chapter]").count() for x in ("origin","research","field","invitation")] == [1,1,1,1])
        check(f"{width}: navigation destinations", page.locator('a[href="/research/lab/"]').count()>0 and page.locator('a[href="/research/notes/"]').count()>0 and page.locator('a[href="/signal-studio/"]').count()>0)
        o = overflow(page)
        check(f"{width}: horizontal overflow", o["excess"] <= 2, o)
        check(f"{width}: JS runtime errors", not errors, errors)
        page.screenshot(path=str(OUT / f"home-{width}-reverse-still.png"), full_page=False)
        if width in (390, 1440):
            page.screenshot(path=str(OUT / f"home-{width}-full.png"), full_page=True,
                            animations="disabled", timeout=30000)
        if width <= 820:
            btn = page.locator(".menu-btn")
            check(f"{width}: menu available", btn.count()==1 and btn.is_visible())
            if btn.count() and btn.is_visible():
                btn.click()
                check(f"{width}: menu expanded", btn.get_attribute("aria-expanded")=="true")
                page.keyboard.press("Escape")
                check(f"{width}: Escape closes menu", btn.get_attribute("aria-expanded")=="false")
        else:
            check(f"{width}: desktop navigation visible", visible(page, "#main-nav"))
        if width == 1440:
            a = page.locator('[data-hero-mode-choice="default"]')
            b = page.locator('[data-hero-mode-choice="reverse"]')
            check("1440: hero A/B controls enabled", a.is_visible() and b.is_visible())
            if a.is_visible() and b.is_visible():
                a.click()
                check("1440: hero A selected", a.get_attribute("aria-pressed")=="true")
                b.click()
                check("1440: hero B selected", b.get_attribute("aria-pressed")=="true")
    except Exception as exc:
        check(f"{width}: browser scenario completed", False, str(exc))
        try:
            page.screenshot(path=str(OUT / f"home-{width}-error.png"), full_page=False)
        except Exception:
            pass
    finally:
        page.close()


def detail_routes(browser):
    routes = {
        "research/lab/": ("관찰", "/#invitation"),
        "research/notes/": ("2026.05.11", "/#invitation"),
        "signal-studio/": ("Gate 0", "/#invitation"),
        "services/": ("함께", "/#invitation"),
        "research/": ("익숙한 장면", "/research/lab/"),
        "about/": ("함께", "/#invitation"),
        "work/weplace/": ("Weplace", "/#invitation"),
        "policies/refund/": ("환불", "/services/"),
    }
    page = browser.new_page(viewport={"width": 390, "height": 844})
    try:
        for route, (term, expected_link) in routes.items():
            try:
                response = load(page, route)
                body = page.locator("body").inner_text()
                check(f"{route}: HTTP 200 + H1", response.status==200 and page.locator("h1").count()==1, response.status)
                check(f"{route}: contents", term in body)
                if route != "policies/refund/":
                    check(f"{route}: next step", page.locator(f'a[href="{expected_link}"]').count()>0)
                canonical = page.locator('link[rel="canonical"]').first.get_attribute("href")
                expected = "https://mashcore.co.kr/" + route
                check(f"{route}: canonical", canonical==expected, canonical)
                robots = page.locator('meta[name="robots"]').first.get_attribute("content") or ""
                header = response.headers.get("x-robots-tag", "")
                check(f"{route}: preview noindex", "noindex" in robots.lower() and "noindex" in header.lower(),
                      {"meta":robots,"header":header})
                check(f"{route}: horizontal overflow 390", overflow(page)["excess"]<=2, overflow(page))
                if route in ("research/lab/","research/notes/","signal-studio/"):
                    page.screenshot(path=str(OUT / f"detail-{route.strip('/').replace('/','-')}.png"), full_page=True, animations="disabled", timeout=30000)
            except Exception as exc:
                check(f"{route}: route scenario completed", False, str(exc))
        load(page,"research/notes/")
        check("Notes: original market URL", page.locator('a[href="https://mashcore-market-notes.netlify.app/"]').count()==1)
        load(page,"signal-studio/")
        text = page.locator("body").inner_text()
        check("Studio: limitations shown", "Mock" in text and "미검증" in text)
        check("Studio: no payment CTA", page.locator('a[href*="checkout"],a[href*="payment"]').count()==0)
        r = load(page,"robots.txt")
        check("Draft robots: crawler can read noindex", r.status==200 and "Disallow: /" not in r.text() and "Allow: /" in r.text())
        r = load(page,"sitemap.xml")
        check("Draft sitemap: no unapproved URLs", r.status==200 and "<url>" not in r.text())
    finally:
        page.close()


def failure_modes(browser):
    # JS disabled still exposes complete static H1, role, CTA and inquiry link.
    context = browser.new_context(viewport={"width":390,"height":844}, java_script_enabled=False)
    page = context.new_page()
    try:
        response = load(page, "?hero=reverse")
        check("JS disabled: home visible", response.status==200 and visible(page,"#opening-title") and visible(page,'a.hero-primary[href="/services/"]'))
        check("JS disabled: inquiry anchor", page.locator('a[href="/#invitation"]').count() > 0)
        page.screenshot(path=str(OUT/"failure-js-disabled.png"), full_page=False)
    finally:
        context.close()

    context = browser.new_context(viewport={"width":390,"height":844}, reduced_motion="reduce")
    page = context.new_page()
    try:
        load(page,"?hero=reverse")
        check("reduced motion: H1 and CTA", visible(page,"#opening-title") and visible(page,'a.hero-primary[href="/services/"]'))
        page.screenshot(path=str(OUT/"failure-reduced-motion.png"),full_page=False,animations="disabled")
    finally:
        context.close()

    context = browser.new_context(viewport={"width":390,"height":844})
    page = context.new_page()
    page.route("**/assets/media/*", lambda route: route.abort())
    try:
        load(page,"?hero=reverse")
        check("media blocked: text and CTA", visible(page,"#opening-title") and visible(page,'a.hero-primary[href="/services/"]'))
        page.screenshot(path=str(OUT/"failure-media-blocked.png"),full_page=False)
    finally:
        context.close()

    context = browser.new_context(viewport={"width":390,"height":844}, is_mobile=True, has_touch=True)
    page = context.new_page()
    try:
        load(page,"?hero=reverse&motion=still")
        check("touch mobile: CTA visible", visible(page,'a.hero-primary[href="/services/"]'))
        page.locator(".menu-btn").tap()
        check("touch mobile: menu opens", page.locator(".menu-btn").get_attribute("aria-expanded")=="true")
    finally:
        context.close()

    context = browser.new_context(viewport={"width":800,"height":900})
    page=context.new_page()
    try:
        load(page,"?hero=reverse&motion=still")
        page.evaluate("document.documentElement.style.zoom = '200%'")
        page.wait_for_timeout(100)
        o=overflow(page)
        check("CSS zoom 200%: no horizontal overflow",o["excess"]<=2,o)
        page.screenshot(path=str(OUT/"simulation-css-zoom-200-percent.png"),full_page=False)
    finally:
        context.close()


def main():
    meta = {"base":BASE,"sha":os.environ.get("QA_COMMIT",""),"check_type":"Remote Chromium automated browser QA", "not_claimed":["real physical devices","real OS preference switch","full-browser true 200% zoom","email delivery","user comprehension test","production CWV"]}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            for w,h in ((320,700),(390,844),(768,1024),(1440,900)):
                scenario(browser,w,h)
            detail_routes(browser)
            failure_modes(browser)
            browser.close()
    except Exception as exc:
        check("browser runner",False,str(exc))
    meta.update({"checks":len(results),"passed":len(results)-len(failures),"failed":len(failures),
                 "result":"PASS" if not failures else "FAIL","details":results})
    (OUT/"result.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:meta[k] for k in ("sha","checks","passed","failed","result")},ensure_ascii=False),flush=True)
    return 0 if not failures else 1


if __name__=="__main__":
    raise SystemExit(main())
