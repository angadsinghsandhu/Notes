import { expect, test } from '@playwright/test';

test('tree branches toggle by keyboard and folder names remain ordinary links', async ({
  page,
}) => {
  await page.goto('/library/tree/');
  const tree = page.getByRole('navigation', { name: 'All published folders' });
  const books = tree
    .locator(':scope > ul > li')
    .first()
    .locator(':scope > details');
  await books.locator(':scope > summary').focus();
  await page.keyboard.press('Enter');
  await expect(books).toHaveAttribute('open', '');
  await expect(books.locator('ul a').first()).toBeVisible();
  await books.locator(':scope > summary > a').click();
  await expect(page).toHaveURL(/\/library\/books\/$/);
});
