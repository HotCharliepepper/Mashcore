(() => {
  'use strict';
  const lab = document.querySelector('[data-observation-lab]');
  if (!lab) return;

  // A/B are two arrangements to inspect, not measured winners. No data is stored or sent.
  const studies = {
    hand: {
      a: ['action', 'intro', 'context'], b: ['intro', 'context', 'action'],
      captions: { a: '배치 A · 안내를 여는 동작이 먼저 보입니다.', b: '배치 B · 내용을 읽은 뒤 안내를 열 수 있습니다.' }
    },
    reading: {
      a: ['intro', 'price', 'context', 'included'], b: ['intro', 'price', 'included', 'context'],
      captions: { a: '배치 A · 요금과 포함 항목 사이에 다른 안내가 있습니다.', b: '배치 B · 요금 바로 다음에 포함 항목이 놓여 있습니다.' }
    },
    decision: {
      a: ['intro', 'action', 'conditions'], b: ['intro', 'conditions', 'action'],
      captions: { a: '배치 A · 예약 방법 뒤에 이용 조건이 놓여 있습니다.', b: '배치 B · 이용 조건을 확인한 뒤 예약 방법을 살펴봅니다.' }
    }
  };
  const panels = Array.from(lab.querySelectorAll('[data-layout-study]'));
  const tabs = lab.querySelector('[data-observation-tabs]');
  if (!tabs || panels.length !== Object.keys(studies).length) return;
  const choices = Array.from(tabs.querySelectorAll('button[aria-controls]'));
  const prepared = panels.map(panel => {
    const study = studies[panel.dataset.layoutStudy];
    const surface = panel.querySelector('[data-layout-surface]');
    const controls = panel.querySelector('[data-layout-controls]');
    const status = panel.querySelector('[data-layout-status]');
    if (!study || !surface || !controls || !status) return null;
    const buttons = Array.from(controls.querySelectorAll('[data-layout-choice]'));
    const blocks = new Map(Array.from(surface.children).map(block => [block.dataset.layoutBlock, block]));
    if (!study.a.every(key => blocks.has(key)) || !study.b.every(key => blocks.has(key)) || buttons.length !== 2) return null;
    return { panel, study, surface, controls, status, buttons, blocks };
  });
  // No partial enhancement: a missing script/marker leaves every static A/B readable.
  if (prepared.some(item => !item) || choices.length !== panels.length ||
      !choices.every(button => panels.some(panel => panel.id === button.getAttribute('aria-controls')))) return;
  prepared.forEach(({ panel, study, surface, controls, status, buttons, blocks }) => {
    function select(layout) {
      if (!study[layout]) return;
      // Move the same nodes so reading order and visual order stay identical.
      // Disclosure state and all original information are preserved.
      study[layout].forEach(key => surface.append(blocks.get(key)));
      surface.dataset.layout = layout;
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.layoutChoice === layout)));
      status.textContent = study.captions[layout];
    }
    buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.layoutChoice)));
    select('a');
    controls.hidden = false;
    panel.removeAttribute('tabindex');
    panel.setAttribute('role', 'region');
  });
  tabs.setAttribute('role', 'group');
  choices.forEach(button => {
    button.removeAttribute('role');
    button.removeAttribute('aria-selected');
    button.tabIndex = 0;
  });
  function choose(button, focus = false) {
    choices.forEach(choice => choice.setAttribute('aria-pressed', String(choice === button)));
    panels.forEach(panel => { panel.hidden = panel.id !== button.getAttribute('aria-controls'); });
    if (focus) button.focus();
  }
  choices.forEach((button, index) => {
    button.addEventListener('click', () => choose(button));
    button.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % choices.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + choices.length) % choices.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = choices.length - 1;
      if (next !== undefined) { event.preventDefault(); choose(choices[next], true); }
    });
  });
  choose(choices[0]);
  lab.querySelectorAll('[data-layout-fallback]').forEach(fallback => { fallback.hidden = true; });
  lab.dataset.observationReady = 'true';
  tabs.hidden = false;
})();
