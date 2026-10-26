/* Review-only controls: actual iframe viewport, static motion, failure injection and measurements. */
(() => {
  'use strict';
  const byId=id=>document.getElementById(id);
  const frame=byId('site-preview'),holder=document.querySelector('.preview-frame'),space=document.querySelector('.preview-space'),open=byId('open-view');
  const page=byId('preview-page'),text=byId('preview-text'),nojs=byId('preview-nojs'),full=byId('preview-full');
  const hero=byId('preview-hero'),still=byId('preview-still'),failure=byId('preview-failure'),result=byId('preview-result');
  const buttons=[...document.querySelectorAll('[data-view]')];
  const views={desktop:{width:1440,height:960,label:'데스크톱'},mobile:{width:390,height:844,label:'모바일'},small:{width:320,height:844,label:'작은 모바일'},tablet:{width:768,height:1024,label:'태블릿'}};
  const params=new URL(location.href).searchParams;
  let selected=Object.hasOwn(views,params.get('view'))?params.get('view'):'desktop';
  let observers=[],metrics={};
  full.checked=params.get('full')==='1'; still.checked=params.get('motion')==='still';
  hero.value=params.get('hero')==='reverse'?'reverse':'default';
  if([...page.options].some(o=>o.value===params.get('page')))page.value=params.get('page');
  function target(){const u=new URL(page.value,location.origin);u.searchParams.set('preview',selected);if(hero.value==='reverse')u.searchParams.set('hero','reverse');if(still.checked)u.searchParams.set('motion','still');return u;}
  function resize(){const v=views[selected],scale=Math.min(1,space.clientWidth/v.width);frame.style.width=v.width+'px';let height=v.height;try{if(full.checked&&frame.contentDocument?.body)height=Math.max(height,frame.contentDocument.body.scrollHeight);}catch(_){}holder.style.width=v.width*scale+'px';holder.style.height=height*scale+'px';frame.style.height=height+'px';frame.style.transform='scale('+scale+')';}
  function load(){
    observers.forEach(o=>o.disconnect());observers=[];metrics={lcp_ms:null,cls:0};result.textContent='페이지 로드 중 · 아직 측정하지 않았습니다.';
    if(nojs.checked)frame.setAttribute('sandbox','allow-same-origin');else frame.removeAttribute('sandbox');
    frame.src=target().href;frame.title='Mashcore '+views[selected].label+' '+views[selected].width+'px';open.href=target().pathname+target().search;
    buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===selected)));
    byId('preview-caption').textContent=views[selected].label+' · '+views[selected].width+'px · '+(hero.value==='reverse'?'B':'A')+(still.checked?' · 정지 보기':'')+(text.checked?' · 글자 200%':'')+(nojs.checked?' · 스크립트 차단':'');
    const u=new URL(location.href);u.searchParams.set('view',selected);u.searchParams.set('page',page.value);u.searchParams.set('hero',hero.value);if(still.checked)u.searchParams.set('motion','still');else u.searchParams.delete('motion');history.replaceState(null,'',u);resize();
  }
  frame.addEventListener('load',async()=>{
    const d=frame.contentDocument,w=frame.contentWindow;if(!d?.body)return;
    if(text.checked){const sizes=[...d.querySelectorAll('body *')].map(e=>[e,parseFloat(w.getComputedStyle(e).fontSize)]);for(const[e,size]of sizes)if(Number.isFinite(size))e.style.fontSize=(size*2)+'px';}
    if(failure.value==='poster'){
      d.querySelectorAll('.origin-media source').forEach(e=>e.srcset='/__p01_missing_poster__.webp');
      const img=d.querySelector('[data-hero-poster]');if(img)img.src='/__p01_missing_poster__.webp';
    }
    if(failure.value==='video'){const v=d.querySelector('[data-hero-video]');if(v){v.src='/__p01_missing_video__.mp4';v.load();}}
    if(!nojs.checked&&w.PerformanceObserver){
      try{const lcp=new w.PerformanceObserver(list=>{for(const e of list.getEntries())metrics.lcp_ms=Math.round(e.startTime);});lcp.observe({type:'largest-contentful-paint',buffered:true});observers.push(lcp);}catch(_){}
      try{let sum=0,first=0,last=0;const cls=new w.PerformanceObserver(list=>{for(const e of list.getEntries()){if(e.hadRecentInput)continue;if(!first||e.startTime-last>1000||e.startTime-first>5000){sum=0;first=e.startTime;}sum+=e.value;last=e.startTime;metrics.cls=Math.max(metrics.cls,sum);}});cls.observe({type:'layout-shift',buffered:true});observers.push(cls);}catch(_){}
    }
    try{await d.fonts.ready;}catch(_){}resize();result.textContent='로드 완료 · 현재 화면 측정을 눌러주세요.';
  });
  byId('preview-measure').addEventListener('click',()=>{
    const d=frame.contentDocument,w=frame.contentWindow;if(!d?.body)return;
    const box=selector=>{const e=d.querySelector(selector);if(!e)return null;const r=e.getBoundingClientRect(),s=w.getComputedStyle(e);return {text:e.innerText,top:Math.round(r.top),bottom:Math.round(r.bottom),visible:s.display!=='none'&&s.visibility!=='hidden'&&r.width>0,above_fold:r.top>=0&&r.bottom<=w.innerHeight};};
    const root=d.querySelector('[data-hero-experience]'),stage=d.querySelector('[data-hero-media]');
    result.textContent=JSON.stringify({environment:'review iframe; single sample',viewport:[w.innerWidth,w.innerHeight],route:page.value,hero:root?.dataset.heroMode,still:still.checked,no_js:nojs.checked,text_200:text.checked,failure:failure.value,overflow_px:Math.max(0,d.documentElement.scrollWidth-w.innerWidth),h1:box('h1'),cta:box('.hero-primary'),signal_state:root?.dataset.heroMotion,media_state:stage?.dataset.mediaState,poster_loaded:!!d.querySelector('[data-hero-poster]')?.naturalWidth,video_src:d.querySelector('[data-hero-video]')?.getAttribute('src'),lcp_ms:metrics.lcp_ms,cls:Number(metrics.cls.toFixed(5)),inp:'NOT_MEASURED',font_status:d.fonts.status},null,2);
  });
  full.addEventListener('change',()=>{const u=new URL(location.href);u.searchParams.set('full',full.checked?'1':'0');history.replaceState(null,'',u);resize();});
  buttons.forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.view;load();}));
  [page,text,nojs,hero,still,failure].forEach(el=>el.addEventListener('change',load));
  window.addEventListener('resize',resize);if('ResizeObserver'in window)new ResizeObserver(resize).observe(space);load();
})();
