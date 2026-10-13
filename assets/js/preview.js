(() => {
  'use strict';
  const frame = document.getElementById('site-preview');
  const holder = document.querySelector('.preview-frame');
  const space = document.querySelector('.preview-space');
  const open = document.getElementById('open-view');
  const buttons = Array.from(document.querySelectorAll('[data-view]'));
  const views = {
    desktop: { width: 1440, height: 960, path: '/', label: '데스크톱' },
    mobile: { width: 390, height: 844, path: '/mobile/', label: '모바일' }
  };
  let selected;
  function resize() {
    const view = views[selected];
    if (!view) return;
    const scale = Math.min(1, space.clientWidth / view.width);
    holder.style.width = (view.width * scale) + 'px';
    holder.style.height = (view.height * scale) + 'px';
    frame.style.width = view.width + 'px';
    frame.style.height = view.height + 'px';
    frame.style.transform = 'scale(' + scale + ')';
  }
  function select(name, updateURL = true) {
    selected = Object.hasOwn(views, name) ? name : 'desktop';
    const view = views[selected];
    frame.src = view.path + '?preview=' + selected;
    frame.title = 'Mashcore ' + view.label + ' 화면';
    open.href = view.path;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === selected)));
    document.getElementById('preview-caption').textContent = view.label + ' · ' + view.width + 'px';
    if (updateURL) {
      const url = new URL(window.location.href);
      url.searchParams.set('view', selected);
      window.history.replaceState(null, '', url);
    }
    resize();
  }
  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.view)));
  window.addEventListener('resize', resize);
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(space);
  select(new URL(window.location.href).searchParams.get('view'), false);
})();
