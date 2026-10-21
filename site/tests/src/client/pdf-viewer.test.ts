// @vitest-environment jsdom
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { initPdfViewers } from '../../../src/client/pdf-viewer.js';

const mock = vi.hoisted(() => ({
  getDocument: vi.fn(),
  text: vi.fn(),
  options: {},
}));
vi.mock('pdfjs-dist', () => ({
  GlobalWorkerOptions: mock.options,
  getDocument: mock.getDocument,
  TextLayer: class {
    constructor(options: { container: HTMLElement }) {
      options.container.innerHTML = '<span>Selectable PDF text</span>';
    }
    render = mock.text;
    cancel = vi.fn();
  },
}));
const url = `/content-assets/${'a'.repeat(64)}.pdf`;
let resize: () => void;
let canvasRender: ReturnType<typeof vi.fn>;
let getPage: ReturnType<
  typeof vi.fn<
    () => Promise<{
      getViewport: (options: { scale: number }) => {
        width: number;
        height: number;
        scale: number;
        userUnit: number;
      };
      render: ReturnType<typeof vi.fn>;
      getTextContent: ReturnType<typeof vi.fn>;
      cleanup: ReturnType<typeof vi.fn>;
    }>
  >
>;
let destroy: ReturnType<typeof vi.fn>;
let loadingDestroy: ReturnType<typeof vi.fn>;
const cancels: ReturnType<typeof vi.fn>[] = [];
const flush = async () => {
  await vi.dynamicImportSettled();
  for (let i = 0; i < 15; i++) await Promise.resolve();
};
const el = <T extends Element>(selector: string) =>
  document.querySelector<T>(selector)!;
const click = async (action: string) => {
  el<HTMLButtonElement>(`[data-pdf-${action}]`).click();
  await flush();
};
function markup(asset = url) {
  document.body.innerHTML = `<section data-pdf-viewer data-pdf-url="${asset}">
  <button data-pdf-previous>Previous</button><button data-pdf-next>Next</button>
  <form><input data-pdf-page type="number"><button>Go</button></form>
  <span data-pdf-count></span><button data-pdf-out>Zoom out</button><button data-pdf-in>Zoom in</button>
  <button data-pdf-fit>Fit width</button><span data-pdf-zoom></span><button data-pdf-retry hidden>Retry</button>
  <p data-pdf-status></p><div data-pdf-viewport><div data-pdf-stage></div></div></section>`;
}
beforeEach(() => {
  vi.resetAllMocks();
  cancels.length = 0;
  markup();
  vi.stubGlobal(
    'ResizeObserver',
    class {
      constructor(callback: () => void) {
        resize = callback;
      }
      observe = vi.fn();
      disconnect = vi.fn();
    },
  );
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(
    {} as CanvasRenderingContext2D,
  );
  canvasRender = vi.fn(() => {
    const cancel = vi.fn();
    cancels.push(cancel);
    return { promise: Promise.resolve(), cancel };
  });
  getPage = vi.fn(async () => ({
    getViewport: ({ scale }: { scale: number }) => ({
      width: 600 * scale,
      height: 800 * scale,
      scale,
      userUnit: 1,
    }),
    render: canvasRender,
    getTextContent: vi.fn(async () => ({})),
    cleanup: vi.fn(),
  }));
  destroy = vi.fn(async () => {});
  loadingDestroy = vi.fn(async () => {});
  mock.getDocument.mockReturnValue({
    promise: Promise.resolve({ numPages: 3, getPage, destroy }),
    destroy,
  });
  mock.text.mockResolvedValue(undefined);
});
afterEach(() => {
  window.dispatchEvent(new Event('pagehide'));
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});
it('does nothing on notes, rejects untrusted URLs and initializes only once', async () => {
  document.body.innerHTML = '';
  initPdfViewers(document);
  expect(mock.getDocument).not.toHaveBeenCalled();
  for (const bad of [
    'https://evil.test/x.pdf',
    '/content-assets/../x.pdf',
    '//evil.test/x.pdf',
    `${url}?x=1`,
    '/content-assets/a.ppt',
  ]) {
    markup(bad);
    initPdfViewers(document);
    await flush();
    expect(el('[data-pdf-status]').textContent).toContain('unavailable');
  }
  expect(mock.getDocument).not.toHaveBeenCalled();
  markup();
  initPdfViewers(document);
  initPdfViewers(document);
  await flush();
  expect(mock.getDocument).toHaveBeenCalledTimes(1);
  expect(mock.getDocument).toHaveBeenCalledWith(
    expect.objectContaining({
      url,
      enableXfa: false,
      cMapUrl: '/pdfjs/cmaps/',
      standardFontDataUrl: '/pdfjs/standard_fonts/',
      wasmUrl: '/pdfjs/wasm/',
    }),
  );
  expect(mock.options).toEqual({ workerSrc: '/pdfjs/pdf.worker.min.mjs' });
  expect(el('[data-pdf-stage] canvas')).toBeTruthy();
  expect(el('.textLayer').textContent).toBe('Selectable PDF text');
  expect(el('[data-pdf-status]').textContent).toBe('Page 1 of 3');
});
it('navigates, validates jumps and clamps at document bounds', async () => {
  initPdfViewers(document);
  await flush();
  expect(el<HTMLButtonElement>('[data-pdf-previous]').disabled).toBe(true);
  await click('next');
  expect(getPage).toHaveBeenLastCalledWith(2);
  for (const invalid of ['0', '4', '1.5', '']) {
    el<HTMLInputElement>('[data-pdf-page]').value = invalid;
    el('form').dispatchEvent(new Event('submit', { cancelable: true }));
    await flush();
    expect(getPage).toHaveBeenLastCalledWith(2);
  }
  el<HTMLInputElement>('[data-pdf-page]').value = '3';
  el('form').dispatchEvent(new Event('submit', { cancelable: true }));
  await flush();
  expect(getPage).toHaveBeenLastCalledWith(3);
  expect(el<HTMLButtonElement>('[data-pdf-next]').disabled).toBe(true);
  await click('previous');
  expect(getPage).toHaveBeenLastCalledWith(2);
});
it('zooms, fits and rerenders on width changes with one live canvas', async () => {
  initPdfViewers(document);
  await flush();
  const width = el<HTMLCanvasElement>('canvas').width;
  await click('in');
  expect(el<HTMLCanvasElement>('canvas').width).toBeGreaterThan(width);
  await click('out');
  expect(el<HTMLCanvasElement>('canvas').width).toBe(width);
  await click('fit');
  Object.defineProperty(el('[data-pdf-viewport]'), 'clientWidth', {
    value: 300,
  });
  resize();
  await flush();
  expect(el<HTMLCanvasElement>('canvas').width).toBeLessThan(width);
  expect(document.querySelectorAll('canvas')).toHaveLength(1);
});
it('shows document and rendering failures and retries; password is a useful fallback', async () => {
  mock.getDocument.mockReturnValueOnce({
    promise: Promise.reject(
      Object.assign(new Error('password'), { name: 'PasswordException' }),
    ),
    destroy: loadingDestroy,
  });
  initPdfViewers(document);
  await flush();
  expect(el('[data-pdf-status]').textContent).toContain('password');
  expect(el<HTMLButtonElement>('[data-pdf-retry]').hidden).toBe(false);
  await click('retry');
  expect(el('[data-pdf-status]').textContent).toBe('Page 1 of 3');
  canvasRender.mockImplementationOnce(() => ({
    promise: Promise.reject(new Error('render')),
    cancel: vi.fn(),
  }));
  await click('next');
  expect(el('[data-pdf-status]').textContent).toContain('unavailable');
  await click('retry');
  expect(el('[data-pdf-status]').textContent).toBe('Page 1 of 3');
  expect(destroy).toHaveBeenCalled();
});
it('cancels superseded work, guards late pages and destroys document on teardown', async () => {
  initPdfViewers(document);
  await flush();
  let resolvePage: (
    value: Awaited<ReturnType<typeof getPage>>,
  ) => void = () => {};
  const late = await getPage();
  getPage.mockReturnValueOnce(
    new Promise((resolve) => {
      resolvePage = resolve;
    }),
  );
  await click('next');
  await click('previous');
  resolvePage(late);
  await flush();
  expect(el('[data-pdf-status]').textContent).toBe('Page 1 of 3');
  expect(cancels[0]).toHaveBeenCalled();
  window.dispatchEvent(new Event('pagehide'));
  await flush();
  expect(destroy).toHaveBeenCalled();
});
it('waits until visible before loading the heavy module and cancels an unfinished load', async () => {
  let visible: (entries: { isIntersecting: boolean }[]) => void = () => {};
  const disconnect = vi.fn();
  vi.stubGlobal(
    'IntersectionObserver',
    class {
      constructor(callback: typeof visible) {
        visible = callback;
      }
      observe = vi.fn();
      disconnect = disconnect;
    },
  );
  initPdfViewers(document);
  await flush();
  expect(mock.getDocument).not.toHaveBeenCalled();
  visible([{ isIntersecting: false }]);
  await flush();
  expect(mock.getDocument).not.toHaveBeenCalled();
  mock.getDocument.mockReturnValueOnce({
    promise: new Promise(() => {}),
    destroy: loadingDestroy,
  });
  visible([{ isIntersecting: true }]);
  await flush();
  expect(mock.getDocument).toHaveBeenCalledOnce();
  expect(disconnect).toHaveBeenCalled();
  window.dispatchEvent(new Event('pagehide'));
  await flush();
  expect(loadingDestroy).toHaveBeenCalled();
});
it('handles absent URLs and actions before the document is ready', async () => {
  el('[data-pdf-viewer]').removeAttribute('data-pdf-url');
  initPdfViewers(document);
  expect(el('[data-pdf-status]').textContent).toContain('unavailable');
  markup();
  mock.getDocument.mockReturnValueOnce({
    promise: new Promise(() => {}),
    destroy: loadingDestroy,
  });
  initPdfViewers(document);
  await click('next');
  await click('in');
  await click('fit');
  el('form').dispatchEvent(new Event('submit', { cancelable: true }));
  expect(el('[data-pdf-status]').textContent).toContain(
    'Enter a page from 1 to 1',
  );
  window.dispatchEvent(
    new PageTransitionEvent('pagehide', { persisted: true }),
  );
  expect(loadingDestroy).not.toHaveBeenCalled();
});
it('reports unavailable canvas and leaves no half-rendered page', async () => {
  vi.mocked(HTMLCanvasElement.prototype.getContext).mockReturnValueOnce(null);
  initPdfViewers(document);
  await flush();
  expect(el('[data-pdf-status]').textContent).toContain('unavailable');
  expect(document.querySelector('canvas')).toBeNull();
});
it.each(['canvas', 'content', 'text'])(
  'ignores late %s work after a newer page completes',
  async (phase) => {
    initPdfViewers(document);
    await flush();
    let release: () => void = () => {};
    const pending = new Promise<void>((resolve) => {
      release = resolve;
    });
    if (phase === 'canvas')
      canvasRender.mockReturnValueOnce({ promise: pending, cancel: vi.fn() });
    if (phase === 'text') mock.text.mockReturnValueOnce(pending);
    if (phase === 'content') {
      const late = await getPage();
      late.getTextContent.mockReturnValueOnce(pending.then(() => ({})));
      getPage.mockResolvedValueOnce(late);
    }
    await click('next');
    await click('previous');
    release();
    await flush();
    expect(el('[data-pdf-status]').textContent).toBe('Page 1 of 3');
    expect(document.querySelectorAll('canvas')).toHaveLength(1);
  },
);
it('ignores rejected stale renders and resolved or rejected document loads after closing', async () => {
  initPdfViewers(document);
  await flush();
  let rejectRender: (reason: Error) => void = () => {};
  canvasRender.mockReturnValueOnce({
    promise: new Promise((_resolve, reject) => {
      rejectRender = reject;
    }),
    cancel: vi.fn(),
  });
  await click('next');
  await click('previous');
  rejectRender(new Error('cancelled'));
  await flush();
  expect(el('[data-pdf-status]').textContent).toBe('Page 1 of 3');
  window.dispatchEvent(new Event('pagehide'));
  for (const rejection of [false, true]) {
    markup();
    let release: () => void = () => {};
    const pending = new Promise((resolve, reject) => {
      release = () =>
        rejection
          ? reject(new Error('closed'))
          : resolve({ numPages: 3, getPage });
    });
    mock.getDocument.mockReturnValueOnce({
      promise: pending,
      destroy: loadingDestroy,
    });
    initPdfViewers(document);
    await flush();
    window.dispatchEvent(new Event('pagehide'));
    release();
    await flush();
    expect(document.querySelector('canvas')).toBeNull();
  }
});
it('does not start a worker when closed during the lazy import', async () => {
  initPdfViewers(document);
  window.dispatchEvent(new Event('pagehide'));
  await flush();
  expect(mock.getDocument).not.toHaveBeenCalled();
});
it('resets reading offsets only after a different page successfully renders', async () => {
  initPdfViewers(document);
  await flush();
  const viewport = el<HTMLElement>('[data-pdf-viewport]');
  viewport.scrollTop = 137;
  viewport.scrollLeft = 89;
  await click('in');
  expect([viewport.scrollTop, viewport.scrollLeft]).toEqual([137, 89]);
  await click('next');
  expect([viewport.scrollTop, viewport.scrollLeft]).toEqual([0, 0]);
  viewport.scrollTop = 75;
  viewport.scrollLeft = 42;
  el<HTMLInputElement>('[data-pdf-page]').value = '3';
  el('form').dispatchEvent(new Event('submit', { cancelable: true }));
  await flush();
  expect([viewport.scrollTop, viewport.scrollLeft]).toEqual([0, 0]);
  viewport.scrollTop = 61;
  viewport.scrollLeft = 23;
  await click('previous');
  expect([viewport.scrollTop, viewport.scrollLeft]).toEqual([0, 0]);
});
