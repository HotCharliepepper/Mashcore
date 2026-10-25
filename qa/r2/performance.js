/* LOCAL ONLY. Native navigation/render sample, not CrUX or an INP audit. */
(() => {
  const sample={environment:'local Chromium, real iframe navigation, no network/CPU throttle',started:new Date().toISOString(),viewport:innerWidth,lcp_ms:null,cls:0,observed_event_duration_ms:0,inp:'NOT RUN: no field population or full-session web-vitals computation'};
  const observers=[];
  function observe(type,callback,extra={}){try{const o=new PerformanceObserver(list=>callback(list.getEntries()));o.observe({type,buffered:true,...extra});observers.push(o);}catch(e){sample[type+'_unsupported']=e.name;}}
  observe('largest-contentful-paint',entries=>{const e=entries.at(-1);sample.lcp_ms=Math.round(e.startTime);sample.lcp_element=e.element?.tagName;});
  sample.layout_shifts=[];
  observe('layout-shift',entries=>{for(const e of entries)if(!e.hadRecentInput){sample.cls+=e.value;sample.layout_shifts.push({value:e.value,time:Math.round(e.startTime),sources:e.sources.map(s=>({node:s.node?.id||s.node?.className||s.node?.tagName,from:{x:s.previousRect.x,y:s.previousRect.y,width:s.previousRect.width,height:s.previousRect.height},to:{x:s.currentRect.x,y:s.currentRect.y,width:s.currentRect.width,height:s.currentRect.height}}))});}});
  observe('event',entries=>{for(const e of entries)if(e.interactionId)sample.observed_event_duration_ms=Math.max(sample.observed_event_duration_ms,e.duration);},{durationThreshold:16});
  addEventListener('load',()=>{
    const out=document.createElement('pre');out.id='qa-performance';out.style.cssText='white-space:pre-wrap;padding:24px;background:white;color:black;font:13px/1.6 monospace';document.body.append(out);
    function paint(){sample.sample_age_ms=Math.round(performance.now());sample.media_state=document.querySelector('[data-hero-media]')?.dataset.mediaState;sample.resources=performance.getEntriesByType('resource').filter(r=>/assets\/(media|js)\//.test(r.name)).map(r=>({file:r.name.split('/').pop(),transferSize:r.transferSize,encodedBodySize:r.encodedBodySize,duration_ms:Math.round(r.duration)}));out.textContent=JSON.stringify(sample,null,2);}
    paint();const timer=setInterval(paint,500);addEventListener('pagehide',()=>{clearInterval(timer);observers.forEach(o=>o.disconnect());},{once:true});
  });
})();
