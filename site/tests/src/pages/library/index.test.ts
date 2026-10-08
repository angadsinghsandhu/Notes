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

test('real upstream templates remain accessible only in supplemental browsing', async ({
  page,
}) => {
  const route =
    '/notes/courses/scrimba/learn-react/src/projects/01-first-react/';
  await page.goto('/library/');
  await expect(
    page.locator(`[data-library-notes] a[href="${route}"]`),
  ).toHaveCount(0);
  await page.getByText('Course code & resources', { exact: true }).click();
  await page
    .getByText('Supplemental documents', { exact: false })
    .first()
    .click();
  let branch = page
    .getByText('Supplemental documents', { exact: false })
    .first()
    .locator('..');
  for (const label of [
    'Scrimba',
    'Learn React',
    'src',
    'projects',
    '01-first-react',
  ]) {
    branch = branch
      .locator(':scope > details')
      .filter({ has: page.getByText(label, { exact: true }) });
    await branch.locator(':scope > summary').click();
  }
  const link = page.locator(`[data-library-resources] a[href="${route}"]`);
  await expect(link).toBeVisible();
  await link.click();
  await expect(page.locator('article')).toContainText(
    'This template provides a minimal setup',
  );
  await expect(
    page.getByRole('link', { name: 'View original source' }),
  ).toBeVisible();
});
