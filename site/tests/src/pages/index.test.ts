import { expect, test } from '@playwright/test';

test('test_homepage_is_a_readable_document', async ({ page }) => {
  const response = await page.goto('/');

  expect(response?.status()).toBe(200);
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  await expect(page.getByRole('heading', { level: 1 })).toHaveCount(1);
  await expect(page.getByRole('heading', { level: 1 })).toHaveText(
    'Notes Library',
  );
});

test('homepage counts the actual primary archive without supplemental templates', async ({
  page,
}) => {
  await page.goto('/');
  const counts = await page.locator('.section-card p').allTextContents();
  expect(
    counts.reduce(
      (sum, count) =>
        sum + Number(/(\d+) learning notes/.exec(count)?.[1] ?? 0),
      0,
    ),
  ).toBe(325);
});
