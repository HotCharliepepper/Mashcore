(() => {
  'use strict';
  const chapters = Array.from(document.querySelectorAll('[data-chapter]'));
  if (!chapters.length) return;
  // Keep shared links to the former long homepage useful.
  if (['#way', '#rooms', '#archive'].includes(window.location.hash)) {
    window.location.replace('/explore/' + window.location.hash);
    return;
  }
  const links = Array.from(document.querySelectorAll('.chapter-index a'));
  let active = null;
  function activate(chapter) {
    if (!chapter || active === chapter) return;
    active = chapter;
    chapters.forEach(item => item.classList.toggle('is-active', item === chapter));
    links.forEach(link => {
      if (link.hash === '#' + chapter.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  // Native scrolling: no wheel, touchmove, or keyboard interception.
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) activate(entry.target); });
    }, { rootMargin: '-18% 0px -55% 0px', threshold: 0 });
    chapters.forEach(chapter => observer.observe(chapter));
    document.documentElement.classList.add('chapters-ready');
    window.addEventListener('pagehide', () => observer.disconnect(), { once: true });
    window.addEventListener('pageshow', event => {
      if (event.persisted) chapters.forEach(chapter => observer.observe(chapter));
    });
  }
  document.addEventListener('focusin', event => {
    const chapter = event.target.closest('[data-chapter]');
    if (chapter) activate(chapter);
  });
})();
