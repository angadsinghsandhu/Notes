import { expect, test } from '@playwright/test';
test('populated topic tree hides uncurated taxonomy branches', async ({
  page,
}) => {
  await page.goto('/library/topics/');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Topics');
  await expect(
    page.getByRole('navigation', { name: 'Topic tree' }),
  ).toContainText('Deep Learning');
  await expect(
    page.getByRole('navigation', { name: 'Topic tree' }),
  ).not.toContainText('Human Languages');
});
