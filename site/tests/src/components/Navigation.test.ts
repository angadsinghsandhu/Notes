import { expect, test } from '@playwright/test';

test('mobile native drawer traps keyboard focus, Escape closes, and focus returns', async ({
  page,
}) => {
  await page.setViewportSize({ width: 375, height: 800 });
  await page.goto(
    '/notes/interview/applied-science/breadth/6-6-2-transformers/',
  );
  const trigger = page.getByRole('button', { name: 'Browse sections' });
  await trigger.click();
  const drawer = page.getByRole('dialog', { name: 'Browse sections' });
  await expect(drawer).toBeVisible();
  const close = drawer.getByRole('button', { name: 'Close navigation' });
  await expect(close).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  expect(
    await page.evaluate(
      () => document.activeElement?.closest('dialog') !== null,
    ),
  ).toBe(true);
  await page.keyboard.press('Escape');
  await expect(drawer).not.toBeVisible();
  await expect(trigger).toBeFocused();
  const box = await trigger.boundingBox();
  expect(box!.width).toBeGreaterThanOrEqual(44);
  expect(box!.height).toBeGreaterThanOrEqual(44);
});

test('light dark system choices persist and reduced motion is respected', async ({
  page,
}) => {
  await page.emulateMedia({ colorScheme: 'dark', reducedMotion: 'reduce' });
  await page.goto('/');
  expect(
    await page.evaluate(
      () => getComputedStyle(document.documentElement).backgroundColor,
    ),
  ).toBe('rgb(15, 23, 42)');
  await page.getByLabel('Theme').selectOption('light');
  expect(
    await page.evaluate(
      () => getComputedStyle(document.documentElement).backgroundColor,
    ),
  ).toBe('rgb(248, 250, 252)');
  await page.reload();
  await expect(page.getByLabel('Theme')).toHaveValue('light');
  await page.getByLabel('Theme').selectOption('dark');
  expect(
    await page.evaluate(
      () => getComputedStyle(document.documentElement).backgroundColor,
    ),
  ).toBe('rgb(15, 23, 42)');
  await page.getByLabel('Theme').selectOption('system');
  expect(
    await page.evaluate(
      () => getComputedStyle(document.documentElement).backgroundColor,
    ),
  ).toBe('rgb(15, 23, 42)');
  await page.emulateMedia({ colorScheme: 'light', reducedMotion: 'reduce' });
  expect(
    await page.evaluate(
      () => getComputedStyle(document.documentElement).backgroundColor,
    ),
  ).toBe('rgb(248, 250, 252)');
  expect(
    await page.evaluate(
      () => getComputedStyle(document.documentElement).scrollBehavior,
    ),
  ).toBe('auto');
});

test('theme selector and visible keyboard focus meet the 44px contract', async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 900 });
  await page.goto('/search/');
  const theme = page.getByRole('combobox', { name: 'Theme', exact: true });
  const box = await theme.boundingBox();
  expect(box!.width).toBeGreaterThanOrEqual(44);
  expect(box!.height).toBeGreaterThanOrEqual(44);
  await page.keyboard.press('Tab');
  await expect(
    page.getByRole('link', { name: 'Skip to content' }),
  ).toBeFocused();
  expect(
    await page
      .getByRole('link', { name: 'Skip to content' })
      .evaluate((el) => getComputedStyle(el).outlineWidth),
  ).toBe('3px');
  await page.screenshot({
    path: '../.superpowers/sdd/2026-10-04-notes-website/screenshots/keyboard-focus-light-320.png',
  });
  await theme.selectOption('dark');
  await theme.focus();
  await page.keyboard.press('Tab');
  await page.keyboard.press('Shift+Tab');
  await expect(theme).toBeFocused();
  expect(await theme.evaluate((el) => getComputedStyle(el).outlineWidth)).toBe(
    '3px',
  );
  await page.screenshot({
    path: '../.superpowers/sdd/2026-10-04-notes-website/screenshots/keyboard-focus-dark-320.png',
  });
});

test('real supplemental template does not appear as a primary group-navigation note', async ({
  page,
}) => {
  await page.goto(
    '/notes/courses/scrimba/learn-react/src/projects/01-first-react/',
  );
  await expect(page.locator('.group-navigation')).toHaveCount(0);
  await expect(page.locator('article')).toContainText(
    'This template provides a minimal setup',
  );
});
