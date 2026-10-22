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
it('dry_run_never_writes_and_apply_rejects_changed_inputs', async () => {
  expect(content.planOrganizationMigration).toBeTypeOf('function');
  const root = await fixture();
  const before = await fs.readdir(root, { recursive: true });
  const plan = await content.planOrganizationMigration(root, empty());
  expect(await fs.readdir(root, { recursive: true })).toEqual(before);
  expect(plan.inventory[0]).toMatchObject({
    sourcePath: 'Tutorials/note.md',
    route: '/notes/tutorials/note/',
    headings: [{ id: 'note', text: 'Note', depth: 1 }],
    anchors: ['saved'],
    disposition: 'page',
  });
  expect(JSON.parse(plan.sidecars[2]!.proposedBytes).entries[0]).toMatchObject({
    uid: `doc-${plan.inventory[0]!.entryId}`,
    topics: [],
    purpose: 'note',
    status: 'unreviewed',
  });
  await fs.writeFile(
    join(root, 'Tutorials/note.md'),
    '# Edit\n<a id="saved"></a>\n',
  );
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'source',
  );
  await expect(
    fs.stat(join(root, 'site/content/organization')),
  ).rejects.toThrow();
});
it('apply_is_idempotent and retains registered UIDs and reviewed classification', async () => {
  const root = await fixture();
  const plan = await content.planOrganizationMigration(root, empty());
  await content.applyOrganizationMigration(plan);
  const before = await sidecars(root);
  await content.applyOrganizationMigration(JSON.parse(JSON.stringify(plan)));
  expect(await sidecars(root)).toEqual(before);
  const definition = await content.readOrganization(
    join(root, 'site/content/organization'),
  );
  const record = definition.entries.entries[0]!;
  record.uid = `doc-${'a'.repeat(64)}`;
  record.purpose = 'exercise';
  record.status = 'reviewed';
  // An independently established registry must retain its persistent identifier.
  await fs.writeFile(
    join(root, 'site/content/organization/entries.json'),
    JSON.stringify(definition.entries),
  );
  await fs.writeFile(join(root, 'Tutorials/next.py'), 'print("never execute")');
  const next = await content.planOrganizationMigration(root, definition);
  expect(JSON.parse(next.sidecars[2]!.proposedBytes).entries).toEqual(
    expect.arrayContaining([
      record,
      expect.objectContaining({
        sourcePath: 'Tutorials/next.py',
        purpose: 'project-file',
      }),
    ]),
  );
  expect(next.coverage).toMatchObject({
    publicEntries: 2,
    reviewed: 1,
    unclassified: 2,
  });
});
it('retains existing registry entries omitted from a full proposal and prevents UID reassignment', async () => {
  const root = await fixture();
  await content.applyOrganizationMigration(
    await content.planOrganizationMigration(root, empty()),
  );
  const plan = await content.planOrganizationMigration(root, empty());
  expect(JSON.parse(plan.sidecars[2]!.proposedBytes).entries).toHaveLength(1);
  const definition = await content.readOrganization(
    join(root, 'site/content/organization'),
  );
  definition.entries.entries[0]!.uid = `doc-${'a'.repeat(64)}`;
  await expect(
    content.planOrganizationMigration(root, definition),
  ).rejects.toThrow('UID');
  const forged = structuredClone(plan);
  forged.sidecars[2]!.proposedBytes = JSON.stringify(definition.entries);
  await expect(content.applyOrganizationMigration(forged)).rejects.toThrow(
    'UID',
  );
});
