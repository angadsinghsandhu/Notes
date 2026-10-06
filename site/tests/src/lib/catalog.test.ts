import {
  mkdtemp,
  mkdir,
  writeFile,
  readFile,
  rename,
  rm,
  symlink,
  readdir,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { prepareContent } from '../../../src/content/index.js';
const faults = vi.hoisted(() => ({
  afterRename: undefined as undefined | (() => Promise<void>),
  beforeRename: undefined as undefined | ((to: string) => void),
}));
vi.mock('node:fs/promises', async (original) => {
  const fs = await original<typeof import('node:fs/promises')>();
  return {
    ...fs,
    rename: async (from: string, to: string) => {
      faults.beforeRename?.(to);
      await fs.rename(from, to);
      await faults.afterRename?.();
    },
  };
});
const roots: string[] = [];
afterEach(async () => {
  faults.afterRename = undefined;
  faults.beforeRename = undefined;
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function archive() {
  const root = await mkdtemp(join(tmpdir(), 'notes-handoff-'));
  roots.push(root);
  await mkdir(join(root, 'site/content'), { recursive: true });
  const policyPath = join(root, 'site/content/publication.json');
  await writeFile(
    policyPath,
    JSON.stringify({
      roots: [
        'Books',
        'Classes',
        'Courses',
        'Interview',
        'Languages',
        'Tutorials',
      ],
      repositoryPublic: true,
      repositoryUrl: 'https://github.com/owner/repo',
      revision: 'a'.repeat(40),
    }),
  );
  return {
    rootDir: root,
    outputDir: join(root, 'site/.generated'),
    policyPath,
    hosted: false,
  };
}
async function put(root: string, path: string, value: string | Buffer) {
  await mkdir(dirname(join(root, path)), { recursive: true });
  await writeFile(join(root, path), value);
}
import {
  loadCatalog,
  readPreparedCatalog,
  readPreparedBody,
} from '../../../src/lib/catalog.js';
import type { ContentEntry, Manifest } from '../../../src/content/index.js';

function entry(name: string, fields: Partial<ContentEntry> = {}): ContentEntry {
  return {
    id: name,
    title: name,
    sourcePath: `Tutorials/Group/${name}.md`,
    section: 'tutorials',
    kind: 'markdown',
    bytes: 10,
    groupSegments: ['Group'],
    route: `/notes/tutorials/group/${name}/`,
    headings: [],
    description: '',
    tags: [],
    draft: false,
    aliases: [],
    ...fields,
  };
}
const manifest: Manifest = {
  version: 1,
  entries: [
    entry('10 topic'),
    entry('2 topic'),
    entry('code', { kind: 'code' }),
    entry('draft', { draft: true }),
    entry('first', { order: -1 }),
    entry('book', { section: 'books', aliases: ['/old-book/'] }),
  ],
  assets: [],
  ledger: [
    { sourcePath: 'secret', disposition: 'excluded', reason: 'internal' },
  ],
};

describe('published catalog', () => {
  it('filters sections and kinds, excludes drafts, and sorts naturally within groups with author order first', () => {
    const catalog = loadCatalog(manifest);
    expect(
      catalog.listEntries({ section: 'tutorials' }).map((item) => item.id),
    ).toEqual(['first', '2 topic', '10 topic', 'code']);
    expect(
      catalog.listEntries({ kind: 'code' }).map((item) => item.id),
    ).toEqual(['code']);
    expect(catalog.getEntry('/old-book/')).toMatchObject({ id: 'book' });
    expect(catalog.getEntry('/notes/tutorials/group/draft/')).toBeUndefined();
    expect(JSON.stringify(catalog.listEntries())).not.toContain('secret');
  });
  it('provides note-only adjacency inside a section and rejects resource/draft identities', () => {
    const catalog = loadCatalog(manifest);
    expect(catalog.getAdjacentNotes('2 topic')).toMatchObject({
      previous: { id: 'first' },
      next: { id: '10 topic' },
    });
    expect(catalog.getAdjacentNotes('10 topic').next).toBeUndefined();
    expect(catalog.getAdjacentNotes('book')).toEqual({});
    expect(catalog.getAdjacentNotes('code')).toEqual({});
    expect(catalog.getAdjacentNotes('draft')).toEqual({});
  });
  it('projects explicit public fields instead of forwarding untrusted filesystem/internal properties', () => {
    const polluted = {
      ...entry('safe'),
      absolutePath: '/private/secret',
      ledger: ['secret'],
    };
    const catalog = loadCatalog({ ...manifest, entries: [polluted] });
    expect(JSON.stringify(catalog.listEntries())).not.toMatch(
      /absolutePath|private|ledger/,
    );
  });
});

it('reads only the prepared snapshot and bounded selected body paths', async () => {
  const root = await mkdtemp(join(tmpdir(), 'notes-catalog-'));
  try {
    const snapshot = join(root, 'site/.generated/current');
    await mkdir(join(snapshot, 'bodies'), { recursive: true });
    const note = entry('published', {
      id: 'a'.repeat(64),
      bodyFile: `bodies/${'a'.repeat(64)}.html`,
    });
    await writeFile(
      join(snapshot, 'manifest.json'),
      JSON.stringify({ ...manifest, entries: [note] }),
    );
    await writeFile(join(snapshot, note.bodyFile!), '<h1>Prepared body</h1>');
    const catalog = await readPreparedCatalog(snapshot);
    const selected = catalog.getEntry(note.route)!;
    expect(await readPreparedBody(selected, snapshot)).toBe(
      '<h1>Prepared body</h1>',
    );
    expect(
      await readPreparedBody(entry('pdf', { kind: 'pdf' }), snapshot),
    ).toBe('');
    await expect(
      readPreparedBody({ ...note, bodyFile: '../manifest.json' }, snapshot),
    ).rejects.toThrow(/body/i);
    await expect(
      readPreparedBody({ ...note, draft: true }, snapshot),
    ).rejects.toThrow(/draft/i);
    await rm(join(snapshot, note.bodyFile!));
    await writeFile(join(root, 'private'), 'secret');
    await symlink(join(root, 'private'), join(snapshot, note.bodyFile!));
    await expect(readPreparedBody(note, snapshot)).rejects.toThrow(
      /symbolic|symlink/i,
    );
    await expect(readPreparedCatalog(join(root, 'site/dist'))).rejects.toThrow(
      /generated/i,
    );
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

it('keeps previous and next notes within the exact original group', () => {
  const catalog = loadCatalog({
    ...manifest,
    entries: [
      ...manifest.entries,
      entry('sibling', {
        groupSegments: ['Group B'],
        sourcePath: 'Tutorials/Group B/sibling.md',
      }),
      entry('child', {
        groupSegments: ['Group', 'Child'],
        sourcePath: 'Tutorials/Group/Child/child.md',
      }),
    ],
  });
  expect(catalog.getAdjacentNotes('10 topic').next).toBeUndefined();
  expect(catalog.getAdjacentNotes('sibling')).toEqual({});
  expect(catalog.getAdjacentNotes('child')).toEqual({});
});

// Renaming live directories away or losing a catalog's body generation must fail this.
it.each([true, false])(
  'keeps catalog and body generations coherent at every rename handoff (development=%s)',
  async (development) => {
    const options = await archive();
    const image = await readFile('tests/fixtures/synthetic/task3/pixel.png');
    await put(
      options.rootDir,
      'Tutorials/old.md',
      '# Old\n![pixel](pixel.png)',
    );
    await put(options.rootDir, 'Tutorials/pixel.png', image);
    const first = await prepareContent(options);
    const snapshot = join(options.outputDir, 'current');
    const old = (await readPreparedCatalog(snapshot)).listEntries()[0]!;
    await rename(
      join(options.rootDir, 'Tutorials/old.md'),
      join(options.rootDir, 'Tutorials/new.md'),
    );
    await put(
      options.rootDir,
      'Tutorials/new.md',
      '# New\n![new pixel](second.png)',
    );
    await put(
      options.rootDir,
      'Tutorials/second.png',
      Buffer.concat([image, Buffer.from('second')]),
    );
    const observations: string[] = [];
    const assetCounts: number[] = [];
    expect(JSON.stringify(old)).not.toMatch(
      /preparedBodies|<h1|ledger|absolutePath/,
    );
    faults.afterRename = async () => {
      const catalog = await readPreparedCatalog(snapshot);
      const selected = catalog.listEntries()[0]!;
      const body = await readPreparedBody(selected, snapshot);
      expect(body).toContain(selected.title === 'Old' ? 'Old' : 'New');
      expect(await readPreparedBody(old, snapshot)).toContain('Old');
      if (development)
        expect(
          await readFile(
            join(
              options.rootDir,
              'site/public',
              first.manifest.assets[0]!.url.slice(1),
            ),
          ),
        ).toEqual(image);
      observations.push(selected.title);
      assetCounts.push(
        (await readdir(join(options.rootDir, 'site/public/content-assets')))
          .length,
      );
    };
    const result = await prepareContent({ ...options, development });
    faults.afterRename = undefined;
    expect(result.diagnostics).toEqual([]);
    expect(observations).toEqual(
      development ? ['Old', 'New'] : ['Old', 'Old', 'New'],
    );
    expect(assetCounts).toEqual(development ? [2, 2] : [2, 1, 1]);
    expect((await readPreparedCatalog(snapshot)).listEntries()[0]?.title).toBe(
      'New',
    );
    expect(await readPreparedBody(old, snapshot)).toContain('Old');
  },
);

it('preserves a removed note body through handoff, bounds development assets to one predecessor and prunes them in production', async () => {
  const options = await archive();
  const snapshot = join(options.outputDir, 'current');
  const image = await readFile('tests/fixtures/synthetic/task3/pixel.png');
  await put(
    options.rootDir,
    'Tutorials/note.md',
    '# Note\n![pixel](pixel.png)',
  );
  await put(options.rootDir, 'Tutorials/pixel.png', image);
  const first = await prepareContent(options);
  const catalog = await readPreparedCatalog(snapshot);
  const selected = catalog.listEntries()[0]!;
  const asset = join(
    options.rootDir,
    'site/public',
    first.manifest.assets[0]!.url.slice(1),
  );
  await rm(join(options.rootDir, 'Tutorials/note.md'));
  let handoffs = 0;
  faults.afterRename = async () => {
    expect((await readPreparedCatalog(snapshot)).listEntries()).toEqual([]);
    expect(await readPreparedBody(selected, snapshot)).toContain('Note');
    expect(await readFile(asset)).toEqual(image);
    handoffs++;
  };
  expect(
    (await prepareContent({ ...options, development: true })).diagnostics,
  ).toEqual([]);
  faults.afterRename = undefined;
  expect(handoffs).toBe(1);
  expect(await readPreparedBody(selected, snapshot)).toContain('Note');
  expect(
    (await prepareContent({ ...options, development: true })).diagnostics,
  ).toEqual([]);
  await expect(readFile(asset)).rejects.toMatchObject({ code: 'ENOENT' });
  await put(
    options.rootDir,
    'Tutorials/note.md',
    '# Again\n![pixel](pixel.png)',
  );
  expect(
    (await prepareContent({ ...options, development: true })).diagnostics,
  ).toEqual([]);
  await put(
    options.rootDir,
    'Tutorials/note.md',
    '---\ntitle: Draft\ndraft: true\n---\n# Private',
  );
  expect(
    (await prepareContent({ ...options, development: true })).diagnostics,
  ).toEqual([]);
  expect(await readFile(asset)).toEqual(image);
  expect((await prepareContent(options)).diagnostics).toEqual([]);
  await expect(readFile(asset)).rejects.toMatchObject({ code: 'ENOENT' });
  expect((await readPreparedCatalog(snapshot)).listEntries()).toEqual([]);
  expect(
    JSON.stringify((await readPreparedCatalog(snapshot)).listEntries()),
  ).not.toMatch(/preparedBodies|ledger/);
});

it('rolls back asset additions and retired assets when the single publication rename fails', async () => {
  const options = await archive();
  const snapshot = join(options.outputDir, 'current');
  const image = await readFile('tests/fixtures/synthetic/task3/pixel.png');
  await put(options.rootDir, 'Tutorials/note.md', '# Old\n![pixel](pixel.png)');
  await put(options.rootDir, 'Tutorials/pixel.png', image);
  const first = await prepareContent(options);
  const before = await readFile(join(snapshot, 'manifest.json'));
  const old = (await readPreparedCatalog(snapshot)).listEntries()[0]!;
  await put(
    options.rootDir,
    'Tutorials/pixel.png',
    Buffer.concat([image, Buffer.from('new')]),
  );
  await put(options.rootDir, 'Tutorials/note.md', '# New\n![pixel](pixel.png)');
  faults.beforeRename = (to) => {
    if (to.endsWith('/current/manifest.json'))
      throw new Error('injected commit failure');
  };
  const result = await prepareContent(options);
  faults.beforeRename = undefined;
  expect(result.diagnostics[0]?.message).toBe('injected commit failure');
  expect(await readFile(join(snapshot, 'manifest.json'))).toEqual(before);
  expect(await readPreparedBody(old, snapshot)).toContain('Old');
  const assets = await readdir(
    join(options.rootDir, 'site/public/content-assets'),
  );
  expect(assets).toEqual([first.manifest.assets[0]!.url.split('/').at(-1)]);
  expect(
    await readFile(
      join(
        options.rootDir,
        'site/public',
        first.manifest.assets[0]!.url.slice(1),
      ),
    ),
  ).toEqual(image);
});

it('reuses one prepared catalog per file generation and invalidates after atomic replacement', async () => {
  const options = await archive();
  await put(options.rootDir, 'Tutorials/cache.md', '# First body');
  await prepareContent(options);
  const snapshot = join(options.outputDir, 'current');
  const first = await readPreparedCatalog(snapshot);
  expect(await readPreparedCatalog(snapshot)).toBe(first);
  const selected = first.listEntries()[0]!;
  await put(options.rootDir, 'Tutorials/cache.md', '# Second body');
  await prepareContent(options);
  const second = await readPreparedCatalog(snapshot);
  expect(second).not.toBe(first);
  expect(await readPreparedBody(selected, snapshot)).toContain('First body');
  expect(await readPreparedBody(second.listEntries()[0]!, snapshot)).toContain(
    'Second body',
  );
});

it.each([
  '/',
  '/search/',
  '/library/',
  '/library/books/',
  '/404.html',
  '/sitemap.xml',
])('rejects an alias shadowing fixed website route %s', (alias) => {
  expect(() =>
    loadCatalog({
      ...manifest,
      entries: [entry('reserved', { aliases: [alias] })],
    }),
  ).toThrow(/reserved website route/);
});

it.each([
  '/search',
  '/LIBRARY/',
  '/search/index.html',
  '/index.html',
  '/sitemap.xml/x',
  '/pagefind/unsafe/',
])(
  'facade independently rejects unsafe alias %s with owner diagnostics',
  (alias) => {
    expect(() =>
      loadCatalog({
        ...manifest,
        entries: [entry('reserved', { aliases: [alias] })],
      }),
    ).toThrow('Tutorials/Group/reserved.md');
  },
);
