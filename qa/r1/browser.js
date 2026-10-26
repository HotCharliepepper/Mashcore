/* Local test code; excluded from dist. Results distinguish injections and browser rendering. */
const frame=document.querySelector('#qa-frame'),result=document.querySelector('#results'),statusNode=document.querySelector('#status');
const results=[];
const paths=['/','/mobile/','/services/','/about/','/research/','/research/chore-to-play/','/research/market-interpretation/','/research/log/','/explore/','/work/weplace/','/policies/refund/'];
const tick=()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
const until=async(fn,timeout=6000)=>{const start=performance.now();while(!fn()){if(performance.now()-start>timeout)throw Error('condition timed out');await new Promise(r=>setTimeout(r,40));}};
function record(name,fn){try{const evidence=fn();results.push({name,status:'PASS',evidence});}catch(e){results.push({name,status:'FAIL',error:e.message});}result.textContent=JSON.stringify(results,null,2);}
function assert(value,message){if(!value)throw Error(message);}
async function load(path='/',width=390,options={}){
 frame.width=width;frame.height=width>700?960:844;frame.style.width=width+'px';frame.removeAttribute('srcdoc');
 if(options.nojs)frame.setAttribute('sandbox','allow-same-origin');else frame.removeAttribute('sandbox');
 let source=await (await fetch(path)).text();
 source=source.replace('<head>','<head><base href="'+new URL(path,location.href).href+'">');
 let inject='';
 if(options.reduced)inject+=`const originalMatch=window.matchMedia.bind(window);window.matchMedia=q=>q.includes('prefers-reduced-motion')?{matches:true,media:q,addEventListener(){},removeEventListener(){}}:originalMatch(q);`;
 if(options.blocked)inject+=`let denied=false;const originalPlay=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){if(!denied){denied=true;return Promise.reject(new DOMException('QA autoplay rejection','NotAllowedError'));}return originalPlay.call(this)};`;
 if(options.rejectCopy)inject+=`Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(Error('QA clipboard denial'))}});`;
 if(options.visibility)inject+=`let qaHidden=false;Object.defineProperty(document,'hidden',{get:()=>qaHidden});window.qaSetHidden=value=>{qaHidden=value;document.dispatchEvent(new Event('visibilitychange'))};`;
 if(inject)source=source.replace('<head>','<head><script>'+inject+'</scr'+'ipt>');
 if(options.reduced)source=source.replace('</head>','<style>*,*:before,*:after{animation:none!important;transition:none!important}html{scroll-behavior:auto!important}</style></head>');
 if(options.media){
   source=source.replace(/(<script type="application\/json" data-hero-config>)(.*?)(<\/script>)/s,(_,a,s,b)=>{const c=JSON.parse(s);c.video.desktop=options.error?'/qa/missing.webm':'/qa/fixture.webm';c.video.mobile=null;return a+JSON.stringify(c)+b;});
   source=source.replace('</picture>','</picture><video data-hero-video muted playsinline preload="none" aria-label="TEST FIXTURE color bars" hidden></video>');
 }
 const loaded=new Promise(r=>frame.onload=r);frame.srcdoc=source;await loaded;
 await frame.contentDocument.fonts.ready;frame.scrollIntoView({block:'start',behavior:'instant'});await tick();
 return {d:frame.contentDocument,w:frame.contentWindow,q:s=>frame.contentDocument.querySelector(s)};
}
async function matrix(){
 results.length=0;statusNode.textContent='Running layout matrix';
 for(const width of [320,390,768,1440])for(const path of paths){
   statusNode.textContent='Layout '+width+' '+path+' ('+results.length+'/58)';
   const e=await load(path,width);
   record('layout '+width+' '+path,()=>{const d=e.d;assert(d.documentElement.scrollWidth<=d.documentElement.clientWidth+1,'horizontal overflow '+d.documentElement.scrollWidth+' > '+d.documentElement.clientWidth);assert(d.querySelector('h1'),'missing H1');return {viewport:width,client:d.documentElement.clientWidth,scroll:d.documentElement.scrollWidth};});
 }
 for(const path of paths){statusNode.textContent='Text 200% '+path+' ('+results.length+'/58)';const e=await load(path,390);const sizes=[...e.d.querySelectorAll('body *')].map(el=>[el,parseFloat(e.w.getComputedStyle(el).fontSize)]);sizes.forEach(([el,size])=>{if(Number.isFinite(size))el.style.fontSize=size*2+'px'});await tick();record('text 200% '+path,()=>{assert(e.d.documentElement.scrollWidth<=e.d.documentElement.clientWidth+1,'horizontal overflow');return 'CSS text enlargement, not browser zoom';});}
 for(const path of ['/','/services/','/research/chore-to-play/']){const e=await load(path,390,{nojs:true});record('no JS '+path,()=>{assert(e.q('h1'),'H1 missing');assert(e.q('footer').textContent.includes('247-02-04104'),'business missing');if(path==='/'){assert(e.q('[data-hero-poster]').complete,'poster missing');assert(!e.q('[data-hero-video]'),'empty video');assert([...e.d.querySelectorAll('[data-layout-fallback]')].every(el=>!el.hidden),'static alternatives hidden');}return 'sandbox blocks actual script execution';});}
 statusNode.textContent='Layout matrix complete: '+results.filter(r=>r.status==='PASS').length+'/'+results.length;
}
async function functional(){
 results.length=0;statusNode.textContent='Running interaction/media tests';
 let e=await load('/',390,{rejectCopy:true});
 record('poster_only',()=>{assert(e.q('[data-hero-media]').dataset.mediaState==='poster_only','wrong state');assert(!e.q('video'),'null source video created');assert(e.q('[data-hero-controls]').hidden,'dead controls visible');return 'No video or media request; eager picture and H1 in HTML';});
 record('A/B same nodes all 3 perspectives',()=>{for(const p of e.d.querySelectorAll('[data-layout-study]')){const b=[...p.querySelector('[data-layout-surface]').children];p.querySelector('[data-layout-choice=b]').click();assert(p.querySelector('[data-layout-choice=b]').getAttribute('aria-pressed')==='true','B not selected');assert(b.every(el=>p.querySelector('[data-layout-surface]').contains(el)),'nodes replaced');p.querySelector('[data-layout-choice=a]').click();}return '3 perspectives, reversible order, exact original nodes';});
 e.q('#question').value='가'.repeat(1001);e.q('#question').dispatchEvent(new e.w.Event('input'));
 record('1001 Korean input',()=>{assert(e.q('#question').value.length===1001,'truncated');assert(e.q('#email-question').getAttribute('aria-disabled')==='true','mail not blocked');assert(e.q('#question-error').textContent.includes('남아'),'no retention guidance');});
 e.q('#question').value='한글 & # %\n두 번째 질문';e.q('#question').dispatchEvent(new e.w.Event('input'));e.q('#copy-question').click();await tick();
 record('clipboard denial',()=>{assert(!e.q('#copy-status').textContent.includes('복사했습니다'),'false success');assert(e.q('#copy-status').textContent.includes('직접'),'no fallback');return e.q('#copy-status').textContent;});
 record('mailto exact encoding',()=>{const u=new URL(e.q('#email-question').href);assert(u.pathname==='weplacehyun@naver.com','wrong recipient');assert(u.searchParams.get('body')===e.q('#question').value,'body differs');});
 e.q('#question').dispatchEvent(new e.w.CompositionEvent('compositionstart'));e.q('#copy-question').click();
 record('composition guard',()=>assert(e.q('#copy-status').textContent.includes('한글 입력'),'composition not blocked'));
 e.q('#question').dispatchEvent(new e.w.CompositionEvent('compositionend'));e.q('#question').value='';e.q('#question').dispatchEvent(new e.w.Event('input'));e.q('#copy-question').click();
 record('empty copy',()=>assert(e.q('#copy-status').textContent.includes('먼저'),'empty success'));
 e=await load('/research/chore-to-play/',390,{reduced:true});
 record('reduced-motion 3D JS preference injection',()=>{e.q('[data-spatial-select=meaning]').click();assert(e.q('[data-spatial]').dataset.spatialSelected==='meaning','selection lost');assert(e.q('[data-spatial-turn="1"]').disabled,'motion control enabled');return 'matchMedia injected; real system preference NOT RUN';});
 e=await load('/',390,{media:true,reduced:true});await tick();
 record('reduced-motion media',()=>{assert(e.q('[data-hero-media]').dataset.mediaState==='reduced_motion','state');assert(!e.q('video').getAttribute('src'),'unrequested media fetched');return 'matchMedia injected; no autoplay';});
 e.q('[data-hero-toggle]').click();await until(()=>e.q('[data-hero-media]').dataset.mediaState==='playing');record('reduced-motion explicit play',()=>assert(!e.q('video').hidden,'not revealed on playing'));
 e=await load('/',390,{media:true,blocked:true});await until(()=>e.q('[data-hero-media]').dataset.mediaState==='blocked');
 record('autoplay denied',()=>{assert(e.w.getComputedStyle(e.q('video')).opacity==='0','video exposed');assert(e.q('[data-hero-poster]').complete,'poster not ready');return 'one injected NotAllowedError';});
 e.q('[data-hero-toggle]').click();await until(()=>e.q('[data-hero-media]').dataset.mediaState==='playing');
 record('manual recovery actual playback',()=>assert(e.q('video').currentTime>=0&&!e.q('video').paused,'not playing'));
 e.q('[data-hero-toggle]').click();await tick();record('paused_user',()=>assert(e.q('[data-hero-media]').dataset.mediaState==='paused_user','not paused'));
 e.w.scrollTo({top:e.q('#field').offsetTop,behavior:'instant'});await tick();e.w.scrollTo({top:0,behavior:'instant'});await new Promise(r=>setTimeout(r,250));
 record('user pause survives scroll return',()=>assert(e.q('video').paused&&e.q('[data-hero-media]').dataset.mediaState==='paused_user','unexpected restart'));
 e.q('[data-hero-toggle]').click();await until(()=>e.q('[data-hero-media]').dataset.mediaState==='ended');
 record('ended and replay',()=>assert(e.q('[data-hero-toggle]').textContent==='영상 다시 보기','missing replay'));
 e.w.scrollTo({top:e.q('#field').offsetTop,behavior:'instant'});await tick();e.w.scrollTo({top:0,behavior:'instant'});await new Promise(r=>setTimeout(r,250));record('ended remains ended',()=>assert(e.q('[data-hero-media]').dataset.mediaState==='ended','restarted'));
 e.q('[data-hero-toggle]').click();await until(()=>e.q('[data-hero-media]').dataset.mediaState==='playing');record('explicit replay',()=>assert(!e.q('video').paused,'did not replay'));
 e=await load('/',390,{media:true,visibility:true});await until(()=>e.q('[data-hero-media]').dataset.mediaState==='playing');e.w.qaSetHidden(true);await tick();
 record('environment pause (visibility injection)',()=>assert(e.q('video').paused&&e.q('[data-hero-media]').dataset.mediaState==='paused_environment','not paused'));
 e.w.qaSetHidden(false);await until(()=>e.q('[data-hero-media]').dataset.mediaState==='playing');record('environment resume',()=>assert(!e.q('video').paused,'not resumed'));
 e.q('[data-hero-toggle]').click();e.w.qaSetHidden(true);e.w.qaSetHidden(false);await tick();record('user pause survives visibility return',()=>assert(e.q('video').paused,'unexpected start'));
 e=await load('/',390,{media:true,error:true});await until(()=>e.q('[data-hero-media]').dataset.mediaState==='error');
 record('video 404',()=>{assert(e.q('video').hidden,'failed player visible');assert(e.q('[data-hero-poster]').complete,'poster missing');assert(e.q('.origin-next').getAttribute('href')==='#research','navigation changed');});
 statusNode.textContent='Interaction/media tests complete: '+results.filter(r=>r.status==='PASS').length+'/'+results.length;
}
let busy=false;
async function run(task){if(busy)return;busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);try{await task();}catch(e){statusNode.textContent='FAILED '+e.message;results.push({name:'incomplete run',status:'FAIL',error:e.message,mediaState:frame.contentDocument?.querySelector('[data-hero-media]')?.dataset.mediaState});result.textContent=JSON.stringify(results,null,2);console.error(e);}finally{busy=false;document.querySelectorAll('button').forEach(b=>b.disabled=false);}}
document.querySelector('#matrix').onclick=()=>run(matrix);
document.querySelector('#functional').onclick=()=>run(functional);
document.querySelector('#reduced').onclick=()=>run(()=>load('/',390,{reduced:true}).then(()=>statusNode.textContent='Reduced motion preference injected, poster_only'));
