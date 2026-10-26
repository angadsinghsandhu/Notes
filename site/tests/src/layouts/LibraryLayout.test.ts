import { expect, test } from '@playwright/test';

test('shared layout skip link moves keyboard focus into main', async ({
  page,
}) => {
  await page.goto('/');
  const skipLink = page.getByRole('link', { name: 'Skip to content' });
  await expect(skipLink).toHaveAttribute('href', '#main');
  await page.keyboard.press('Tab');
  await expect(skipLink).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('main')).toBeFocused();
});

test('shared navigation exposes curated views in the existing mobile drawer', async ({
  page,
}) => {
  await page.setViewportSize({ width: 375, height: 900 });
  await page.goto('/library/topics/');
  await page.getByRole('button', { name: 'Browse sections' }).click();
  const drawer = page.getByRole('dialog');
  for (const name of [
    'Topics',
    'Collections',
    'Learning Paths',
    'Source Archive',
  ])
    await expect(drawer.getByRole('link', { name, exact: true })).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(
    page.getByRole('button', { name: 'Browse sections' }),
  ).toBeFocused();
});
