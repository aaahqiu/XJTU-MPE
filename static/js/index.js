'use strict';

const scrollButton = document.querySelector('.scroll-to-top');

if (scrollButton) {
  const updateScrollButton = () => {
    scrollButton.classList.toggle('visible', window.scrollY > 300);
  };
  window.addEventListener('scroll', updateScrollButton, { passive: true });
  scrollButton.addEventListener('click', () => {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
  });
  updateScrollButton();
}
