/* Progressive enhancement. All reading and native controls survive script failure. */
(() => {
  'use strict';
  const $ = (selector) => document.querySelector(selector);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const video = $('#origin-video');
  const videoToggle = $('#video-toggle');
  const media = $('.origin-media');
  const videoStatus = $('#video-status');
  let playRequest = 0;
  let pending = false;

  function stopVideo(message = '') {
    playRequest += 1;
    pending = false;
    video.pause();
    media.classList.remove('is-playing');
    videoToggle.textContent = '장면 재생';
    videoToggle.setAttribute('aria-pressed', 'false');
    videoToggle.removeAttribute('aria-busy');
    videoStatus.textContent = message;
  }
  videoToggle.addEventListener('click', async () => {
    if (reduced.matches) return;
    if (pending || !video.paused) { stopVideo(); return; }
    const request = ++playRequest;
    pending = true;
    videoToggle.textContent = '불러오기 취소';
    videoToggle.setAttribute('aria-busy', 'true');
    videoStatus.textContent = '장면을 불러오는 중입니다.';
    if (!video.getAttribute('src')) video.src = video.dataset.src;
    try {
      await video.play();
      if (request !== playRequest) {
        if (!pending && videoToggle.getAttribute('aria-pressed') !== 'true') video.pause();
        return;
      }
      pending = false;
      media.classList.add('is-playing');
      videoToggle.removeAttribute('aria-busy');
      videoToggle.textContent = '장면 멈추기';
      videoToggle.setAttribute('aria-pressed', 'true');
      videoStatus.textContent = '';
    } catch {
      if (request !== playRequest) return;
      stopVideo('영상을 재생하지 못했습니다. 정지 장면으로 살펴보거나 다시 재생해 보세요.');
      video.removeAttribute('src');
      video.load();
    }
  });
  video.addEventListener('ended', () => stopVideo());
  video.addEventListener('error', () => {
    if (pending || !video.paused) stopVideo('영상을 불러오지 못했습니다. 정지 장면으로 계속 살펴볼 수 있습니다.');
    video.removeAttribute('src');
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopVideo(); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) stopVideo();
    }, { threshold: 0.1 }).observe(media);
  }

  const hypothesisStatus = $('#hypothesis-status');
  document.querySelectorAll('input[name=hypothesis]').forEach((input) => {
    input.addEventListener('change', () => {
      const reading = document.getElementById(input.getAttribute('aria-controls'));
      hypothesisStatus.textContent = `${input.closest('label').querySelector('span').childNodes[0].textContent.trim()} 선택했습니다. 정답이 아닌 가설입니다. ${reading.textContent}`;
    });
  });

  const traceToggle = $('#trace-toggle');
  const traceStatus = $('#trace-status');
  const board = $('#gaze-board');
  const items = [...board.querySelectorAll('.gaze-item')];
  let trace = null;
  function clearTrace() {
    trace?.kill();
    trace = null;
    items.forEach((item) => { item.querySelector('.order-number').style.opacity = ''; });
    board.classList.remove('tracing');
    traceToggle.setAttribute('aria-pressed', 'false');
    traceToggle.textContent = '읽기 순서 예시 보기';
    traceStatus.textContent = '실제 시선 추적이 아닌, 설계한 읽기 순서의 예시입니다.';
  }
  traceToggle.addEventListener('click', (event) => {
    if (board.classList.contains('tracing')) { clearTrace(); return; }
    board.classList.add('tracing');
    traceToggle.setAttribute('aria-pressed', 'true');
    traceToggle.textContent = '읽기 순서 예시 닫기';
    traceStatus.textContent = '예시 순서: 예약 여부 → 성함 → 안내 장소. 실제로 읽은 순서는 사람마다 다를 수 있습니다.';
    // Only this explicit explanatory sequence uses GSAP. Keyboard and reduced
    // motion immediately show the same numbered, fully readable static result.
    if (!reduced.matches && event.detail !== 0 && window.gsap) {
      trace = window.gsap.timeline({ onComplete: () => { trace = null; } });
      items.forEach((item) => {
        const number = item.querySelector('.order-number');
        trace.to(number, { opacity: 0.35, duration: 0.18, ease: 'power2.out' })
          .to(number, { opacity: 1, duration: 0.35, ease: 'power2.out' });
      });
    }
  });
  document.querySelectorAll('input[name=layout]').forEach((input) => input.addEventListener('change', clearTrace));
  $('#control-form').addEventListener('change', () => {
    $('#control-status').textContent = `현재 선택: ${$('input[name=detail]:checked').value === 'full' ? '자세히 읽기' : '짧게 읽기'}. 선택은 이 화면에서만 유지됩니다.`;
  });
  $('#control-form').addEventListener('reset', () => {
    $('#control-status').textContent = '처음 선택인 짧게 읽기로 돌아왔습니다.';
  });
  function applyMotionPreference() {
    stopVideo();
    clearTrace();
    videoToggle.hidden = reduced.matches;
    if (reduced.matches) videoStatus.textContent = '동작 줄이기 설정에 따라 정지 장면을 보여 드립니다.';
  }
  reduced.addEventListener('change', applyMotionPreference);
  applyMotionPreference();
  traceToggle.hidden = false;
  $('#control-status').hidden = false;
  document.documentElement.classList.add('enhanced');
})();
