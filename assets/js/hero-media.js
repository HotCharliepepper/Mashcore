/* Poster-first review media. No requests when a source is absent; no analytics. */
(() => {
  'use strict';
  const root = document.querySelector('[data-hero-media]');
  if (!root) return;
  const configNode = root.querySelector('[data-hero-config]');
  let config;
  try { config = JSON.parse(configNode.textContent); } catch (_) { return; }
  const video = root.querySelector('[data-hero-video]');
  const controls = root.querySelector('[data-hero-controls]');
  const button = root.querySelector('[data-hero-toggle]');
  const status = root.querySelector('[data-hero-status]');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const narrow = window.matchMedia('(max-width: 900px)').matches;
  const source = narrow ? (config.video.mobile || config.video.desktop) : (config.video.desktop || config.video.mobile);
  // Only explicit local media paths are used. Invalid configuration keeps the poster.
  if (!video || typeof source !== 'string' || !source.startsWith('/') || source.startsWith('//')) return;
  let state = 'loading', userPaused = false, ended = false, inView = false;
  let requested = false, hasPlayed = false, pending = false, explicitChoice = false;
  let autoplayAttempted = false, blocked = false, failed = false;
  let environmentResume = false, manualPending = false, generation = 0;
  const saveData = Boolean(navigator.connection && navigator.connection.saveData);
  const ui = config.ui;
  const labels = {
    loading: '정지 이미지로 먼저 살펴보세요.',
    playing: '영상 재생 중', paused_user: '직접 일시정지했습니다.',
    paused_environment: '화면으로 돌아오면 이어집니다.', ended: '영상이 끝났습니다.',
    blocked: '버튼을 눌러 영상을 재생할 수 있습니다.',
    error: '영상을 불러오지 못해 정지 이미지를 표시합니다.',
    reduced_motion: '모션 감소 설정으로 자동재생하지 않습니다.'
  };
  function setState(next) {
    state = next; root.dataset.mediaState = next;
    status.textContent = labels[next] || '';
    button.textContent = next === 'playing' ? ui.pause_label : next === 'ended' ? ui.replay_label : ui.play_label;
    button.disabled = next === 'error';
    // The poster remains below the video; only an actual playing event reveals it.
    const reveal = hasPlayed && !['loading','blocked','error','reduced_motion'].includes(next);
    // A requested video prepares in layout at zero opacity; the poster stays visible.
    video.hidden = !requested || failed;
    video.setAttribute('aria-hidden', reveal ? 'false' : 'true');
    if (reveal && !video.classList.contains('is-visible')) {
      requestAnimationFrame(() => requestAnimationFrame(() => {
        if (!video.hidden && video.getAttribute('aria-hidden') === 'false') video.classList.add('is-visible');
      }));
    } else if (!reveal) {
      video.classList.remove('is-visible');
    }
  }
  function eligible() { return inView && !document.hidden && !userPaused && !ended && !failed; }
  function load() {
    if (requested) return;
    requested = true; video.hidden = false;
    video.muted = true; video.playsInline = true; video.loop = Boolean(config.video.loop);
    video.preload = 'auto'; video.src = source; video.load();
  }
  function pauseForEnvironment() {
    if (state !== 'playing' && !pending) return;
    environmentResume = !userPaused && !ended;
    generation++; pending = false; video.pause();
    setState('paused_environment');
  }
  async function attempt(manual = false) {
    if (!eligible() || pending) return;
    if (!manual && (blocked || (!explicitChoice && (reduced.matches || saveData)))) return;
    if (!manual && !environmentResume && autoplayAttempted) return;
    if (!manual) autoplayAttempted = true;
    if (manual) { blocked = false; explicitChoice = true; manualPending = false; }
    pending = true; environmentResume = false;
    const ticket = ++generation;
    setState('loading');
    try {
      await video.play();
      // A settled older play promise must not pause a newer explicit request.
      if (ticket !== generation) { if (!eligible()) video.pause(); return; }
      if (!eligible()) {
        video.pause();
        if (!userPaused && !ended && !failed) setState('paused_environment');
      }
      // Promise resolution alone never changes the poster to a playing frame.
    } catch (error) {
      if (ticket !== generation) return;
      if (error.name === 'NotAllowedError') { blocked = true; setState('blocked'); }
      else if (error.name === 'AbortError' && !eligible()) setState('paused_environment');
      else { failed = true; setState('error'); }
    } finally { if (ticket === generation) pending = false; }
  }
  function reconcile() {
    if (!eligible()) { pauseForEnvironment(); return; }
    if (!requested && !reduced.matches && !saveData) load();
    if (video.readyState >= 3) attempt(manualPending);
  }
  video.addEventListener('canplay', reconcile);
  video.addEventListener('playing', () => {
    if (!eligible()) { video.pause(); return; }
    hasPlayed = true; pending = false; setState('playing');
  });
  video.addEventListener('ended', () => { ended = true; environmentResume = false; setState('ended'); });
  video.addEventListener('error', () => { failed = true; generation++; pending = false; video.pause(); setState('error'); });
  button.addEventListener('click', () => {
    if (state === 'playing' || pending) {
      userPaused = true; manualPending = false; environmentResume = false; generation++; pending = false;
      video.pause(); setState('paused_user'); return;
    }
    if (failed) return;
    userPaused = false; explicitChoice = true; manualPending = true;
    if (ended) { video.currentTime = 0; ended = false; }
    load();
    if (video.readyState >= 3) attempt(true);
    else setState('loading');
  });
  document.addEventListener('visibilitychange', reconcile);
  reduced.addEventListener('change', () => {
    if (reduced.matches) {
      explicitChoice = false; manualPending = false; userPaused = true; generation++; pending = false;
      video.pause(); setState('reduced_motion');
    }
    // Toggling the preference back is not consent to restart.
  });
  let observer;
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(entries => {
      inView = entries.some(entry => entry.isIntersecting); reconcile();
    }, {threshold: 0.15});
    observer.observe(root);
  } else { inView = true; }
  window.addEventListener('pagehide', () => { inView = false; pauseForEnvironment(); observer?.disconnect(); });
  window.addEventListener('pageshow', event => { if (event.persisted) { if (observer) observer.observe(root); else { inView = true; reconcile(); } } });
  controls.hidden = false;
  setState(reduced.matches ? 'reduced_motion' : saveData ? 'blocked' : 'loading');
  reconcile();
})();
