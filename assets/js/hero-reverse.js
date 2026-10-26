/* P01: finite visual cue; core content and existing video player stay independent. */
(() => {
  'use strict';
  const root = document.querySelector('[data-hero-experience]');
  if (!root) return;
  const bar = root.querySelector('[data-hero-mode-controls]');
  const buttons = [...root.querySelectorAll('[data-hero-mode-choice]')];
  const status = root.querySelector('[data-hero-variant-status]');
  const toggle = root.querySelector('[data-hero-motion-toggle]');
  const trace = root.querySelector('.hero-reverse-trace');
  const stage = root.querySelector('[data-hero-media]');
  const poster = root.querySelector('[data-hero-poster]');
  if (!bar || !status || !toggle || !trace || !stage || buttons.length !== 2) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const compact = window.matchMedia('(max-width: 1100px)');
  const connection = navigator.connection;
  let frame = null, mode = null, inView = true, userPaused = false;
  let motion = 'complete', posterFailed = false;
  const fromUrl = () => new URLSearchParams(window.location.search).get('hero') === 'reverse' ? 'reverse' : 'default';
  const stillRequested = () => new URLSearchParams(window.location.search).get('motion') === 'still';
  const quiet = () => reduced.matches || Boolean(connection?.saveData) || stillRequested();
  const canAnimate = () => mode === 'reverse' && !compact.matches && !quiet() && !posterFailed;
  function render() {
    const environmentPaused = document.hidden || !inView;
    root.dataset.heroMotion = motion === 'running' && (userPaused || environmentPaused) ? 'paused' : motion;
    root.dataset.heroReduced = String(quiet());
    root.dataset.heroPosterError = String(posterFailed);
    toggle.hidden = !canAnimate();
    toggle.textContent = motion === 'running' ? (userPaused ? '신호선 이어보기' : '신호선 정지') : '신호선 다시보기';
    status.textContent = mode === 'default' ? 'A 구성. 기존 R2의 질문, 설명과 서비스 링크입니다.'
      : 'B 구성. 안내를 확인하는 자리에서 질문으로 시선을 연결합니다. 질문, 설명과 서비스 링크는 A와 같습니다.'
        + (quiet() || compact.matches ? ' 정지된 구성으로 표시합니다.' : '')
        + (userPaused ? ' 신호선을 일시정지했습니다.' : '');
  }
  function finish() {
    if (frame !== null) cancelAnimationFrame(frame);
    frame = null; motion = 'complete'; userPaused = false;
    root.classList.remove('hero-reverse-replay'); render();
  }
  function replay() {
    finish();
    if (!canAnimate() || document.hidden || !inView) return;
    frame = requestAnimationFrame(() => {
      frame = requestAnimationFrame(() => {
        frame = null;
        if (!canAnimate() || document.hidden || !inView) return;
        motion = 'running'; root.classList.add('hero-reverse-replay'); render();
      });
    });
  }
  function activate(next, updateUrl = false) {
    if (!['default', 'reverse'].includes(next)) return;
    const changed = mode !== next;
    mode = next; root.dataset.heroMode = mode;
    document.documentElement.dataset.heroInitialMode = mode;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.heroModeChoice === mode)));
    if (updateUrl) {
      const url = new URL(window.location.href);
      if (mode === 'reverse') url.searchParams.set('hero', 'reverse');
      else url.searchParams.delete('hero');
      history.replaceState(history.state, '', url.pathname + url.search + url.hash);
    }
    bar.hidden = false;
    if (changed) { if (mode === 'reverse') replay(); else finish(); }
    render();
  }
  buttons.forEach(b => b.addEventListener('click', () => activate(b.dataset.heroModeChoice, true)));
  toggle.addEventListener('click', () => {
    if (motion === 'running') { userPaused = !userPaused; render(); } else replay();
  });
  trace.addEventListener('animationend', e => {
    if (e.animationName === 'hero-reverse-draw') { motion = 'complete'; userPaused = false; render(); }
  });
  function preferencesChanged() {
    // Restoring a preference is not consent to restart a completed cue.
    if (!canAnimate()) finish(); else render();
  }
  reduced.addEventListener('change', preferencesChanged);
  compact.addEventListener('change', preferencesChanged);
  connection?.addEventListener?.('change', preferencesChanged);
  document.addEventListener('visibilitychange', render);
  window.addEventListener('popstate', () => activate(fromUrl()));
  poster?.addEventListener('error', () => { posterFailed = true; finish(); });
  poster?.addEventListener('load', () => { posterFailed = false; render(); });
  if (poster?.complete && poster.naturalWidth === 0) posterFailed = true;
  const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    inView = entries.some(e => e.isIntersecting); render();
  }, {threshold: 0.15}) : null;
  observer?.observe(stage);
  window.addEventListener('pagehide', () => {
    if (frame !== null) { cancelAnimationFrame(frame); frame = null; }
    inView = false; render(); observer?.disconnect();
  });
  window.addEventListener('pageshow', e => {
    if (!e.persisted) return;
    if (observer) observer.observe(stage); else inView = true;
    activate(fromUrl()); render();
  });
  activate(fromUrl());
})();
