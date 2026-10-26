import { expect, test } from '@playwright/test';
test('canonical organization cards expose separate learning and resource counts', async ({
  page,
}) => {
  await page.goto('/library/collections/');
  await expect(page.locator('main .organization-card').first()).toContainText(
    'learning items',
  );
  await expect(page.locator('main .organization-card').first()).toContainText(
    'resources',
  );
  await page.locator('main .organization-card').first().click();
  await expect(page).toHaveURL(
    /\/library\/collections\/programming-pytorch-deep-learning\//,
  );
});

test('organization cards use singular labels for one learning item, resource and project', async ({
  page,
}) => {
  await page.goto('/library/collections/programming-pytorch-deep-learning/');
  const cards = page.locator('main .organization-card');
  await expect(cards.first().locator('.organization-counts')).toHaveText(
    '1 learning item · 0 resources',
  );
  await expect(
    cards.filter({ hasText: 'Chapter 4:' }).locator('.organization-counts'),
  ).toHaveText('0 learning items · 1 resource');
  await page.goto('/library/collections/react-complete-guide/');
  await expect(
    page
      .locator('main .organization-card')
      .filter({ hasText: '02 JS Refresher' })
      .locator('.organization-counts'),
  ).toHaveText('2 learning items · 4 resources · 1 project');
  await expect(page.locator('main')).not.toContainText(/\b1 projects\b/);
});
