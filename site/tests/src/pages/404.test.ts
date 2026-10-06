import { expect, test } from '@playwright/test';

test('404 provides useful recovery', async ({ page }) => {
  await page.goto('/404.html');
  await expect(
    page.getByRole('heading', { name: 'Page not found' }),
  ).toBeVisible();
  await expect(
    page.getByRole('link', { name: 'Browse the library' }),
  ).toHaveAttribute('href', '/library/');
  await expect(
    page.getByRole('link', { name: 'Search the notes' }),
  ).toHaveAttribute('href', '/search/');
});

test('404 is excluded from indexing and canonical output', async ({ page }) => {
  await page.goto('/404.html');
  await expect(page.locator('meta[name=robots]')).toHaveAttribute(
    'content',
    'noindex',
  );
  await expect(page.locator('link[rel=canonical]')).toHaveCount(0);
  await expect(page.locator('[data-pagefind-body]')).toHaveCount(0);
});
