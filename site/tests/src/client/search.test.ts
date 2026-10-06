// @vitest-environment jsdom
import { beforeEach, expect, it, vi } from 'vitest';
import { initSearch, type SearchIndex } from '../../../src/client/search.js';

beforeEach(() => {
  document.body.innerHTML =
    '<form data-search-form><input name="q"><select name="section"><option value="">All</option><option value="interview">Interview</option></select><select name="kind"><option value="">All</option><option>markdown</option></select><button>Search</button></form><p data-search-status role="status"></p><ol data-search-results></ol><button data-search-more hidden>Load more results</button>';
});
function submit(query = 'attention') {
  document.querySelector('input')!.value = query;
  document
    .querySelector('form')!
    .dispatchEvent(new Event('submit', { cancelable: true }));
}
const data = {
  url: '/notes/test/',
  meta: {
    title: '<script>title</script>',
    breadcrumb: 'Interview / Group',
    kind: 'markdown',
  },
  plain_excerpt: 'Safe &lt;script&gt;text&lt;/script&gt;',
};
it('empty query stays local; initialized once, loading/results and filters are correct', async () => {
  const search = vi
    .fn()
    .mockResolvedValue({ results: [{ data: async () => data }] });
  const load = vi.fn(async () => ({ search }) as SearchIndex);
  initSearch(document, load);
  initSearch(document, load);
  submit('');
  expect(document.querySelector('[data-search-status]')!.textContent).toContain(
    'Enter a phrase',
  );
  expect(load).not.toHaveBeenCalled();
  document.querySelector<HTMLSelectElement>('[name="section"]')!.value =
    'interview';
  document.querySelector<HTMLSelectElement>('[name="kind"]')!.value =
    'markdown';
  submit();
  expect(document.querySelector('[data-search-status]')!.textContent).toContain(
    'Searching',
  );
  await vi.waitFor(() =>
    expect(
      document.querySelector('[data-search-results]')!.textContent,
    ).toContain('<script>title</script>'),
  );
  expect(document.querySelector('script')).toBeNull();
  expect(search).toHaveBeenCalledWith('attention', {
    filters: { section: 'interview', kind: 'markdown' },
  });
  expect(load).toHaveBeenCalledTimes(1);
});
it('no matches and unavailable indexes provide actionable feedback, then retry', async () => {
  const load = vi
    .fn()
    .mockRejectedValueOnce(new Error('Unavailable'))
    .mockResolvedValue({ search: async () => ({ results: [] }) });
  initSearch(document, load);
  submit();
  await vi.waitFor(() =>
    expect(
      document.querySelector('[data-search-status]')!.textContent,
    ).toContain('Search is unavailable'),
  );
  submit();
  await vi.waitFor(() =>
    expect(
      document.querySelector('[data-search-status]')!.textContent,
    ).toContain('No results'),
  );
});
it('superseded asynchronous results never overwrite a newer query or empty state', async () => {
  let finish!: (value: {
    results: { data: () => Promise<typeof data> }[];
  }) => void;
  const search = vi
    .fn()
    .mockImplementationOnce(
      () =>
        new Promise((resolve) => {
          finish = resolve;
        }),
    )
    .mockResolvedValue({ results: [] });
  initSearch(document, async () => ({ search }));
  submit('old');
  await vi.waitFor(() => expect(search).toHaveBeenCalledTimes(1));
  submit('');
  finish({ results: [{ data: async () => data }] });
  await Promise.resolve();
  await Promise.resolve();
  expect(document.querySelector('[data-search-results]')!.textContent).toBe('');
  expect(document.querySelector('[data-search-status]')!.textContent).toContain(
    'Enter a phrase',
  );
});
it('loads twenty results at a time and safely rejects nonlocal result URLs', async () => {
  const results = Array.from({ length: 21 }, (_, i) => ({
    data: async () => ({
      ...data,
      url: i === 0 ? 'javascript:alert(1)' : '/notes/test/',
    }),
  }));
  initSearch(document, async () => ({ search: async () => ({ results }) }));
  submit();
  await vi.waitFor(() =>
    expect(
      document.querySelector('[data-search-more]')!.hasAttribute('hidden'),
    ).toBe(false),
  );
  expect(document.querySelector('a[href^="javascript"]')).toBeNull();
  document.querySelector<HTMLButtonElement>('[data-search-more]')!.click();
  await vi.waitFor(() =>
    expect(document.querySelectorAll('[data-search-results] li')).toHaveLength(
      20,
    ),
  );
  expect(
    document.querySelector<HTMLButtonElement>('[data-search-more]')!.hidden,
  ).toBe(true);
});
it('missing form is harmless', () => {
  document.body.innerHTML = '';
  initSearch(document);
});

it.each(['/\\external.test/', '/\n/external.test/', '/\t/external.test/'])(
  'rejects a DOM-resolved external URL %j while keeping the real local route',
  async (url) => {
    const probe = document.createElement('a');
    probe.href = url;
    expect(probe.hostname).toBe('external.test');
    const results = [url, data.url].map((value) => ({
      data: async () => ({ ...data, url: value }),
    }));
    initSearch(document, async () => ({ search: async () => ({ results }) }));
    submit();
    await vi.waitFor(() =>
      expect(
        document.querySelector('[data-search-status]')!.textContent,
      ).toContain('Showing'),
    );
    expect(
      Array.from(document.querySelectorAll('[data-search-results] a')).map(
        (el) => el.getAttribute('href'),
      ),
    ).toEqual([data.url]);
  },
);
