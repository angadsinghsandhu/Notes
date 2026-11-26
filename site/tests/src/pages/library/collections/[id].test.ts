import { expect, test } from '@playwright/test';
test('book keeps immediate ordered chapter cards and attribution', async ({
  page,
}) => {
  await page.goto('/library/collections/programming-pytorch-deep-learning/');
  await expect(page.locator('main')).toContainText('Ian Pointer');
  await expect(page.locator('main .organization-card').first()).toContainText(
    'Chapter 0',
  );
  await expect(page.locator('main .organization-card')).toHaveCount(7);
  await expect(
    page.getByRole('heading', { name: 'Resources', exact: true }),
  ).toBeVisible();
});

test('collection empty sections distinguish direct entries from chapter content', async ({
  page,
}) => {
  await page.goto('/library/collections/programming-pytorch-deep-learning/');
  await expect(page.locator('.sidebar .collection-navigation > a')).toHaveText(
    'Collection overview & full tree',
  );
  await expect(page.locator('[data-organization-documents]')).toContainText(
    'No exercises directly in this collection.',
  );
  await expect(page.locator('[data-organization-documents]')).not.toContainText(
    'directly in this group',
  );
});
