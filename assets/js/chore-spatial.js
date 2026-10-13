/* Progressive enhancement: a qualitative concept model, never a score or physics claim. */
(() => {
  'use strict';
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
  const angleDifference = (value, origin) => ((value - origin + 540) % 360) - 180;
  document.querySelectorAll('[data-spatial]').forEach(root => {
    if (root.dataset.spatialReady === 'true') return;
    const stage = root.querySelector('[data-spatial-stage]');
    const world = root.querySelector('[data-spatial-world]');
    const buttons = Array.from(root.querySelectorAll('[data-spatial-select]'));
    const nodes = Array.from(root.querySelectorAll('[data-spatial-node]'));
    const title = root.querySelector('[data-spatial-heading]');
    const copy = root.querySelector('[data-spatial-description]');
    const sensorButton = root.querySelector('[data-spatial-sensor-button]');
    const status = root.querySelector('[data-spatial-status]');
    const resetButton = root.querySelector('[data-spatial-reset]');
    const turnButtons = Array.from(root.querySelectorAll('[data-spatial-turn]'));
    if (!stage || !world || !buttons.length || !title || !copy || !sensorButton || !status || !resetButton) return;
    const motionQuery = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
    const cleanups = [];
    const listen = (element, name, callback, options) => {
      element.addEventListener(name, callback, options);
      cleanups.push(() => element.removeEventListener(name, callback, options));
    };
    let reduced = motionQuery.matches;
    let pitch = -8;
    let yaw = 0;
    let frame = 0;
    let pointer = null;
    let dragged = false;
    let sensorActive = false;
    let sensorPending = false;
    let sensorTimer = 0;
    let sensorToken = 0;
    let baseline = null;
    let disposed = false;
    const fallback = '좌우로 밀거나 방향 버튼으로 시점을 바꿀 수 있습니다.';
    const say = message => { status.textContent = message; };
    function paint() {
      frame = 0;
      world.style.setProperty('--sp-pitch', pitch.toFixed(2) + 'deg');
      world.style.setProperty('--sp-yaw', yaw.toFixed(2) + 'deg');
    }
    function render() {
      if (!frame) frame = window.requestAnimationFrame(paint);
    }
    function select(key) {
      const selected = buttons.find(button => button.dataset.spatialSelect === key);
      if (!selected) return;
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button === selected)));
      nodes.forEach(node => node.classList.toggle('is-selected', node.dataset.spatialNode === key));
      title.textContent = selected.dataset.spatialTitle;
      copy.textContent = selected.dataset.spatialCopy;
      root.dataset.spatialSelected = key;
    }
    function stopSensor(message) {
      sensorToken += 1;
      sensorActive = false;
      sensorPending = false;
      baseline = null;
      window.clearTimeout(sensorTimer);
      sensorTimer = 0;
      window.removeEventListener('deviceorientation', onOrientation);
      root.dataset.spatialSensor = 'false';
      sensorButton.setAttribute('aria-pressed', 'false');
      sensorButton.disabled = reduced;
      sensorButton.textContent = '기울기로 살펴보기';
      if (message) say(message);
    }
    function reset(message = true) {
      stopSensor();
      pitch = -8; yaw = 0;
      render();
      if (message) say(reduced ? '움직임을 줄인 보기입니다. 아래에서 관점을 고를 수 있습니다.' : '원래 시점으로 돌아왔습니다. ' + fallback);
    }
    function rotate(amount, vertical = false) {
      if (reduced) return;
      if (sensorActive || sensorPending) say('버튼으로 시점을 바꿉니다. 기울기 반응은 껐습니다.');
      stopSensor();
      if (vertical) pitch = clamp(pitch + amount, -28, 15);
      else yaw = clamp(yaw + amount, -32, 32);
      render();
    }
    function onOrientation(event) {
      if (!sensorActive || reduced || document.hidden || !Number.isFinite(event.beta) || !Number.isFinite(event.gamma)) return;
      if (!baseline) {
        baseline = { beta: event.beta, gamma: event.gamma };
        window.clearTimeout(sensorTimer);
        sensorTimer = 0;
        say('현재 휴대폰 각도가 기준입니다. 가볍게 기울여 보세요.');
      }
      const orientation = window.screen && window.screen.orientation;
      const screenAngle = orientation && Number.isFinite(orientation.angle) ? orientation.angle : Number(window.orientation) || 0;
      const radians = screenAngle * Math.PI / 180;
      const horizontal = angleDifference(event.gamma, baseline.gamma);
      const vertical = angleDifference(event.beta, baseline.beta);
      yaw = clamp((horizontal * Math.cos(radians) + vertical * Math.sin(radians)) * .6, -24, 24);
      pitch = clamp(-8 - (vertical * Math.cos(radians) - horizontal * Math.sin(radians)) * .4, -23, 7);
      render();
    }
    async function toggleSensor() {
      if (sensorActive || sensorPending) { stopSensor('기울기 반응을 껐습니다. ' + fallback); return; }
      if (reduced) { say('기기의 움직임 줄이기 설정을 따르고 있습니다. 관점 버튼을 이용해 주세요.'); return; }
      if (!window.isSecureContext || !window.DeviceOrientationEvent) {
        say('이 환경에서는 기울기를 사용할 수 없습니다. ' + fallback);
        return;
      }
      const token = ++sensorToken;
      sensorPending = true;
      sensorButton.disabled = true;
      sensorButton.textContent = '기울기 확인 중';
      try {
        // Keep this permission request directly within the explicit click gesture.
        const permission = typeof window.DeviceOrientationEvent.requestPermission === 'function'
          ? await window.DeviceOrientationEvent.requestPermission() : 'granted';
        if (disposed || token !== sensorToken || reduced || document.hidden) return;
        if (permission !== 'granted') { stopSensor('기울기 접근이 허용되지 않았습니다. ' + fallback); return; }
        sensorPending = false;
        sensorActive = true;
        baseline = null;
        sensorButton.disabled = false;
        sensorButton.textContent = '기울기 끄기';
        sensorButton.setAttribute('aria-pressed', 'true');
        root.dataset.spatialSensor = 'true';
        window.addEventListener('deviceorientation', onOrientation, { passive: true });
        say('휴대폰을 편한 각도로 잡아 주세요.');
        sensorTimer = window.setTimeout(() => {
          if (sensorActive && !baseline) stopSensor('기울기 신호를 받지 못했습니다. ' + fallback);
        }, 4000);
      } catch {
        if (token === sensorToken && !disposed) stopSensor('기울기를 연결하지 못했습니다. ' + fallback);
      }
    }
    function releasePointer() {
      if (pointer && stage.hasPointerCapture && stage.hasPointerCapture(pointer.id)) stage.releasePointerCapture(pointer.id);
      pointer = null;
      root.dataset.spatialDragging = 'false';
    }
    listen(stage, 'pointerdown', event => {
      if (reduced || event.isPrimary === false || (event.pointerType === 'mouse' && event.button !== 0)) return;
      if (sensorActive || sensorPending) say('손으로 시점을 바꿉니다. 기울기 반응은 껐습니다.');
      stopSensor();
      dragged = false;
      pointer = { id: event.pointerId, x: event.clientX, y: event.clientY, yaw, pitch, touch: event.pointerType === 'touch' };
      // No preventDefault: vertical panning and pinch zoom remain browser-owned.
    });
    listen(stage, 'pointermove', event => {
      if (!pointer || pointer.id !== event.pointerId) return;
      const dx = event.clientX - pointer.x;
      const dy = event.clientY - pointer.y;
      if (!dragged && Math.abs(dx) < 6 && Math.abs(dy) < 6) return;
      if (pointer.touch && !dragged && Math.abs(dy) > Math.abs(dx)) { releasePointer(); return; }
      if (!dragged) {
        dragged = true;
        root.dataset.spatialDragging = 'true';
        if (stage.setPointerCapture) stage.setPointerCapture(event.pointerId);
      }
      yaw = clamp(pointer.yaw + dx * .18, -32, 32);
      if (!pointer.touch) pitch = clamp(pointer.pitch - dy * .12, -28, 15);
      render();
    });
    listen(stage, 'pointerup', releasePointer);
    listen(stage, 'pointercancel', releasePointer);
    listen(stage, 'pointerleave', () => { if (pointer && !dragged) releasePointer(); });
    listen(stage, 'lostpointercapture', () => { pointer = null; root.dataset.spatialDragging = 'false'; });
    listen(stage, 'click', event => {
      if (dragged) { dragged = false; return; }
      const node = event.target.closest('[data-spatial-node]');
      if (node) select(node.dataset.spatialNode);
    });
    listen(stage, 'keydown', event => {
      if (reduced) return;
      const movements = { ArrowLeft: [-8, false], ArrowRight: [8, false], ArrowUp: [-6, true], ArrowDown: [6, true] };
      if (movements[event.key]) { event.preventDefault(); rotate(...movements[event.key]); }
      if (event.key === 'Home') { event.preventDefault(); reset(); }
    });
    buttons.forEach(button => listen(button, 'click', () => select(button.dataset.spatialSelect)));
    turnButtons.forEach(button => listen(button, 'click', () => rotate(Number(button.dataset.spatialTurn) * 8)));
    listen(resetButton, 'click', () => reset());
    listen(sensorButton, 'click', toggleSensor);
    const changeScreen = () => {
      baseline = null;
      if (sensorActive) { pitch = -8; yaw = 0; render(); say('바뀐 화면 방향에 맞춰 기울기 기준을 다시 잡습니다.'); }
    };
    if (window.screen && window.screen.orientation && window.screen.orientation.addEventListener) listen(window.screen.orientation, 'change', changeScreen);
    else listen(window, 'orientationchange', changeScreen);
    listen(document, 'visibilitychange', () => {
      if (document.hidden) { releasePointer(); if (sensorActive || sensorPending) stopSensor('기울기 반응이 멈췄습니다. 필요할 때 다시 켜 주세요.'); }
    });
    listen(window, 'pagehide', () => { stopSensor(); releasePointer(); if (frame) window.cancelAnimationFrame(frame); frame = 0; });
    const updateMotion = () => {
      reduced = motionQuery.matches;
      root.dataset.spatialReduced = String(reduced);
      stage.tabIndex = reduced ? -1 : 0;
      turnButtons.forEach(button => { button.disabled = reduced; });
      resetButton.disabled = reduced;
      sensorButton.disabled = reduced;
      reset(false);
      say(reduced ? '움직임을 줄인 보기입니다. 관점 버튼으로 내용을 살펴보세요.' : fallback);
    };
    if (motionQuery.addEventListener) listen(motionQuery, 'change', updateMotion);
    else if (motionQuery.addListener) { motionQuery.addListener(updateMotion); cleanups.push(() => motionQuery.removeListener(updateMotion)); }
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        if (!entries[0].isIntersecting && (sensorActive || sensorPending)) stopSensor('기울기 반응이 멈췄습니다. 필요할 때 다시 켜 주세요.');
      });
      observer.observe(root);
      cleanups.push(() => observer.disconnect());
    }
    listen(root, 'mashcore:spatial-destroy', () => {
      disposed = true; stopSensor(); releasePointer();
      if (frame) window.cancelAnimationFrame(frame);
      cleanups.forEach(cleanup => cleanup());
      delete root.dataset.spatialReady;
    });
    root.dataset.spatialReady = 'true';
    const controls = root.querySelector('[data-spatial-controls]');
    if (controls) controls.hidden = false;
    select((buttons.find(button => button.getAttribute('aria-pressed') === 'true') || buttons[0]).dataset.spatialSelect);
    updateMotion();
  });
})();
