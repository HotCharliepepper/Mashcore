/* R3.1 word motion: additive, optional, and independent of app.js. */
(() => {
  'use strict';
  const VERSION = '3.15.0';
  const motion = Object.freeze({ duration: .85, stagger: .18, y: 8, ease: 'power2.out' });
  const origin = document.querySelector('[data-word-motion="origin"]');
  const research = document.querySelector('[data-word-motion="research"]');
  if (!origin && !research) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  const records = new Set();
  const played = new WeakSet();
  let trigger;
  let stopped = false;
  let resizeFrame;
  let width = document.documentElement.clientWidth;
  const optedOut = () => reduced.matches || !!connection?.saveData;
  const mark = (element, state) => { if (element) element.dataset.wordMotionState = state; };

  function revert(record) {
    record.timeline?.kill();
    record.split.revert();
    records.delete(record);
    mark(record.element, 'complete');
  }
  function stop(reason) {
    stopped = true;
    trigger?.kill();
    records.forEach(revert);
    [origin, research].forEach(element => mark(element, reason));
  }
  function loadPlugin(name) {
    if (window[name]) return Promise.resolve(window[name]);
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = `/assets/r31/${name}.min.js`;
      script.async = true;
      let settled = false;
      const timer = setTimeout(() => finish(new Error('Plugin timeout')), 4000);
      function finish(error) {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        script.onload = script.onerror = null;
        if (error) { script.remove(); reject(error); }
        else resolve(window[name]);
      }
      script.onload = () => finish(window[name] ? null : new Error('Plugin unavailable'));
      script.onerror = () => finish(new Error('Plugin failed'));
      document.head.append(script);
    });
  }
  function play(element) {
    if (!element || stopped || optedOut() || played.has(element)) return;
    played.add(element);
    let record;
    try {
      // Split only at playback, not while Research is below the viewport.
      // Keep <em>, <br>, language, DOM order and the existing accessible name.
      const split = window.SplitText.create(element, { type: 'words', wordsClass: 'r31-word', tag: 'span', aria: 'auto' });
      record = { element, split, timeline: null };
      records.add(record);
      mark(element, 'playing');
      const timeline = window.gsap.timeline({ onComplete: () => revert(record) });
      record.timeline = timeline;
      const emphasis = getComputedStyle(element).getPropertyValue('--r31-word-emphasis').trim();
      timeline.fromTo(split.words, { y: motion.y }, {
        y: 0, duration: motion.duration, stagger: motion.stagger, ease: motion.ease,
      }, 0);
      // No opacity-zero start or clipping: every word stays readable.
      split.words.forEach((word, index) => {
        const color = getComputedStyle(word).color;
        timeline.to(word, { color: emphasis || color, duration: motion.duration / 2, ease: 'sine.inOut' }, index * motion.stagger)
          .to(word, { color, duration: motion.duration / 2, ease: 'sine.inOut' }, index * motion.stagger + motion.duration / 2);
      });
    } catch (_) {
      if (record) revert(record);
      mark(element, 'fallback');
    }
  }
  async function initialize() {
    if (optedOut()) { stop('preference'); return; }
    if (window.gsap?.version !== VERSION) { stop('core-unavailable'); return; }
    try {
      const plugins = await Promise.all([loadPlugin('SplitText'), ...(research ? [loadPlugin('ScrollTrigger')] : [])]);
      if (stopped || optedOut()) { stop('preference'); return; }
      if (plugins.some(plugin => plugin?.version !== VERSION)) { stop('version-mismatch'); return; }
      window.gsap.registerPlugin(...plugins);
      // Avoid a late split that competes with font swap and Korean wrapping.
      let fontTimer;
      const fonts = await Promise.race([
        document.fonts.ready.then(() => true),
        new Promise(resolve => { fontTimer = setTimeout(() => resolve(false), 3000); }),
      ]);
      clearTimeout(fontTimer);
      if (stopped || optedOut()) return;
      if (!fonts) { stop('font-timeout'); return; }
      if (!document.hidden) play(origin);
      else mark(origin, 'background');
      if (research) {
        mark(research, 'waiting');
        trigger = window.ScrollTrigger.create({
          id: 'r31-word-research', trigger: research, start: 'top 86%', once: true,
          onEnter: () => play(research),
        });
      }
    } catch (_) { stop('plugin-unavailable'); }
  }
  const preferenceChanged = () => { if (optedOut()) stop('preference'); };
  reduced.addEventListener('change', preferenceChanged);
  connection?.addEventListener?.('change', preferenceChanged);
  // Never keep nowrap word wrappers through a viewport change or backgrounding.
  window.addEventListener('resize', () => {
    cancelAnimationFrame(resizeFrame);
    resizeFrame = requestAnimationFrame(() => {
      const next = document.documentElement.clientWidth;
      if (next !== width) records.forEach(revert);
      width = next;
    });
  }, { passive: true });
  document.addEventListener('visibilitychange', () => { if (document.hidden) records.forEach(revert); });
  window.addEventListener('pagehide', () => stop('pagehide'));
  initialize();
})();
