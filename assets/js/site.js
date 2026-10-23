(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const business = window.MASHCORE_BUSINESS || {};
  const businessLabels = { companyName: '상호', representative: '대표자', registrationNumber: '사업자등록번호', address: '사업장 주소', phone: '전화', email: '이메일' };
  document.querySelectorAll('[data-business-info]').forEach(list => {
    // Build-time public details are authoritative and remain readable if config fails.
    if (list.children.length) { list.hidden = false; return; }
    Object.entries(businessLabels).forEach(([key, label]) => {
      const value = typeof business[key] === 'string' ? business[key].trim() : '';
      if (!value) return;
      const row = document.createElement('div');
      const term = document.createElement('dt');
      const description = document.createElement('dd');
      term.textContent = label;
      if (key === 'email') {
        const link = document.createElement('a');
        link.setAttribute('href', `mailto:${value}`);
        link.textContent = value;
        description.append(link);
      } else description.textContent = value;
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
      if (!open) menuButton.focus();
    });
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => closeMenu(true)));
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
    if (list.hasAttribute('data-observation-tabs')) return;
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
    const error = document.getElementById('question-error');
    const counter = document.getElementById('question-count');
    const email = document.getElementById('email-question');
    const copyButton = document.getElementById('copy-question');
    const selectButton = document.getElementById('select-question');
    const recipient = typeof business.email === 'string' && business.email.trim() ? business.email.trim() : 'weplacehyun@naver.com';
    const baseMail = 'mailto:' + recipient + '?subject=' + encodeURIComponent('[Mashcore] 함께할 일 문의');
    const limit = 1000;
    let composing = false;
    // Count Unicode code points consistently; never trim, truncate, or rewrite input.
    const length = () => Array.from(question.value).length;
    const notify = message => { if (status) status.textContent = message; };
    const overflowMessage = '1,000자 이내로 줄여주세요. 작성한 내용은 입력란에 남아 있습니다. 내용을 직접 선택해 복사하거나 아래 이메일로 보내실 수 있습니다.';
    question.removeAttribute('maxlength');
    function updateQuestion() {
      const over = length() > limit;
      if (counter) counter.textContent = length().toLocaleString('ko-KR') + ' / 1,000';
      question.setAttribute('aria-invalid', String(over));
      if (error) error.textContent = over ? overflowMessage : '';
      if (email) {
        email.setAttribute('aria-disabled', String(over));
        email.href = baseMail + (!over && question.value.trim() ? '&body=' + encodeURIComponent(question.value) : '');
      }
      if (copyButton) copyButton.setAttribute('aria-disabled', String(over));
      if (over && !error) notify(overflowMessage);
      return !over;
    }
    function canUseQuestion() {
      if (composing) { notify('한글 입력을 마친 뒤 다시 눌러주세요.'); return false; }
      if (!updateQuestion()) { notify(overflowMessage); return false; }
      return true;
    }
    question.addEventListener('compositionstart', () => { composing = true; });
    question.addEventListener('compositionend', () => { composing = false; updateQuestion(); });
    question.addEventListener('input', () => { notify(''); updateQuestion(); });
    if (email) email.addEventListener('click', event => {
      if (!canUseQuestion()) { event.preventDefault(); return; }
      notify('메일 앱에서 내용을 확인한 뒤 직접 보내주세요. 메일 앱이 열리지 않으면 질문을 복사해 아래 주소로 보내주세요.');
    });
    if (copyButton) {
      copyButton.hidden = false;
      copyButton.addEventListener('click', async () => {
        if (!canUseQuestion()) return;
        const value = question.value;
        if (!value.trim()) { notify('복사할 내용을 먼저 적어주세요.'); question.focus(); return; }
        try {
          if (!navigator.clipboard || !window.isSecureContext) throw new Error('Manual copy');
          notify('복사를 시도하고 있습니다. 응답이 없으면 내용을 직접 선택해 복사해 주세요.');
          await navigator.clipboard.writeText(value);
          notify('질문을 복사했습니다. 아직 전송되지 않았습니다.');
        } catch {
          question.focus(); question.select();
          notify('자동 복사가 되지 않았습니다. 내용을 선택해 직접 복사해 주세요. Ctrl+C 또는 ⌘C, 모바일 선택 메뉴의 복사를 사용할 수 있습니다.');
        }
      });
    }
    if (selectButton) {
      selectButton.hidden = false;
      selectButton.addEventListener('click', () => {
        question.focus(); question.select();
        notify('내용을 선택했습니다. Ctrl+C 또는 ⌘C, 모바일 선택 메뉴에서 직접 복사해 주세요. 아직 전송되지 않았습니다.');
      });
    }
    updateQuestion();
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
