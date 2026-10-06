import { expect, test } from '@playwright/test';
import { spawn, execFile } from 'node:child_process';
import { createServer } from 'node:net';
import {
  readFile,
  writeFile,
  rename,
  unlink,
  mkdir,
  access,
  symlink,
  readlink,
  readdir,
} from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { promisify } from 'node:util';

const site = resolve('.');
const evidence = resolve('../.superpowers/sdd/2026-10-04-notes-website');
const execute = promisify(execFile);

async function freePort(): Promise<number> {
  const socket = createServer();
  await new Promise<void>((done) => socket.listen(0, '127.0.0.1', done));
  const address = socket.address();
  if (!address || typeof address === 'string') throw new Error('No port');
  await new Promise<void>((done, reject) =>
    socket.close((e) => (e ? reject(e) : done())),
  );
  return address.port;
}

// These explicitly labelled synthetic notes exercise the real watcher and HTTP routes.
// Exact owned bytes are verified before cleanup; unexpected edits are preserved.
test('actual npm dev updates bodies, new routes, aliases and deletion without restarting Astro', async ({
  request,
  page,
}) => {
  test.setTimeout(480_000);
  const name = `task6-owned-${randomUUID()}`;
  const original = resolve('../Tutorials', `${name}.md`);
  let source = '';
  let owned = `---\ntitle: Task 6 synthetic lifecycle proof\n---\n# First lifecycle body\n`;
  const port = await freePort();
  const url = `http://127.0.0.1:${port}`;
  let output = '';
  const child = spawn('npm', ['run', 'dev', '--', '--port', String(port)], {
    cwd: site,
    detached: true,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  child.stdout.on('data', (bytes: Buffer) => {
    output += bytes.toString();
  });
  child.stderr.on('data', (bytes: Buffer) => {
    output += bytes.toString();
  });
  const exited = new Promise<void>((done) => child.once('exit', () => done()));
  const log: string[] = [];
  async function until(
    path: string,
    body: string,
    status = 200,
  ): Promise<string> {
    let last = '';
    await expect
      .poll(
        async () => {
          try {
            const response = await request.get(`${url}${path}`);
            last = await response.text();
            return response.status() === status && last.includes(body);
          } catch {
            return false;
          }
        },
        { timeout: 75_000, intervals: [500, 1000] },
      )
      .toBe(true);
    log.push(`${path} HTTP ${status} includes ${body}`);
    return last;
  }
  async function pid(): Promise<string> {
    return (
      await execute('lsof', ['-t', `-iTCP:${port}`, '-sTCP:LISTEN'])
    ).stdout.trim();
  }
  try {
    const route = `/notes/tutorials/${name}/`;
    await until(
      '/notes/interview/applied-science/breadth/6-6-2-transformers/',
      'Transformer',
    );
    const astroPid = await pid();
    const indexBefore = await readFile('dist/pagefind/pagefind-entry.json');
    expect(astroPid).toMatch(/^\d+$/);
    log.push(
      `Owned Astro listener PID ${astroPid}; npm PID ${child.pid}; port ${port}`,
    );
    await writeFile(original, owned, { flag: 'wx' });
    source = original;
    await until(route, 'First lifecycle body');
    await page.goto(`${url}${route}`);
    expect(await pid()).toBe(astroPid);
    owned = owned.replace('First lifecycle body', 'Changed lifecycle body');
    await writeFile(source, owned);
    await until(route, 'Changed lifecycle body');
    await expect(page.locator('article')).toContainText(
      'Changed lifecycle body',
      { timeout: 75_000 },
    );
    log.push('Open browser reader updated automatically after source edit');
    expect(await pid()).toBe(astroPid);
    const renamed = resolve('../Tutorials', `${name}-renamed.md`);
    await rename(source, renamed);
    source = renamed;
    owned = owned.replace('---\n#', `aliases: [${route}]\n---\n#`);
    await writeFile(source, owned);
    const newRoute = `/notes/tutorials/${name}-renamed/`;
    await until(newRoute, 'Changed lifecycle body');
    const alias = await until(route, 'noindex');
    expect(alias).toContain(newRoute);
    expect(alias).not.toContain('data-pagefind-body');
    expect(await pid()).toBe(astroPid);
    const published = owned;
    owned = owned.replace('---\n#', 'draft: true\n---\n#');
    await writeFile(source, owned);
    await until(newRoute, 'Page not found', 404);
    await until(route, 'Page not found', 404);
    expect(await pid()).toBe(astroPid);
    owned = published;
    await writeFile(source, owned);
    await until(newRoute, 'Changed lifecycle body');
    await until(route, 'noindex');
    expect(await pid()).toBe(astroPid);
    expect(await readFile('dist/pagefind/pagefind-entry.json')).toEqual(
      indexBefore,
    );
    log.push('Production Pagefind index bytes unchanged by archive edits');
    const search = await request.get(`${url}/search/`);
    expect(await search.text()).toContain('does not update with note edits');
    expect(await readFile(source, 'utf8')).toBe(owned);
    await writeFile(join(evidence, `${name}-source.txt`), owned, {
      flag: 'wx',
    });
    await unlink(source);
    source = '';
    await until(newRoute, 'Page not found', 404);
    await until(route, 'Page not found', 404);
    expect(await pid()).toBe(astroPid);
    log.push(
      `Same Astro PID ${astroPid} after modify/add/rename+alias/delete; dev notice present`,
    );
  } finally {
    if (child.pid) process.kill(-child.pid, 'SIGTERM');
    await exited;
    if (source) {
      const actual = await readFile(source, 'utf8');
      expect(actual, `Unexpected edits preserved at ${source}`).toBe(owned);
      await writeFile(join(evidence, `${name}-source.txt`), owned, {
        flag: 'wx',
      }).catch((error: unknown) => {
        if (!(
          error instanceof Error &&
          'code' in error &&
          error.code === 'EEXIST'
        ))
          throw error;
      });
      await unlink(source);
    }
    await mkdir(evidence, { recursive: true });
    await writeFile(
      join(evidence, `${name}-http.log`),
      `${log.join('\n')}\n\n${output}`,
    );
  }
});

test('built known alias and an actual owned draft are excluded from Pagefind and sitemap', async ({
  page,
  request,
}) => {
  test.setTimeout(180_000);
  const name = `task6-production-${randomUUID()}`;
  const published = resolve('../Tutorials', `${name}.md`);
  const draft = resolve('../Tutorials', `${name}-draft.md`);
  const alias = `/task6-old-${name}/`;
  const target = `/notes/tutorials/${name}/`;
  const phrase = 'saffron unpublished sentinel';
  const publicBytes = `---\ntitle: Task 6 synthetic alias proof\naliases: [${alias}]\n---\n# Public alias proof\n\nSynthetic Unicode UI fixture: 日本語 · café · λ.\n`;
  const draftBytes = `---\ntitle: Task 6 synthetic draft proof\ndraft: true\n---\n# ${phrase}\n`;
  const owned: [string, string][] = [];
  const env = { ...process.env, SITE_URL: 'https://notes.example.test' };
  const logs: string[] = [];
  try {
    await writeFile(published, publicBytes, { flag: 'wx' });
    owned.push([published, publicBytes]);
    await writeFile(draft, draftBytes, { flag: 'wx' });
    owned.push([draft, draftBytes]);
    logs.push(
      (
        await execute('npm', ['run', 'build'], {
          cwd: site,
          env,
          maxBuffer: 32 * 1024 * 1024,
        })
      ).stdout,
    );
    const response = await request.get(alias);
    expect(response.status()).toBe(200);
    const html = await response.text();
    expect(html).toContain('noindex');
    expect(html).toContain(`https://notes.example.test${target}`);
    expect(html).not.toContain('data-pagefind-body');
    const sitemap = await readFile('dist/sitemap.xml', 'utf8');
    expect(sitemap).toContain(`https://notes.example.test${target}`);
    expect(sitemap).not.toContain(alias);
    expect(sitemap).not.toContain(`${name}-draft`);
    expect(sitemap).not.toContain('/404');
    await expect(
      page.goto(`/notes/tutorials/${name}-draft/`),
    ).resolves.toBeTruthy();
    await page.setViewportSize({ width: 320, height: 900 });
    await page.goto(target);
    await expect(page.locator('article')).toContainText(
      'Synthetic Unicode UI fixture: 日本語 · café · λ.',
    );
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    for (const theme of ['light', 'dark']) {
      await page
        .getByRole('combobox', { name: 'Theme', exact: true })
        .selectOption(theme, { timeout: 5_000 });
      await page.screenshot({
        path: join(
          evidence,
          'screenshots',
          `synthetic-unicode-320-${theme}.png`,
        ),
      });
    }
    await page.goto('/search/');
    await page.getByRole('searchbox').fill('synthetic alias proof');
    await page.getByRole('button', { name: 'Search', exact: true }).click();
    await expect(page.locator('[data-search-results]')).toContainText(
      'Task 6 synthetic alias proof',
    );
    await page.getByRole('searchbox').fill(phrase);
    await page.getByRole('button', { name: 'Search', exact: true }).click();
    await expect(page.locator('[data-search-status]')).toContainText(
      'No results',
    );
    // The excluded phrase was authored before preparation, not an invented absent query.
    expect(await readFile(draft, 'utf8')).toContain(phrase);
    logs.push(
      `HTTP alias ${alias}:200/noindex/canonical target; sitemap excludes alias/draft/404; authored draft phrase ${phrase}: Pagefind no results`,
    );
  } finally {
    for (const [file, bytes] of owned) {
      expect(await readFile(file, 'utf8')).toBe(bytes);
      await writeFile(
        join(
          evidence,
          `${name}-${file === draft ? 'draft' : 'public'}-source.txt`,
        ),
        bytes,
        { flag: 'wx' },
      );
      await unlink(file);
    }
    const cleanEnv = { ...process.env };
    delete cleanEnv['SITE_URL'];
    logs.push(
      (
        await execute('npm', ['run', 'build'], {
          cwd: site,
          env: cleanEnv,
          maxBuffer: 32 * 1024 * 1024,
        })
      ).stdout,
    );
    await writeFile(join(evidence, `${name}-production.log`), logs.join('\n'));
  }
});

test('unconfigured production build emits no sitemap file', async () => {
  await expect(access('dist/sitemap.xml')).rejects.toMatchObject({
    code: 'ENOENT',
  });
});

test('development serves the last built real Pagefind index and displays its update limitation', async ({
  page,
}) => {
  test.setTimeout(120_000);
  const port = await freePort();
  const url = `http://127.0.0.1:${port}`;
  let output = '';
  const entryBefore = await readFile('dist/pagefind/pagefind-entry.json');
  const child = spawn('npm', ['run', 'dev', '--', '--port', String(port)], {
    cwd: site,
    detached: true,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  child.stdout.on('data', (bytes: Buffer) => {
    output += bytes.toString();
  });
  child.stderr.on('data', (bytes: Buffer) => {
    output += bytes.toString();
  });
  const exited = new Promise<void>((done) => child.once('exit', () => done()));
  const outside = resolve('src/lib/catalog.ts');
  const link = resolve('dist/pagefind', `task6-link-${randomUUID()}.js`);
  let linked = false;
  let moved = false;
  const indexRoot = resolve('dist/pagefind');
  const backup = resolve('dist', `task6-index-backup-${randomUUID()}`);
  try {
    await symlink(outside, link);
    linked = true;
    await expect
      .poll(
        async () => {
          try {
            return (await page.request.get(`${url}/search/`)).status();
          } catch {
            return 0;
          }
        },
        { timeout: 75_000, intervals: [500, 1000] },
      )
      .toBe(200);
    await page.goto(`${url}/search/`);
    await expect(page.locator('.development-search-notice')).toContainText(
      'does not update with note edits',
    );
    await page.getByRole('searchbox').fill('scaled dot');
    await page.getByRole('button', { name: 'Search', exact: true }).click();
    await expect(page.locator('[data-search-results]')).toContainText(
      'Transformer Architecture',
    );
    const linkResponse = await page.request.get(
      `${url}/pagefind/${link.split('/').at(-1)}`,
    );
    expect(linkResponse.status()).toBe(404);
    expect(await linkResponse.text()).not.toContain('readPreparedCatalog');
    const traversal = await page.request.get(
      `${url}/pagefind/%2e%2e%2f..%2fsrc%2flib%2fcatalog.ts`,
    );
    expect(traversal.status()).toBe(404);
    expect(await traversal.text()).not.toContain('preparedBodies');
    const wasms = (await readdir('dist/pagefind')).filter((name) =>
      name.startsWith('wasm.'),
    );
    expect(wasms.length).toBeGreaterThan(0);
    for (const wasm of wasms)
      expect(
        (await page.request.get(`${url}/pagefind/${wasm}`)).headers()[
          'content-type'
        ],
      ).toBe('application/wasm');
    await expect(access(backup)).rejects.toMatchObject({ code: 'ENOENT' });
    await rename(indexRoot, backup);
    moved = true;
    expect(
      (await page.request.get(`${url}/pagefind/pagefind.js`)).status(),
    ).toBe(404);
    await page.reload();
    await page.getByRole('searchbox').fill('attention');
    await page.getByRole('button', { name: 'Search', exact: true }).click();
    await expect(page.locator('[data-search-status]')).toContainText(
      'npm run build and npm run preview',
    );
  } finally {
    if (child.pid) process.kill(-child.pid, 'SIGTERM');
    await exited;
    if (moved) {
      await expect(access(indexRoot)).rejects.toMatchObject({ code: 'ENOENT' });
      expect(await readFile(join(backup, 'pagefind-entry.json'))).toEqual(
        entryBefore,
      );
      await rename(backup, indexRoot);
    }
    if (linked) {
      expect(await readlink(link)).toBe(outside);
      await unlink(link);
    }
    await writeFile(join(evidence, `task6-dev-search-${port}.log`), output);
  }
});
