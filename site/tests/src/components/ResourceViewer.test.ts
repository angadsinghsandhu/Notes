import { expect, test } from '@playwright/test';
import { readPreparedCatalog } from '../../../src/lib/catalog.js';

const catalog = await readPreparedCatalog();
const entries = catalog.listEntries();
const pdf = entries.find(
  (e) => e.kind === 'pdf' && e.assetUrl?.startsWith('/'),
)!;
const large = entries.find((e) => e.kind === 'pdf' && e.bytes > 26_214_400)!;
const slides = entries.find((e) => e.kind === 'slides')!;
test('PDF has a responsive preview and all-viewport source actions', async ({
  page,
}) => {
  await page.goto(pdf.route);
  await expect(
    page.getByRole('link', { name: 'Open PDF', exact: true }),
  ).toHaveAttribute('href', pdf.assetUrl!);
  await expect(
    page.getByRole('link', { name: 'Download PDF', exact: true }),
  ).toHaveAttribute('download', '');
  await page.locator('[data-pdf-viewer]').scrollIntoViewIfNeeded();
  await expect(page.locator('[data-pdf-stage] canvas')).toBeVisible();
  await page.setViewportSize({ width: 320, height: 800 });
  await expect(
    page.getByRole('link', { name: 'Open PDF', exact: true }),
  ).toBeVisible();
  await expect(page.locator('[data-pdf-stage] canvas')).toBeVisible();
  await expect(page.locator('iframe')).toHaveCount(0);
});

test('slide and oversized resources are honest', async ({ page }) => {
  await page.goto(slides.route);
  await expect(
    page.getByRole('link', { name: 'Download slides' }),
  ).toHaveAttribute('href', slides.assetUrl!);
  await expect(page.locator('iframe')).toHaveCount(0);
  await page.goto(large.route);
  await expect(
    page.getByRole('link', { name: 'Open external source' }),
  ).toHaveAttribute('href', large.sourceUrl!);
  await expect(page.locator('iframe')).toHaveCount(0);
  await expect(page.getByRole('link', { name: 'Open PDF' })).toHaveCount(0);
});

const longestFilename = entries
  .filter((e) => !['markdown', 'notebook'].includes(e.kind))
  .sort(
    (a, b) =>
      (b.sourcePath.split('/').at(-1)?.length ?? 0) -
      (a.sourcePath.split('/').at(-1)?.length ?? 0),
  )[0]!;
for (const width of [320, 375, 768, 1024, 1440]) {
  for (const theme of ['light', 'dark']) {
    test(`real long resource filename stays usable ${width}px ${theme}`, async ({
      page,
    }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.addInitScript(
        (value) => localStorage.setItem('notes-theme', value),
        theme,
      );
      await page.goto(longestFilename.route);
      await expect(page.locator('.resource-details')).toContainText(
        longestFilename.sourcePath.split('/').at(-1)!,
      );
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      ).toBe(true);
      await page.screenshot({
        path: `../.superpowers/sdd/2026-10-04-notes-website/screenshots/resource-${width}-${theme}.png`,
      });
    });
  }
}
