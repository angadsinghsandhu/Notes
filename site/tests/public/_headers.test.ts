import { expect, test } from '@playwright/test';
import { createServer, request as upstreamRequest } from 'node:http';
import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { readPreparedCatalog } from '../../src/lib/catalog.js';

test.use({ channel: 'chromium' });
declare global {
  interface Window {
    headerViolations: string[];
  }
}

// Local compatibility proof, not Cloudflare parsing or a live-host check.
test('built response policy permits the actual theme, math, search, images and native PDF', async ({
  page,
  request,
}) => {
  test.setTimeout(120_000);
  const built = await readFile('dist/_headers', 'utf8');
  expect(built).toBe(await readFile('public/_headers', 'utf8'));
  const lines = built.trimEnd().split('\n');
  expect(lines.shift()).toBe('/*');
  expect(lines).toHaveLength(4);
  const headers = Object.fromEntries(
    lines.map((line) => {
      expect(line.length).toBeLessThanOrEqual(2000);
      const match = /^ {2}([A-Za-z-]+): (.+)$/.exec(line);
      expect(match).not.toBeNull();
      return [match![1]!.toLowerCase(), match![2]!];
    }),
  );
  const csp = headers['content-security-policy']!;
  expect(headers).toMatchObject({
    'x-content-type-options': 'nosniff',
    'x-frame-options': 'SAMEORIGIN',
    'referrer-policy': 'strict-origin-when-cross-origin',
  });
  expect(csp).toContain(
    "script-src 'self' 'wasm-unsafe-eval' 'sha256-+vBxHCmbBgzwPWfoMU+qssZj2N1wXWZmmEoIDtbDpM0='",
  );
  expect(csp).toContain("style-src 'self' 'unsafe-inline'");
  expect(csp).toContain("img-src 'self' data: https:");
  expect(csp).toContain('upgrade-insecure-requests');
  expect(csp).toContain("frame-src 'self'");
  expect(csp).toContain("frame-ancestors 'self'");
  expect(csp).not.toContain("script-src 'self' 'unsafe-inline'");
  expect(csp).not.toContain("'unsafe-eval'");

  // The one /* block above applies unchanged to streamed preview responses.
  // Streaming also preserves the native viewer's PDF range requests.
  const proxy = createServer((incoming, response) => {
    const upstream = upstreamRequest(
      {
        hostname: '127.0.0.1',
        port: 4328,
        path: incoming.url,
        method: incoming.method,
        headers: { ...incoming.headers, host: '127.0.0.1:4328' },
      },
      (result) => {
        response.writeHead(result.statusCode!, {
          ...result.headers,
          ...headers,
        });
        result.pipe(response);
      },
    );
    upstream.on('error', () => {
      response.writeHead(502);
      response.end('Local preview unavailable');
    });
    incoming.pipe(upstream);
  });
  await new Promise<void>((done, reject) => {
    proxy.once('error', reject);
    proxy.listen(0, '127.0.0.1', done);
  });
  const address = proxy.address();
  if (!address || typeof address === 'string') throw new Error('No proxy port');
  const origin = `http://127.0.0.1:${address.port}`;
  try {
    await page.addInitScript(() => {
      const windowWithEvidence = window;
      windowWithEvidence.headerViolations = [];
      document.addEventListener('securitypolicyviolation', (event) => {
        windowWithEvidence.headerViolations.push(
          `${event.violatedDirective}: ${event.blockedURI}`,
        );
      });
      if (!localStorage.getItem('notes-theme'))
        localStorage.setItem('notes-theme', 'dark');
    });
    await page.route('**/_astro/*.js', (route) => route.abort());
    const home = (await page.goto(`${origin}/`))!;
    expect(home.status()).toBe(200);
    expect(await home.allHeaders()).toMatchObject(headers);
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    const inline = await page.locator('script:not([src])').allTextContents();
    expect(inline).toHaveLength(1);
    expect(createHash('sha256').update(inline[0]!).digest('base64')).toBe(
      '+vBxHCmbBgzwPWfoMU+qssZj2N1wXWZmmEoIDtbDpM0=',
    );
    expect(await page.evaluate(() => window.headerViolations)).toEqual([]);
    await page.unroute('**/_astro/*.js');
    await page.reload();
    await page
      .getByRole('combobox', { name: 'Theme', exact: true })
      .selectOption('light');
    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
    expect(await page.evaluate(() => localStorage.getItem('notes-theme'))).toBe(
      'light',
    );
    expect(await page.evaluate(() => window.headerViolations)).toEqual([]);

    const font = page.waitForResponse(
      (response) => response.request().resourceType() === 'font',
    );
    await page.goto(`${origin}/notes/classes/johns-hopkins/sem-1/nlp/week-1/`);
    const fontResponse = await font;
    expect(fontResponse.ok()).toBe(true);
    expect(await fontResponse.allHeaders()).toMatchObject(headers);
    await page.evaluate(() => document.fonts.ready);
    expect(
      await page
        .locator('.katex .katex-strut')
        .first()
        .evaluate((element) => parseFloat(getComputedStyle(element).height)),
    ).toBeGreaterThan(0);
    expect(
      await page.evaluate(() =>
        Array.from(document.fonts).some(
          (font) => font.family.includes('KaTeX') && font.status === 'loaded',
        ),
      ),
    ).toBe(true);
    expect(await page.evaluate(() => window.headerViolations)).toEqual([]);

    // Deterministic transport only: existing local PNG bytes stand in for remote
    // image payloads. This proves original URLs, native HTTPS upgrade and CSP,
    // not upstream HTTPS availability or the remote images' actual content.
    const pngName = (await readdir('dist/content-assets')).find((name) =>
      name.endsWith('.png'),
    )!;
    const png = await readFile(`dist/content-assets/${pngName}`);
    const imageRequests: string[] = [];
    await page.route('https://**/*', async (route) => {
      expect(route.request().resourceType()).toBe('image');
      imageRequests.push(route.request().url());
      await route.fulfill({ contentType: 'image/png', body: png });
    });
    const codeRoute =
      '/notes/books/programming-pytorch-for-deep-learning-ian-pointer/chapter-2-image-clasification-with-pytorch/';
    await page.goto(`${origin}${codeRoute}`);
    const httpsImage =
      'https://cdn.analyticsvidhya.com/wp-content/uploads/2021/02/Screenshot-from-2021-02-25-13-19-20-244x300.png';
    await expect(page.locator(`img[src="${httpsImage}"]`)).toBeVisible();
    await expect
      .poll(() =>
        page
          .locator(`img[src="${httpsImage}"]`)
          .evaluate((element) => (element as HTMLImageElement).naturalWidth),
      )
      .toBeGreaterThan(0);
    expect(imageRequests).toContain(httpsImage);
    expect(
      await page
        .locator('pre.shiki')
        .first()
        .evaluate((element) => getComputedStyle(element).backgroundColor),
    ).toBe('rgb(30, 41, 59)');
    expect(
      await page
        .locator('pre.shiki span[style]')
        .first()
        .evaluate((element) => getComputedStyle(element).color),
    ).toBe('rgb(249, 117, 131)');
    expect(await page.evaluate(() => window.headerViolations)).toEqual([]);
    const historical =
      'http://www.laurencemoroney.com/wp-content/uploads/2019/07/plot1.png';
    await page.goto(
      `${origin}/notes/courses/coursera/deep-learning-ai-course/tensorflow-in-practice/course-4-s-p/s-p-week-2-exercise-question/`,
    );
    await expect(page.locator(`img[src="${historical}"]`)).toBeVisible();
    await expect
      .poll(() =>
        page
          .locator(`img[src="${historical}"]`)
          .evaluate((element) => (element as HTMLImageElement).naturalWidth),
      )
      .toBeGreaterThan(0);
    expect(imageRequests).toContain(historical.replace('http:', 'https:'));
    expect(imageRequests).not.toContain(historical);
    expect(await page.evaluate(() => window.headerViolations)).toEqual([]);
    console.log(
      'Deterministic image transport: original HTTPS URL decoded; historical HTTP src retained and native outgoing request upgraded to HTTPS. Upstream availability unverified.',
    );

    const wasm = page.waitForResponse((response) =>
      /\/pagefind\/wasm\./.test(response.url()),
    );
    await page.goto(`${origin}/search/`);
    await page.getByRole('searchbox').fill('scaled dot');
    await page.getByRole('button', { name: 'Search', exact: true }).click();
    await expect(page.locator('[data-search-results]')).toContainText(
      'Transformer Architecture',
    );
    const wasmResponse = await wasm;
    expect(wasmResponse.ok()).toBe(true);
    expect(await wasmResponse.allHeaders()).toMatchObject(headers);
    const wasmName = new URL(wasmResponse.url()).pathname.split('/').at(-1)!;
    expect(await wasmResponse.body()).toEqual(
      await readFile(`dist/pagefind/${wasmName}`),
    );
    expect(await page.evaluate(() => window.headerViolations)).toEqual([]);

    const catalog = await readPreparedCatalog();
    const pdf = catalog
      .listEntries()
      .find(
        (entry) => entry.kind === 'pdf' && entry.assetUrl?.startsWith('/'),
      )!;
    const asset = await request.get(`${origin}${pdf.assetUrl}`);
    expect(asset.ok()).toBe(true);
    expect(asset.headers()).toMatchObject(headers);
    expect(asset.headers()['content-type']).toMatch(/^application\/pdf\b/);
    expect((await asset.body()).subarray(0, 5).toString()).toBe('%PDF-');
    await page.goto(`${origin}${pdf.route}`);
    await page.locator('iframe[title="PDF preview"]').scrollIntoViewIfNeeded();
    await expect
      .poll(() =>
        page
          .frames()
          .some((frame) => frame.url().startsWith('chrome-extension://')),
      )
      .toBe(true);
    const viewer = page
      .frames()
      .find((frame) => frame.url().startsWith('chrome-extension://'))!;
    await expect
      .poll(() =>
        viewer.evaluate(() => {
          const documentViewer = document.querySelector('pdf-viewer') as
            (HTMLElement & { loadState_?: string; docLength_?: number }) | null;
          return {
            load: documentViewer?.loadState_,
            pages: documentViewer?.docLength_,
          };
        }),
      )
      .toEqual({ load: 'success', pages: 220 });
    expect(await page.evaluate(() => window.headerViolations)).toEqual([]);
    await page.screenshot({
      path: '../.superpowers/sdd/2026-10-04-notes-website/task-8-headers-native-pdf.png',
      fullPage: true,
    });
    console.log(
      'Actual built-header local proxy: exact theme SHA and persisted choice, loaded KaTeX font/inline strut, Shiki styles, native Pagefind WASM/search, native PDF loadState=success/docLength=220; no CSP violations on tested documents.',
    );
  } finally {
    proxy.closeAllConnections();
    await new Promise<void>((done, reject) =>
      proxy.close((error) => (error ? reject(error) : done())),
    );
  }
});
