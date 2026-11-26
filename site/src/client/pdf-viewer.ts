import type {
  PDFDocumentLoadingTask,
  PDFDocumentProxy,
  PDFPageProxy,
  RenderTask,
  TextLayer,
} from 'pdfjs-dist';

/** Only content-addressed local PDFs prepared by the publication pipeline are trusted. */
export function initPdfViewers(document: Document): void {
  for (const root of document.querySelectorAll<HTMLElement>(
    '[data-pdf-viewer]',
  )) {
    if (root.dataset['ready']) continue;
    root.dataset['ready'] = 'true';
    const find = <T extends HTMLElement>(name: string) =>
      root.querySelector<T>(`[data-pdf-${name}]`)!;
    const status = find('status');
    const retry = find<HTMLButtonElement>('retry');
    const input = find<HTMLInputElement>('page');
    const stage = find('stage');
    const viewport = find('viewport');
    const previous = find<HTMLButtonElement>('previous');
    const next = find<HTMLButtonElement>('next');
    const url = root.dataset['pdfUrl'] ?? '';
    if (!/^\/content-assets\/[a-f0-9]{64}\.pdf$/.test(url)) {
      status.textContent =
        'PDF preview unavailable. Use Open PDF or Download PDF.';
      continue;
    }
    let pdf: PDFDocumentProxy | undefined;
    let loading: PDFDocumentLoadingTask | undefined;
    let renderTask: RenderTask | undefined;
    let activePage: PDFPageProxy | undefined;
    let textTask: TextLayer | undefined;
    let library: typeof import('pdfjs-dist');
    let generation = 0;
    let closed = false;
    let page = 1;
    let displayedPage: number | undefined;
    let zoom: number | undefined;
    let lastWidth = 0;
    const listeners = new AbortController();
    function cancel() {
      generation++;
      renderTask?.cancel();
      textTask?.cancel();
      activePage?.cleanup();
      activePage = undefined;
      renderTask = undefined;
      textTask = undefined;
    }
    function failed(error: unknown) {
      status.textContent =
        error instanceof Error && error.name === 'PasswordException'
          ? 'This PDF needs a password. Use Open PDF or Download PDF to unlock it.'
          : 'PDF preview unavailable. Retry, Open PDF or Download PDF.';
      retry.hidden = false;
      root.setAttribute('aria-busy', 'false');
    }
    async function render() {
      if (!pdf || closed) return;
      cancel();
      const current = generation;
      const active = () => !closed && generation === current;
      root.setAttribute('aria-busy', 'true');
      status.textContent = `Loading page ${page}…`;
      input.value = String(page);
      input.max = String(pdf.numPages);
      previous.disabled = page === 1;
      next.disabled = page === pdf.numPages;
      find('count').textContent = `of ${pdf.numPages}`;
      try {
        const pdfPage = await pdf.getPage(page);
        if (!active()) {
          pdfPage.cleanup();
          return;
        }
        activePage = pdfPage;
        const natural = pdfPage.getViewport({ scale: 1 });
        lastWidth = viewport.clientWidth || 600;
        // Bound the bitmap to 8 megapixels even for unusually large PDF pages.
        const scale = Math.min(
          zoom ?? lastWidth / natural.width,
          3,
          Math.sqrt(8_000_000 / (natural.width * natural.height)),
        );
        const view = pdfPage.getViewport({ scale });
        const wrapper = document.createElement('div');
        wrapper.className = 'pdf-page';
        wrapper.style.width = `${view.width}px`;
        wrapper.style.height = `${view.height}px`;
        wrapper.style.setProperty(
          '--total-scale-factor',
          String(view.scale * view.userUnit),
        );
        const canvas = document.createElement('canvas');
        canvas.width = Math.ceil(view.width);
        canvas.height = Math.ceil(view.height);
        canvas.setAttribute('aria-label', `PDF page ${page}`);
        const text = document.createElement('div');
        text.className = 'textLayer';
        wrapper.append(canvas, text);
        const context = canvas.getContext('2d');
        if (!context) throw new Error('Canvas unavailable');
        // Each generation owns a detached canvas; cancellation never reuses a busy canvas.
        renderTask = pdfPage.render({
          canvas,
          canvasContext: context,
          viewport: view,
        });
        await renderTask.promise;
        if (!active()) return;
        const content = await pdfPage.getTextContent();
        if (!active()) return;
        textTask = new library.TextLayer({
          textContentSource: content,
          container: text,
          viewport: view,
        });
        await textTask.render();
        if (!active()) return;
        stage.replaceChildren(wrapper);
        if (displayedPage !== page) {
          viewport.scrollTop = 0;
          viewport.scrollLeft = 0;
          displayedPage = page;
        }
        viewport.tabIndex = 0;
        find('zoom').textContent = `${Math.round(view.scale * 100)}%`;
        status.textContent = `Page ${page} of ${pdf.numPages}`;
        root.setAttribute('aria-busy', 'false');
        retry.hidden = true;
        // Only one page's render resources remain live between interactions.
        pdfPage.cleanup();
      } catch (error) {
        if (active()) failed(error);
      }
    }
    async function load() {
      cancel();
      const current = generation;
      const oldLoading = loading;
      pdf = undefined;
      loading = undefined;
      stage.replaceChildren();
      retry.hidden = true;
      root.setAttribute('aria-busy', 'true');
      status.textContent = 'Loading PDF…';
      try {
        if (oldLoading) await oldLoading.destroy();
        library = await import('pdfjs-dist');
        if (closed || generation !== current) return;
        library.GlobalWorkerOptions.workerSrc = '/pdfjs/pdf.worker.min.mjs';
        const options = {
          url,
          enableXfa: false,
          cMapUrl: '/pdfjs/cmaps/',
          cMapPacked: true,
          standardFontDataUrl: '/pdfjs/standard_fonts/',
          wasmUrl: '/pdfjs/wasm/',
          iccUrl: '/pdfjs/iccs/',
        };
        const task = library.getDocument(options);
        loading = task;
        const result = await task.promise;
        if (closed || generation !== current) {
          await task.destroy();
          return;
        }
        pdf = result;
        page = 1;
        await render();
      } catch (error) {
        if (!closed && generation === current) failed(error);
      }
    }
    const on = (name: string, callback: () => void) =>
      find(name).addEventListener('click', callback, {
        signal: listeners.signal,
      });
    const move = (offset: number) => {
      if (pdf) {
        page = Math.max(1, Math.min(pdf.numPages, page + offset));
        void render();
      }
    };
    on('previous', () => move(-1));
    on('next', () => move(1));
    input.form!.addEventListener(
      'submit',
      (event) => {
        event.preventDefault();
        const value = Number(input.value);
        if (
          pdf &&
          Number.isInteger(value) &&
          value >= 1 &&
          value <= pdf.numPages
        ) {
          page = value;
          void render();
        } else {
          input.value = String(page);
          status.textContent = `Enter a page from 1 to ${pdf?.numPages ?? 1}.`;
        }
      },
      { signal: listeners.signal },
    );
    const changeZoom = (factor: number) => {
      const current =
        Number.parseFloat(find('zoom').textContent || '100') / 100;
      zoom = Math.max(0.25, Math.min(3, current * factor));
      void render();
    };
    on('in', () => changeZoom(1.25));
    on('out', () => changeZoom(0.8));
    on('fit', () => {
      zoom = undefined;
      void render();
    });
    on('retry', () => {
      void load();
    });
    const resize = new ResizeObserver(() => {
      if (viewport.clientWidth !== lastWidth && zoom === undefined)
        void render();
    });
    resize.observe(viewport);
    let observer: IntersectionObserver | undefined;
    if (typeof IntersectionObserver !== 'undefined') {
      observer = new IntersectionObserver(
        (entries) => {
          if (entries.some((entry) => entry.isIntersecting)) {
            observer!.disconnect();
            void load();
          }
        },
        { rootMargin: '200px' },
      );
      observer.observe(root);
    } else void load();
    document.defaultView!.addEventListener(
      'pagehide',
      (event) => {
        // A bfcache entry resumes with its existing document and observers.
        if ((event as PageTransitionEvent).persisted) return;
        closed = true;
        cancel();
        resize.disconnect();
        observer?.disconnect();
        listeners.abort();
        stage.replaceChildren();
        const cleanup = loading?.destroy();
        void cleanup?.catch(() => {});
      },
      { signal: listeners.signal },
    );
  }
}
