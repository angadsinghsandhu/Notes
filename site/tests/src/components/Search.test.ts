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

for (const width of [320, 1280]) {
  test(`search filters remain labeled and contained at ${width}px`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height: 1000 });
    await page.goto('/search/');
    await expect(
      page.getByRole('combobox', { name: 'Scope', exact: true }),
    ).toHaveValue('learning');
    await expect(
      page
        .getByRole('combobox', { name: 'Topic', exact: true })
        .locator('option[value="deep-learning"]'),
    ).toHaveText('Deep Learning');
    await expect(
      page
        .getByRole('combobox', { name: 'Collection', exact: true })
        .locator('option[value="react-complete-guide"]'),
    ).not.toHaveText('');
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await page.screenshot({
      path: `../.superpowers/sdd/2026-10-21-library-information-architecture/task-6-search-${width}.png`,
    });
  });
}
