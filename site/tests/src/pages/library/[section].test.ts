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

test('Courses separates real provider guides from primary notes without dropping access', async ({
  page,
}) => {
  const route = '/notes/courses/udemy/react/other/course-update-guide-udemy/';
  await page.goto('/library/courses/');
  await expect(
    page.locator(`[data-library-notes] a[href="${route}"]`),
  ).toHaveCount(0);
  await page.getByText('Course code & resources', { exact: true }).click();
  await page.getByText('Supplemental documents', { exact: false }).click();
  let branch = page
    .getByText('Supplemental documents', { exact: false })
    .locator('..');
  for (const label of ['Udemy', 'React', 'other']) {
    branch = branch
      .locator(':scope > details')
      .filter({ has: page.getByText(label, { exact: true }) });
    await branch.locator(':scope > summary').click();
  }
  const link = page.locator(`[data-library-resources] a[href="${route}"]`);
  await expect(link).toBeVisible();
});
