import { expect, test } from '@playwright/test';

test('an unknown alias returns excluded useful recovery without a redirect', async ({
  request,
}) => {
  const response = await request.get('/task6-never-published-alias/');
  expect(response.status()).toBe(404);
  const html = await response.text();
  expect(html).toContain('Page not found');
  expect(html).toContain('Browse the library');
  expect(html).toContain('noindex');
  expect(html).not.toContain('http-equiv="refresh"');
  expect(html).not.toContain('data-pagefind-body');
});
