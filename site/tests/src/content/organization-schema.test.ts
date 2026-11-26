import { afterEach, describe, expect, it } from 'vitest';
import { mkdir, mkdtemp, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  readOrganization,
  validateOrganization,
} from '../../../src/content/organization-schema.js';

const uid = `doc-${'a'.repeat(64)}`;
const otherUid = `doc-${'b'.repeat(64)}`;
function definition() {
  return {
    taxonomy: {
      version: 1,
      topics: [{ id: 'ml', title: 'Machine learning', summary: 'x < y' }],
    },
    collections: {
      version: 1,
      collections: [{ id: 'book', title: 'Book', summary: '', type: 'book' }],
      groups: [
        {
          id: 'chapter',
          collectionId: 'book',
          title: 'Chapter',
          summary: '',
          type: 'chapter',
        },
      ],
    },
    entries: {
      version: 1,
      entries: [
        {
          uid,
          sourcePath: 'Books/note.md',
          topics: ['ml'],
          collectionId: 'book',
          groupId: 'chapter',
          purpose: 'note',
          status: 'unreviewed',
          relatedUids: [otherUid],
        },
        {
          uid: otherUid,
          sourcePath: 'Books/other.md',
          topics: [],
          purpose: 'reference',
          status: 'reviewed',
        },
      ],
    },
    paths: {
      version: 1,
      paths: [
        {
          id: 'study',
          title: 'Study',
          summary: '',
          steps: [
            {
              id: 'first',
              title: 'First',
              summary: '',
              entryUids: [uid],
              topicIds: ['ml'],
            },
          ],
        },
      ],
    },
  };
}
const dirs: string[] = [];
afterEach(async () => {
  await Promise.all(
    dirs.splice(0).map((dir) => rm(dir, { recursive: true, force: true })),
  );
});

describe('strict organization registry', () => {
  it('accepts four strict versioned sidecars and preserves plain text', () => {
    const value = definition();
    expect(validateOrganization(value)).toEqual(value);
  });
  it.each([
    [
      'topic duplicate',
      (v: ReturnType<typeof definition>) =>
        v.taxonomy.topics.push({ ...v.taxonomy.topics[0]! }),
      'ml',
    ],
    [
      'topic case collision',
      (v: ReturnType<typeof definition>) =>
        v.taxonomy.topics.push({ id: 'ML', title: 'Other', summary: '' }),
      'ML',
    ],
    [
      'collection duplicate',
      (v: ReturnType<typeof definition>) =>
        v.collections.collections.push({ ...v.collections.collections[0]! }),
      'book',
    ],
    [
      'group duplicate',
      (v: ReturnType<typeof definition>) =>
        v.collections.groups.push({ ...v.collections.groups[0]! }),
      'chapter',
    ],
    [
      'UID duplicate',
      (v: ReturnType<typeof definition>) =>
        v.entries.entries.push({
          ...v.entries.entries[0]!,
          sourcePath: 'Books/new.md',
        }),
      uid,
    ],
    [
      'source case collision',
      (v: ReturnType<typeof definition>) =>
        (v.entries.entries[1]!.sourcePath = 'Books/NOTE.md'),
      'Books/NOTE.md',
    ],
    [
      'path duplicate',
      (v: ReturnType<typeof definition>) =>
        v.paths.paths.push({ ...v.paths.paths[0]! }),
      'study',
    ],
    [
      'step duplicate',
      (v: ReturnType<typeof definition>) =>
        v.paths.paths[0]!.steps.push({ ...v.paths.paths[0]!.steps[0]! }),
      'first',
    ],
    [
      'topic reference',
      (v: ReturnType<typeof definition>) =>
        (v.entries.entries[0]!.topics = ['missing']),
      'Books/note.md',
    ],
    [
      'related reference',
      (v: ReturnType<typeof definition>) =>
        (v.entries.entries[0]!.relatedUids = [`doc-${'c'.repeat(64)}`]),
      'Books/note.md',
    ],
    [
      'step UID',
      (v: ReturnType<typeof definition>) =>
        (v.paths.paths[0]!.steps[0]!.entryUids = [`doc-${'c'.repeat(64)}`]),
      'first',
    ],
    [
      'step topic',
      (v: ReturnType<typeof definition>) =>
        (v.paths.paths[0]!.steps[0]!.topicIds = ['missing']),
      'first',
    ],
    [
      'collection reference',
      (v: ReturnType<typeof definition>) =>
        (v.entries.entries[0]!.collectionId = 'missing'),
      'Books/note.md',
    ],
    [
      'group reference',
      (v: ReturnType<typeof definition>) =>
        (v.entries.entries[0]!.groupId = 'missing'),
      'Books/note.md',
    ],
    [
      'empty step',
      (v: ReturnType<typeof definition>) => {
        v.paths.paths[0]!.steps[0]!.entryUids = [];
        v.paths.paths[0]!.steps[0]!.topicIds = [];
      },
      'first',
    ],
  ])('rejects_invalid_registry_graphs: %s', (_name, mutate, record) => {
    const value = definition();
    mutate(value);
    expect(() => validateOrganization(value)).toThrow(record);
  });
  it.each([
    ['unknown root field', { ...definition(), extra: true }, 'extra'],
    [
      'unknown topic field',
      {
        ...definition(),
        taxonomy: {
          version: 1,
          topics: [{ id: 'ml', title: 'ML', summary: '', extra: true }],
        },
      },
      'ml',
    ],
    [
      'unknown entry enum',
      {
        ...definition(),
        entries: {
          version: 1,
          entries: [
            {
              uid,
              sourcePath: 'Books/note.md',
              topics: [],
              purpose: 'lesson',
              status: 'unreviewed',
            },
          ],
        },
      },
      'Books/note.md',
    ],
    [
      'unknown collection enum',
      {
        ...definition(),
        collections: {
          version: 1,
          collections: [
            { id: 'book', title: 'Book', summary: '', type: 'magazine' },
          ],
          groups: [],
        },
      },
      'book',
    ],
    [
      'invalid UID',
      {
        ...definition(),
        entries: {
          version: 1,
          entries: [
            {
              uid: 'doc-ABC',
              sourcePath: 'Books/note.md',
              topics: [],
              purpose: 'note',
              status: 'unreviewed',
            },
          ],
        },
      },
      'Books/note.md',
    ],
    [
      'future version',
      { ...definition(), taxonomy: { version: 2, topics: [] } },
      'version',
    ],
    [
      'group without collection membership',
      {
        ...definition(),
        entries: {
          version: 1,
          entries: [
            {
              uid,
              sourcePath: 'Books/note.md',
              topics: [],
              groupId: 'chapter',
              purpose: 'note',
              status: 'unreviewed',
            },
          ],
        },
      },
      'Books/note.md',
    ],
  ])('rejects_invalid_registry_graphs: %s', (_name, value, record) => {
    expect(() => validateOrganization(value)).toThrow(record);
  });
  it.each([
    '/Books/note.md',
    'Books/../note.md',
    'Books//note.md',
    'Books\\note.md',
    'Other/note.md',
    'Books/note.md/',
    'Books/cafe\u0301.md',
    'Books/line\n.md',
  ])('rejects invalid source path %j', (sourcePath) => {
    const value = definition();
    value.entries.entries[0]!.sourcePath = sourcePath;
    expect(() => validateOrganization(value)).toThrow('sourcePath');
  });
  it('rejects topic cycles, missing parents and depth beyond three', () => {
    for (const topics of [
      [{ id: 'ml', parentId: 'ml', title: 'ML', summary: '' }],
      [{ id: 'ml', parentId: 'absent', title: 'ML', summary: '' }],
      ['a', 'b', 'c', 'ml'].map((id, index, all) => ({
        id,
        title: id,
        summary: '',
        ...(index ? { parentId: all[index - 1] } : {}),
      })),
      [
        { id: 'ml', parentId: 'other', title: 'ML', summary: '' },
        { id: 'other', parentId: 'ml', title: 'Other', summary: '' },
      ],
    ]) {
      expect(() =>
        validateOrganization({
          ...definition(),
          taxonomy: { version: 1, topics },
        }),
      ).toThrow(/ml|depth/);
    }
  });
  it('rejects group cycles, missing collection and cross-collection parents', () => {
    for (const groups of [
      [
        {
          id: 'chapter',
          collectionId: 'book',
          parentId: 'chapter',
          title: 'Chapter',
          summary: '',
          type: 'chapter',
        },
      ],
      [
        {
          id: 'chapter',
          collectionId: 'missing',
          title: 'Chapter',
          summary: '',
          type: 'chapter',
        },
      ],
      [
        {
          id: 'chapter',
          collectionId: 'book',
          parentId: 'foreign',
          title: 'Chapter',
          summary: '',
          type: 'chapter',
        },
        {
          id: 'foreign',
          collectionId: 'second',
          title: 'Foreign',
          summary: '',
          type: 'reference',
        },
      ],
      [
        {
          id: 'chapter',
          collectionId: 'book',
          parentId: 'child',
          title: 'Chapter',
          summary: '',
          type: 'chapter',
        },
        {
          id: 'child',
          collectionId: 'book',
          parentId: 'chapter',
          title: 'Child',
          summary: '',
          type: 'module',
        },
      ],
    ]) {
      const value = definition();
      expect(() =>
        validateOrganization({
          ...value,
          collections: {
            ...value.collections,
            collections: [
              ...value.collections.collections,
              { id: 'second', title: 'Second', summary: '', type: 'workshop' },
            ],
            groups,
          },
        }),
      ).toThrow('chapter');
    }
  });
  it('permits group and step IDs in distinct owning namespaces', () => {
    const value = definition();
    value.collections.collections.push({
      id: 'second',
      title: 'Second',
      summary: '',
      type: 'book',
    });
    value.collections.groups.push({
      ...value.collections.groups[0]!,
      collectionId: 'second',
    });
    value.paths.paths.push({ ...value.paths.paths[0]!, id: 'second' });
    expect(validateOrganization(value)).toEqual(value);
  });
  it('reads absent organization as empty without writing files', async () => {
    const directory = await mkdtemp(join(tmpdir(), 'notes-organization-'));
    dirs.push(directory);
    expect(await readOrganization(join(directory, 'missing'))).toEqual({
      taxonomy: { version: 1, topics: [] },
      collections: { version: 1, collections: [], groups: [] },
      entries: { version: 1, entries: [] },
      paths: { version: 1, paths: [] },
    });
    expect(await readdir(directory)).toEqual([]);
  });
  it('reads all sidecars and identifies missing, malformed or invalid files', async () => {
    const directory = await mkdtemp(join(tmpdir(), 'notes-organization-'));
    dirs.push(directory);
    const value = definition();
    await expect(readOrganization(directory)).rejects.toThrow('taxonomy.json');
    for (const [name, data] of Object.entries(value))
      await writeFile(join(directory, `${name}.json`), JSON.stringify(data));
    expect(await readOrganization(directory)).toEqual(value);
    await writeFile(join(directory, 'entries.json'), '{broken');
    await expect(readOrganization(directory)).rejects.toThrow('entries.json');
    await writeFile(
      join(directory, 'entries.json'),
      JSON.stringify({ ...value.entries, extra: true }),
    );
    await expect(readOrganization(directory)).rejects.toThrow('extra');
    await mkdir(join(directory, 'taxonomy.json.child'));
  });
});
