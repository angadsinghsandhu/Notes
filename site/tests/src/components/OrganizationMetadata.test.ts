import { expect, test } from '@playwright/test';
test('curated reader metadata preserves original source breadcrumbs', async ({
  page,
}) => {
  await page.goto(
    '/notes/interview/applied-science/breadth/6-6-2-transformers/',
  );
  await expect(page.locator('.organization-metadata')).toContainText(
    'Unreviewed',
  );
  await expect(page.locator('.organization-metadata a')).toContainText([
    'Attention, Transformers & Language Models',
  ]);
  await expect(
    page.getByRole('navigation', { name: 'Breadcrumbs' }),
  ).toContainText('Interview');
});
