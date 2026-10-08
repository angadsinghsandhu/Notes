import { expect, test } from '@playwright/test';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { resolve } from 'node:path';
const execute = promisify(execFile);

test('sitemap and canonical output require an explicit HTTPS production URL', async ({
  request,
  page,
}) => {
  test.setTimeout(180_000);
  const incoming = { ...process.env };
  const unconfigured = { ...incoming };
  delete unconfigured['SITE_URL'];
  const configured = { ...incoming, SITE_URL: 'https://notes.example.test' };
  try {
    await execute('npm', ['exec', 'astro', 'build'], {
      cwd: resolve('.'),
      env: unconfigured,
      maxBuffer: 32 * 1024 * 1024,
    });
    expect((await request.get('/sitemap.xml')).status()).toBe(404);
    expect(await (await request.get('/')).text()).not.toContain(
      'rel="canonical"',
    );
    await execute('npm', ['run', 'build'], {
      cwd: resolve('.'),
      env: configured,
      maxBuffer: 32 * 1024 * 1024,
    });
    const response = await request.get('/sitemap.xml');
    expect(response.status()).toBe(200);
    const xml = await response.text();
    expect(
      await page.evaluate(
        (source) =>
          new DOMParser()
            .parseFromString(source, 'application/xml')
            .querySelectorAll('parsererror').length,
        xml,
      ),
    ).toBe(0);
    expect(xml).toContain(
      'https://notes.example.test/notes/interview/applied-science/breadth/6-6-2-transformers/',
    );
    expect(await (await request.get('/')).text()).toContain(
      'href="https://notes.example.test/"',
    );
    for (const SITE_URL of [
      'http://notes.example.test',
      'https://user:secret@notes.example.test',
      'https://notes.example.test/?token=secret',
    ]) {
      await expect(
        execute('npm', ['exec', 'astro', 'build'], {
          cwd: resolve('.'),
          env: { ...process.env, SITE_URL },
          maxBuffer: 32 * 1024 * 1024,
        }),
      ).rejects.toThrow();
    }
  } finally {
    await execute('npm', ['run', 'build'], {
      cwd: resolve('.'),
      env: incoming,
      maxBuffer: 32 * 1024 * 1024,
    });
  }
  const response = await request.get('/sitemap.xml');
  const home = await (await request.get('/')).text();
  if (incoming['SITE_URL']) {
    expect(response.status()).toBe(200);
    expect(await response.text()).toContain(
      new URL('/library/', incoming['SITE_URL']).href,
    );
    expect(home).toContain(`href="${new URL('/', incoming['SITE_URL']).href}"`);
  } else {
    expect(response.status()).toBe(404);
    expect(home).not.toContain('rel="canonical"');
  }
});
