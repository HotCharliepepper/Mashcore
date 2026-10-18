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
  lab.querySelectorAll('[data-layout-study]').forEach(panel => {
    const study = studies[panel.dataset.layoutStudy];
    const surface = panel.querySelector('[data-layout-surface]');
    const controls = panel.querySelector('[data-layout-controls]');
    const status = panel.querySelector('[data-layout-status]');
    if (!study || !surface || !controls || !status) return;
    const buttons = Array.from(controls.querySelectorAll('[data-layout-choice]'));
    const blocks = new Map(Array.from(surface.children).map(block => [block.dataset.layoutBlock, block]));
    function select(layout) {
      if (!study[layout] || !study[layout].every(key => blocks.has(key))) return;
      // Move the same nodes: visual and assistive reading order change together;
      // native disclosures keep their state, and the information itself does not change.
      study[layout].forEach(key => surface.append(blocks.get(key)));
      surface.dataset.layout = layout;
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.layoutChoice === layout)));
      status.textContent = study.captions[layout];
    }
    buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.layoutChoice)));
    select('a');
    controls.hidden = false;
  });
  // site.js provides the shared accessible tab behavior. No-JS documents show all studies.
  const tabs = lab.querySelector('[data-observation-tabs]');
  if (tabs) tabs.hidden = false;
})();
