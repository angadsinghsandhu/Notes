import { expect, test } from '@playwright/test';

test('folder contents show immediate note and resource files with readable metadata', async ({
  page,
}) => {
  await page.goto(
    '/library/books/folders/Programming~20PyTorch~20for~20Deep~20Learning~20-~20Ian~20Pointer/Chapter~201~20-~20Getting~20Started~20with~20Pytorch/',
  );
  const notes = page.locator('[data-library-notes]');
  await expect(
    notes.getByRole('link', {
      name: 'Getting Started with Pytorch',
      exact: true,
    }),
  ).toBeVisible();
  const note = notes.locator('.entry-list li').first();
  const link = await note.locator('a').boundingBox();
  const metadata = await note.locator('.entry-meta').boundingBox();
  expect(metadata!.y).toBeGreaterThanOrEqual(link!.y + link!.height);
  await expect(page.locator('main .group-disclosure')).toHaveCount(0);
});
