import {mountWhyResonance} from './why-resonance.js';

// Published scene: the reviewed restrained composition, with existing motion policy.
function initializeWhyResonance() {
 const container=document.querySelector('#core-reveal > .closing');
 const anchor=container?.querySelector(':scope > .signature svg > path');
 if(!container || !anchor)return;
 const motionControl=document.querySelector('.motion-control');
 const siteReduced=()=>motionControl?.getAttribute('aria-pressed')==='true';
 const exclusions=[container.querySelector('.final-brand'),...container.querySelectorAll('.afterword p,.afterword a')].filter(Boolean);
 let lastSiteReduced=siteReduced(),destroyed=false,observer=null;
 const engine=mountWhyResonance({container,anchor,mode:'subtle',questionMarks:false,exclusions,bpm:Number(new URLSearchParams(location.search).get('y-bpm'))||71.4});
 engine.setReduced(lastSiteReduced);
 window.mashcoreWhyResonance={
  getState(){return {reviewControls:false,anchorSelector:'#core-reveal > .closing > .signature svg > path',...engine.getState()};},
  setPaused(value){if(!destroyed)engine.setPaused(!!value);},
  destroy(){if(destroyed)return;destroyed=true;observer?.disconnect();engine.destroy();}
 };
 if(motionControl){
  observer=new MutationObserver(()=>{
   const next=siteReduced();
   if(next===lastSiteReduced)return;
   lastSiteReduced=next;engine.setReduced(next);
  });
  observer.observe(motionControl,{attributes:true,attributeFilter:['aria-pressed']});
 }
}

if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initializeWhyResonance,{once:true});
else initializeWhyResonance();
