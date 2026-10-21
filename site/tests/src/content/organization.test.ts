import { describe, expect, it } from 'vitest';
import { createEntry } from '../../../src/content/identifiers.js';
import { validateOrganization } from '../../../src/content/organization-schema.js';
import { resolveOrganization } from '../../../src/content/organization.js';
import type { ContentEntry } from '../../../src/content/types.js';

function entry(
  sourcePath = 'Books/note.md',
  overrides: Partial<ContentEntry> = {},
): ContentEntry {
  return {
    ...createEntry(
      {
        sourcePath,
        absolutePath: `/repository/${sourcePath}`,
        section: 'books',
        kind: 'markdown',
        bytes: 10,
      },
      {
        title: 'Note',
        description: 'Original description',
        draft: false,
        tags: [],
        aliases: [],
      },
    ),
    bodyFile: 'bodies/original.json',
    ...overrides,
  };
}
const uid = `doc-${'a'.repeat(64)}`;
const secondUid = `doc-${'b'.repeat(64)}`;
function definition() {
  return {
    taxonomy: {
      version: 1,
      topics: [
        { id: 'ml', title: 'Machine Learning', summary: '' },
        { id: 'child', parentId: 'ml', title: 'Child', summary: '' },
      ],
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
          topics: ['child'],
          collectionId: 'book',
          groupId: 'chapter',
          purpose: 'exercise',
          status: 'reviewed',
          summary: 'Curated',
          relatedUids: [secondUid],
        },
        {
          uid: secondUid,
          sourcePath: 'Books/second.md',
          topics: [],
          purpose: 'reference',
          status: 'unreviewed',
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
              id: 'second',
              title: 'Second',
              summary: '',
              entryUids: [secondUid],
              topicIds: [],
            },
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

describe('organization resolution', () => {
  it('preserves_registered_uid_when_source_path_changes', () => {
    const original = entry();
    const moved = entry('Books/moved.md');
    const value = definition();
    value.entries.entries[0]!.sourcePath = moved.sourcePath;
    const frozen = JSON.stringify([moved, value]);
    const snapshot = resolveOrganization(
      [moved, entry('Books/second.md')],
      validateOrganization(value),
    );
    expect(snapshot.memberships[0]).toEqual({
      entryId: moved.id,
      uid,
      topics: ['child'],
      collectionId: 'book',
      groupId: 'chapter',
      purpose: 'exercise',
      status: 'reviewed',
      summary: 'Curated',
      relatedUids: [secondUid],
    });
    expect(moved.id).not.toBe(original.id);
    expect(moved.bodyFile).toBe('bodies/original.json');
    expect(JSON.stringify([moved, value])).toBe(frozen);
    expect(snapshot.paths[0]!.steps.map((step) => step.id)).toEqual([
      'second',
      'first',
    ]);
    expect(JSON.stringify(snapshot)).not.toContain('/repository');
  });
  it('resolves_unregistered_defaults', () => {
    const entries = [
      entry('Books/note.md'),
      entry('Books/notebook.ipynb', { kind: 'notebook', description: '' }),
      entry('Books/code.py', { kind: 'code' }),
      entry('Books/reference.pdf', { kind: 'pdf' }),
      entry('Books/slides.pptx', { kind: 'slides' }),
      entry('Books/template.md', { role: 'supplemental' }),
      entry('Books/template.ipynb', { kind: 'notebook', role: 'supplemental' }),
    ];
    const snapshot = resolveOrganization(
      entries,
      validateOrganization({
        taxonomy: { version: 1, topics: [] },
        collections: { version: 1, collections: [], groups: [] },
        entries: { version: 1, entries: [] },
        paths: { version: 1, paths: [] },
      }),
    );
    expect(snapshot.memberships.map((record) => record.purpose)).toEqual([
      'note',
      'note',
      'project-file',
      'reference',
      'reference',
      'reference',
      'reference',
    ]);
    for (const [index, record] of snapshot.memberships.entries()) {
      expect(record).toEqual({
        entryId: entries[index]!.id,
        topics: [],
        purpose: record.purpose,
        status: 'unreviewed',
        summary: entries[index]!.description,
        relatedUids: [],
      });
      expect(record).not.toHaveProperty('uid');
    }
  });
  it('uses authored description when a registered summary is absent, including explicit empty summary', () => {
    const value = definition();
    const record = value.entries.entries[0]!;
    const withoutSummary = Object.fromEntries(
      Object.entries(record).filter(([key]) => key !== 'summary'),
    );
    const noSummary = {
      ...value,
      entries: {
        version: 1,
        entries: [withoutSummary, value.entries.entries[1]!],
      },
    };
    expect(
      resolveOrganization(
        [entry(), entry('Books/second.md')],
        validateOrganization(noSummary),
      ).memberships[0]!.summary,
    ).toBe('Original description');
    record.summary = '';
    expect(
      resolveOrganization(
        [entry(), entry('Books/second.md')],
        validateOrganization(value),
      ).memberships[0]!.summary,
    ).toBe('');
  });
  it('retains draft classification in definition and omits public memberships', () => {
    const value = definition();
    value.entries.entries[0]!.status = 'draft';
    value.entries.entries[0]!.relatedUids = [];
    value.paths.paths = [];
    const validated = validateOrganization(value);
    const snapshot = resolveOrganization(
      [
        entry(),
        entry('Books/second.md'),
        entry('Books/unregistered.md', { draft: true }),
      ],
      validated,
    );
    expect(validated.entries.entries[0]!.status).toBe('draft');
    expect(snapshot.memberships.map((record) => record.entryId)).toEqual([
      entry('Books/second.md').id,
    ]);
  });
  it('rejects stale sources even if their registry status is draft', () => {
    const value = definition();
    value.entries.entries[0]!.status = 'draft';
    expect(() =>
      resolveOrganization(
        [entry('Books/second.md')],
        validateOrganization(value),
      ),
    ).toThrow('Books/note.md');
  });
  it.each(['organization', 'publication'])(
    'rejects path and related links to %s drafts',
    (source) => {
      const value = definition();
      const entries = [
        entry(),
        entry('Books/second.md', { draft: source === 'publication' }),
      ];
      if (source === 'organization') value.entries.entries[1]!.status = 'draft';
      expect(() =>
        resolveOrganization(entries, validateOrganization(value)),
      ).toThrow(/Books\/note.md.*draft/);
      value.entries.entries[0]!.relatedUids = [];
      expect(() =>
        resolveOrganization(entries, validateOrganization(value)),
      ).toThrow(/second.*draft/);
    },
  );
  it('rejects missing or excluded related/path targets instead of treating them as drafts', () => {
    expect(() =>
      resolveOrganization([entry()], validateOrganization(definition())),
    ).toThrow('Books/second.md');
  });
  it('requires every topic-only step to contain a public learning entry, considering descendants', () => {
    const value = definition();
    value.paths.paths[0]!.steps = [
      {
        id: 'topic',
        title: 'Topic',
        summary: '',
        entryUids: [],
        topicIds: ['ml'],
      },
    ];
    expect(
      resolveOrganization(
        [entry(), entry('Books/second.md')],
        validateOrganization(value),
      ).paths[0]!.steps[0]!.topicIds,
    ).toEqual(['ml']);
    for (const overrides of [
      { role: 'supplemental' as const },
      { draft: true },
    ])
      expect(() =>
        resolveOrganization(
          [entry('Books/note.md', overrides), entry('Books/second.md')],
          validateOrganization({
            ...value,
            entries: {
              ...value.entries,
              entries: value.entries.entries.map((record) => ({
                ...record,
                relatedUids: [],
              })),
            },
          }),
        ),
      ).toThrow('topic');
    for (const purpose of ['project-file', 'note']) {
      value.entries.entries[0]!.purpose = purpose;
      value.entries.entries[0]!.status =
        purpose === 'note' ? 'outline' : 'unreviewed';
      expect(() =>
        resolveOrganization(
          [entry(), entry('Books/second.md')],
          validateOrganization(value),
        ),
      ).toThrow('topic');
    }
  });
  it('returns independent public copies', () => {
    const value = validateOrganization(definition());
    const snapshot = resolveOrganization(
      [entry(), entry('Books/second.md')],
      value,
    );
    snapshot.topics[0]!.title = 'Changed';
    snapshot.memberships[0]!.topics.push('changed');
    snapshot.paths[0]!.steps[0]!.entryUids.push(uid);
    expect(value.taxonomy.topics[0]!.title).toBe('Machine Learning');
    expect(value.entries.entries[0]!.topics).toEqual(['child']);
    expect(value.paths.paths[0]!.steps[0]!.entryUids).toEqual([secondUid]);
  });
});
