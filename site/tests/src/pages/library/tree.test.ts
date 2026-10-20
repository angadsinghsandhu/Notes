import { expect, test } from '@playwright/test';

test('shared full tree opens the reader current path and links actual folders', async ({
  page,
}) => {
  await page.goto(
    '/notes/interview/applied-science/breadth/6-6-2-transformers/',
  );
  await page
    .locator('.sidebar')
    .getByRole('link', { name: 'Folder tree', exact: true })
    .click();
  const tree = page.getByRole('navigation', { name: 'All published folders' });
  await expect(tree.locator('a')).toHaveCount(2300);
  const current = tree.locator('[aria-current=location]');
  await expect(current).toBeVisible();
  await expect(current).toHaveText('breadth');
  await current.click();
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('breadth');
});

test('full tree remains expandable and navigable without JavaScript on mobile', async ({
  browser,
}) => {
  const context = await browser.newContext({
    javaScriptEnabled: false,
    viewport: { width: 375, height: 900 },
  });
  const page = await context.newPage();
  await page.goto('/library/books/');
  await page.locator('.no-js-navigation > summary').click();
  await page
    .locator('.no-js-navigation')
    .getByRole('link', { name: 'Folder tree', exact: true })
    .click();
  const tree = page.getByRole('navigation', { name: 'All published folders' });
  const books = tree.locator(':scope > ul > li').first();
  await books.locator(':scope > details > summary').focus();
  await page.keyboard.press('Enter');
  await books.locator('details > ul a').first().click();
  await expect(page).toHaveURL(/\/library\/books\/folders\//);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  await context.close();
});

test('expanded deep hierarchy fits a narrow screen and is available from the mobile drawer', async ({
  page,
}) => {
  await page.setViewportSize({ width: 375, height: 900 });
  await page.goto(
    '/notes/interview/applied-science/breadth/6-6-2-transformers/',
  );
  await page.getByRole('button', { name: 'Browse sections' }).click();
  await page
    .getByRole('dialog')
    .getByRole('link', { name: 'Folder tree', exact: true })
    .click();
  await expect(
    page
      .getByRole('navigation', { name: 'All published folders' })
      .locator('[aria-current=location]'),
  ).toBeVisible();
  await page.locator('.folder-tree details').evaluateAll((branches) =>
    branches.forEach((branch) => {
      (branch as HTMLDetailsElement).open = true;
    }),
  );
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  await page.screenshot({
    path: '../.superpowers/sdd/2026-10-19-folder-navigation/tree-375.png',
  });
});
