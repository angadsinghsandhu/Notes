import { expect, test } from '@playwright/test';
test('learning path steps keep stored order and canonical links', async ({
  page,
}) => {
  await page.goto('/library/paths/applied-scientist-interview-preparation/');
  await expect(page.locator('.path-steps > li').first()).toContainText(
    'Orientation',
  );
  await expect(page.locator('.path-steps > li').nth(1)).toContainText(
    '1. Fundamentals',
  );
  await expect(page.locator('.path-steps a[href^="/notes/"]')).not.toHaveCount(
    0,
  );
});
