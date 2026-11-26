import { expect, test } from '@playwright/test';
test('topic tree disclosure and links work using the keyboard', async ({
  page,
}) => {
  await page.goto('/library/topics/');
  const summary = page
    .locator('main .organization-tree > li > details > summary')
    .first();
  await summary.focus();
  await page.keyboard.press('Enter');
  await expect(summary.locator('..')).toHaveAttribute('open', '');
  await page.keyboard.press('Tab');
  await expect(page.locator('main .organization-tree a').first()).toBeFocused();
});
