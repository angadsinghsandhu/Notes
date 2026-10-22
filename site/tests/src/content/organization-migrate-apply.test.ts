import * as fs from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import * as content from '../../../src/content/index.js';

vi.mock('node:fs/promises', async (importOriginal) => ({
  ...(await importOriginal<typeof import('node:fs/promises')>()),
}));
const roots: string[] = [];
afterEach(async () => {
  vi.restoreAllMocks();
  for (const root of roots.splice(0))
    await fs.rm(root, { recursive: true, force: true });
});
const empty = (): content.OrganizationDefinition => ({
  taxonomy: { version: 1, topics: [] },
  collections: { version: 1, collections: [], groups: [] },
  entries: { version: 1, entries: [] },
  paths: { version: 1, paths: [] },
});
async function fixture() {
  const root = await fs.realpath(
    await fs.mkdtemp(join(tmpdir(), 'organization-')),
  );
  roots.push(root);
  await fs.mkdir(join(root, 'site/content'), { recursive: true });
  await fs.mkdir(join(root, 'Tutorials'));
  await fs.writeFile(
    join(root, 'site/content/publication.json'),
    JSON.stringify({
      roots: [
        'Books',
        'Classes',
        'Courses',
        'Interview',
        'Languages',
        'Tutorials',
      ],
      exclude: ['Tutorials/private.md'],
    }),
  );
  await fs.writeFile(
    join(root, 'Tutorials/note.md'),
    '# Note\n<a id="saved"></a>\n',
  );
  return root;
}
async function sidecars(root: string) {
  return Promise.all(
    ['taxonomy', 'collections', 'entries', 'paths'].map((name) =>
      fs.readFile(join(root, `site/content/organization/${name}.json`), 'utf8'),
    ),
  );
}
it('rejects changed destinations before touching any sidecar', async () => {
  const root = await fixture();
  await content.applyOrganizationMigration(
    await content.planOrganizationMigration(root, empty()),
  );
  const plan = await content.planOrganizationMigration(root, empty());
  await fs.appendFile(join(root, 'site/content/organization/paths.json'), ' ');
  const before = await sidecars(root);
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'destination',
  );
  expect(await sidecars(root)).toEqual(before);
});
it('partial_write_failure_restores_previous_sidecars and keeps recovery evidence', async () => {
  const root = await fixture();
  await content.applyOrganizationMigration(
    await content.planOrganizationMigration(root, empty()),
  );
  const before = await sidecars(root);
  const proposed = await content.readOrganization(
    join(root, 'site/content/organization'),
  );
  proposed.taxonomy.topics.push({ id: 'topic', title: 'Topic', summary: '' });
  const plan = await content.planOrganizationMigration(root, proposed);
  const rename = fs.rename;
  let replacements = 0;
  vi.spyOn(fs, 'rename').mockImplementation(async (from, to) => {
    if (String(from).includes('/stage/') && ++replacements === 2)
      throw new Error('middle replacement failure');
    await rename(from, to);
  });
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'recovery',
  );
  expect(await sidecars(root)).toEqual(before);
  expect(
    (
      await fs.readdir(join(root, '.superpowers/organization-migrations'), {
        recursive: true,
      })
    ).some((path) => path.endsWith('recovery.json')),
  ).toBe(true);
});

it.each(['organization', 'content', 'backup', 'sidecar', 'root'])(
  'rejects symbolic link write paths: %s',
  async (mode) => {
    const root = await fixture();
    const plan = await content.planOrganizationMigration(root, empty());
    const outside = await fixture();
    if (mode === 'root') {
      await fs.symlink(root, join(outside, 'alias'));
      await expect(
        content.applyOrganizationMigration({
          ...plan,
          rootDir: join(outside, 'alias'),
        }),
      ).rejects.toThrow('canonical');
      return;
    }
    if (mode === 'content') {
      await fs.rename(
        join(root, 'site/content'),
        join(root, 'site/old-content'),
      );
      await fs.symlink(
        join(root, 'site/old-content'),
        join(root, 'site/content'),
      );
    }
    if (mode === 'organization')
      await fs.symlink(
        join(outside, 'site/content'),
        join(root, 'site/content/organization'),
      );
    if (mode === 'backup')
      await fs.symlink(outside, join(root, '.superpowers'));
    if (mode === 'sidecar') {
      await fs.mkdir(join(root, 'site/content/organization'));
      await fs.symlink(
        join(outside, 'site/content/publication.json'),
        join(root, 'site/content/organization/taxonomy.json'),
      );
    }
    const before = await fs.readdir(outside, { recursive: true });
    await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
      /Unsafe|symlink/,
    );
    expect(await fs.readdir(outside, { recursive: true })).toEqual(before);
  },
);
it.each([
  '../outside',
  'other.json',
  'duplicate',
  'unknown-field',
  'version',
  'bad-hash',
  'bad-definition',
  'bad-reference',
  'audit',
  'inventory',
  'noncanonical-root',
])('rejects malformed or forged plans: %s', async (mode) => {
  const root = await fixture();
  const plan = await content.planOrganizationMigration(root, empty());
  const candidate = structuredClone(plan);
  if (mode === '../outside' || mode === 'other.json')
    Reflect.set(candidate.sidecars[0]!, 'filename', mode);
  if (mode === 'duplicate') candidate.sidecars[1] = candidate.sidecars[0]!;
  if (mode === 'unknown-field') Reflect.set(candidate, 'outputDir', '/tmp');
  if (mode === 'version') Reflect.set(candidate, 'version', 2);
  if (mode === 'bad-hash') candidate.policyHash = 'bad';
  if (mode === 'bad-definition') candidate.sidecars[0]!.proposedBytes = '{}';
  if (mode === 'bad-reference') {
    const entries = JSON.parse(candidate.sidecars[2]!.proposedBytes);
    entries.entries[0].topics = ['missing'];
    candidate.sidecars[2]!.proposedBytes = JSON.stringify(entries);
  }
  if (mode === 'audit') candidate.coverage.publicEntries = 100;
  if (mode === 'inventory') candidate.inventory[0]!.route = '/forged/';
  if (mode === 'noncanonical-root') candidate.rootDir += '/.';
  await expect(content.applyOrganizationMigration(candidate)).rejects.toThrow();
  await expect(
    fs.stat(join(root, 'site/content/organization')),
  ).rejects.toThrow();
});
it('preserves all original bytes and recoverable evidence when rollback itself fails', async () => {
  const root = await fixture();
  await content.applyOrganizationMigration(
    await content.planOrganizationMigration(root, empty()),
  );
  const before = await sidecars(root);
  const definition = await content.readOrganization(
    join(root, 'site/content/organization'),
  );
  definition.taxonomy.topics.push({ id: 'new', title: 'New', summary: '' });
  const plan = await content.planOrganizationMigration(root, definition);
  const rename = fs.rename;
  let replacements = 0;
  vi.spyOn(fs, 'rename').mockImplementation(async (from, to) => {
    if (String(from).includes('/restore-')) throw new Error('rollback blocked');
    if (String(from).includes('/stage/') && ++replacements === 2)
      throw new Error('replacement blocked');
    await rename(from, to);
  });
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'rollback incomplete',
  );
  const backups = join(root, '.superpowers/organization-migrations');
  const names = await fs.readdir(backups);
  let found = false;
  for (const name of names) {
    const recovery = JSON.parse(
      await fs.readFile(join(backups, name, 'recovery.json'), 'utf8'),
    );
    if (recovery.sidecars[0].previousBytes !== null) {
      found = true;
      expect(
        recovery.sidecars.map((row: { previousBytes: string }) =>
          Buffer.from(row.previousBytes, 'base64').toString('utf8'),
        ),
      ).toEqual(before);
    }
  }
  expect(found).toBe(true);
});
it('rolls back newly created destinations to absence', async () => {
  const root = await fixture();
  const plan = await content.planOrganizationMigration(root, empty());
  const rename = fs.rename;
  let calls = 0;
  vi.spyOn(fs, 'rename').mockImplementation(async (from, to) => {
    if (++calls === 3) throw new Error('third replacement');
    await rename(from, to);
  });
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'restored',
  );
  await expect(
    fs.stat(join(root, 'site/content/organization')),
  ).rejects.toThrow();
  expect(
    await content.readOrganization(join(root, 'site/content/organization')),
  ).toEqual(empty());
});

it('rejects source changes during staging before the first replacement', async () => {
  const root = await fixture();
  const plan = await content.planOrganizationMigration(root, empty());
  const writeFile = fs.writeFile;
  let changed = false;
  vi.spyOn(fs, 'writeFile').mockImplementation(async (path, data, options) => {
    await writeFile(path, data, options);
    if (!changed && String(path).includes('/stage/')) {
      changed = true;
      await writeFile(
        join(root, 'Tutorials/note.md'),
        '# Changed during staging',
      );
    }
  });
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'source',
  );
  expect(
    await content.readOrganization(join(root, 'site/content/organization')),
  ).toEqual(empty());
});
it('preserves recoverable evidence when a new unrelated file prevents bootstrap directory removal', async () => {
  const root = await fixture();
  const plan = await content.planOrganizationMigration(root, empty());
  const rename = fs.rename;
  let calls = 0;
  vi.spyOn(fs, 'rename').mockImplementation(async (from, to) => {
    if (++calls === 2) {
      await fs.writeFile(
        join(root, 'site/content/organization/unrelated.txt'),
        'preserve',
      );
      throw new Error('replacement failure');
    }
    await rename(from, to);
  });
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'rollback incomplete',
  );
  expect(await fs.readdir(join(root, 'site/content/organization'))).toEqual([
    'unrelated.txt',
  ]);
  expect(
    await fs.readFile(
      join(root, 'site/content/organization/unrelated.txt'),
      'utf8',
    ),
  ).toBe('preserve');
});
it('rejects altered destination bytes during staging before replacement', async () => {
  const root = await fixture();
  const plan = await content.planOrganizationMigration(root, empty());
  const rename = fs.rename;
  let changed = false;
  vi.spyOn(fs, 'rename').mockImplementation(async (from, to) => {
    await rename(from, to);
    if (!changed) {
      changed = true;
      await fs.writeFile(
        join(root, 'site/content/organization/collections.json'),
        'unrelated bytes',
      );
    }
  });
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'rollback incomplete',
  );
  expect(
    await fs.readFile(
      join(root, 'site/content/organization/collections.json'),
      'utf8',
    ),
  ).toBe('unrelated bytes');
});

it('preserves a foreign edit to an already replaced sidecar when a later replacement fails', async () => {
  const root = await fixture();
  await content.applyOrganizationMigration(
    await content.planOrganizationMigration(root, empty()),
  );
  const before = await sidecars(root);
  const definition = await content.readOrganization(
    join(root, 'site/content/organization'),
  );
  definition.taxonomy.topics.push({ id: 'topic', title: 'Topic', summary: '' });
  const plan = await content.planOrganizationMigration(root, definition);
  const rename = fs.rename;
  let replacements = 0;
  const foreign = 'foreign writer bytes must survive';
  vi.spyOn(fs, 'rename').mockImplementation(async (from, to) => {
    if (String(from).includes('/stage/')) {
      if (++replacements === 2) throw new Error('later replacement failure');
      await rename(from, to);
      await fs.writeFile(to, foreign);
    } else await rename(from, to);
  });
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'rollback incomplete',
  );
  expect(await sidecars(root)).toEqual([foreign, ...before.slice(1)]);
  const backups = join(root, '.superpowers/organization-migrations');
  const recoveries = await Promise.all(
    (await fs.readdir(backups)).map(async (name) =>
      JSON.parse(
        await fs.readFile(join(backups, name, 'recovery.json'), 'utf8'),
      ),
    ),
  );
  expect(
    recoveries.some(
      (recovery) =>
        recovery.sidecars[0].previousBytes ===
        Buffer.from(before[0]!).toString('base64'),
    ),
  ).toBe(true);
});
