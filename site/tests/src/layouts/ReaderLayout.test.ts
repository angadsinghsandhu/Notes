import { expect, test } from '@playwright/test';
import { resolve } from 'node:path';
import { AxeBuilder } from '@axe-core/playwright';

const math = '/notes/interview/applied-science/breadth/6-6-2-transformers/';
const mathNote = '/notes/classes/johns-hopkins/sem-1/nlp/week-2/';
const table = '/notes/classes/johns-hopkins/sem-1/nlp/';
const screenshots = resolve(
  '../.superpowers/sdd/2026-10-04-notes-website/screenshots',
);
const notebook = '/notes/tutorials/gpu/nv-gpu-workshop/1-0-cpu-gpu-comparison/';

for (const width of [320, 375, 768, 1024, 1440]) {
  for (const theme of ['light', 'dark']) {
    test(`responsive reader ${width}px ${theme}`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.addInitScript(
        (value) => localStorage.setItem('notes-theme', value),
        theme,
      );
      for (const url of [math, mathNote, notebook, table]) {
        await page.goto(url);
        await expect(page.locator('article')).toBeVisible();
        expect(
          await page.evaluate(
            () => document.documentElement.scrollWidth <= innerWidth,
          ),
        ).toBe(true);
        await page.screenshot({
          path: resolve(
            screenshots,
            `viewport-${url === math ? 'transformer' : url === mathNote ? 'math' : url === table ? 'table' : 'notebook'}-${width}-${theme}.png`,
          ),
        });
        await page.screenshot({
          path: resolve(
            screenshots,
            `reader-${url === math ? 'transformer' : url === mathNote ? 'math' : url === table ? 'table' : 'notebook'}-${width}-${theme}.png`,
          ),
          fullPage: true,
        });
        const region = page
          .getByRole('region', {
            name:
              url === mathNote
                ? 'Mathematical formula'
                : url === table
                  ? 'Data table'
                  : 'Code or stored notebook output',
            exact: true,
          })
          .first();
        await region.focus();
        await page.screenshot({
          path: resolve(
            screenshots,
            `body-${url === math ? 'transformer' : url === mathNote ? 'math' : url === table ? 'table' : 'notebook'}-${width}-${theme}.png`,
          ),
        });
      }
    });
  }
}

for (const theme of ['light', 'dark']) {
  test(`serious and critical axe findings absent in ${theme}`, async ({
    page,
  }) => {
    await page.addInitScript(
      (value) => localStorage.setItem('notes-theme', value),
      theme,
    );
    for (const url of [
      '/',
      '/library/',
      math,
      '/resources/classes/johns-hopkins/sem-1/nlp/week-1/l1-intro-ppt/',
      '/search/',
    ]) {
      await page.goto(url);
      const result = await new AxeBuilder({ page }).analyze();
      expect(
        result.violations.filter((v) =>
          ['serious', 'critical'].includes(v.impact ?? ''),
        ),
      ).toEqual([]);
    }
  });
}

test('actual course math uses KaTeX CSS and labeled local overflow', async ({
  page,
}) => {
  await page.goto(mathNote);
  await expect(page.locator('.katex')).not.toHaveCount(0);
  expect(
    await page
      .locator('.katex')
      .first()
      .evaluate((el) => getComputedStyle(el).fontFamily),
  ).toContain('KaTeX');
  await expect(
    page.getByRole('region', { name: 'Mathematical formula' }).first(),
  ).toHaveAttribute('tabindex', '0');
});

for (const theme of ['light', 'dark']) {
  test(`visible article and search-result controls meet 44px in ${theme}`, async ({
    page,
  }) => {
    await page.setViewportSize({ width: 320, height: 900 });
    await page.addInitScript(
      (value) => localStorage.setItem('notes-theme', value),
      theme,
    );
    for (const url of [table, '/search/']) {
      await page.goto(url);
      if (url === '/search/') {
        await page.getByRole('searchbox').fill('scaled dot');
        await page.getByRole('button', { name: 'Search', exact: true }).click();
        await expect(page.locator('[data-search-results]')).toContainText(
          'Transformer Architecture',
        );
      }
      const tooSmall = await page
        .locator('a, button, select, summary, input:not(:disabled)')
        .evaluateAll((elements) =>
          elements
            .filter((el) => {
              const box = el.getBoundingClientRect();
              return (
                box.width > 0 &&
                box.height > 0 &&
                getComputedStyle(el).visibility !== 'hidden' &&
                (box.width < 44 || box.height < 44)
              );
            })
            .map((el) => ({
              label: el.textContent?.trim().slice(0, 100),
              tag: el.tagName,
              width: el.getBoundingClientRect().width,
              height: el.getBoundingClientRect().height,
            })),
        );
      expect(tooSmall, `${url} ${theme}`).toEqual([]);
    }
  });
}

test('actual wide code math and table scroll locally with keyboard focus at 320px', async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 900 });
  for (const [url, name] of [
    [math, 'Code or stored notebook output'],
    [mathNote, 'Mathematical formula'],
    [table, 'Data table'],
  ]) {
    await page.goto(url!);
    const region = page
      .getByRole('region', { name: name!, exact: true })
      .first();
    await region.focus();
    expect(await region.evaluate((el) => el.scrollWidth > el.clientWidth)).toBe(
      true,
    );
    await page.keyboard.press('ArrowRight');
    await expect
      .poll(() => region.evaluate((el) => el.scrollLeft))
      .toBeGreaterThan(0);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
  }
});
