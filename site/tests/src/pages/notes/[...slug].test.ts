import { expect, test } from '@playwright/test';

const math = '/notes/interview/applied-science/breadth/6-6-2-transformers/';

test('reader route retains numeric adjacency and immutable source action', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1024, height: 900 });
  await page.goto(math);
  await expect(
    page.getByRole('link', { name: 'View original source' }),
  ).toHaveAttribute('href', /github.com.*6.6.2-transformers.md/);
  await expect(
    page.getByRole('navigation', { name: 'Previous and next notes' }),
  ).toContainText('6.6.1');
});

test('reading and navigation work without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({
    javaScriptEnabled: false,
    viewport: { width: 375, height: 900 },
  });
  const page = await context.newPage();
  await page.goto(math);
  await expect(page.locator('article')).toContainText('Transformer');
  await expect(
    page
      .getByRole('region', { name: 'Code or stored notebook output' })
      .first(),
  ).toHaveAttribute('tabindex', '0');
  await page.locator('.no-js-navigation > summary').click();
  await page
    .getByRole('link', { name: 'Languages', exact: true })
    .first()
    .click();
  await expect(
    page.getByRole('heading', { name: 'Languages', exact: true }),
  ).toBeVisible();
  await context.close();
});
