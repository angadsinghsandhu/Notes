import { expect, test } from '@playwright/test';

test('real transformer phrase is indexed with metadata and filters', async ({
  page,
}) => {
  await page.goto('/search/');
  await page
    .getByRole('searchbox', { name: 'Search notes and resources' })
    .fill('scaled dot');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-results]')).toContainText(
    'Transformer Architecture',
  );
  await expect(page.locator('[data-search-results]')).toContainText(
    'Interview',
  );
  await expect(page.locator('[data-search-results]')).toContainText('markdown');
  await page
    .getByRole('combobox', { name: 'Kind', exact: true })
    .selectOption('pdf');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-status]')).toContainText(
    'No results',
  );
  await page
    .getByRole('combobox', { name: 'Kind', exact: true })
    .selectOption('markdown');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-results]')).toContainText(
    'Transformer Architecture',
  );
  await page
    .getByRole('combobox', { name: 'Section', exact: true })
    .selectOption('languages');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-status]')).toContainText(
    'No results',
  );
});

test('native Pagefind scopes and metadata match actual canonical readers', async ({
  page,
}) => {
  await page.goto('/search/');
  const cases = [
    {
      query: 'genRandomInt',
      url: '/resources/courses/udemy/react/notes/03-react-essentials/app-jsx/',
      learning: false,
    },
    {
      query: 'scaled dot',
      url: '/notes/interview/applied-science/breadth/6-6-2-transformers/',
      learning: true,
    },
    {
      query: 'Transfer Learning',
      url: '/notes/books/programming-pytorch-for-deep-learning-ian-pointer/chapter-4-transfer-learning-and-other-tricks/',
      learning: false,
    },
    {
      query: 'Browser-based Models',
      url: '/notes/courses/coursera/deep-learning-ai-course/tensorflow-deployment/course-1-tensorflow-js/',
      learning: false,
    },
    {
      query: 'Programming PyTorch',
      url: '/resources/books/programming-pytorch-for-deep-learning-ian-pointer/programming-pytorch-for-deep-learning-ian-pointer-pdf/',
      learning: true,
    },
  ];
  const results = await page.evaluate(async (cases) => {
    const path = '/pagefind/pagefind.js';
    const index = await import(/* @vite-ignore */ path);
    const urls = async (query: string, filters: Record<string, string>) => {
      const response = await index.search(query, { filters });
      return Promise.all(
        response.results.map(
          async (result: { data(): Promise<{ url: string }> }) =>
            (await result.data()).url,
        ),
      );
    };
    const memberships = [];
    for (const item of cases) {
      memberships.push({
        ...item,
        files: await urls(item.query, { scope: 'files' }),
        learningUrls: await urls(item.query, { scope: 'learning' }),
      });
    }
    return {
      memberships,
      filters: await index.filters(),
      ancestor: await urls('scaled dot', {
        scope: 'learning',
        topic: 'deep-learning',
      }),
      leaf: await urls('scaled dot', {
        scope: 'learning',
        topic: 'attention-transformers-language-models',
      }),
      wrongTopic: await urls('scaled dot', {
        scope: 'learning',
        topic: 'web-development',
      }),
      collection: await urls('Transfer Learning', {
        scope: 'files',
        collection: 'programming-pytorch-deep-learning',
      }),
      wrongCollection: await urls('Transfer Learning', {
        scope: 'files',
        collection: 'react-complete-guide',
      }),
    };
  }, cases);
  for (const item of results.memberships) {
    expect(item.files, item.url).toContain(item.url);
    expect(item.learningUrls.includes(item.url), item.url).toBe(item.learning);
    expect(item.files.filter((url) => url === item.url)).toHaveLength(1);
    expect(item.files.every((url) => !url.startsWith('/library/'))).toBe(true);
  }
  expect(Object.keys(results.filters.scope).sort()).toEqual([
    'files',
    'learning',
  ]);
  expect(results.ancestor).toContain(cases[1]!.url);
  expect(results.leaf).toContain(cases[1]!.url);
  expect(results.wrongTopic).not.toContain(cases[1]!.url);
  expect(results.collection).toContain(cases[2]!.url);
  expect(results.wrongCollection).not.toContain(cases[2]!.url);
});

test('scope topic collection and reset work with real production results', async ({
  page,
}) => {
  await page.goto('/search/');
  const scope = page.getByRole('combobox', { name: 'Scope', exact: true });
  const topic = page.getByRole('combobox', { name: 'Topic', exact: true });
  const collection = page.getByRole('combobox', {
    name: 'Collection',
    exact: true,
  });
  await expect(scope).toHaveValue('learning');
  await page.getByRole('searchbox').fill('genRandomInt');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-status]')).toContainText(
    'No results',
  );
  await scope.selectOption('files');
  await expect(
    page.locator(
      '[data-search-results] a[href="/resources/courses/udemy/react/notes/03-react-essentials/app-jsx/"]',
    ),
  ).toBeVisible();
  await topic.selectOption('deep-learning');
  await expect(page.locator('[data-search-status]')).toContainText(
    'No results',
  );
  await topic.selectOption('');
  await collection.selectOption('react-complete-guide');
  await expect(page.locator('[data-search-results]')).toContainText('App');
  await collection.selectOption('programming-pytorch-deep-learning');
  await expect(page.locator('[data-search-status]')).toContainText(
    'No results',
  );
  await page.getByRole('button', { name: 'Reset filters' }).click();
  await expect(scope).toHaveValue('learning');
  await expect(topic).toHaveValue('');
  await expect(collection).toHaveValue('');
  await expect(page.getByRole('searchbox')).toHaveValue('');
  await expect(page.locator('[data-search-status]')).toContainText(
    'Enter a phrase',
  );
});

test('filter changes restart real result pagination', async ({ page }) => {
  await page.goto('/search/');
  await page
    .getByRole('combobox', { name: 'Scope', exact: true })
    .selectOption('files');
  await page.getByRole('searchbox').fill('react');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-results] li')).toHaveCount(20);
  await page.getByRole('button', { name: 'Load more results' }).click();
  await expect(page.locator('[data-search-results] li')).toHaveCount(40);
  await page
    .getByRole('combobox', { name: 'Kind', exact: true })
    .selectOption('markdown');
  await expect(page.locator('[data-search-results] li')).toHaveCount(20);
});
