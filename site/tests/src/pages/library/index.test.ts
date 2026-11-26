import { expect, test } from '@playwright/test';

test('library offers six section pages with separate note and resource counts', async ({
  page,
}) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'Browse the library' }).click();
  await expect(
    page.getByRole('heading', { name: 'Library', exact: true }),
  ).toBeVisible();
  await expect(page.locator('[data-library-notes]')).toContainText(
    '325 learning notes',
  );
  await expect(page.locator('[data-library-resources]')).toContainText(
    'course code & resources',
  );
  await expect(
    page
      .getByRole('navigation', { name: 'Browse by section' })
      .getByRole('link'),
  ).toHaveCount(6);
});

test('real upstream templates remain accessible only in supplemental browsing', async ({
  page,
}) => {
  const route =
    '/notes/courses/scrimba/learn-react/src/projects/01-first-react/';
  await page.goto('/library/courses/');
  for (const label of [
    'Scrimba',
    'Learn React',
    'src',
    'projects',
    '01-first-react',
  ])
    await page
      .locator('.folder-cards')
      .getByRole('link', { name: new RegExp(`^${label}`) })
      .click();
  await expect(
    page.locator(`[data-library-notes] a[href="${route}"]`),
  ).toHaveCount(0);
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

test('library gives three equal curated entry points and retains the source archive', async ({
  page,
}) => {
  await page.goto('/library/');
  await expect(page.locator('main .organization-card')).toHaveCount(3);
  await expect(page.locator('main .organization-counts')).toHaveCount(0);
  await expect(page.locator('#source-archive .section-card')).toHaveCount(6);
});
