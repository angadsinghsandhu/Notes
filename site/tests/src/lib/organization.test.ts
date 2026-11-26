import { describe, expect, it } from 'vitest';
import { createEntry } from '../../../src/content/index.js';
import type {
  ContentEntry,
  Membership,
  OrganizationSnapshot,
} from '../../../src/content/index.js';
import { buildOrganizationIndex } from '../../../src/lib/organization.js';

function entry(name: string, fields: Partial<ContentEntry> = {}): ContentEntry {
  return {
    ...createEntry(
      {
        sourcePath: `Books/${name}.md`,
        absolutePath: `/private/${name}`,
        section: 'books',
        kind: 'markdown',
        bytes: 1,
      },
      {
        title: name,
        description: 'Authored',
        tags: [],
        aliases: [],
        draft: false,
      },
    ),
    ...fields,
  };
}
const note = entry('note', { aliases: ['/alias/'] });
const code = entry('code', { kind: 'code' });
const outline = entry('outline');
const supplement = entry('supplement', { role: 'supplemental' });
const pdf = entry('pdf', { kind: 'pdf' });
const uid = (char: string) => `doc-${char.repeat(64)}`;
function membership(
  item: ContentEntry,
  fields: Partial<Membership> = {},
): Membership {
  return {
    entryId: item.id,
    topics: [],
    purpose: 'note',
    status: 'reviewed',
    summary: 'Curated',
    relatedUids: [],
    ...fields,
  };
}
function snapshot(): OrganizationSnapshot {
  return {
    topics: [
      { id: 'root', title: 'Root', summary: '' },
      { id: 'left', title: 'Left', summary: '', parentId: 'root', order: 2 },
      { id: 'right', title: 'Right', summary: '', parentId: 'root', order: 1 },
      { id: 'empty', title: 'Empty', summary: '' },
    ],
    collections: [
      { id: 'book', title: 'Book', summary: '', type: 'book' },
      { id: 'empty', title: 'Empty', summary: '', type: 'workshop' },
    ],
    groups: [
      {
        id: 'chapter',
        collectionId: 'book',
        title: 'Chapter',
        summary: '',
        type: 'chapter',
      },
      {
        id: 'start',
        collectionId: 'book',
        parentId: 'chapter',
        title: 'Start',
        summary: '',
        type: 'project',
        order: 1,
      },
      {
        id: 'finish',
        collectionId: 'book',
        parentId: 'chapter',
        title: 'Finish',
        summary: '',
        type: 'project',
        order: 2,
      },
      {
        id: 'empty',
        collectionId: 'book',
        title: 'Empty',
        summary: '',
        type: 'module',
      },
    ],
    memberships: [
      membership(note, {
        uid: uid('a'),
        topics: ['left', 'right'],
        collectionId: 'book',
        groupId: 'chapter',
      }),
      membership(code, {
        uid: uid('b'),
        topics: ['left'],
        collectionId: 'book',
        groupId: 'start',
        purpose: 'project-file',
      }),
      membership(outline, {
        uid: uid('c'),
        topics: ['right'],
        status: 'outline',
      }),
      membership(supplement, { uid: uid('d'), topics: ['right'] }),
      membership(pdf, {
        uid: uid('e'),
        topics: ['left'],
        collectionId: 'book',
        groupId: 'finish',
        purpose: 'reference',
      }),
    ],
    paths: [
      {
        id: 'study',
        title: 'Study',
        summary: '',
        steps: [
          {
            id: 'resources',
            title: 'Resources',
            summary: '',
            entryUids: [uid('e')],
            topicIds: [],
          },
          {
            id: 'outline',
            title: 'Outline',
            summary: '',
            entryUids: [uid('c')],
            topicIds: [],
          },
          {
            id: 'notes',
            title: 'Notes',
            summary: '',
            entryUids: [uid('a'), uid('b'), uid('d')],
            topicIds: ['root', 'empty'],
          },
        ],
      },
    ],
  };
}
const entries = [note, code, outline, supplement, pdf];
describe('organization index', () => {
  it('topic_descendants_deduplicate_shared_entries', () => {
    const index = buildOrganizationIndex(entries, snapshot());
    expect(index.listNodes('topic').map((n) => n.id)).toEqual(['root']);
    expect(index.listNodes('topic', 'root').map((n) => n.id)).toEqual([
      'right',
      'left',
    ]);
    expect(index.listNodeEntries('topic', 'root')).toEqual([]);
    expect(
      index
        .listNodeEntries('topic', 'root', { descendants: true })
        .map((e) => e.route),
    ).toEqual([note.route, pdf.route]);
    expect(index.getNode('topic', 'root')).toMatchObject({
      type: 'topic',
      entryCount: 2,
      route: '/library/topics/root/',
    });
    expect(index.getNode('topic', 'empty')).toBeUndefined();
    expect(index.getNode('topic', 'missing')).toBeUndefined();
    expect(index.listNodes('topic', 'missing')).toEqual([]);
    expect(index.listNodeEntries('topic', 'missing')).toEqual([]);
  });
  it('group_children_do_not_flatten_projects', () => {
    const index = buildOrganizationIndex(entries, snapshot());
    expect(index.listNodes('collection').map((n) => n.id)).toEqual(['book']);
    expect(index.listNodes('group', 'book').map((n) => n.id)).toEqual([
      'chapter',
    ]);
    expect(index.listNodes('group', 'book/chapter').map((n) => n.id)).toEqual([
      'start',
      'finish',
    ]);
    expect(
      index.listNodeEntries('group', 'book/chapter').map((e) => e.id),
    ).toEqual([note.id]);
    expect(
      index
        .listNodeEntries('group', 'book/chapter', { descendants: true })
        .map((e) => e.id),
    ).toEqual([note.id, pdf.id]);
    expect(
      index
        .listNodeEntries('group', 'book/chapter', {
          descendants: true,
          scope: 'files',
        })
        .map((e) => e.id),
    ).toEqual([note.id, code.id, pdf.id]);
    expect(index.listNodeEntries('collection', 'book')).toEqual([]);
    expect(
      index.listNodeEntries('collection', 'book', {
        descendants: true,
        scope: 'files',
      }),
    ).toHaveLength(3);
    expect(index.getNode('group', 'book/start')).toMatchObject({
      type: 'group',
      record: { type: 'project' },
      entryCount: 0,
      route: '/library/collections/book/groups/start/',
    });
    expect(index.getNode('collection', 'book')).toMatchObject({
      type: 'collection',
      record: { type: 'book' },
    });
    expect(index.listNodes('group').map((n) => n.id)).toEqual(['chapter']);
  });
  it('unregistered_and_outline_access_remains', () => {
    const unregistered = entry('new');
    const index = buildOrganizationIndex(
      [...entries, unregistered, entry('draft', { draft: true })],
      snapshot(),
    );
    expect(index.getMembership(unregistered.id)).toEqual(
      membership(unregistered, { status: 'unreviewed', summary: 'Authored' }),
    );
    expect(index.getEntryByUid(uid('c'))?.id).toBe(outline.id);
    expect(index.getEntryByUid('missing')).toBeUndefined();
    expect(
      index.listNodeEntries('topic', 'root', {
        descendants: true,
        scope: 'files',
      }),
    ).toHaveLength(5);
    const path = index.getNode('path', 'study');
    expect(path?.type).toBe('path');
    if (path?.type !== 'path') throw new Error('missing path');
    expect(path.steps.map((s) => s.id)).toEqual(['resources', 'notes']);
    expect(path.steps[1]!.entries).toEqual([
      { id: note.id, title: note.title, route: note.route },
    ]);
    expect(path.steps[1]!.topics.map((t) => t.id)).toEqual(['root']);
    expect(index.listNodes('path')).toHaveLength(1);
    expect(() => index.getMembership('missing')).toThrow(
      /unknown public entry/i,
    );
  });
  it('provides independent public copies and snapshots its immutable inputs', () => {
    const value = snapshot();
    const polluted = {
      ...note,
      absolutePath: '/private/secret',
      ledger: ['secret'],
    };
    const index = buildOrganizationIndex(
      [polluted, ...entries.slice(1)],
      value,
    );
    const node = index.getNode('path', 'study')!;
    if (node.type !== 'path') throw new Error('missing path');
    node.steps[0]!.entries[0]!.title = 'mutated';
    node.record.steps[0]!.entryUids.push('mutated');
    index.getMembership(note.id).topics.push('mutated');
    index.getEntryByUid(uid('a'))!.tags.push('mutated');
    index.listNodeEntries('topic', 'left')[0]!.aliases.push('/mutated/');
    index.listNodes('topic')[0]!.title = 'mutated';
    value.topics[0]!.title = 'mutated input';
    polluted.title = 'mutated input';
    expect(index.getNode('topic', 'root')!.title).toBe('Root');
    expect(index.getEntryByUid(uid('a'))!.title).toBe('note');
    expect(
      JSON.stringify([
        index.listNodes('path'),
        index.getMembership(note.id),
        index.getEntryByUid(uid('a')),
      ]),
    ).not.toMatch(/mutated|ledger|absolutePath|private|bodyFile/);
  });
  it('supports a legacy empty organization and omits paths emptied by learning filters', () => {
    const index = buildOrganizationIndex([note, code, supplement, pdf]);
    expect(index.listNodes('topic')).toEqual([]);
    expect(index.listNodes('path')).toEqual([]);
    expect(index.getMembership(code.id).purpose).toBe('project-file');
    expect(index.getMembership(pdf.id).purpose).toBe('reference');
    expect(index.getMembership(supplement.id).purpose).toBe('reference');
    const value = snapshot();
    value.paths[0]!.steps = [value.paths[0]!.steps[1]!];
    expect(buildOrganizationIndex(entries, value).listNodes('path')).toEqual(
      [],
    );
  });
});

it('retains collection metadata, direct collection entries and deterministic natural group order', () => {
  const first = entry('direct');
  const second = entry('other');
  const third = entry('third');
  const value = snapshot();
  value.collections[0] = {
    id: 'book',
    title: 'Book',
    summary: 'Authored collection',
    type: 'book',
    provider: 'Provider',
    courseCode: 'Course',
    edition: 'Second',
    year: 2026,
    semester: 'Autumn',
  };
  value.groups = [
    {
      id: 'group-b',
      collectionId: 'book',
      title: 'Chapter 10',
      summary: '',
      type: 'module',
    },
    {
      id: 'group-a',
      collectionId: 'book',
      title: 'Chapter 2',
      summary: '',
      type: 'reference',
    },
    {
      id: 'same-b',
      collectionId: 'book',
      title: 'Same',
      summary: '',
      type: 'assessment',
    },
    {
      id: 'same-a',
      collectionId: 'book',
      title: 'Same',
      summary: '',
      type: 'assessment',
    },
  ];
  const fourth = entry('fourth');
  const fifth = entry('fifth');
  value.memberships = [
    membership(first, { collectionId: 'book' }),
    membership(second, { collectionId: 'book', groupId: 'group-b' }),
    membership(third, { collectionId: 'book', groupId: 'group-a' }),
    membership(fourth, { collectionId: 'book', groupId: 'same-b' }),
    membership(fifth, { collectionId: 'book', groupId: 'same-a' }),
  ];
  value.paths = [];
  const index = buildOrganizationIndex(
    [first, second, third, fourth, fifth],
    value,
  );
  expect(index.getNode('collection', 'book')).toMatchObject({
    record: value.collections[0],
    entryCount: 5,
  });
  expect(index.listNodeEntries('collection', 'book').map((e) => e.id)).toEqual([
    first.id,
  ]);
  expect(index.listNodes('group', 'book').map((n) => n.id)).toEqual([
    'group-a',
    'group-b',
    'same-a',
    'same-b',
  ]);
});

it('excludes editorial drafts and filters missing path references without exposing internal metadata', () => {
  const value = snapshot();
  value.memberships[0]!.status = 'draft';
  value.paths[0]!.steps[0]!.entryUids.push('missing');
  value.paths[0]!.steps[0]!.topicIds.push('missing');
  const index = buildOrganizationIndex(entries, value);
  expect(index.getEntryByUid(uid('a'))).toBeUndefined();
  expect(() => index.getMembership(note.id)).toThrow('Unknown public entry');
  expect(
    index.listNodeEntries('topic', 'left', { scope: 'files' }).map((e) => e.id),
  ).toEqual([code.id, pdf.id]);
  const path = index.getNode('path', 'study');
  if (path?.type !== 'path') throw new Error('missing path');
  expect(path.steps[0]!.entries.map((e) => e.id)).toEqual([pdf.id]);
});
