// @vitest-environment jsdom
import { beforeEach, expect, it, vi } from 'vitest';
import { initNavigation } from '../../../src/client/navigation.js';

beforeEach(() => {
  document.body.innerHTML =
    '<button data-drawer-open hidden>Browse sections</button><dialog id="navigation-drawer"><button data-drawer-close>Close navigation</button><a href="/library/">Library</a></dialog>';
  HTMLDialogElement.prototype.showModal = vi.fn(function (
    this: HTMLDialogElement,
  ) {
    this.open = true;
  });
  HTMLDialogElement.prototype.close = vi.fn(function (this: HTMLDialogElement) {
    this.open = false;
    this.dispatchEvent(new Event('close'));
  });
});
it('enhances once, opens native modal, closes and returns focus', () => {
  initNavigation(document);
  initNavigation(document);
  const trigger =
    document.querySelector<HTMLButtonElement>('[data-drawer-open]')!;
  const dialog = document.querySelector('dialog')!;
  expect(trigger.hidden).toBe(false);
  trigger.click();
  expect(dialog.showModal).toHaveBeenCalledTimes(1);
  document.querySelector<HTMLButtonElement>('[data-drawer-close]')!.click();
  expect(dialog.open).toBe(false);
  expect(document.activeElement).toBe(trigger);
});
it('native close (including Escape) returns focus; absent controls are harmless', () => {
  initNavigation(document);
  const trigger =
    document.querySelector<HTMLButtonElement>('[data-drawer-open]')!;
  trigger.click();
  document.querySelector('dialog')!.close();
  expect(document.activeElement).toBe(trigger);
  document.body.innerHTML = '';
  expect(() => initNavigation(document)).not.toThrow();
});

it('opens and highlights only a matching published folder from the shared-tree URL', () => {
  window.history.replaceState(
    {},
    '',
    '/library/tree/?current=%2Flibrary%2Fbooks%2F',
  );
  document.body.insertAdjacentHTML(
    'beforeend',
    '<details><summary>Books</summary><a id="folder-/library/books/" data-folder-route href="/library/books/">Books</a></details>',
  );
  initNavigation(document);
  expect(document.querySelector('details')!.open).toBe(true);
  expect(
    document
      .getElementById('folder-/library/books/')!
      .getAttribute('aria-current'),
  ).toBe('location');
  window.history.replaceState({}, '', '/library/tree/?current=missing');
  expect(() => initNavigation(document)).not.toThrow();
  window.history.replaceState({}, '', '/');
});

it('scrolls to a published current folder and ignores matching non-folder elements', () => {
  window.history.replaceState({}, '', '/library/tree/?current=selected');
  document.body.insertAdjacentHTML(
    'beforeend',
    '<a id="folder-selected" data-folder-route>Selected</a>',
  );
  const selected = document.getElementById('folder-selected')!;
  selected.scrollIntoView = vi.fn();
  initNavigation(document);
  expect(selected.scrollIntoView).toHaveBeenCalledWith({ block: 'center' });
  selected.removeAttribute('data-folder-route');
  selected.removeAttribute('aria-current');
  initNavigation(document);
  expect(selected.hasAttribute('aria-current')).toBe(false);
  window.history.replaceState({}, '', '/');
});
