/* Additive R3 hero comparison. No analytics, autoplay triggers or user input persistence. */
(() => {
  'use strict';
  const root = document.querySelector('[data-hero-experience]');
  if (!root) return;
  const bar = root.querySelector('[data-hero-mode-controls]');
  const buttons = [...root.querySelectorAll('[data-hero-mode-choice]')];
  const status = root.querySelector('[data-hero-variant-status]');
  if (!bar || !status || buttons.length !== 2) return;
  const validModes = ['default', 'reverse'];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const saveData = Boolean(navigator.connection && navigator.connection.saveData);
  if (saveData) root.dataset.heroReduced = 'true';
  let frame = null;
  function fromUrl() {
    const requested = new URLSearchParams(window.location.search).get('hero');
    return requested === 'reverse' ? 'reverse' : 'default';
  }
  function activate(mode, updateUrl = false) {
    if (!validModes.includes(mode)) return;
    root.dataset.heroMode = mode;
    root.classList.remove('hero-reverse-replay');
    if (frame !== null) cancelAnimationFrame(frame);
    buttons.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.heroModeChoice === mode));
    });
    status.textContent = mode === 'reverse'
      ? 'B 구성: 오른쪽 장면의 신호를 왼쪽 질문까지 거슬러 살핍니다. 제목과 서비스 링크는 A와 같습니다.'
      : 'A 구성: 기존 R2 히어로를 보고 있습니다. 제목과 서비스 링크는 B와 같습니다.';
    bar.hidden = false;
    if (mode === 'reverse' && !reduced.matches && !saveData) {
      frame = requestAnimationFrame(() => {
        if (root.dataset.heroMode === 'reverse') root.classList.add('hero-reverse-replay');
        frame = null;
      });
    }
    if (updateUrl) {
      const url = new URL(window.location.href);
      if (mode === 'reverse') url.searchParams.set('hero', 'reverse');
      else url.searchParams.delete('hero');
      history.replaceState(history.state, '', url.pathname + url.search + url.hash);
    }
  }
  for (const button of buttons) {
    button.addEventListener('click', () => activate(button.dataset.heroModeChoice, true));
  }
  window.addEventListener('popstate', () => activate(fromUrl()));
  reduced.addEventListener('change', () => activate(root.dataset.heroMode));
  activate(fromUrl());
})();
