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
