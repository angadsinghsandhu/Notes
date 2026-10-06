/** Native modal owns focus trapping and Escape; close restores the trigger. */
export function initNavigation(document: Document): void {
  const trigger =
    document.querySelector<HTMLButtonElement>('[data-drawer-open]');
  const dialog =
    document.querySelector<HTMLDialogElement>('#navigation-drawer');
  if (!trigger || !dialog || trigger.dataset['ready']) return;
  trigger.dataset['ready'] = 'true';
  trigger.hidden = false;
  document.documentElement.classList.add('navigation-enhanced');
  trigger.addEventListener('click', () => dialog.showModal());
  dialog
    .querySelector('[data-drawer-close]')
    ?.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => trigger.focus());
}
