import { expect, test } from '@playwright/test';

test('native contents disclose on tablet and become a rail on desktop', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1024, height: 900 });
  await page.goto(
    '/notes/interview/applied-science/breadth/6-6-2-transformers/',
  );
  await expect(page.locator('.contents-disclosure')).not.toHaveAttribute(
    'open',
    '',
  );
  await page.locator('.contents-disclosure > summary').click();
  await expect(
    page.getByRole('navigation', { name: 'On this page' }).first(),
  ).toBeVisible();
  const heading = page.locator('.contents-disclosure a').first();
  const href = await heading.getAttribute('href');
  await heading.click();
  await expect(page.locator(`[id="${href!.slice(1)}"]`)).toBeVisible();
  await page.setViewportSize({ width: 1440, height: 900 });
  await expect(page.locator('.contents-disclosure')).not.toBeVisible();
  await expect(page.locator('.contents-rail')).toBeVisible();
});
