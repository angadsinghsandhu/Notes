import { expect, test } from '@playwright/test';

test('Books folder cards open a bookmarkable book and chapter with immediate files', async ({
  page,
}) => {
  await page.goto('/library/books/');
  await page
    .locator('.folder-cards')
    .getByRole('link', { name: /^Programming PyTorch for Deep Learning/ })
    .click();
  const bookUrl = page.url();
  await expect(page).toHaveURL(/\/library\/books\/folders\//);
  await expect(page.locator('main .group-disclosure')).toHaveCount(0);
  const chapters = page.locator('.folder-cards a');
  await expect(chapters.first()).toBeVisible();
  await chapters.first().click();
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  await expect(page.locator('.breadcrumbs a').last()).toHaveAttribute(
    'href',
    new URL(bookUrl).pathname,
  );
  await page.reload();
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
});

for (const width of [375, 1280])
  test(`folder browsing fits ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/library/books/');
    await expect(page.locator('.folder-cards a').first()).toBeVisible();
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await page.screenshot({
      path: `../.superpowers/sdd/2026-10-19-folder-navigation/books-${width}.png`,
      fullPage: true,
    });
  });
