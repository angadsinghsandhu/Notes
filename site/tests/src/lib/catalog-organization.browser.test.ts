import { expect, test } from '@playwright/test';
import { spawn, execFile } from 'node:child_process';
import { readFile, writeFile, rename, unlink, mkdir } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { promisify } from 'node:util';
import type {
  Manifest,
  OrganizationDefinition,
} from '../../../src/content/index.js';
import {
  developmentDiagnostics,
  freePort,
  fullArchiveReadinessTimeout,
  fullArchivePublicationTimeout,
} from './catalog-development.js';
const execute = promisify(execFile);
const manifestPath = '.generated/current/manifest.json';

function sha256(bytes: Buffer | string): string {
  return createHash('sha256').update(bytes).digest('hex');
}

function expectSameBytes(
  actual: Buffer,
  expected: Buffer,
  description: string,
) {
  // Playwright deep equality enumerates every byte as an object key.
  if (!actual.equals(expected))
    throw new Error(
      `${description}: expected ${expected.length} bytes (SHA256 ${sha256(expected)}), got ${actual.length} (SHA256 ${sha256(actual)})`,
    );
}

// Only these UUID-owned notes and exact backed-up sidecars are mutated.
test('actual npm dev organization enrollment edits drafts invalid recovery remap and stale deletion retain one Astro PID', async ({
  request,
  page,
}, info) => {
  test.setTimeout(1_500_000);
  const name = `task7-owned-${randomUUID()}`;
  const uid = 'doc-' + sha256(name);
  const original = resolve('../Tutorials', `${name}.md`);
  const renamed = resolve('../Tutorials', `${name}-renamed.md`);
  const route = `/notes/tutorials/${name}/`;
  const newRoute = `/notes/tutorials/${name}-renamed/`;
  const sidecarNames = ['taxonomy', 'collections', 'entries', 'paths'] as const;
  const backups = new Map<string, Buffer>();
  const current = new Map<string, Buffer>();
  const ownedSources = new Map<string, string>();
  const notes: string[] = [];
  const stamp = (message: string) =>
    notes.push(`${new Date().toISOString()} ${message}`);
  async function preserve(file: string, bytes: string | Buffer) {
    const path = info.outputPath(file);
    await mkdir(dirname(path), { recursive: true });
    await writeFile(path, bytes);
  }
  const definition = {} as OrganizationDefinition;
  for (const key of sidecarNames) {
    const path = resolve('content/organization', `${key}.json`);
    const bytes = await readFile(path);
    backups.set(path, bytes);
    current.set(path, bytes);
    await preserve(`original-${key}.json`, bytes);
    Object.assign(definition, { [key]: JSON.parse(bytes.toString()) });
  }
  async function writeSidecar(
    key: (typeof sidecarNames)[number],
    raw?: string,
  ) {
    const path = resolve('content/organization', `${key}.json`);
    expectSameBytes(await readFile(path), current.get(path)!, path);
    const bytes = Buffer.from(raw ?? JSON.stringify(definition[key]));
    await writeFile(path, bytes);
    current.set(path, bytes);
    await preserve(`last-${key}.json`, bytes);
    stamp(`wrote ${key} sidecar SHA256 ${sha256(bytes)}`);
  }
  async function writeSource(path: string, bytes: string, create = false) {
    if (!create)
      expect(await readFile(path, 'utf8')).toBe(ownedSources.get(path));
    await writeFile(path, bytes, create ? { flag: 'wx' } : undefined);
    ownedSources.set(path, bytes);
    await preserve(
      `${path === renamed ? 'renamed' : 'original'}-source.md`,
      bytes,
    );
  }
  const port = await freePort();
  const url = `http://127.0.0.1:${port}`;
  const child = spawn('npm', ['run', 'dev', '--', '--port', String(port)], {
    cwd: resolve('.'),
    detached: true,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  const diagnostics = developmentDiagnostics(child, info);
  async function until(
    path: string,
    body: string,
    status = 200,
    timeout = fullArchivePublicationTimeout,
  ) {
    const started = Date.now();
    diagnostics.record(`waiting for ${path} HTTP ${status} including ${body}`);
    let html = '';
    await expect
      .poll(
        async () => {
          try {
            const response = await request.get(`${url}${path}`);
            try {
              html = await response.text();
              return response.status() === status && html.includes(body);
            } finally {
              await response.dispose();
            }
          } catch {
            return false;
          }
        },
        { timeout, intervals: [500, 1000] },
      )
      .toBe(true);
    stamp(
      `${path} HTTP ${status} includes ${body}; publication wait ${Date.now() - started}ms`,
    );
    return html;
  }
  async function pid() {
    return (
      await execute('lsof', ['-t', `-iTCP:${port}`, '-sTCP:LISTEN'])
    ).stdout.trim();
  }
  async function generated() {
    return JSON.parse(await readFile(manifestPath, 'utf8')) as Manifest & {
      preparedBodies: Record<string, string>;
    };
  }
  const topicRoute = `/library/topics/${name}/`;
  const collectionRoute = `/library/collections/${name}/`;
  const groupRoute = `${collectionRoute}groups/chapter/`;
  const pathRoute = `/library/paths/${name}/`;
  let failure: unknown;
  let astroPid = '';
  let source = original;
  let body =
    '---\ntitle: Task 7 synthetic lifecycle proof\n---\n# First lifecycle body\n';
  try {
    await until(
      '/notes/interview/applied-science/breadth/6-6-2-transformers/',
      'Transformer',
      200,
      fullArchiveReadinessTimeout,
    );
    astroPid = await pid();
    expect(astroPid).toMatch(/^\d+$/);
    stamp(
      `Owned Astro listener PID ${astroPid}; npm PID ${child.pid}; port ${port}`,
    );
    const indexBefore = await readFile('dist/pagefind/pagefind-entry.json');
    await writeSource(source, body, true);
    await until(route, 'First lifecycle body');
    const plain = await generated();
    const plainEntry = plain.entries.find(
      (e) => e.sourcePath === `Tutorials/${name}.md`,
    )!;
    expect(plainEntry).toBeTruthy();
    expect(
      plain.organization!.memberships.find((m) => m.entryId === plainEntry.id)
        ?.uid,
    ).toBeUndefined();
    stamp(
      'Ordinary unenrolled Markdown published with unregistered fallback membership',
    );
    await page.goto(`${url}${route}`);
    body = body.replace('First lifecycle body', 'Changed lifecycle body');
    await writeSource(source, body);
    await until(route, 'Changed lifecycle body');
    await expect(page.locator('article')).toContainText(
      'Changed lifecycle body',
      { timeout: 75_000 },
    );
    stamp('Already open browser updated automatically after source edit');
    expect(await pid()).toBe(astroPid);

    definition.taxonomy.topics.push({
      id: name,
      title: 'Task7 first topic',
      summary: '',
    });
    definition.collections.collections.push({
      id: name,
      title: 'Task7 first collection',
      summary: '',
      type: 'book',
    });
    definition.collections.groups.push({
      id: 'chapter',
      collectionId: name,
      title: 'Task7 first chapter',
      summary: '',
      type: 'chapter',
    });
    const record = {
      uid,
      sourcePath: `Tutorials/${name}.md`,
      topics: [name],
      collectionId: name,
      groupId: 'chapter',
      purpose: 'note' as const,
      status: 'reviewed' as const,
      summary: 'Task7 enrolled summary',
    };
    definition.entries.entries.push(record);
    definition.paths.paths.push({
      id: name,
      title: 'Task7 first path',
      summary: '',
      steps: [
        {
          id: 'owned-step',
          title: 'Owned step',
          summary: '',
          entryUids: [uid],
          topicIds: [name],
        },
      ],
    });
    for (const key of sidecarNames) await writeSidecar(key);
    await until(route, 'Task7 enrolled summary');
    await until(topicRoute, 'Task7 first topic');
    await until(collectionRoute, 'Task7 first collection');
    await until(groupRoute, 'Task7 first chapter');
    const pathHtml = await until(pathRoute, 'Owned step');
    expect(pathHtml).toContain(`href="${route}"`);
    expect(pathHtml).toContain(`href="${topicRoute}"`);
    expect(await pid()).toBe(astroPid);

    definition.taxonomy.topics.at(-1)!.title = 'Task7 edited topic';
    definition.taxonomy.topics.push({
      id: name + '-child',
      parentId: name,
      title: 'Task7 child topic',
      summary: '',
    });
    record.topics = [name + '-child'];
    definition.collections.collections.at(-1)!.title =
      'Task7 edited collection';
    definition.collections.groups.at(-1)!.title = 'Task7 edited chapter';
    definition.paths.paths.at(-1)!.title = 'Task7 edited path';
    record.summary = 'Task7 edited summary';
    for (const key of sidecarNames) await writeSidecar(key);
    for (const [path, label] of [
      [route, 'Task7 edited summary'],
      [topicRoute, 'Task7 edited topic'],
      [collectionRoute, 'Task7 edited collection'],
      [groupRoute, 'Task7 edited chapter'],
      [pathRoute, 'Task7 edited path'],
    ])
      await until(path!, label!);
    await until(`/library/topics/${name}-child/`, 'Task7 child topic');
    await expect(page.locator('.organization-metadata')).toContainText(
      'Task7 child topic',
    );
    expect(await pid()).toBe(astroPid);
    const goodGeneration = await readFile(manifestPath);
    await writeSidecar('entries', '{ invalid task7 sidecar');
    await expect
      .poll(() => diagnostics.contains('cannot read organization sidecar'), {
        timeout: fullArchivePublicationTimeout,
        intervals: [500, 1000],
      })
      .toBe(true);
    expectSameBytes(
      await readFile(manifestPath),
      goodGeneration,
      'Invalid JSON changed the last good manifest',
    );
    await until(route, 'Task7 edited summary');
    stamp(
      `Invalid JSON diagnosed and exact last good manifest retained, SHA256 ${sha256(goodGeneration)}`,
    );
    await writeSidecar('entries');
    body = body.replace('Changed lifecycle body', 'Recovered lifecycle body');
    await writeSource(source, body);
    await until(route, 'Recovered lifecycle body');
    expect(await pid()).toBe(astroPid);

    expect(await readFile(source, 'utf8')).toBe(ownedSources.get(source));
    await rename(source, renamed);
    ownedSources.delete(source);
    ownedSources.set(renamed, body);
    source = renamed;
    body = body.replace('---\n#', `aliases: [${route}]\n---\n#`);
    await writeSource(source, body);
    record.sourcePath = `Tutorials/${name}-renamed.md`;
    await writeSidecar('entries');
    await until(newRoute, 'Recovered lifecycle body');
    const alias = await until(route, 'noindex');
    expect(alias).toContain(newRoute);
    expect(alias).not.toContain('data-pagefind-body');
    const remapped = await generated();
    const entry = remapped.entries.find(
      (e) => e.sourcePath === record.sourcePath,
    )!;
    expect(entry.id).not.toBe(plainEntry.id);
    expect(
      remapped.organization!.memberships.find((m) => m.uid === uid)?.entryId,
    ).toBe(entry.id);
    expect(remapped.preparedBodies[entry.bodyFile!]).toContain(
      'Recovered lifecycle body',
    );
    expect(await until(pathRoute, 'Owned step')).toContain(
      `href="${newRoute}"`,
    );
    stamp(
      `Explicit source remap preserved UID ${uid}; new entry/body/old alias/path target agree`,
    );
    expect(await pid()).toBe(astroPid);

    // Remove the owned path before hiding its only UID/topic; real public-reference rules stay strict.
    definition.paths.paths.pop();
    await writeSidecar('paths');
    await until(pathRoute, 'Page not found', 404);
    const publicBody = body;
    body = body.replace('---\n#', 'draft: true\n---\n#');
    await writeSource(source, body);
    await until(newRoute, 'Page not found', 404);
    await until(route, 'Page not found', 404);
    expect(
      (await generated()).entries.some(
        (e) => e.sourcePath === record.sourcePath,
      ),
    ).toBe(false);
    body = publicBody;
    await writeSource(source, body);
    await until(newRoute, 'Recovered lifecycle body');
    Object.assign(record, { status: 'draft' });
    await writeSidecar('entries');
    await until(newRoute, 'Page not found', 404);
    await until(route, 'Page not found', 404);
    const editorial = await generated();
    expect(
      editorial.ledger.find((r) => r.sourcePath === record.sourcePath),
    ).toMatchObject({
      disposition: 'excluded',
      reason: 'Excluded organizational draft content',
    });
    Object.assign(record, { status: 'reviewed' });
    await writeSidecar('entries');
    await until(newRoute, 'Recovered lifecycle body');
    expect(await pid()).toBe(astroPid);
    const beforeDeletion = await readFile(manifestPath);
    expect(await readFile(source, 'utf8')).toBe(ownedSources.get(source));
    await unlink(source);
    ownedSources.delete(source);
    await expect
      .poll(
        () =>
          diagnostics.contains(
            `entry ${record.sourcePath} (${uid}): registered source is missing`,
          ),
        { timeout: fullArchivePublicationTimeout, intervals: [500, 1000] },
      )
      .toBe(true);
    expectSameBytes(
      await readFile(manifestPath),
      beforeDeletion,
      'Stale source record changed the last good manifest',
    );
    await until(newRoute, 'Recovered lifecycle body');
    stamp(
      `Stale source record diagnosed; deletion retains exact last good generation, SHA256 ${sha256(beforeDeletion)}`,
    );
    definition.entries.entries.pop();
    await writeSidecar('entries');
    await until(newRoute, 'Page not found', 404);
    await until(route, 'Page not found', 404);
    await until(topicRoute, 'Page not found', 404);
    await until(`/library/topics/${name}-child/`, 'Page not found', 404);
    await until(collectionRoute, 'Page not found', 404);
    await until(groupRoute, 'Page not found', 404);
    expect(await pid()).toBe(astroPid);
    expectSameBytes(
      await readFile('dist/pagefind/pagefind-entry.json'),
      indexBefore,
      'Development changed the production search index',
    );
    expect(await (await request.get(`${url}/search/`)).text()).toContain(
      'does not update with note edits',
    );
    stamp(
      `Same Astro PID ${astroPid} after all lifecycle changes; production index unchanged`,
    );
  } catch (error) {
    failure = error;
  } finally {
    const cleanupErrors: unknown[] = [];
    try {
      if (child.pid && child.exitCode === null && child.signalCode === null)
        process.kill(-child.pid, 'SIGTERM');
      await diagnostics.exited;
      stamp(`Owned npm process closed; Astro PID was ${astroPid}`);
    } catch (error) {
      cleanupErrors.push(error);
    }
    for (const [path, bytes] of backups) {
      try {
        const actual = await readFile(path);
        if (!actual.equals(current.get(path)!)) {
          await preserve(`unexpected-${path.split('/').at(-1)}`, actual);
          cleanupErrors.push(
            new Error(`Unexpected sidecar edits preserved for ${path}`),
          );
          continue;
        }
        if (!actual.equals(bytes)) await writeFile(path, bytes);
        expectSameBytes(
          await readFile(path),
          bytes,
          `Could not restore ${path}`,
        );
        stamp(`Restored ${path}; SHA256 ${sha256(bytes)}`);
      } catch (error) {
        cleanupErrors.push(error);
      }
    }
    for (const [path, bytes] of ownedSources) {
      try {
        const actual = await readFile(path, 'utf8');
        await preserve(`cleanup-${path.split('/').at(-1)}`, actual);
        expect(actual, `Unexpected source edits preserved at ${path}`).toBe(
          bytes,
        );
        await unlink(path);
      } catch (error) {
        cleanupErrors.push(error);
      }
    }
    await diagnostics.save('task-7-organization-http.log', notes.join('\n'));
    if (cleanupErrors.length)
      failure = new AggregateError(
        [...(failure ? [failure] : []), ...cleanupErrors],
        'Task7 cleanup requires attention',
      );
    await expect(
      execute('lsof', ['-t', `-iTCP:${port}`, '-sTCP:LISTEN']),
    ).rejects.toMatchObject({ code: 1 });
  }
  if (failure) diagnostics.fail(failure);
});
