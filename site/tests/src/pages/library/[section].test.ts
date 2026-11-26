import { expect, test } from '@playwright/test';

test('section folder cards open actual Languages notes', async ({ page }) => {
  await page.goto('/library/');
  await page
    .getByRole('navigation', { name: 'Browse by section' })
    .getByRole('link', { name: /^Languages/ })
    .click();
  await expect(
    page.getByRole('heading', { name: 'Languages', exact: true }),
  ).toBeVisible();
  await expect(page.locator('main .group-disclosure')).toHaveCount(0);
  await page.locator('.folder-cards').getByRole('link').first().click();
  await page
    .locator('.folder-cards')
    .getByRole('link', { name: /^unit 1-4/ })
    .click();
  await expect(
    page.getByRole('link', { name: 'unit 1-4', exact: true }).first(),
  ).toBeVisible();
});

test('Courses separates real provider guides from primary notes without dropping access', async ({
  page,
}) => {
  const route = '/notes/courses/udemy/react/other/course-update-guide-udemy/';
  await page.goto('/library/courses/');
  await expect(
    page.locator(`[data-library-notes] a[href="${route}"]`),
  ).toHaveCount(0);
  for (const label of ['Udemy', 'React', 'other'])
    await page
      .locator('.folder-cards')
      .getByRole('link', { name: new RegExp(`^${label}`) })
      .click();
  await expect(
    page.getByRole('heading', { name: 'Supplemental documents' }),
  ).toBeVisible();
  await expect(
    page.locator(`[data-library-notes] a[href="${route}"]`),
  ).toHaveCount(0);
  await expect(
    page.locator(`[data-library-resources] a[href="${route}"]`),
  ).toBeVisible();
});

for (const section of [
  'books',
  'classes',
  'courses',
  'interview',
  'languages',
  'tutorials',
])
  test(`${section} uses the shared immediate-folder navigation`, async ({
    page,
  }) => {
    await page.goto(`/library/${section}/`);
    await expect(page.locator('.folder-cards a').first()).toBeVisible();
    await expect(page.locator('main .group-disclosure')).toHaveCount(0);
    await expect(page.locator('[data-library-notes]')).toBeVisible();
    await expect(page.locator('[data-library-resources]')).toBeVisible();
  });
