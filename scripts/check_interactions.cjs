const {parseHTML}=require('linkedom');
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=require('node:path').resolve(__dirname,'..')+'/';
const checks=[];
function setup(route,search=''){
 const {document,Event}=parseHTML(fs.readFileSync(root+route,'utf8'));
 const listener={};const media={matches:false,addEventListener(){}};
 const win={matchMedia:()=>media,addEventListener(n,f){listener[n]=f},isSecureContext:true,innerHeight:800,scrollY:0,location:{href:'https://mashcore.netlify.app/'+search,hash:'',replace(v){win.replaced=v}},history:{replaceState(a,b,u){win.location.href=String(u)}}};
 let copied='';const navigator={clipboard:{writeText:async value=>{copied=value}}};
 Object.defineProperty(document.documentElement,'scrollHeight',{value:2400});
 for(const input of document.querySelectorAll('input[type="radio"]'))Object.defineProperty(input,'checked',{get(){return this.hasAttribute('checked')},set(v){if(v)this.setAttribute('checked','');else this.removeAttribute('checked')}});
 const context={document,window:win,navigator,requestAnimationFrame:()=>1,URL,console};
 const run=name=>vm.runInNewContext(fs.readFileSync(root+'assets/js/'+name,'utf8'),context);
 const click=el=>el.dispatchEvent(new Event('click',{bubbles:true}));
 const key=(el,k)=>{const e=new Event('keydown',{bubbles:true,cancelable:true});e.key=k;el.dispatchEvent(e)};
 return {document,Event,win,navigator,run,click,key,get copied(){return copied}};
}
async function main(){
 for(const route of ['index.html','mobile/index.html','explore/index.html','about/index.html','research/index.html','research/chore-to-play/index.html','research/market-interpretation/index.html','research/log/index.html']){
  const env=setup(route),{document,run,click,key,Event,win}=env;
  run('site-config.js');run('site.js');
  assert.equal(document.querySelector('[data-business-info]').hidden,true);
  click(document.querySelector('.menu-btn'));assert.equal(document.querySelector('.menu-btn').getAttribute('aria-expanded'),'true');key(document.querySelector('.menu-btn'),'Escape');assert.equal(document.querySelector('.menu-btn').getAttribute('aria-expanded'),'false');
  if(document.getElementById('question')){
   const q=document.getElementById('question');q.select=()=>{};q.value='왜 망설일까요? & 작은 질문';q.dispatchEvent(new Event('input'));
   assert.equal(new URL(document.getElementById('email-question').getAttribute('href')).searchParams.get('body'),q.value);
   click(document.getElementById('copy-question'));await Promise.resolve();assert.equal(env.copied,q.value);
   win.isSecureContext=false;click(document.getElementById('copy-question'));await Promise.resolve();assert.match(document.getElementById('copy-status').textContent,/문장을 선택/);
   q.value='';click(document.getElementById('copy-question'));assert.match(document.getElementById('copy-status').textContent,/한 줄/);
  }
  if(route.startsWith('explore')){
   const tab=document.getElementById('lens-brand');click(tab);assert.equal(document.getElementById('lens-panel-brand').hidden,false);assert.equal(document.getElementById('lens-panel-person').hidden,true);
   key(tab,'End');key(document.getElementById('lens-place'),'ArrowRight');assert.equal(document.getElementById('lens-person').getAttribute('aria-selected'),'true');key(document.getElementById('room-person'),'ArrowDown');assert.equal(document.getElementById('room-brand').getAttribute('aria-selected'),'true');
  }
  if(route.includes('chore-to-play')){
   const titles=new Set();for(const agency of ['low','high'])for(const feedback of ['low','high']){
    for(const input of document.querySelectorAll('input'))input.checked=input.value===(input.name==='agency'?agency:feedback);
    document.querySelector('input').dispatchEvent(new Event('change'));titles.add(document.getElementById('condition-title').textContent);
   }assert.equal(titles.size,4);click(document.getElementById('reset-conditions'));assert.equal(document.querySelector('[name="agency"]:checked').value,'low');assert.equal(document.querySelector('[name="feedback"]:checked').value,'low');
  }
  checks.push(route+': navigation, blank business fields, retained page interactions pass');
 }
 const biz=setup('index.html');biz.win.MASHCORE_BUSINESS={companyName:'Example <script>alert(1)</script>',registrationNumber:'',address:''};biz.run('site.js');assert.equal(biz.document.querySelector('[data-business-info]').hidden,false);assert.equal(biz.document.querySelector('[data-business-info]').children.length,1);assert.equal(biz.document.querySelector('[data-business-info] script'),null);checks.push('Business update: only nonempty fields render; values are text, not executable HTML');
 const scene=setup('index.html');scene.run('chapters.js');assert.equal(scene.document.querySelectorAll('[data-chapter]').length,4);scene.win.location.hash='#rooms';scene.run('chapters.js');assert.equal(scene.win.replaced,'/explore/#rooms');checks.push('Chapters: readable without IntersectionObserver; old deep links reach preserved content');
 const preview=setup('preview/index.html','preview/?view=mobile');Object.defineProperty(preview.document.querySelector('.preview-space'),'clientWidth',{value:320});preview.run('preview.js');assert.equal(preview.document.getElementById('site-preview').src,'/mobile/?preview=mobile');assert.equal(preview.document.querySelector('.preview-frame').style.width,'320px');assert.equal(preview.document.getElementById('open-view').href,'/mobile/');preview.click(preview.document.querySelector('[data-view="desktop"]'));assert.equal(preview.document.getElementById('site-preview').src,'/?preview=desktop');assert.equal(preview.document.querySelector('[data-view="desktop"]').getAttribute('aria-pressed'),'true');assert.match(preview.win.location.href,/view=desktop/);checks.push('Viewer: shareable mobile/desktop modes, fitting frame geometry, matching open-page link');
 console.log(JSON.stringify({status:'passed',environment:'Node DOM simulation; not rendered browser or physical device',checks},null,2));
}
main().catch(e=>{console.error(e);process.exit(1)});
