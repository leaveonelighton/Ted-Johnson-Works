(() => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('primary-navigation');
  const more = document.querySelector('.more-works');
  if (!toggle || !nav) return;
  toggle.hidden = false;
  document.documentElement.classList.add('nav-ready');
  const closeMenu = () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (more?.open) {
      more.open = false;
      more.querySelector('summary').focus();
    } else if (nav.classList.contains('is-open')) {
      closeMenu();
      toggle.focus();
    }
  });
  document.addEventListener('click', event => {
    if (more?.open && !more.contains(event.target)) more.open = false;
  });
  window.matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);
})();
