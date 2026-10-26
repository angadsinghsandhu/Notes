import { expect, test } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';
import { resolve } from 'node:path';
const collection = '/library/collections/react-complete-guide/';
const book = '/library/collections/programming-pytorch-deep-learning/';
const transformer =
  '/notes/interview/applied-science/breadth/6-6-2-transformers/';
const topic = '/library/topics/attention-transformers-language-models/';
const project =
  collection + 'groups/project-03-react-essentials-01-starting-project/';
const screenshots = resolve(
  '../.superpowers/sdd/2026-10-21-library-information-architecture/task-5-screenshots',
);
test('transformer topic opens the actual evidenced pilot reader', async ({
  page,
}) => {
  await page.goto(topic);
  await page.locator('main a[href="' + transformer + '"]').click();
  await expect(page.locator('article')).toContainText('Transformer');
  await expect(
    page.getByRole('navigation', { name: 'Previous and next notes' }),
  ).toContainText('6.6.1');
});
test('book chapter opens its notebook and canonical original-source action', async ({
  page,
}) => {
  await page.goto(book);
  await page
    .locator('main .organization-card')
    .filter({ hasText: 'Chapter 2:' })
    .click();
  const notebook = page.locator(
    '[data-organization-documents] a[href$="/ch2/"]',
  );
  await expect(notebook).toHaveCount(1);
  await notebook.click();
  await expect(
    page.getByRole('link', { name: 'View original source' }),
  ).toHaveAttribute('href', /github.com/);
  await expect(page.locator('.organization-metadata')).toContainText(
    'Chapter 2',
  );
});
test('React module reaches a distinct snapshot source tree and canonical file reader', async ({
  page,
}) => {
  await page.goto(collection);
  await page
    .locator('main .organization-card')
    .filter({ hasText: '03 React Essentials' })
    .click();
  await expect(page.locator('main .organization-card')).toHaveCount(18);
  await page
    .locator('main .organization-card')
    .filter({ hasText: '01-starting-project' })
    .click();
  await expect(page).toHaveURL(new RegExp(project));
  await page
    .locator('main [data-project-files] details > summary')
    .first()
    .click();
  const source = page
    .locator('main [data-project-files] a[href^="/resources/"]')
    .first();
  await source.click();
  await expect(page.locator('article')).toBeVisible();
  await expect(page.locator('.organization-metadata')).toContainText(
    '01-starting-project',
  );
  await expect(page.locator('main [data-project-files]')).toHaveCount(0);
  await expect(
    page.locator('.section-navigation a[href*="/resources/"]'),
  ).toHaveCount(0);
});
test('source archive and full original folder tree remain reachable', async ({
  page,
}) => {
  await page.goto('/library/');
  await page
    .locator('main')
    .getByRole('link', { name: 'Source Archive', exact: true })
    .click();
  await expect(page.locator('#source-archive')).toBeVisible();
  await page
    .locator('main')
    .getByRole('link', { name: 'Explore the complete folder tree' })
    .click();
  await expect(page.getByRole('heading', { level: 1 })).toHaveText(
    'Folder tree',
  );
});
for (const width of [320, 375, 768, 1280])
  for (const theme of ['light', 'dark']) {
    test(`curated browsing ${width}px ${theme} wraps labels, aligns breadcrumbs and keeps controls accessible`, async ({
      page,
    }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.addInitScript(
        (value) => localStorage.setItem('notes-theme', value),
        theme,
      );
      for (const route of [
        '/library/',
        '/library/topics/',
        topic,
        '/library/collections/',
        collection,
        project,
        book + 'groups/chapter-4/',
        '/library/paths/applied-scientist-interview-preparation/',
        transformer,
      ]) {
        await page.goto(route);
        await expect(
          route === transformer
            ? page.locator('.reader-header h1')
            : page.getByRole('heading', { level: 1 }),
        ).toBeVisible();
        expect(
          await page.evaluate(
            () => document.documentElement.scrollWidth <= innerWidth,
          ),
        ).toBe(true);
        const small = await page
          .locator('a, button, select, summary')
          .evaluateAll((elements) =>
            elements
              .filter((el) => {
                const b = el.getBoundingClientRect();
                return (
                  b.width > 0 &&
                  b.height > 0 &&
                  getComputedStyle(el).visibility !== 'hidden' &&
                  (b.width < 44 || b.height < 44)
                );
              })
              .map((el) => el.textContent?.trim().slice(0, 80)),
          );
        expect(small).toEqual([]);
        const rows = await page
          .locator('.breadcrumbs li')
          .evaluateAll((items) =>
            items.map((el) => {
              const b = el.getBoundingClientRect();
              return {
                top: b.top,
                bottom: b.bottom,
                center: b.top + b.height / 2,
              };
            }),
          );
        for (let i = 1; i < rows.length; i++)
          if (
            Math.max(rows[i]!.top, rows[i - 1]!.top) <
            Math.min(rows[i]!.bottom, rows[i - 1]!.bottom)
          )
            expect(
              Math.abs(rows[i]!.center - rows[i - 1]!.center),
            ).toBeLessThan(2);
      }
      await page.goto(collection);
      await page.screenshot({
        path: resolve(screenshots, `collection-${width}-${theme}.png`),
      });
      await page.goto(project);
      await page.screenshot({
        path: resolve(screenshots, `project-${width}-${theme}.png`),
      });
      for (const [name, route] of [
        ['book-chapter', book + 'groups/chapter-2/'],
        ['transformer-topic', topic],
        ['transformer-reader', transformer],
      ]) {
        await page.goto(route!);
        await page.screenshot({
          path: resolve(screenshots, `${name}-${width}-${theme}.png`),
        });
      }
    });
  }
for (const theme of ['light', 'dark'])
  test(`curated pages have no serious or critical Axe findings in ${theme}`, async ({
    page,
  }) => {
    await page.addInitScript(
      (value) => localStorage.setItem('notes-theme', value),
      theme,
    );
    for (const route of [
      '/library/',
      '/library/topics/',
      topic,
      '/library/collections/',
      collection,
      project,
      book + 'groups/chapter-4/',
      '/library/paths/applied-scientist-interview-preparation/',
    ]) {
      await page.goto(route);
      const result = await new AxeBuilder({ page }).analyze();
      expect(
        result.violations.filter((v) =>
          ['serious', 'critical'].includes(v.impact ?? ''),
        ),
      ).toEqual([]);
    }
  });
test('native curated cards and trees remain usable without JavaScript', async ({
  browser,
}) => {
  const context = await browser.newContext({
    javaScriptEnabled: false,
    viewport: { width: 375, height: 900 },
  });
  const page = await context.newPage();
  await page.goto('/library/');
  await page
    .locator('main .organization-card')
    .filter({ hasText: 'Collections' })
    .click();
  await page
    .locator('main .organization-card')
    .filter({ hasText: 'Programming PyTorch' })
    .click();
  await page
    .locator('main .organization-card')
    .filter({ hasText: 'Chapter 2:' })
    .click();
  await page.locator('[data-organization-documents] a').first().click();
  await expect(page.locator('article')).toBeVisible();
  await page.locator('.no-js-navigation > summary').click();
  await expect(
    page
      .locator('.no-js-navigation')
      .getByRole('link', { name: 'Topics', exact: true }),
  ).toBeVisible();
  await context.close();
});
test('keyboard cards retain visible focus and canonical listing SEO', async ({
  page,
  request,
}) => {
  await page.goto('/library/');
  const link = page.locator('main .organization-card').first();
  await link.focus();
  await page.keyboard.press('Tab');
  await page.keyboard.press('Shift+Tab');
  await expect(link).toBeFocused();
  expect(await link.evaluate((el) => getComputedStyle(el).outlineWidth)).toBe(
    '3px',
  );
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Topics');
  await expect(page.locator('link[rel=canonical]')).toHaveAttribute(
    'href',
    'https://notes.example.test/library/topics/',
  );
  const xml = await (await request.get('/sitemap.xml')).text();
  expect(xml).toContain('https://notes.example.test' + project);
  expect(await (await request.get(topic)).text()).not.toContain(
    'data-pagefind-body',
  );
});
