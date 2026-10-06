type ResultData = {
  url: string;
  meta: Record<string, string>;
  plain_excerpt: string;
};
type Result = { data(): Promise<ResultData> };
export type SearchIndex = {
  search(
    query: string,
    options: { filters: Record<string, string> },
  ): Promise<{ results: Result[] }>;
};

async function loadPagefind(): Promise<SearchIndex> {
  const path = '/pagefind/pagefind.js';
  return import(/* @vite-ignore */ path) as Promise<SearchIndex>;
}

/** Pagefind owns the index; only local result URLs and text metadata become DOM. */
export function initSearch(document: Document, load = loadPagefind): void {
  const form = document.querySelector<HTMLFormElement>('[data-search-form]');
  const status = document.querySelector<HTMLElement>('[data-search-status]');
  const list = document.querySelector<HTMLOListElement>(
    '[data-search-results]',
  );
  const more = document.querySelector<HTMLButtonElement>('[data-search-more]');
  if (!form || !status || !list || !more || form.dataset['ready']) return;
  form.dataset['ready'] = 'true';
  let index: SearchIndex | undefined;
  let generation = 0;
  let results: Result[] = [];
  let shown = 0;
  async function append(token: number): Promise<void> {
    const start = shown;
    const data = await Promise.all(
      results.slice(start, start + 20).map((result) => result.data()),
    );
    if (token !== generation) return;
    for (const result of data) {
      if (
        !result.url.startsWith('/') ||
        result.url.startsWith('//') ||
        /[\\\s]/.test(result.url)
      )
        continue;
      const item = document.createElement('li');
      const title = document.createElement('a');
      title.href = result.url;
      title.textContent = result.meta['title'] ?? 'Untitled';
      const metadata = document.createElement('p');
      metadata.className = 'muted';
      metadata.textContent = `${result.meta['breadcrumb'] ?? ''} · ${result.meta['kind'] ?? ''}`;
      // A textarea decodes entities as text without interpreting markup or scripts.
      const text = document.createElement('textarea');
      text.innerHTML = result.plain_excerpt;
      const excerpt = document.createElement('p');
      excerpt.textContent = text.value;
      item.append(title, metadata, excerpt);
      list!.append(item);
    }
    shown = Math.min(start + 20, results.length);
    more!.hidden = shown >= results.length;
    status!.textContent = results.length
      ? `Showing ${shown} of ${results.length} results.`
      : 'No results. Try another phrase or broader filters.';
  }
  async function search(): Promise<void> {
    const token = ++generation;
    list!.replaceChildren();
    more!.hidden = true;
    const query = form!
      .querySelector<HTMLInputElement>('[name="q"]')!
      .value.trim();
    if (!query) {
      status!.textContent = 'Enter a phrase to search notes and resources.';
      return;
    }
    status!.textContent = 'Searching…';
    const filters: Record<string, string> = {};
    for (const name of ['section', 'kind']) {
      const value = form!.querySelector<HTMLSelectElement>(
        `[name="${name}"]`,
      )!.value;
      if (value) filters[name] = value;
    }
    try {
      index ??= await load();
      const response = await index.search(query, { filters });
      if (token !== generation) return;
      results = response.results;
      shown = 0;
      await append(token);
    } catch {
      if (token !== generation) return;
      index = undefined;
      status!.textContent =
        'Search is unavailable. Retry, or browse the library. Locally, run npm run build and npm run preview.';
    }
  }
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    void search();
  });
  more.addEventListener('click', async () => {
    more.disabled = true;
    try {
      await append(generation);
    } catch {
      status.textContent = 'More results could not load. Retry the search.';
    } finally {
      more.disabled = false;
    }
  });
}
