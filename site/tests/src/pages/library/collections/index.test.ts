import { expect, test } from '@playwright/test';
test('collections group source works by type then provider', async ({
  page,
}) => {
  await page.goto('/library/collections/');
  await expect(
    page.getByRole('heading', { name: 'Books', exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole('heading', { name: 'Online Courses', exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole('heading', { name: 'Udemy', exact: true }),
  ).toBeVisible();
  await expect(page.locator('main .organization-card')).toHaveCount(2);
});
