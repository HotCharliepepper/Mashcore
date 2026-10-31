/* R3.3, adapted from Draft #14: optional and independent of R3.1 app.js. */
(() => {
  'use strict';
  const VERSION = '3.15.0';
  const params = new URLSearchParams(location.search);
  const preset = params.get('motion') === 'calm' ? 'calm' : params.get('motion') === 'still' ? 'still' : 'slow';
  const before = document.documentElement.dataset.r32Layout === 'before';
  const motion = Object.freeze({ duration: preset === 'calm' ? 1.85 : 2.2, stagger: preset === 'calm' ? .70 : .90, y: 14, ease: 'sine.out' });
  document.documentElement.dataset.wordMotionPreset = preset;
  document.documentElement.dataset.wordMotionDuration = String(motion.duration);
  document.querySelectorAll('[data-r32-motion-choice]').forEach(link => {
    if ((!before && link.dataset.r32MotionChoice === preset) || (before && link.dataset.r32MotionChoice === 'before')) link.setAttribute('aria-current', 'page');
  });
  const comparisonStatus = document.querySelector('[data-r32-motion-status]');
  if (comparisonStatus) comparisonStatus.textContent = before ? 'R3.1 기준 화면 · 워드 모션 없음' : preset === 'still' ? '워드 모션 정지 · 원문은 그대로 읽을 수 있습니다.' : `의미 구절 ${motion.duration}초 · 시작 간격 ${motion.stagger}초 · 기기의 모션 감소 설정을 우선합니다.`;
  const origin = document.querySelector('[data-word-motion="origin"]');
  const research = document.querySelector('[data-word-motion="research"]');
  if (!origin && !research) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  const records = new Set();
  let played = new WeakSet();
  let trigger;
  let stopped = false;
  let resizeFrame;
  let width = document.documentElement.clientWidth;
  const optedOut = () => reduced.matches || !!connection?.saveData || preset === 'still' || before;
  const replayButton = document.querySelector('[data-r32-replay]');
  if (replayButton) replayButton.disabled = optedOut();
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
      script.src = `/assets/r32/${name}.min.js`;
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
      // Delimiter retains the original <em>/<br> structure and spaces exactly.
      const originalHTML = element.innerHTML;
      const accessibleName = element.getAttribute('aria-label') || element.innerText.replace(/\s+/g, ' ').trim();
      const delimiter = '\uE000';
      if (element === origin) element.innerHTML = originalHTML
        .replace('그 사람은,', '그 사람은,' + delimiter)
        .replace('멈췄을까요?', delimiter + '멈췄을까요?');
      let split;
      try {
        split = window.SplitText.create(element, { type: 'words', wordsClass: 'r32-word', tag: 'span', aria: 'auto', ...(element === origin ? { wordDelimiter: delimiter } : {}) });
      } catch (error) { element.innerHTML = originalHTML; throw error; }
      // SplitText reads the temporary delimiter too; expose only the original name.
      element.setAttribute('aria-label', accessibleName);
      const pluginRevert = split.revert.bind(split);
      split.revert = () => { pluginRevert(); element.innerHTML = originalHTML; };
      record = { element, split, timeline: null };
      records.add(record);
      mark(element, 'playing');
      const timeline = window.gsap.timeline({ onComplete: () => revert(record) });
      record.timeline = timeline;
      const emphasis = getComputedStyle(element).getPropertyValue('--r31-word-emphasis').trim();
      // No opacity-zero start or clipping: every word stays readable.
      split.words.forEach((word, index) => {
        timeline.fromTo(word, { y: motion.y }, { y: 0, duration: motion.duration, ease: motion.ease }, index * motion.stagger);
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
    if (optedOut()) {
      if (comparisonStatus && (reduced.matches || connection?.saveData)) comparisonStatus.textContent = '모션 감소 또는 데이터 절약 설정으로 정지 화면을 표시합니다.';
      stop('preference'); return;
    }
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
          id: 'r32-word-research', trigger: research, start: 'top 86%', once: true,
          onEnter: () => play(research),
        });
      }
    } catch (_) { stop('plugin-unavailable'); }
  }
  const preferenceChanged = () => { if (optedOut()) stop('preference'); if (replayButton) replayButton.disabled = optedOut(); };
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
  window.addEventListener('pageshow', event => { if (event.persisted) { stopped = false; mark(origin, 'restored'); } });
  document.querySelector('[data-r33-skip]')?.addEventListener('click', () => stop('skipped'));
  if ('IntersectionObserver' in window && origin) new IntersectionObserver(entries => {
    if (!entries[0].isIntersecting) records.forEach(record => { if (record.element === origin) revert(record); });
  }).observe(origin);
  // Replay controls may already be below the title. An observer does not emit
  // another exit when replay starts offscreen, so scroll also checks active work.
  window.addEventListener('scroll', () => {
    if (!origin || !records.size) return;
    const rect = origin.getBoundingClientRect();
    if (rect.bottom <= 0 || rect.top >= innerHeight)
      records.forEach(record => { if (record.element === origin) revert(record); });
  }, { passive: true });
  document.querySelector('[data-r32-replay]')?.addEventListener('click', () => {
    if (optedOut()) return;
    records.forEach(revert);
    trigger?.kill();
    played = new WeakSet();
    stopped = false;
    initialize();
  });
  initialize();
})();

/* Native proximity only: no wheel/touch interception, pin, or nested scroller.
   Root participates only while the two fitting scenes are near the viewport. */
(() => {
  const root = document.documentElement;
  const origin = document.getElementById('origin');
  const research = document.getElementById('research');
  if (!origin || !research) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const params = new URLSearchParams(location.search);
  let frame;
  function update() {
    const header = document.querySelector('.site-header')?.getBoundingClientRect().height || 0;
    const available = innerHeight - header;
    const a = origin.getBoundingClientRect(), b = research.getBoundingClientRect();
    const fits = a.height <= available + 2 && b.height <= available + 2;
    const eligible = params.get('scroll') !== 'free' && !reduced.matches && !navigator.connection?.saveData
      && !location.hash && fits && innerHeight > 600 && (visualViewport?.scale || 1) <= 1
      && scrollY < research.offsetTop - header - 4;
    root.classList.toggle('r33-proximity', eligible);
    root.dataset.r33Scroll = eligible ? 'proximity' : 'free';
    root.style.setProperty('--r33-header', header + 'px');
  }
  const schedule = () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(update); };
  ['scroll','resize','pageshow','hashchange'].forEach(name => addEventListener(name, schedule, {passive:true}));
  reduced.addEventListener('change', schedule);
  navigator.connection?.addEventListener?.('change', schedule);
  visualViewport?.addEventListener('resize', schedule);
  new ResizeObserver(schedule).observe(research);
  new ResizeObserver(schedule).observe(origin);
  document.addEventListener('focusin', () => root.classList.remove('r33-proximity'));
  addEventListener('pagehide', () => root.classList.remove('r33-proximity'));
  update();
})();
