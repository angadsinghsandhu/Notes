// @vitest-environment jsdom
import { beforeEach, expect, it, vi } from 'vitest';
import { initTheme } from '../../../src/client/theme.js';

beforeEach(() => {
  localStorage.clear();
  delete document.documentElement.dataset['theme'];
  document.body.innerHTML =
    '<label hidden data-theme-control>Theme<select data-theme-select><option>system</option><option>light</option><option>dark</option></select></label>';
});
it.each(['light', 'dark', 'system'])(
  'restores and persists %s theme once',
  (value) => {
    localStorage.setItem('notes-theme', value);
    initTheme(document);
    initTheme(document);
    expect(document.documentElement.dataset['theme']).toBe(value);
    const select = document.querySelector('select')!;
    expect(select.value).toBe(value);
    expect(
      document.querySelector<HTMLElement>('[data-theme-control]')!.hidden,
    ).toBe(false);
    select.value = 'dark';
    select.dispatchEvent(new Event('change'));
    expect(localStorage.getItem('notes-theme')).toBe('dark');
  },
);
it('invalid stored values use system; restricted storage still changes theme', () => {
  localStorage.setItem('notes-theme', 'invalid');
  initTheme(document);
  expect(document.documentElement.dataset['theme']).toBe('system');
  vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    throw new Error('Denied');
  });
  const select = document.querySelector('select')!;
  select.value = 'light';
  select.dispatchEvent(new Event('change'));
  expect(document.documentElement.dataset['theme']).toBe('light');
  vi.restoreAllMocks();
});
it('restricted reads use system and absent controls are harmless', () => {
  vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
    throw new Error('Denied');
  });
  initTheme(document);
  expect(document.documentElement.dataset['theme']).toBe('system');
  vi.restoreAllMocks();
  document.body.innerHTML = '';
  initTheme(document);
});
