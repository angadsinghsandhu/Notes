import { expect, test } from '@playwright/test';
test('topic descendants use canonical notes and related collections', async ({
  page,
}) => {
  await page.goto('/library/topics/computer-vision/');
  await expect(
    page.locator('[data-organization-documents] a[href^="/notes/books/"]'),
  ).not.toHaveCount(0);
  await expect(page.locator('[data-related-collections]')).toContainText(
    'Programming PyTorch',
  );
  await expect(page.locator('[data-pagefind-body]')).toHaveCount(0);
});

test('topic navigation and empty sections describe topic descendants', async ({
  page,
}) => {
  await page.goto('/library/topics/attention-transformers-language-models/');
  await expect(page.locator('.sidebar .collection-navigation > a')).toHaveText(
    'Topic overview & full tree',
  );
  await expect(page.locator('[data-organization-documents]')).toContainText(
    'No exercises in this topic or its descendants.',
  );
  await expect(page.locator('[data-organization-documents]')).not.toContainText(
    'directly in this group',
  );
});
