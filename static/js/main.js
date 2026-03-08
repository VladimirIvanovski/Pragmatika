(function () {
  /* ── Mobile hamburger ───────────────────────────────────────── */
  const navToggle = document.getElementById('navToggle');
  const siteNav   = document.getElementById('siteNav');

  if (navToggle && siteNav) {
    navToggle.addEventListener('click', () => {
      const isOpen = siteNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close nav when a non-dropdown link is clicked (mobile)
    siteNav.querySelectorAll('a:not(.nav-link--has-drop)').forEach((link) => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 900 && siteNav.classList.contains('open')) {
          siteNav.classList.remove('open');
          navToggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  /* ── Dropdown toggle on mobile (tap) ────────────────────────── */
  document.querySelectorAll('.nav-link--has-drop').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if (window.innerWidth <= 900) {
        e.preventDefault();
        const parent = btn.closest('.nav-dropdown');
        parent.classList.toggle('open');
      }
    });
  });

  /* ── Close dropdowns when clicking outside ───────────────────── */
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-dropdown')) {
      document.querySelectorAll('.nav-dropdown.open').forEach((el) => {
        if (window.innerWidth > 900) el.classList.remove('open');
      });
    }
  });
})();
