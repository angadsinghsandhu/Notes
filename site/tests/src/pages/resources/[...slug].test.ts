import { expect, test } from '@playwright/test';

import { readPreparedCatalog } from '../../../../src/lib/catalog.js';
const code = (await readPreparedCatalog())
  .listEntries()
  .find((e) => e.sourcePath.endsWith('78_Subsets.py'))!;

test('direct code resource displays controlled escaped source', async ({
  page,
}) => {
  await page.goto(code.route);
  await expect(page.locator('pre')).toContainText('class Solution');
  await expect(
    page.getByRole('link', { name: 'View original source' }),
  ).toHaveAttribute('href', code.sourceUrl!);
});

test('code copy reports success and clipboard failure', async ({
  page,
  context,
}) => {
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  await page.goto('/resources/interview/leetcode/solutions/78-subsets-py/');
  const copy = page
    .getByRole('button', { name: 'Copy code', exact: true })
    .first();
  await copy.click();
  await expect(page.getByRole('status').first()).toContainText('Code copied');
  expect(await page.evaluate(() => navigator.clipboard.readText())).toContain(
    'class Solution',
  );
  await page.evaluate(() => {
    navigator.clipboard.writeText = async () => {
      throw new Error('Denied');
    };
  });
  await copy.click();
  await expect(page.getByRole('status').first()).toContainText('Copy failed');
});
