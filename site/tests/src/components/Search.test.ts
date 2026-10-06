import { expect, test } from '@playwright/test';

test('empty and unavailable search states are useful', async ({ page }) => {
  await page.goto('/search/');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-status]')).toContainText(
    'Enter a phrase',
  );
  await page.route('**/pagefind/**', (route) => route.abort());
  await page.getByRole('searchbox').fill('attention');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-status]')).toContainText(
    'Search is unavailable',
  );
});
