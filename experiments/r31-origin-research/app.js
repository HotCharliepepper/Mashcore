(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const desktop = matchMedia('(min-width: 821px)');
  const connection = navigator.connection;
  const saveData = () => !!connection?.saveData;
  const canAnimate = () => desktop.matches && !reduced.matches && !saveData();
  const buttons = [...document.querySelectorAll('[data-research-step]')];
  const panels = [...document.querySelectorAll('[data-step-panel]')];
  const reading = document.getElementById('research-reading');
  function selectStep(id) {
    if (!panels.some(panel => panel.dataset.stepPanel === id)) return;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.researchStep === id)));
    panels.forEach(panel => { panel.hidden = panel.dataset.stepPanel !== id; });
    if (window.gsap && canAnimate()) {
      window.gsap.killTweensOf(reading);
      window.gsap.fromTo(reading, { y: 6 }, { y: 0, duration: .3, ease: 'power2.out', clearProps: 'transform' });
    }
  }
  // All explanations remain readable when JavaScript is unavailable.
  panels.forEach(panel => { panel.hidden = panel.dataset.stepPanel !== 'observation'; });
  document.querySelector('.r31-steps').hidden = false;
  buttons.forEach(button => button.addEventListener('click', () => selectStep(button.dataset.researchStep)));

  const video = document.getElementById('origin-video');
  const toggle = document.getElementById('video-toggle');
  let requested = false;
  let autoAttempted = false;
  let finished = false;
  let failed = false;
  let visible = true;
  let requestID = 0;
  let loadTimer;
  const update = () => {
    const playing = !video.paused && !video.ended && !failed && !reduced.matches;
    video.classList.toggle('is-playing', playing);
    toggle.setAttribute('aria-pressed', String(playing));
    toggle.disabled = failed || reduced.matches;
    toggle.textContent = failed ? '정지 이미지 보기' : reduced.matches ? '모션 감소 · 정지 이미지' : playing ? '영상 일시정지' : finished ? '영상 다시보기' : video.currentTime > 0 ? '영상 이어보기' : '영상 재생';
  };
  function pause() {
    requested = false;
    requestID++;
    clearTimeout(loadTimer);
    video.pause();
    update();
  }
  async function play() {
    if (failed || reduced.matches || document.hidden || !visible) return;
    const id = ++requestID;
    requested = true;
    if (!video.getAttribute('src')) video.src = video.dataset.src;
    if (finished || video.ended) { video.currentTime = 0; finished = false; }
    clearTimeout(loadTimer);
    loadTimer = setTimeout(() => { if (id === requestID && video.readyState < 2) pause(); }, 10000);
    try {
      await video.play();
      if (id !== requestID || !requested || !visible || document.hidden || reduced.matches) video.pause();
      clearTimeout(loadTimer);
      update();
    } catch (_) {
      if (id === requestID) { requested = false; clearTimeout(loadTimer); update(); }
    }
  }
  toggle.hidden = false;
  toggle.addEventListener('click', () => { autoAttempted = true; if (requested || !video.paused) pause(); else play(); });
  video.addEventListener('playing', update);
  video.addEventListener('pause', update);
  video.addEventListener('ended', () => { finished = true; requested = false; update(); });
  video.addEventListener('error', () => { failed = true; pause(); });
  const stopForPreference = () => { if (reduced.matches || !desktop.matches || saveData()) pause(); update(); };
  reduced.addEventListener('change', stopForPreference);
  desktop.addEventListener('change', stopForPreference);
  connection?.addEventListener?.('change', stopForPreference);
  document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
  window.addEventListener('pagehide', pause);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      if (!visible) pause();
      else if (!autoAttempted && canAnimate() && !document.hidden) { autoAttempted = true; play(); }
    }, { threshold: .2 }).observe(document.querySelector('.r31-media'));
  }
  update();

  // Motion never owns visibility of the copy, navigation or research content.
  if (window.gsap && !saveData()) {
    const gsap = window.gsap;
    const media = gsap.matchMedia();
    media.add('(min-width: 821px) and (prefers-reduced-motion: no-preference)', () => {
      const timeline = gsap.timeline({ defaults: { ease: 'power2.out' } });
      timeline.fromTo('.r31-focus', { scale: .9, transformOrigin: '50% 50%', opacity: .35 }, { scale: 1, opacity: .8, duration: 1.2 });
      timeline.fromTo('.r31-signal-line', { strokeDashoffset: 24, opacity: .3 }, { strokeDashoffset: 0, opacity: .85, duration: 1.6, stagger: .15 }, .3);
      return () => { gsap.killTweensOf(reading); gsap.set(reading, { clearProps: 'transform' }); };
    });
    connection?.addEventListener?.('change', () => { if (saveData()) media.revert(); });
  }
})();
