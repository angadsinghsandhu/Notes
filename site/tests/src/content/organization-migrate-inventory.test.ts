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

it('retains policy/frontmatter/organization drafts but rejects a stale registry source', async () => {
  const root = await fixture();
  await fs.writeFile(join(root, 'Tutorials/private.md'), 'private');
  await fs.writeFile(
    join(root, 'Tutorials/draft.md'),
    '---\ntitle: Draft\ndraft: true\n---\n# Draft',
  );
  const definition = empty();
  for (const [index, sourcePath] of [
    'Tutorials/private.md',
    'Tutorials/draft.md',
    'Tutorials/note.md',
  ].entries())
    definition.entries.entries.push({
      uid: `doc-${String(index + 1).repeat(64)}`,
      sourcePath,
      topics: [],
      purpose: 'note',
      status: 'draft',
    });
  const plan = await content.planOrganizationMigration(root, definition);
  expect(plan.coverage.publicEntries).toBe(0);
  expect(JSON.parse(plan.sidecars[2]!.proposedBytes).entries).toHaveLength(3);
  expect(plan.inventory.every((row) => row.disposition === 'excluded')).toBe(
    true,
  );
  await content.applyOrganizationMigration(plan);
  definition.entries.entries.push({
    uid: `doc-${'a'.repeat(64)}`,
    sourcePath: 'Tutorials/missing.md',
    topics: [],
    purpose: 'note',
    status: 'draft',
  });
  await expect(
    content.planOrganizationMigration(root, definition),
  ).rejects.toThrow('registered source is missing');
});
it('reads fresh stored notebook markdown with shared heading slugs, titles and explicit anchors', async () => {
  const root = await fixture();
  await fs.writeFile(
    join(root, 'Tutorials/book.ipynb'),
    JSON.stringify({
      cells: [
        { cell_type: 'code', source: 'throw new Error("never execute")' },
        {
          cell_type: 'markdown',
          source: ['# Same\n', '<span id="explicit"></span>'],
        },
        { cell_type: 'markdown', source: '# Same' },
        { cell_type: 'raw', source: 'raw' },
      ],
    }),
  );
  await fs.writeFile(
    join(root, 'Tutorials/copy.md'),
    '# Note\n<a id="saved"></a>\n',
  );
  await fs.writeFile(
    join(root, 'Tutorials/title.md'),
    '---\ntitle: Authored\nslug: preserved\n---\n# Fresh',
  );
  const plan = await content.planOrganizationMigration(root, empty());
  expect(
    plan.inventory.find((row) => row.sourcePath.endsWith('book.ipynb')),
  ).toMatchObject({
    headings: [
      { id: 'same', text: 'Same', depth: 1 },
      { id: 'same-1', text: 'Same', depth: 1 },
    ],
    anchors: ['explicit'],
  });
  expect(
    plan.inventory.find((row) => row.sourcePath.endsWith('title.md'))?.route,
  ).toBe('/notes/tutorials/preserved/');
  expect(plan.candidates.duplicates).toEqual([
    ['Tutorials/copy.md', 'Tutorials/note.md'],
  ]);
  expect(plan.candidates.outlines).toContain('Tutorials/title.md');
  await fs.writeFile(
    join(root, 'Tutorials/title.md'),
    '---\ntitle: Authored\nslug: preserved\n---\n# Other',
  );
  await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
    'source',
  );
});
it.each(['policy', 'new', 'removed', 'same-length-body'])(
  'rejects fresh source drift: %s',
  async (mode) => {
    const root = await fixture();
    const plan = await content.planOrganizationMigration(root, empty());
    if (mode === 'policy')
      await fs.appendFile(join(root, 'site/content/publication.json'), ' ');
    if (mode === 'new')
      await fs.writeFile(join(root, 'Tutorials/new.md'), '# New');
    if (mode === 'removed') await fs.unlink(join(root, 'Tutorials/note.md'));
    if (mode === 'same-length-body')
      await fs.writeFile(
        join(root, 'Tutorials/note.md'),
        '# Note\n<a id="other"></a>\n',
      );
    await expect(content.applyOrganizationMigration(plan)).rejects.toThrow(
      /source|missing/,
    );
  },
);
it('hashes decomposed filesystem names using normalized source identity', async () => {
  const root = await fixture();
  await fs.writeFile(join(root, 'Tutorials/cafe\u0301.md'), '# Unicode');
  const plan = await content.planOrganizationMigration(root, empty());
  expect(
    plan.inventory.find((row) => row.sourcePath === 'Tutorials/café.md'),
  ).toMatchObject({
    disposition: 'page',
    sha256: expect.stringMatching(/^[a-f0-9]{64}$/),
  });
  await content.applyOrganizationMigration(plan);
});
it('does not parse organizational draft notebook cells excluded by publication', async () => {
  const root = await fixture();
  await fs.writeFile(
    join(root, 'Tutorials/draft.ipynb'),
    'not valid notebook JSON',
  );
  const definition = empty();
  definition.entries.entries.push({
    uid: `doc-${'a'.repeat(64)}`,
    sourcePath: 'Tutorials/draft.ipynb',
    topics: [],
    purpose: 'note',
    status: 'draft',
  });
  const plan = await content.planOrganizationMigration(root, definition);
  expect(
    plan.inventory.find((row) => row.sourcePath.endsWith('draft.ipynb')),
  ).toMatchObject({ disposition: 'excluded', headings: [], anchors: [] });
});

it.each(['missing-cells', 'non-array-cells', 'bad-source', 'mixed-source'])(
  'rejects malformed public notebook Markdown: %s',
  async (mode) => {
    const root = await fixture();
    const input =
      mode === 'missing-cells'
        ? {}
        : mode === 'non-array-cells'
          ? { cells: null }
          : {
              cells: [
                {
                  cell_type: 'markdown',
                  source: mode === 'bad-source' ? 22 : ['# Heading', 3],
                },
              ],
            };
    await fs.writeFile(
      join(root, 'Tutorials/bad.ipynb'),
      JSON.stringify(input),
    );
    await expect(
      content.planOrganizationMigration(root, empty()),
    ).rejects.toThrow(/notebook|Markdown/);
  },
);
it('inventories all dispositions without following symbolic links or executing code', async () => {
  const root = await fixture();
  await fs.writeFile(
    join(root, 'Tutorials/script.py'),
    'raise Exception("must never execute")',
  );
  await fs.writeFile(join(root, 'Tutorials/unknown.txt'), 'unsupported');
  await fs.writeFile(join(root, 'Tutorials/image.png'), 'image bytes');
  await fs.writeFile(join(root, 'Tutorials/resource.pdf'), 'resource bytes');
  await fs.writeFile(join(root, 'Tutorials/supplement.md'), '# Supplement');
  await fs.symlink(
    join(root, 'Tutorials/note.md'),
    join(root, 'Tutorials/link.md'),
  );
  const policyPath = join(root, 'site/content/publication.json');
  const policy = JSON.parse(await fs.readFile(policyPath, 'utf8'));
  policy.overrides = {
    'Tutorials/resource.pdf': {
      resourceUrl: 'https://example.test/resource.pdf',
    },
    'Tutorials/supplement.md': { role: 'supplemental' },
  };
  await fs.writeFile(policyPath, JSON.stringify(policy));
  const plan = await content.planOrganizationMigration(root, empty());
  expect(
    plan.inventory.find((row) => row.sourcePath.endsWith('unknown.txt')),
  ).toMatchObject({ disposition: 'unsupported', sha256: expect.any(String) });
  expect(
    plan.inventory.find((row) => row.sourcePath.endsWith('image.png')),
  ).toMatchObject({
    disposition: 'supporting-asset',
    sha256: expect.any(String),
  });
  expect(
    plan.inventory.find((row) => row.sourcePath.endsWith('link.md')),
  ).toMatchObject({ disposition: 'excluded', sha256: null });
  expect(
    plan.inventory.find((row) => row.sourcePath.endsWith('resource.pdf')),
  ).toMatchObject({
    disposition: 'external-resource',
    destination: 'https://example.test/resource.pdf',
  });
  const records = JSON.parse(plan.sidecars[2]!.proposedBytes).entries;
  expect(records).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        sourcePath: 'Tutorials/script.py',
        purpose: 'project-file',
      }),
      expect.objectContaining({
        sourcePath: 'Tutorials/resource.pdf',
        purpose: 'reference',
      }),
      expect.objectContaining({
        sourcePath: 'Tutorials/supplement.md',
        purpose: 'reference',
      }),
    ]),
  );
});
it('validates path components and propagates non-absence filesystem errors', async () => {
  const { safePath, optionalBytes } =
    await import('../../../src/content/organization-migrate-inventory.js');
  const root = await fixture();
  for (const path of [
    '',
    '../escape',
    '/tmp/escape',
    'a\\b',
    'Tutorials/note.md/child',
  ])
    await expect(safePath(root, path)).rejects.toThrow('Unsafe');
  await expect(optionalBytes(join(root, 'Tutorials'))).rejects.toThrow();
  expect(await optionalBytes(join(root, 'absent'))).toBe(null);
});
