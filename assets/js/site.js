(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const business = window.MASHCORE_BUSINESS || {};
  const businessLabels = { companyName: '상호', representative: '대표자', registrationNumber: '사업자등록번호', address: '사업장 주소', phone: '전화' };
  document.querySelectorAll('[data-business-info]').forEach(list => {
    Object.entries(businessLabels).forEach(([key, label]) => {
      const value = typeof business[key] === 'string' ? business[key].trim() : '';
      if (!value) return;
      const row = document.createElement('div');
      const term = document.createElement('dt');
      const description = document.createElement('dd');
      term.textContent = label; description.textContent = value;
      row.append(term, description); list.append(row);
    });
    list.hidden = list.children.length === 0;
  });
  const menuButton = document.querySelector('.menu-btn');
  const menu = document.getElementById('main-nav');
  function closeMenu(returnFocus = false) {
    if (!menu || !menuButton) return;
    menu.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', '메뉴 열기');
    menuButton.textContent = '메뉴';
    if (returnFocus) menuButton.focus();
  }
  if (menu && menuButton) {
    menuButton.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
      menuButton.textContent = open ? '닫기' : '메뉴';
    });
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => closeMenu()));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && menu.classList.contains('open')) closeMenu(true);
    });
    document.addEventListener('click', e => {
      if (!e.target.closest('.site-header')) closeMenu();
    });
    menu.addEventListener('focusout', e => {
      if (e.relatedTarget && !e.relatedTarget.closest('.site-header')) closeMenu();
    });
  }
  const mobile = window.matchMedia('(max-width: 820px)');
  function responsiveTabs() {
    document.querySelectorAll('.room-tabs').forEach(el => el.setAttribute('aria-orientation', mobile.matches ? 'horizontal' : 'vertical'));
    if (!mobile.matches) closeMenu();
  }
  if (mobile.addEventListener) mobile.addEventListener('change', responsiveTabs);
  responsiveTabs();
  document.querySelectorAll('[role="tablist"]').forEach(list => {
    const tabs = Array.from(list.querySelectorAll('[role="tab"]'));
    if (!tabs.length) return;
    function select(tab, focus = false) {
      tabs.forEach(item => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
        const panel = document.getElementById(item.getAttribute('aria-controls'));
        if (panel) panel.hidden = !selected;
      });
      if (focus) tab.focus();
    }
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => select(tab));
      tab.addEventListener('keydown', e => {
        const vertical = list.getAttribute('aria-orientation') === 'vertical';
        const next = vertical ? 'ArrowDown' : 'ArrowRight';
        const prev = vertical ? 'ArrowUp' : 'ArrowLeft';
        let index;
        if (e.key === next) index = (i + 1) % tabs.length;
        if (e.key === prev) index = (i - 1 + tabs.length) % tabs.length;
        if (e.key === 'Home') index = 0;
        if (e.key === 'End') index = tabs.length - 1;
        if (index !== undefined) { e.preventDefault(); select(tabs[index], true); }
      });
    });
    select(tabs.find(x => x.getAttribute('aria-selected') === 'true') || tabs[0]);
  });
  const question = document.getElementById('question');
  if (question) {
    const status = document.getElementById('copy-status');
    const email = document.getElementById('email-question');
    const updateQuestion = () => {
      document.getElementById('question-count').textContent = question.value.length.toLocaleString('ko-KR') + ' / 1,000';
      status.textContent = '';
      if (email) email.href = 'mailto:weplace25@gmail.com?subject=' + encodeURIComponent('Mashcore Lab — 함께 보고 싶은 장면') + '&body=' + encodeURIComponent(question.value.trim());
    };
    question.addEventListener('input', updateQuestion);
    updateQuestion();
    document.getElementById('copy-question').addEventListener('click', async () => {
      const value = question.value.trim();
      if (!value) { status.textContent = '함께 보고 싶은 장면을 한 줄 적어 주세요.'; question.focus(); return; }
      try {
        if (!navigator.clipboard || !window.isSecureContext) throw new Error('Manual copy');
        await navigator.clipboard.writeText(value);
        status.textContent = '질문을 복사했습니다. 아직 전송되지 않았습니다.';
      } catch {
        question.focus(); question.select();
        status.textContent = '문장을 선택했습니다. Ctrl+C 또는 ⌘C로 복사하거나 모바일 선택 메뉴에서 복사를 누르세요.';
      }
    });
  }
  const conditionLab = document.querySelector('.condition-lab');
  if (conditionLab) {
    const readings = {
      'low-low': ['반복을 바꿀 작은 여지가 있나요?', '설명을 반복하는 사람에게 안내 한 줄을 고칠 권한과, 이후 질문을 확인할 방법이 있는지 살펴봅니다.'],
      'low-high': ['반응을 알아도, 바꿀 수 없다면 어떨까요?', '반복되는 질문을 이미 알고 있다면, 수정 제안을 누구에게 어떻게 전할 수 있는지 확인합니다. 책임과 권한이 같은 곳에 있는지도 봅니다.'],
      'high-low': ['바꾼 뒤의 반응을 만날 수 있나요?', '안내를 바꿀 수 있어도 결과를 모르면 기준을 쌓기 어렵습니다. 다음에 나온 질문 하나를 적어 두는 것부터 생각해 봅니다.'],
      'high-high': ['무엇을 기준으로 남길 수 있을까요?', '안내를 바꾼 이유와 이후 반응을 나란히 적어 봅니다. 이 조건만으로 숙련을 단정하지 않고, 무엇이 달랐는지 다시 확인합니다.']
    };
    function updateConditions() {
      const agency = conditionLab.querySelector('[name="agency"]:checked').value;
      const feedback = conditionLab.querySelector('[name="feedback"]:checked').value;
      const [title, copy] = readings[agency + '-' + feedback];
      document.getElementById('condition-title').textContent = title;
      document.getElementById('condition-question').textContent = copy;
    }
    conditionLab.querySelectorAll('input').forEach(input => input.addEventListener('change', updateConditions));
    document.getElementById('reset-conditions').addEventListener('click', () => {
      conditionLab.querySelectorAll('input').forEach(input => { input.checked = input.value === 'low'; });
      updateConditions();
    });
    updateConditions();
  }
  const progress = document.querySelector('.reading-progress');
  let frame = 0;
  function updateProgress() {
    frame = 0;
    if (!progress) return;
    const distance = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = 'scaleX(' + Math.max(0, Math.min(1, distance > 0 ? window.scrollY / distance : 0)) + ')';
  }
  const scheduleProgress = () => { if (!frame) frame = requestAnimationFrame(updateProgress); };
  window.addEventListener('scroll', scheduleProgress, { passive: true });
  window.addEventListener('resize', scheduleProgress);
  window.addEventListener('load', scheduleProgress);
  if ('ResizeObserver' in window) new ResizeObserver(scheduleProgress).observe(document.body);
  updateProgress();
})();
