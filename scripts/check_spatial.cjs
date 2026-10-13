const {parseHTML} = require('linkedom');
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root=require('node:path').resolve(__dirname,'..')+'/';
const fragment = parseHTML(fs.readFileSync(root+'index.html','utf8')).document.querySelector('[data-spatial]').outerHTML;
const script = fs.readFileSync(root+'assets/js/chore-spatial.js','utf8');
function environment(options={}) {
 const {document, Event}=parseHTML('<html><body>'+fragment+'</body></html>');
 const listeners=new Map(), timers=new Map(), frames=new Map(); let next=1, permissionCalls=0;
 const add=(name, fn)=>{if(!listeners.has(name))listeners.set(name,new Set());listeners.get(name).add(fn)};
 const remove=(name,fn)=>listeners.get(name)?.delete(fn);
 const media={matches:!!options.reduced,addEventListener(name,fn){this.onchange=fn},removeEventListener(){}};
 const orientation={angle:0,addEventListener(name,fn){this.onchange=fn},removeEventListener(){}};
 const window={isSecureContext:options.secure!==false,screen:{orientation},matchMedia:()=>media,addEventListener:add,removeEventListener:remove,
 requestAnimationFrame(fn){const id=next++;frames.set(id,fn);return id},cancelAnimationFrame(id){frames.delete(id)},
 setTimeout(fn){const id=next++;timers.set(id,fn);return id},clearTimeout(id){timers.delete(id)}};
 if(options.support!==false)window.DeviceOrientationEvent=options.noRequestPermission ? function(){} : {requestPermission(){permissionCalls++;return options.reject?Promise.reject(new Error('denied')):Promise.resolve(options.permission||'granted')}};
 vm.runInNewContext(script,{document,window});
 const q=selector=>document.querySelector(selector), root=q('[data-spatial]'), stage=q('[data-spatial-stage]');
 const fire=(target,type,fields={})=>{const event=new Event(type,{bubbles:true,cancelable:true});Object.assign(event,fields);target.dispatchEvent(event);return event};
 const flush=()=>{for(const [id,fn] of [...frames]){frames.delete(id);fn()}};
 flush();
 return {document,window,root,stage,q,media,orientation,fire,flush,timers,listeners,
 click:target=>fire(typeof target==='string'?q(target):target,'click'),
 emit:(name,event)=>[...(listeners.get(name)||[])].forEach(fn=>fn(event)),
 calls:()=>permissionCalls,
 settle:async()=>{await Promise.resolve();await Promise.resolve();flush()}};
}
(async()=>{
 const checks=[];
 let e=environment();assert.equal(e.calls(),0);assert.equal(e.q('[data-spatial-controls]').hidden,false);
 e.click('[data-spatial-select=meaning]');assert.equal(e.root.dataset.spatialSelected,'meaning');assert.match(e.q('[data-spatial-heading]').textContent,/의미/);assert.equal(e.document.querySelectorAll('[aria-pressed=true]').length,1);
 e.click('[data-spatial-turn="1"]');e.flush();assert.equal(e.q('[data-spatial-world]').style.getPropertyValue('--sp-yaw'),'8.00deg');
 e.fire(e.stage,'keydown',{key:'Home'});e.flush();assert.equal(e.q('[data-spatial-world]').style.getPropertyValue('--sp-yaw'),'0.00deg');checks.push('Selection, exclusive pressed state, keyboard rotation and reset; no unsolicited sensor request');
 e=environment({permission:'denied'});e.click('[data-spatial-sensor-button]');await e.settle();assert.equal(e.calls(),1);assert.match(e.q('[data-spatial-status]').textContent,/허용되지/);assert.equal(e.listeners.get('deviceorientation')?.size||0,0);assert.equal(e.q('[data-spatial-sensor-button]').disabled,false);checks.push('Permission denial returns to manual controls');
 e=environment({reject:true});e.click('[data-spatial-sensor-button]');await e.settle();assert.match(e.q('[data-spatial-status]').textContent,/연결하지/);checks.push('Permission exception has usable fallback');
 for(const options of [{support:false},{secure:false}]){e=environment(options);e.click('[data-spatial-sensor-button]');await e.settle();assert.equal(e.calls(),0);assert.match(e.q('[data-spatial-status]').textContent,/사용할 수 없습니다/)}checks.push('Unsupported API and insecure context do not request access');
 for(const options of [{},{noRequestPermission:true}]){e=environment(options);e.click('[data-spatial-sensor-button]');await e.settle();assert.equal(e.root.dataset.spatialSensor,'true');assert.equal(e.timers.size,1);e.emit('deviceorientation',{beta:null,gamma:null});for(const fn of [...e.timers.values()])fn();assert.equal(e.root.dataset.spatialSensor,'false');assert.match(e.q('[data-spatial-status]').textContent,/신호를 받지/);assert.equal(e.listeners.get('deviceorientation').size,0)}checks.push('Granted permission and no-permission API paths time out safely without sensor data');
 e=environment();e.click('[data-spatial-sensor-button]');await e.settle();e.emit('deviceorientation',{beta:40,gamma:2});e.flush();assert.equal(e.timers.size,0);e.emit('deviceorientation',{beta:45,gamma:22});e.flush();assert.equal(e.q('[data-spatial-world]').style.getPropertyValue('--sp-yaw'),'12.00deg');
 e.orientation.angle=90;e.orientation.onchange();e.emit('deviceorientation',{beta:45,gamma:22});e.flush();assert.equal(e.q('[data-spatial-world]').style.getPropertyValue('--sp-yaw'),'0.00deg');e.emit('deviceorientation',{beta:65,gamma:22});e.flush();assert.equal(e.q('[data-spatial-world]').style.getPropertyValue('--sp-yaw'),'12.00deg');
 e.document.hidden=true;e.fire(e.document,'visibilitychange');assert.equal(e.root.dataset.spatialSensor,'false');assert.equal(e.listeners.get('deviceorientation').size,0);checks.push('Sensor calibration, bounded camera pose, screen rotation recalibration, background cleanup');
 e=environment({reduced:true});e.click('[data-spatial-sensor-button]');await e.settle();assert.equal(e.calls(),0);assert.equal(e.stage.tabIndex,-1);assert.equal(e.q('[data-spatial-turn="1"]').disabled,true);e.click('[data-spatial-select=relation]');assert.equal(e.root.dataset.spatialSelected,'relation');
 e.media.matches=false;e.media.onchange();e.click('[data-spatial-sensor-button]');await e.settle();assert.equal(e.root.dataset.spatialSensor,'true');e.media.matches=true;e.media.onchange();assert.equal(e.root.dataset.spatialSensor,'false');assert.equal(e.listeners.get('deviceorientation').size,0);checks.push('Reduced-motion preference blocks movement while preserving content selection; live preference changes stop sensors');
 e=environment();let captured=false;e.stage.setPointerCapture=()=>{captured=true};e.stage.hasPointerCapture=()=>captured;e.stage.releasePointerCapture=()=>{captured=false};
 const down=e.fire(e.stage,'pointerdown',{pointerId:1,pointerType:'touch',clientX:100,clientY:100});const vertical=e.fire(e.stage,'pointermove',{pointerId:1,pointerType:'touch',clientX:103,clientY:140});e.flush();assert.equal(down.defaultPrevented,false);assert.equal(vertical.defaultPrevented,false);assert.equal(captured,false);assert.equal(e.q('[data-spatial-world]').style.getPropertyValue('--sp-yaw'),'0.00deg');
 e.fire(e.stage,'pointerdown',{pointerId:2,pointerType:'touch',clientX:100,clientY:100});e.fire(e.stage,'pointermove',{pointerId:2,pointerType:'touch',clientX:150,clientY:103});e.flush();assert.equal(captured,true);assert.equal(e.q('[data-spatial-world]').style.getPropertyValue('--sp-yaw'),'9.00deg');e.fire(e.stage,'pointercancel',{pointerId:2});assert.equal(captured,false);checks.push('Vertical touch motion remains browser-owned; horizontal drag rotates and pointer cancellation clears capture');
 e.click('[data-spatial-sensor-button]');await e.settle();e.emit('pagehide',{});assert.equal(e.listeners.get('deviceorientation').size,0);e.fire(e.root,'mashcore:spatial-destroy');for(const set of e.listeners.values())assert.equal(set.size,0);checks.push('Pagehide and explicit component disposal clean up listeners');
 console.log(JSON.stringify({status:'passed',environment:'Node DOM simulation; no physical sensor or rendered-browser assertion',checks},null,2));
})().catch(error=>{console.error(error);process.exit(1)});
