/* Behaviour checks for finite cues and explicit static media.
 * Node event/DOM simulation, not a browser layout or device test. */
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const assert = require('node:assert/strict');
const rootPath = path.resolve(__dirname, '..', 'dist', 'assets', 'js');
class Element {
  constructor() {
    this.dataset = {}; this.attrs = {}; this.events = {}; this.queries = {};
    this.hidden = false; this.textContent = ''; this.complete = true; this.naturalWidth = 100;
    const names = new Set();
    this.classList = {add: n => names.add(n), remove: n => names.delete(n), contains: n => names.has(n)};
  }
  querySelector(q) { return this.queries[q]?.[0] || null; }
  querySelectorAll(q) { return this.queries[q] || []; }
  addEventListener(name, fn) { (this.events[name] ||= []).push(fn); }
  fire(name, event = {}) { for (const fn of this.events[name] || []) fn({target:this, ...event}); }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  getAttribute(name) { return this.attrs[name] ?? null; }
  removeAttribute(name) { delete this.attrs[name]; }
}
function environment(options = {}) {
  const doc = new Element(), win = new Element(), root = new Element();
  const bar = new Element(), status = new Element(), toggle = new Element(), trace = new Element(), stage = new Element(), poster = new Element();
  const choices = ['default','reverse'].map(mode => {const el = new Element(); el.dataset.heroModeChoice = mode; return el;});
  const reduced = new Element(), compact = new Element(), connection = new Element();
  reduced.matches = Boolean(options.reduced); compact.matches = Boolean(options.compact); connection.saveData = Boolean(options.saveData);
  poster.naturalWidth = options.posterError ? 0 : 100;
  const fields = {'[data-hero-mode-controls]':bar,'[data-hero-variant-status]':status,'[data-hero-motion-toggle]':toggle,'.hero-reverse-trace':trace,'[data-hero-media]':stage,'[data-hero-poster]':poster};
  for (const [key, value] of Object.entries(fields)) root.queries[key] = [value];
  root.queries['[data-hero-mode-choice]'] = choices; doc.queries['[data-hero-experience]'] = [root];
  doc.hidden = false; win.location = new URL('https://review.example/' + (options.query || ''));
  win.matchMedia = q => q.includes('reduced-motion') ? reduced : compact;
  let seq = 0, observer; const frames = new Map();
  class Observer { constructor(fn) { this.fn = fn; observer = this; } observe() { this.connected = true; } disconnect() { this.connected = false; } emit(visible) { this.fn([{isIntersecting:visible}]); } }
  win.IntersectionObserver = Observer;
  const context = {document:doc, window:win, navigator:{connection}, URL, URLSearchParams, IntersectionObserver:Observer,
    history:{state:null, replaceState(state, title, url) {win.location = new URL(url, win.location);}},
    requestAnimationFrame:fn => {frames.set(++seq,fn); return seq;}, cancelAnimationFrame:id => frames.delete(id), console};
  const flush = () => { for(let count=0; frames.size && count<5; count++) { const current=[...frames.values()]; frames.clear(); current.forEach(fn=>fn()); } };
  vm.runInNewContext(fs.readFileSync(path.join(rootPath,'hero-reverse.js'),'utf8'), context);
  return {doc,win,root,bar,status,toggle,trace,stage,poster,choices,reduced,compact,connection,frames,flush,observer:()=>observer,context};
}
const checks = [];
{
  const e=environment(); e.flush(); assert.equal(e.root.dataset.heroMode,'default'); assert.equal(e.root.dataset.heroMotion,'complete'); assert.equal(e.toggle.hidden,true);
  e.choices[1].fire('click'); e.flush(); assert.equal(e.root.dataset.heroMotion,'running'); assert.equal(e.win.location.search,'?hero=reverse'); assert.equal(e.choices[1].attrs['aria-pressed'],'true');
  e.choices[1].fire('click'); assert.equal(e.frames.size,0); assert.equal(e.root.dataset.heroMotion,'running');
  e.toggle.fire('click'); assert.equal(e.root.dataset.heroMotion,'paused'); assert.equal(e.toggle.textContent,'신호선 이어보기');
  e.doc.hidden=true; e.doc.fire('visibilitychange'); e.doc.hidden=false; e.doc.fire('visibilitychange'); assert.equal(e.root.dataset.heroMotion,'paused');
  e.toggle.fire('click'); assert.equal(e.root.dataset.heroMotion,'running');
  e.trace.fire('animationend',{animationName:'hero-reverse-draw'}); assert.equal(e.root.dataset.heroMotion,'complete'); assert.equal(e.toggle.textContent,'신호선 다시보기'); assert.equal(e.frames.size,0);
  checks.push('A default; B updates URL/pressed state; repeated B does not restart; user pause survives background; finite completion offers replay');
}
{
  const e=environment(); e.choices[1].fire('click'); e.choices[0].fire('click'); e.flush(); assert.equal(e.root.dataset.heroMode,'default'); assert.equal(e.root.dataset.heroMotion,'complete'); assert.equal(e.root.classList.contains('hero-reverse-replay'),false);
  e.win.location=new URL('https://review.example/?hero=reverse'); e.win.fire('popstate'); e.flush(); assert.equal(e.root.dataset.heroMode,'reverse');
  checks.push('Rapid B→A cancels queued animation; URL back/forward state is reconciled');
}
for(const option of ['reduced','compact','saveData','posterError']) {
  const e=environment({[option]:true,query:'?hero=reverse'}); e.flush(); assert.equal(e.root.dataset.heroMotion,'complete'); assert.equal(e.toggle.hidden,true); assert.equal(e.bar.hidden,false);
  checks.push(option+': no animation, usable A/B controls remain');
}
{
  const e=environment({query:'?hero=reverse&motion=still'}); e.flush(); assert.equal(e.root.dataset.heroReduced,'true'); assert.equal(e.root.dataset.heroMotion,'complete'); assert.equal(e.toggle.hidden,true);
  checks.push('Explicit static preview is complete without queued motion');
}
{
  const e=environment({query:'?hero=reverse'}); e.flush(); e.observer().emit(false); assert.equal(e.root.dataset.heroMotion,'paused'); e.observer().emit(true); assert.equal(e.root.dataset.heroMotion,'running');
  e.win.fire('pagehide'); assert.equal(e.root.dataset.heroMotion,'paused'); assert.equal(e.observer().connected,false);
  e.win.fire('pageshow',{persisted:true}); assert.equal(e.observer().connected,true); e.observer().emit(true); assert.equal(e.root.dataset.heroMotion,'running');
  e.reduced.matches=true; e.reduced.fire('change'); assert.equal(e.root.dataset.heroMotion,'complete'); e.reduced.matches=false; e.reduced.fire('change'); assert.equal(e.root.dataset.heroMotion,'complete'); assert.equal(e.frames.size,0);
  checks.push('Offscreen and persisted page restoration pause/resume; clearing reduced-motion preference never restarts');
}
{
  const e=environment({query:'?hero=reverse'}); e.flush(); e.poster.fire('error'); assert.equal(e.root.dataset.heroPosterError,'true'); assert.equal(e.root.dataset.heroMotion,'complete'); e.poster.fire('load'); assert.equal(e.root.dataset.heroPosterError,'false'); assert.equal(e.root.dataset.heroMotion,'complete');
  checks.push('Poster failure removes misleading cue; recovered poster does not auto-replay');
}
{
  const e=environment({query:'?hero=reverse&motion=still'}), video=new Element(), controls=new Element(), button=new Element(), status=new Element(), config=new Element();
  config.textContent=JSON.stringify({video:{desktop:'/test.mp4',mobile:'/test-mobile.mp4',loop:false},ui:{pause_label:'정지',play_label:'재생',replay_label:'다시'}});
  video.readyState=0; video.load=()=>{}; video.pause=()=>{}; let playCalls=0; video.play=async()=>{playCalls++;};
  for(const [key,value] of Object.entries({'[data-hero-config]':config,'[data-hero-video]':video,'[data-hero-controls]':controls,'[data-hero-toggle]':button,'[data-hero-status]':status,'[data-hero-poster]':e.poster}))e.stage.queries[key]=[value];
  e.doc.queries['[data-hero-media]']=[e.stage];
  vm.runInNewContext(fs.readFileSync(path.join(rootPath,'hero-media.js'),'utf8'),e.context);
  e.observer().emit(true); assert.equal(e.stage.dataset.mediaState,'reduced_motion'); assert.equal(video.src,undefined); assert.equal(playCalls,0); assert.equal(video.hidden,true);
  button.fire('click'); assert.equal(video.src,'/test.mp4'); video.readyState=3; video.fire('canplay'); assert.equal(playCalls,1);
  assert.equal(video.getAttribute('aria-hidden'),'true'); video.fire('playing'); assert.equal(e.stage.dataset.mediaState,'playing'); assert.equal(video.getAttribute('aria-hidden'),'false');
  checks.push('Static mode makes no video request; explicit play still works and reveal requires actual playing event');
}
console.log(JSON.stringify({status:'passed',environment:'Node VM event/DOM simulation; not a browser/device test',count:checks.length,checks},null,2));
