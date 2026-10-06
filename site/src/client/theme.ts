/** CSS resolves system preference; explicit choices persist when storage is available. */
export function initTheme(document: Document): void {
  const select = document.querySelector<HTMLSelectElement>(
    '[data-theme-select]',
  );
  if (!select || select.dataset['ready']) return;
  select.dataset['ready'] = 'true';
  let theme = 'system';
  try {
    const stored = document.defaultView?.localStorage.getItem('notes-theme');
    if (stored && ['system', 'light', 'dark'].includes(stored)) theme = stored;
  } catch {
    /* Storage can be unavailable in a private or restricted context. */
  }
  document.documentElement.dataset['theme'] = theme;
  select.value = theme;
  const control = document.querySelector<HTMLElement>('[data-theme-control]');
  if (control) control.hidden = false;
  select.addEventListener('change', () => {
    document.documentElement.dataset['theme'] = select.value;
    try {
      document.defaultView?.localStorage.setItem('notes-theme', select.value);
    } catch {
      /* The visible choice still applies for this document. */
    }
  });
}
