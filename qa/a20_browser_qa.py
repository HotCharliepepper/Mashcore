#!/usr/bin/env python3
"""Desktop/mobile smoke QA of built static A20 routes with Playwright Chromium."""
from pathlib import Path
import argparse, contextlib, http.server, json, socketserver, threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def test():
    if not OUT.exists():raise RuntimeError('Run prepare_public.py first')
    pages=sorted('/'+f.relative_to(OUT).as_posix().replace('index.html','') for f in OUT.rglob('index.html'))
    assert len(pages)==19
    failures=[];checks=[]
    import os
    cwd=os.getcwd();os.chdir(OUT)
    try:
        with socketserver.TCPServer(('127.0.0.1',0),QuietHandler) as server:
            port=server.server_address[1]
            threading.Thread(target=server.serve_forever,daemon=True).start()
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True,args=['--no-sandbox'],executable_path=os.environ.get('CHROMIUM_PATH') or None)
                for label,viewport in (('desktop',{'width':1440,'height':900}),('mobile',{'width':390,'height':844})):
                    context=browser.new_context(viewport=viewport,reduced_motion='reduce',device_scale_factor=1)
                    for route in pages:
                        page=context.new_page();errors=[]
                        page.on('pageerror',lambda ex,errs=errors:errs.append(str(ex)))
                        page.on('response',lambda response,errs=errors:errs.append(f'{response.status}: {response.url}') if response.status>=400 and response.url.startswith(f'http://127.0.0.1:{port}/') else None)
                        try:
                            resp=page.goto(f'http://127.0.0.1:{port}{route}',wait_until='domcontentloaded',timeout=20000)
                            page.wait_for_timeout(450)
                            assert resp.status==200, f'HTTP {resp.status}'
                            assert page.locator('h1').count()==1,'H1 mismatch'
                            assert page.locator('body').count()==1
                            dims=page.evaluate('({width:document.documentElement.scrollWidth,viewport:window.innerWidth})')
                            assert dims['width']<=dims['viewport']+5,f'horizontal overflow: {dims}'
                            html=page.content()
                            assert '247-02-04104' in html and '최규현' in html,'legal info missing'
                            assert not errors,'; '.join(errors[:5])
                            checks.append(f'{label} {route}')
                        except Exception as exc: failures.append(f'{label} {route}: {exc}')
                        finally:page.close()
                    context.close()
                browser.close()
            server.shutdown()
    finally:os.chdir(cwd)
    if failures:
        print(json.dumps({'result':'FAIL','passed':len(checks),'failed':len(failures),'examples':failures[:30]},ensure_ascii=False,indent=2))
        raise SystemExit(1)
    print(json.dumps({'result':'PASS','routes':len(pages),'viewport_tests':len(checks),'viewports':['1440x900','390x844']},ensure_ascii=False))
if __name__=='__main__':test()
