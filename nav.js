(function () {
  var nav = document.querySelector('.site-nav');
  if (!nav) return;

  function onScroll() {
    if (window.scrollY > 50) {
      nav.classList.add('nav-scrolled');
    } else {
      nav.classList.remove('nav-scrolled');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}());
