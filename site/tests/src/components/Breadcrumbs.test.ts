import { expect, test } from '@playwright/test';

test('reader breadcrumbs expose section hierarchy and useful links', async ({
  page,
}) => {
  await page.goto(
    '/notes/interview/applied-science/breadth/6-6-2-transformers/',
  );
  const breadcrumbs = page.getByRole('navigation', { name: 'Breadcrumbs' });
  await expect(breadcrumbs).toContainText('Interview');
  await expect(
    breadcrumbs.getByRole('link', { name: 'Home', exact: true }),
  ).toHaveAttribute('href', '/');
  await expect(
    breadcrumbs.getByRole('link', { name: 'Library', exact: true }),
  ).toHaveAttribute('href', '/library/');
  await expect(breadcrumbs.locator('[aria-current=page]')).toContainText(
    'Transformer Architecture',
  );
  await breadcrumbs
    .getByRole('link', { name: 'Interview', exact: true })
    .click();
  await expect(
    page.getByRole('heading', { name: 'Interview', exact: true }),
  ).toBeVisible();
});
