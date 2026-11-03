import { chromium, webkit } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const url = process.env.R35_URL || 'http://127.0.0.1:8350/sense-r35/';
const output = fileURLToPath(new URL('../../evidence/r35/',import.meta.url));
await mkdir(output,{recursive:true});
const results = [], errors = [];
function check(name,condition,detail='') {
  results.push({name,pass:!!condition,...(detail?{detail}:{})});
  console.log(`${condition?'PASS':'FAIL'} ${name}${condition?'':': '+JSON.stringify(detail)}`);
}
const engine = process.env.R35_BROWSER === 'webkit' ? webkit : chromium;
const browser = await engine.launch({headless:true,...(process.env.CI || engine === webkit ? {} : {channel:'chrome'})});
const prefix = engine === webkit ? 'webkit-' : '';
const dimensions = engine === webkit ? [[390,844]] : [[320,780],[390,844],[768,1024],[1440,1000]];
for (const [width,height] of dimensions) {
  const context = await browser.newContext({viewport:{width,height},deviceScaleFactor:1});
  const page = await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  const requests = [];
  page.on('request',request=>requests.push(request.url()));
  await page.goto(url,{waitUntil:'networkidle'});
  await page.evaluate(()=>document.fonts.ready);
  await page.locator('.second-figure').scrollIntoViewIfNeeded();
  await page.locator('img').evaluateAll(images=>Promise.all(images.map(image=>image.decode())));
  await page.evaluate(()=>scrollTo(0,0));
  const metrics=await page.evaluate(()=>({
    width:innerWidth, doc:document.documentElement.scrollWidth,
    h1:document.querySelectorAll('h1').length,
    main:document.querySelectorAll('main').length,
    missingImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),
    videoSrc:document.querySelector('video').getAttribute('src'),
    font:document.fonts.check('40px "Gowun Batang"'),
    ctaBottom:document.querySelector('.origin .primary').getBoundingClientRect().bottom,
    badRefs:[...document.querySelectorAll('[aria-labelledby],[aria-describedby],[aria-controls]')].flatMap(e=>['aria-labelledby','aria-describedby','aria-controls'].flatMap(a=>(e.getAttribute(a)||'').split(' ').filter(id=>id&&!document.getElementById(id))))
  }));
  check(`${prefix}${width}: no horizontal overflow`,metrics.doc<=width,metrics);
  check(`${prefix}${width}: first-screen service CTA`,metrics.ctaBottom<height,metrics.ctaBottom);
  check(`${prefix}${width}: one H1 / main, valid ARIA refs`,metrics.h1===1&&metrics.main===1&&!metrics.badRefs.length,metrics);
  check(`${prefix}${width}: poster and local font loaded`,!metrics.missingImages.length&&metrics.font,metrics);
  check(`${prefix}${width}: video deferred; no external requests`,metrics.videoSrc===null && requests.every(x=>new URL(x).origin===new URL(url).origin),requests);
  const axe = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
  check(`${prefix}${width}: axe WCAG A/AA`,axe.violations.length===0,axe.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})));
  await page.screenshot({path:`${output}/${prefix}desktop-${width}.png`,fullPage:true});
  await page.screenshot({path:`${output}/${prefix}fold-${width}.png`});
  for (const choice of ['sign','wait','pause']) {
    await page.locator(`input[name=hypothesis][value=${choice}]`).check();
    check(`${prefix}${width}: hypothesis ${choice}`,await page.locator(`#hypothesis-${choice}`).isVisible() && await page.locator('.hypothesis-reading:visible').count()===1);
  }
  for (const value of ['ordered','scattered']) {
    await page.locator(`input[name=layout][value=${value}]`).check();
    const box = await page.locator('.gaze-one').evaluate(el=>getComputedStyle(el).paddingLeft);
    check(`${prefix}${width}: layout ${value}`,value==='ordered'?box==='0px':parseFloat(box)>0,box);
  }
  await page.locator('#trace-toggle').click();
  await page.waitForTimeout(1750);
  check(`${prefix}${width}: GSAP sequence reaches static result`,await page.locator('.tracing .order-number:visible').count()===3 && await page.locator('.gaze-item').evaluateAll(els=>els.every(e=>Number(getComputedStyle(e).opacity)===1)));
  await page.locator('#trace-toggle').click();
  check(`${prefix}${width}: trace can close`,await page.locator('.tracing').count()===0);
  await page.locator('#next-steps summary').click();
  check(`${prefix}${width}: predictability opens`,await page.locator('.next-list').isVisible());
  await page.locator('#next-steps summary').click();
  check(`${prefix}${width}: predictability closes`,!await page.locator('.next-list').isVisible());
  await page.locator('input[name=detail][value=full]').check();
  await page.evaluate(()=>document.activeElement.blur());
  check(`${prefix}${width}: full control`,await page.locator('.full-copy').isVisible());
  await page.locator('button[type=reset]').click();
  check(`${prefix}${width}: reset control`,!await page.locator('.full-copy').isVisible() && await page.locator('input[name=detail][value=short]').isChecked());
  // Preserve representative changed states separately from top-of-page captures.
  await page.locator('input[name=layout][value=ordered]').check();
  await page.locator('#trace-toggle').focus();
  await page.keyboard.press('Enter');
  await page.locator('#next-steps summary').click();
  await page.locator('input[name=detail][value=full]').check();
  await page.locator('#second-look').screenshot({path:`${output}/${prefix}second-look-${width}.png`});
  await page.locator('#sense-os').screenshot({path:`${output}/${prefix}sense-os-${width}.png`});
  const stateAxe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
  check(`${prefix}${width}: expanded-state axe`,stateAxe.violations.length===0,stateAxe.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})));
  const broken = await page.evaluate(async()=>{
    const links=[...new Set([...document.querySelectorAll('a[href]')].map(a=>a.href))].filter(x=>new URL(x).origin===location.origin);
    const bad=[];
    for(const link of links){const target=new URL(link);const response=await fetch(target);if(!response.ok){bad.push(link);continue;}if(target.hash){const doc=new DOMParser().parseFromString(await response.text(),'text/html');if(!doc.getElementById(decodeURIComponent(target.hash.slice(1))))bad.push(link);}}
    return bad;
  });
  check(`${prefix}${width}: internal routes and fragments`,broken.length===0,broken);
  await writeFile(`${output}/${prefix}accessibility-${width}.txt`,await page.locator('body').ariaSnapshot());
  await context.close();

  const nojs=await browser.newContext({viewport:{width,height},javaScriptEnabled:false});
  const staticPage=await nojs.newPage();
  await staticPage.goto(url,{waitUntil:'networkidle'});
  check(`${prefix}${width}: JS-off all hypotheses readable`,await staticPage.locator('.hypothesis-reading:visible').count()===3);
  await staticPage.locator('input[name=layout][value=ordered]').check();
  check(`${prefix}${width}: JS-off native layout`,await staticPage.locator('.gaze-one').evaluate(el=>getComputedStyle(el).paddingLeft)==='0px');
  await staticPage.locator('#next-steps summary').click();
  check(`${prefix}${width}: JS-off native details`,await staticPage.locator('.next-list').isVisible());
  await staticPage.locator('input[name=detail][value=full]').check();
  check(`${prefix}${width}: JS-off full explanation`,await staticPage.locator('.full-copy').isVisible());
  check(`${prefix}${width}: JS-off no overflow`,await staticPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  check(`${prefix}${width}: JS-off no dead motion buttons`,!await staticPage.locator('#video-toggle').isVisible()&&!await staticPage.locator('#trace-toggle').isVisible());
  await staticPage.evaluate(()=>scrollTo(0,0));
  await staticPage.screenshot({path:`${output}/${prefix}nojs-${width}.png`,fullPage:true});
  await nojs.close();
}

const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
const page=await context.newPage();
await page.goto(url,{waitUntil:'networkidle'});
check(`${prefix}reduced motion: poster only`,!await page.locator('#video-toggle').isVisible()&&await page.locator('video').getAttribute('src')===null);
await page.locator('#trace-toggle').click();
check(`${prefix}reduced motion: static numbered example`,await page.locator('.order-number:visible').count()===3&&await page.evaluate(()=>window.gsap.globalTimeline.getChildren().length===0));
await page.emulateMedia({reducedMotion:'no-preference'});
await page.waitForFunction(()=>!document.querySelector('#video-toggle').hidden);
check(`${prefix}motion preference can change live`,await page.locator('#video-toggle').isVisible()&&!await page.locator('.tracing').count());
await page.goto(url);
await page.keyboard.press('Tab');
check(`${prefix}keyboard: skip is first`,await page.locator('.skip').evaluate(el=>el===document.activeElement));
await page.keyboard.press('Enter');
check(`${prefix}keyboard: skip reaches main`,await page.locator('#main').evaluate(el=>el===document.activeElement));
await page.locator('input[name=hypothesis][value=sign]').focus();
await page.keyboard.press('ArrowDown');
check(`${prefix}keyboard: radio arrow selection`,await page.locator('input[name=hypothesis][value=wait]').isChecked());
await page.locator('#next-steps summary').focus();
await page.keyboard.press('Enter');
check(`${prefix}keyboard: details Enter`,await page.locator('.next-list').isVisible());
await page.locator('#trace-toggle').focus();
await page.keyboard.press('Enter');
check(`${prefix}keyboard: trace immediate; no animation`,await page.locator('.order-number:visible').count()===3&&await page.evaluate(()=>window.gsap.globalTimeline.getChildren().length===0));
await page.screenshot({path:`${output}/${prefix}keyboard-focus.png`});
await page.emulateMedia({reducedMotion:'reduce'});
await page.evaluate(()=>{document.documentElement.style.zoom='2';scrollTo(0,0);});
check(`${prefix}200% CSS zoom: no horizontal overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
// Chromium fullPage tiling can duplicate content when CSS zoom is active.
// A single tall viewport paints the enlarged document once, without stitching.
const zoomHeight=Math.ceil(await page.evaluate(()=>document.body.getBoundingClientRect().height));
await page.setViewportSize({width:390,height:zoomHeight});
await page.screenshot({path:`${output}/${prefix}zoom-200.png`,fullPage:false});
await context.close();

const fallback=await browser.newContext({viewport:{width:390,height:844}});
const fallbackPage=await fallback.newPage();
await fallbackPage.route('**/gsap.min.js',route=>route.abort());
await fallbackPage.goto(url,{waitUntil:'networkidle'});
await fallbackPage.locator('#trace-toggle').click();
check(`${prefix}GSAP failure: static example still works`,await fallbackPage.locator('.order-number:visible').count()===3);
await fallbackPage.route('**/origin.mp4',route=>route.abort());
await fallbackPage.locator('#video-toggle').click();
await fallbackPage.waitForTimeout(750);
check(`${prefix}video error: poster and recovery`,await fallbackPage.locator('#video-status').innerText()!==''&&!await fallbackPage.locator('.origin-media.is-playing').count());
await fallback.close();

check(`${prefix}no uncaught application errors`,errors.length===0,errors);
await browser.close();
const report={url,engine:engine===webkit?'webkit':'chromium',timestamp:new Date().toISOString(),passed:results.filter(x=>x.pass).length,failed:results.filter(x=>!x.pass).length,results,limits:['No physical mobile device testing','Accessibility tree + axe + keyboard; no human screen-reader testing','CSS zoom is not native browser zoom','No measured customer comprehension or conversion effects']};
await writeFile(`${output}/${prefix}qa-results.json`,JSON.stringify(report,null,2));
console.log(JSON.stringify({passed:report.passed,failed:report.failed,output}));
process.exitCode=report.failed?1:0;
