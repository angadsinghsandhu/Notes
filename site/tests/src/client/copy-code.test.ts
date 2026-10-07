// @vitest-environment jsdom
import { beforeEach, expect, it, vi } from 'vitest';
import { initCopyCode } from '../../../src/client/copy-code.js';

beforeEach(() => {
  document.body.innerHTML =
    '<div><pre><code>&lt;script&gt;literal&lt;/script&gt;</code></pre></div>';
});
it('adds one button, copies visible source and reports success', async () => {
  const writeText = vi.fn().mockResolvedValue(undefined);
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value: { writeText },
  });
  initCopyCode(document);
  initCopyCode(document);
  expect(document.querySelectorAll('button')).toHaveLength(1);
  document.querySelector('button')!.click();
  await vi.waitFor(() =>
    expect(document.querySelector('[role="status"]')?.textContent).toBe(
      'Code copied.',
    ),
  );
  expect(writeText).toHaveBeenCalledWith('<script>literal</script>');
});
it.each([false, true])(
  'reports clipboard failure and permits retry, unavailable=%s',
  async (unavailable) => {
    const writeText = vi.fn().mockRejectedValue(new Error('Denied'));
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: unavailable ? undefined : { writeText },
    });
    initCopyCode(document);
    const button = document.querySelector('button')!;
    button.click();
    await vi.waitFor(() =>
      expect(document.querySelector('[role="status"]')?.textContent).toContain(
        'select the code',
      ),
    );
    expect(button.disabled).toBe(false);
  },
);
it('handles documents without code blocks', () => {
  document.body.innerHTML = '';
  expect(() => initCopyCode(document)).not.toThrow();
});

it('copies an actual empty Element as empty text and handles a detached document without a view', async () => {
  const writeText = vi.fn().mockResolvedValue(undefined);
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value: { writeText },
  });
  document.body.innerHTML = '<pre></pre>';
  expect(document.querySelector('pre')!.textContent).toBe('');
  initCopyCode(document);
  document.querySelector('button')!.click();
  await vi.waitFor(() => expect(writeText).toHaveBeenCalledWith(''));
  const detached = document.implementation.createHTMLDocument();
  detached.body.innerHTML = '<pre>Detached source</pre>';
  expect(detached.defaultView).toBeNull();
  initCopyCode(detached);
  detached.querySelector('button')!.click();
  await vi.waitFor(() =>
    expect(detached.querySelector('[role="status"]')!.textContent).toContain(
      'Copy failed',
    ),
  );
});
