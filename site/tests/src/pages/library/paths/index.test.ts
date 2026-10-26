import { expect, test } from '@playwright/test';
test('only populated learning paths become cards', async ({ page }) => {
  await page.goto('/library/paths/');
  await expect(page.locator('main .organization-card')).toHaveCount(1);
  await expect(page.locator('main')).toContainText(
    'Applied Scientist Interview Preparation',
  );
});
