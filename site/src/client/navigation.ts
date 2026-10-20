/** Native modal owns focus trapping and Escape; close restores the trigger. */
export function initNavigation(document: Document): void {
  const current = new URL(document.URL).searchParams.get('current');
  const active = current ? document.getElementById(`folder-${current}`) : null;
  if (active?.hasAttribute('data-folder-route')) {
    active.setAttribute('aria-current', 'location');
    let branch = active.parentElement;
    while (branch) {
      if (branch instanceof HTMLDetailsElement) branch.open = true;
      branch = branch.parentElement;
    }
    active.scrollIntoView?.({ block: 'center' });
  }
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
