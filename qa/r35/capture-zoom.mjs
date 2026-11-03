import { chromium } from 'playwright';
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const out=fileURLToPath(new URL('../../evidence/r35/',import.meta.url));
const browser=await chromium.launch({headless:true,channel:'chrome'});
const page=await browser.newPage({viewport:{width:390,height:2000},reducedMotion:'reduce'});
await page.goto('http://127.0.0.1:8350/sense-r35/',{waitUntil:'networkidle'});
await page.locator('.second-figure').scrollIntoViewIfNeeded();
await page.locator('img').evaluateAll(images=>Promise.all(images.map(image=>image.decode())));
await page.locator('input[name=hypothesis][value=wait]').check();
await page.locator('#next-steps summary').click();
await page.locator('#trace-toggle').click();
await page.evaluate(()=>{document.activeElement.blur();document.documentElement.style.zoom='2';scrollTo(0,0);});
const height=Math.ceil(await page.evaluate(()=>document.body.getBoundingClientRect().height));
const tiles=[];
for(let top=0,index=1;top<height;top+=2000,index++){
  await page.evaluate(top=>scrollTo(0,top),top);
  await page.waitForTimeout(100);
  const name=index===1?'zoom-200.png':`zoom-200-${String(index).padStart(2,'0')}.png`;
  await page.screenshot({path:`${out}/${name}`,fullPage:false});
  tiles.push({name,scrollY:await page.evaluate(()=>scrollY)});
}
const metrics=await page.evaluate(()=>({width:innerWidth,height:innerHeight,documentWidth:document.documentElement.scrollWidth,body:document.body.getBoundingClientRect().height,footerBottom:document.querySelector('footer').getBoundingClientRect().bottom,headers:document.querySelectorAll('header').length}));
metrics.tiles=tiles;
await writeFile(`${out}/zoom-capture.json`,JSON.stringify(metrics,null,2));
console.log(JSON.stringify(metrics));
await browser.close();
