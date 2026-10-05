import { mkdtemp, mkdir, writeFile, rm, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
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
