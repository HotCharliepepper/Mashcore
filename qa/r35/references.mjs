import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
const out=fileURLToPath(new URL('../../evidence/r35/',import.meta.url));
const browser=await chromium.launch({headless:true,channel:'chrome'});
const page=await browser.newPage();
for(const [label,url] of [['main-r31','http://127.0.0.1:8350/'],['pr18-r34','http://127.0.0.1:8351/']]){
  for(const width of [1440,390]){
    await page.setViewportSize({width,height:width===390?844:1000});
    await page.goto(url,{waitUntil:'domcontentloaded'});
    await page.waitForTimeout(3000);
    await page.evaluate(()=>document.fonts.ready);
    await page.evaluate(()=>document.querySelectorAll('video').forEach(video=>video.pause()));
    await page.screenshot({path:`${out}/before-${label}-${width}.png`});
  }
}
await browser.close();
