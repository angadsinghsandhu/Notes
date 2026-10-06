import { expect, test } from '@playwright/test';

test('real transformer phrase is indexed with metadata and filters', async ({
  page,
}) => {
  await page.goto('/search/');
  await page
    .getByRole('searchbox', { name: 'Search notes and resources' })
    .fill('scaled dot');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-results]')).toContainText(
    'Transformer Architecture',
  );
  await expect(page.locator('[data-search-results]')).toContainText(
    'Interview',
  );
  await expect(page.locator('[data-search-results]')).toContainText('markdown');
  await page
    .getByRole('combobox', { name: 'Kind', exact: true })
    .selectOption('pdf');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-status]')).toContainText(
    'No results',
  );
  await page
    .getByRole('combobox', { name: 'Kind', exact: true })
    .selectOption('markdown');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-results]')).toContainText(
    'Transformer Architecture',
  );
  await page
    .getByRole('combobox', { name: 'Section', exact: true })
    .selectOption('languages');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('[data-search-status]')).toContainText(
    'No results',
  );
});
