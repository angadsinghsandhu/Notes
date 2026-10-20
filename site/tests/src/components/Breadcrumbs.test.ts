import { expect, test } from '@playwright/test';

test('reader breadcrumbs expose section hierarchy and useful links', async ({
  page,
}) => {
  await page.goto(
    '/notes/interview/applied-science/breadth/6-6-2-transformers/',
  );
  const breadcrumbs = page.getByRole('navigation', { name: 'Breadcrumbs' });
  await expect(breadcrumbs).toContainText('Interview');
  await expect(
    breadcrumbs.getByRole('link', { name: 'Home', exact: true }),
  ).toHaveAttribute('href', '/');
  await expect(
    breadcrumbs.getByRole('link', { name: 'Library', exact: true }),
  ).toHaveAttribute('href', '/library/');
  await expect(breadcrumbs.locator('[aria-current=page]')).toContainText(
    'Transformer Architecture',
  );
  await breadcrumbs
    .getByRole('link', { name: 'Interview', exact: true })
    .click();
  await expect(
    page.getByRole('heading', { name: 'Interview', exact: true }),
  ).toBeVisible();
});

test('reader ancestors open folder pages and all breadcrumb items align', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto(
    '/notes/interview/applied-science/breadth/6-6-2-transformers/',
  );
  const breadcrumbs = page.getByRole('navigation', { name: 'Breadcrumbs' });
  const boxes = await breadcrumbs.locator('li').evaluateAll((items) =>
    items.map((item) => {
      const box = item.getBoundingClientRect();
      return { center: box.y + box.height / 2, height: box.height };
    }),
  );
  expect(
    Math.max(...boxes.map((box) => box.center)) -
      Math.min(...boxes.map((box) => box.center)),
  ).toBeLessThan(2);
  expect(boxes.every((box) => box.height >= 44)).toBe(true);
  await breadcrumbs.getByRole('link', { name: 'breadth', exact: true }).click();
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('breadth');
  await page.setViewportSize({ width: 375, height: 900 });
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});
