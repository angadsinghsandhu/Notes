import { expect, test } from '@playwright/test';
test('outline-only chapter exposes resources without invented notes', async ({
  page,
}) => {
  await page.goto(
    '/library/collections/programming-pytorch-deep-learning/groups/chapter-4/',
  );
  await expect(page.locator('[data-organization-documents]')).toContainText(
    'No notes directly in this group.',
  );
  await expect(page.locator('[data-organization-resources]')).toContainText(
    'Outline',
  );
  await expect(page.locator('[data-organization-resources] a')).toHaveCount(1);
});
