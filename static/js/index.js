'use strict';

document.documentElement.classList.add('js');

const scrollButton = document.querySelector('.scroll-to-top');
if (scrollButton) {
  const updateScrollButton = () => { scrollButton.hidden = window.scrollY <= 500; };
  window.addEventListener('scroll', updateScrollButton, { passive: true });
  scrollButton.addEventListener('click', () => {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
  });
  updateScrollButton();
}

const filters = [...document.querySelectorAll('[data-filter]')];
const conditionRows = [...document.querySelectorAll('[data-regime]')];
const conditionCount = document.getElementById('condition-count');
filters.forEach(button => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    conditionRows.forEach(row => { row.hidden = filter !== 'all' && row.dataset.regime !== filter; });
    const count = conditionRows.filter(row => !row.hidden).length;
    if (conditionCount) conditionCount.textContent = `${count} conditions · ${count * 6} in study · ${count} released`;
  });
});

document.querySelectorAll('[data-tabs]').forEach(tablist => {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const selectTab = selected => {
    tabs.forEach(tab => {
      const active = tab === selected;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      const panel = document.getElementById(tab.getAttribute('aria-controls'));
      if (panel) panel.hidden = !active;
    });
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      selectTab(tabs[next]);
      tabs[next].focus();
    });
  });
});

document.querySelectorAll('[data-copy]').forEach(button => {
  let resetTimer;
  button.addEventListener('click', async () => {
    const source = document.getElementById(button.dataset.copy);
    const status = document.getElementById('copy-status');
    if (!source) return;
    clearTimeout(resetTimer);
    try {
      await navigator.clipboard.writeText(source.textContent);
      button.textContent = 'Copied';
      if (status) status.textContent = `${button.getAttribute('aria-label').replace(/^Copy /, '')} copied to clipboard.`;
    } catch {
      const range = document.createRange();
      range.selectNodeContents(source);
      const selection = window.getSelection();
      if (selection) { selection.removeAllRanges(); selection.addRange(range); }
      button.textContent = 'Selected';
      if (status) status.textContent = 'Clipboard access unavailable. Code selected; use your keyboard copy shortcut.';
    }
    resetTimer = window.setTimeout(() => { button.textContent = 'Copy'; }, 2500);
  });
});
