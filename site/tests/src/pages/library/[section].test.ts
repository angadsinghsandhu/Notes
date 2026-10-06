import { expect, test } from '@playwright/test';

test('section links open the actual Languages notes', async ({ page }) => {
  await page.goto('/library/');
  await page
    .getByRole('link', { name: 'Languages', exact: true })
    .first()
    .click();
  await expect(
    page.getByRole('heading', { name: 'Languages', exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole('link', { name: 'unit 1-4', exact: true }).first(),
  ).toBeVisible();
});
