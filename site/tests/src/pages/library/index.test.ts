import { expect, test } from '@playwright/test';

test('library starts with learning notes and offers resource browsing', async ({
  page,
}) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'Browse the library' }).click();
  await expect(
    page.getByRole('heading', { name: 'Library', exact: true }),
  ).toBeVisible();
  await expect(page.locator('[data-library-notes]')).toBeVisible();
  await expect(page.locator('[data-library-resources]')).not.toBeVisible();
  await page.getByText('Course code & resources', { exact: true }).click();
  await expect(page.locator('[data-library-resources]')).toBeVisible();
});
