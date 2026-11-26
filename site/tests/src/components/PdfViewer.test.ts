import { expect, test } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';
import { readPreparedCatalog } from '../../../src/lib/catalog.js';

const entries = (await readPreparedCatalog()).listEntries();
const route =
  '/resources/classes/johns-hopkins/sem-1/ml-dl/mock-exams/cs482682-mock-exam-fall-2023-solutions-pdf/';
const exam = entries.find((entry) => entry.route === route)!;
const other = entries.find(
  (entry) =>
    entry.kind === 'pdf' &&
    entry.assetUrl?.startsWith('/') &&
    entry.route !== route,
)!;
for (const entry of [exam, other]) {
  test(`actual PDF pixels, selectable text, navigation, zoom and mobile: ${entry.title}`, async ({
    page,
  }) => {
    const errors: string[] = [];
    page.on('pageerror', (error) => errors.push(error.message));
    const worker = page.waitForResponse((response) =>
      response.url().endsWith('/pdfjs/pdf.worker.min.mjs'),
    );
    await page.goto(entry.route);
    await page.locator('[data-pdf-viewer]').scrollIntoViewIfNeeded();
    await expect(page.locator('[data-pdf-status]')).toHaveText(/Page 1 of \d+/);
    expect((await worker).ok()).toBe(true);
    expect(
      (await new AxeBuilder({ page }).include('[data-pdf-viewer]').analyze())
        .violations,
    ).toEqual([]);
    const canvas = page.locator('[data-pdf-stage] canvas');
    await expect(canvas).toBeVisible();
    expect(
      await canvas.evaluate((element) => {
        const canvas = element as HTMLCanvasElement;
        const bytes = canvas
          .getContext('2d')!
          .getImageData(0, 0, canvas.width, canvas.height).data;
        let dark = 0;
        for (let i = 0; i < bytes.length; i += 4)
          if (bytes[i]! < 180 && bytes[i + 3]! > 0) dark++;
        return dark;
      }),
    ).toBeGreaterThan(100);
    expect(
      await page.locator('.textLayer').evaluate((element) => {
        const range = document.createRange();
        range.selectNodeContents(element);
        const selection = window.getSelection()!;
        selection.removeAllRanges();
        selection.addRange(range);
        return selection.toString().trim().length;
      }),
    ).toBeGreaterThan(20);
    await page.screenshot({
      path: `../.superpowers/sdd/2026-10-19-pdf-viewer/pdf-selected-${entry === exam ? 'exam' : 'archive'}.png`,
      fullPage: true,
    });
    const span = page
      .locator('.textLayer span')
      .filter({ hasText: /\w/ })
      .first();
    expect(
      await span.evaluate((element) => element.getBoundingClientRect().height),
    ).toBeGreaterThan(4);
    const geometry = await page.locator('.pdf-page').evaluate((element) => {
      const bitmap = element.querySelector('canvas')!;
      const bounds = bitmap.getBoundingClientRect();
      const context = bitmap.getContext('2d')!;
      return [...element.querySelectorAll('.textLayer span')]
        .filter((span) => (span.textContent?.trim().length ?? 0) > 4)
        .slice(0, 10)
        .map((span) => {
          const box = span.getBoundingClientRect();
          const x = Math.max(
            0,
            Math.floor(
              ((box.left - bounds.left) * bitmap.width) / bounds.width,
            ),
          );
          const y = Math.max(
            0,
            Math.floor(
              ((box.top - bounds.top) * bitmap.height) / bounds.height,
            ),
          );
          const width = Math.min(
            bitmap.width - x,
            Math.ceil((box.width * bitmap.width) / bounds.width),
          );
          const height = Math.min(
            bitmap.height - y,
            Math.ceil((box.height * bitmap.height) / bounds.height),
          );
          let dark = 0;
          if (width > 0 && height > 0) {
            const pixels = context.getImageData(x, y, width, height).data;
            for (let i = 0; i < pixels.length; i += 4)
              if (pixels[i]! < 180 && pixels[i + 3]! > 0) dark++;
          }
          return { text: span.textContent, dark, width, height };
        });
    });
    expect(
      geometry.filter((sample) => sample.dark > 10).length,
    ).toBeGreaterThanOrEqual(3);
    console.log(
      'PDF selectable text overlays actual ink',
      entry.title,
      geometry,
    );
    const initial = await canvas.evaluate(
      (element) => (element as HTMLCanvasElement).width,
    );
    await page
      .getByRole('button', { name: 'Zoom in PDF', exact: true })
      .click();
    await expect
      .poll(() =>
        canvas.evaluate((element) => (element as HTMLCanvasElement).width),
      )
      .toBeGreaterThan(initial);
    for (let i = 0; i < 2; i++) {
      await page
        .getByRole('button', { name: 'Zoom in PDF', exact: true })
        .click();
      await expect(page.locator('[data-pdf-status]')).toHaveText(
        /Page 1 of \d+/,
      );
    }
    const scroll = page.getByRole('region', {
      name: 'PDF page, scroll to read when zoomed',
      exact: true,
    });
    await expect(scroll).toHaveAttribute('tabindex', '0');
    await scroll.focus();
    await page.keyboard.press('PageDown');
    await expect
      .poll(() => scroll.evaluate((element) => element.scrollTop))
      .toBeGreaterThan(0);
    await page
      .getByRole('button', { name: 'Next PDF page', exact: true })
      .focus();
    await page.keyboard.press('Enter');
    await expect(page.locator('[data-pdf-status]')).toHaveText(/Page 2 of \d+/);
    await page.getByRole('spinbutton', { name: 'PDF page number' }).fill('1');
    await page
      .getByRole('button', { name: 'Go to PDF page', exact: true })
      .click();
    await expect(page.locator('[data-pdf-status]')).toHaveText(/Page 1 of \d+/);
    for (const width of [320, 375, 1024]) {
      await page.setViewportSize({ width, height: 900 });
      await page
        .getByRole('button', { name: 'Fit width', exact: true })
        .click();
      await expect(page.locator('[data-pdf-status]')).toHaveText(
        /Page 1 of \d+/,
      );
      await expect(canvas).toBeVisible();
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      ).toBe(true);
      const controls = await page
        .locator('.pdf-toolbar button, .pdf-toolbar input')
        .evaluateAll((elements) =>
          elements
            .filter((element) => !(element as HTMLElement).hidden)
            .map((element) => element.getBoundingClientRect().height),
        );
      expect(controls.every((height) => height >= 44)).toBe(true);
      await page.screenshot({
        path: `../.superpowers/sdd/2026-10-19-pdf-viewer/pdf-${entry === exam ? 'exam' : 'archive'}-${width}.png`,
        fullPage: true,
      });
    }
    await page.getByRole('button', { name: 'Next PDF page' }).click();
    await page.getByRole('button', { name: 'Zoom in PDF' }).click();
    await page.getByRole('button', { name: 'Fit width' }).click();
    await expect(page.locator('[data-pdf-status]')).toHaveText(/Page 2 of \d+/);
    await expect(canvas).toHaveCount(1);
    expect(errors).toEqual([]);
  });
}
test('corrupt PDF offers retry and keeps the source actions usable', async ({
  page,
}) => {
  await page.route(`**${exam.assetUrl}`, (request) =>
    request.fulfill({ contentType: 'application/pdf', body: 'corrupt PDF' }),
  );
  await page.goto(exam.route);
  await page.locator('[data-pdf-viewer]').scrollIntoViewIfNeeded();
  await expect(page.locator('[data-pdf-status]')).toContainText('unavailable');
  await expect(
    page.getByRole('link', { name: 'Open PDF', exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole('link', { name: 'Download PDF', exact: true }),
  ).toBeVisible();
  await page.unroute(`**${exam.assetUrl}`);
  await page
    .getByRole('button', { name: 'Retry preview', exact: true })
    .click();
  await expect(page.locator('[data-pdf-status]')).toHaveText(/Page 1 of \d+/);
});
test('ordinary notes and slides never fetch the PDF runtime, worker or document', async ({
  page,
}) => {
  const requests: string[] = [];
  page.on('request', (request) => requests.push(request.url()));
  for (const entry of [
    entries.find((entry) => entry.kind === 'markdown')!,
    entries.find((entry) => entry.kind === 'slides')!,
  ]) {
    await page.goto(entry.route);
    await expect(page.locator('main')).toBeVisible();
    await expect(page.locator('[data-pdf-viewer]')).toHaveCount(0);
  }
  expect(
    requests.filter((url) =>
      /\/pdfjs\/|\/pdf\.[^/]+\.js|\/content-assets\/[^/]+\.pdf/.test(url),
    ),
  ).toEqual([]);
});

test('page navigation resets both reading offsets while same-page zoom preserves them', async ({
  page,
}) => {
  await page.setViewportSize({ width: 375, height: 900 });
  await page.goto(exam.route);
  await page.locator('[data-pdf-viewer]').scrollIntoViewIfNeeded();
  const status = page.locator('[data-pdf-status]');
  const viewport = page.locator('[data-pdf-viewport]');
  const canvas = page.locator('[data-pdf-stage] canvas');
  await expect(status).toHaveText('Page 1 of 7');
  for (let i = 0; i < 4; i++) {
    await page
      .getByRole('button', { name: 'Zoom in PDF', exact: true })
      .click();
    await expect(status).toHaveText('Page 1 of 7');
  }
  const readBottom = async () => {
    const offset = await viewport.evaluate((element) => {
      element.scrollTop = element.scrollHeight;
      element.scrollLeft = element.scrollWidth;
      return { top: element.scrollTop, left: element.scrollLeft };
    });
    expect(offset.top).toBeGreaterThan(0);
    expect(offset.left).toBeGreaterThan(0);
    return offset;
  };
  const offsets = () =>
    viewport.evaluate((element) => ({
      top: element.scrollTop,
      left: element.scrollLeft,
    }));
  const beforeZoom = await readBottom();
  const width = await canvas.evaluate(
    (element) => (element as HTMLCanvasElement).width,
  );
  await page.getByRole('button', { name: 'Zoom in PDF', exact: true }).click();
  await expect
    .poll(() =>
      canvas.evaluate((element) => (element as HTMLCanvasElement).width),
    )
    .toBeGreaterThan(width);
  await expect.poll(offsets).toEqual(beforeZoom);
  await readBottom();
  await page.screenshot({
    path: '../.superpowers/sdd/2026-10-19-pdf-viewer/scroll-before-next.png',
    fullPage: true,
  });
  await page
    .getByRole('button', { name: 'Next PDF page', exact: true })
    .click();
  await expect(status).toHaveText('Page 2 of 7');
  await expect.poll(offsets).toEqual({ top: 0, left: 0 });
  await readBottom();
  await page.getByRole('spinbutton', { name: 'PDF page number' }).fill('3');
  await page
    .getByRole('button', { name: 'Go to PDF page', exact: true })
    .click();
  await expect(status).toHaveText('Page 3 of 7');
  await expect.poll(offsets).toEqual({ top: 0, left: 0 });
  await readBottom();
  await page
    .getByRole('button', { name: 'Previous PDF page', exact: true })
    .click();
  await expect(status).toHaveText('Page 2 of 7');
  await expect.poll(offsets).toEqual({ top: 0, left: 0 });
});
