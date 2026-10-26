import { expect, it } from 'vitest';
import { createEntry } from '../../../src/content/index.js';
import type {
  Manifest,
  OrganizationSnapshot,
} from '../../../src/content/index.js';
import { loadCatalog, readPreparedCatalog } from '../../../src/lib/catalog.js';
import {
  organizationTree,
  readerOrganization,
  organizationDocuments,
  organizationCards,
  projectFileTree,
} from '../../../src/lib/organization-pages.js';
const note = createEntry(
  {
    sourcePath: 'Books/chapter/note.md',
    absolutePath: '/private/note.md',
    section: 'books',
    kind: 'markdown',
    bytes: 1,
  },
  {
    title: 'Note',
    description: 'Original',
    tags: [],
    aliases: [],
    draft: false,
  },
);
const code = {
  ...note,
  id: 'b'.repeat(64),
  sourcePath: 'Books/project/src/App.js',
  kind: 'code' as const,
  route: '/resources/books/project/src/app/',
};
const snapshot: OrganizationSnapshot = {
  topics: [
    { id: 'root', title: 'Root', summary: '' },
    { id: 'leaf', title: 'Leaf', summary: '', parentId: 'root' },
  ],
  collections: [{ id: 'book', title: 'Book', summary: '', type: 'book' }],
  groups: [
    {
      id: 'module',
      collectionId: 'book',
      title: 'Module',
      summary: '',
      type: 'module',
    },
    {
      id: 'project',
      collectionId: 'book',
      parentId: 'module',
      title: 'Project',
      summary: '',
      type: 'project',
    },
  ],
  paths: [],
  memberships: [
    {
      entryId: note.id,
      topics: ['leaf'],
      collectionId: 'book',
      groupId: 'module',
      purpose: 'exercise',
      status: 'unreviewed',
      summary: 'Curated',
      relatedUids: [],
    },
    {
      entryId: code.id,
      topics: [],
      collectionId: 'book',
      groupId: 'project',
      purpose: 'project-file',
      status: 'outline',
      summary: '',
      relatedUids: [],
    },
  ],
};
const manifest: Manifest = {
  version: 1,
  entries: [note, code],
  organization: snapshot,
  assets: [],
  ledger: [],
};
it('builds public topic trees and compact active collection branches', () => {
  const index = loadCatalog(manifest).organization;
  expect(organizationTree(index, 'topic')[0]?.children[0]?.route).toBe(
    '/library/topics/leaf/',
  );
  expect(
    organizationTree(index, 'group', 'book', 'project')[0]?.children[0]?.title,
  ).toBe('Project');
  expect(
    organizationTree(index, 'group', 'book', 'unknown')[0]?.children,
  ).toEqual([]);
});
it('keeps reader metadata small, generation bound and independent of subsequent selections', () => {
  const first = loadCatalog(manifest);
  const metadata = readerOrganization(first, note);
  const later = loadCatalog({
    ...manifest,
    organization: {
      ...snapshot,
      topics: snapshot.topics.map((t) => ({ ...t, title: 'New' })),
    },
  });
  expect(metadata.topics[0]?.title).toBe('Leaf');
  expect(readerOrganization(later, note).topics[0]?.title).toBe('New');
  expect(metadata.collection?.title).toBe('Book');
  expect(metadata.group?.title).toBe('Module');
  expect(metadata.status).toBe('unreviewed');
  expect(metadata.summary).toBe('Curated');
  expect(JSON.stringify(metadata)).not.toMatch(
    /bodyFile|memberships|headings|absolutePath/,
  );
  expect(
    readerOrganization(
      loadCatalog({ version: 1, entries: [note], assets: [], ledger: [] }),
      note,
    ).topics,
  ).toEqual([]);
});
it('separates direct notes exercises and resource outlines without flattening child projects', () => {
  const index = loadCatalog(manifest).organization;
  expect(
    organizationDocuments(index, 'group', 'book/module').exercises.map(
      (d) => d.title,
    ),
  ).toEqual(['Note']);
  expect(
    organizationDocuments(index, 'group', 'book/module').resources,
  ).toEqual([]);
  expect(
    organizationDocuments(index, 'group', 'book/project').resources[0]?.status,
  ).toBe('outline');
  expect(
    organizationDocuments(index, 'topic', 'root', true).exercises,
  ).toHaveLength(1);
  const changed = loadCatalog({
    ...manifest,
    organization: {
      ...snapshot,
      memberships: snapshot.memberships.map((m) => ({ ...m, purpose: 'note' })),
    },
  }).organization;
  expect(
    organizationDocuments(changed, 'group', 'book/module').notes,
  ).toHaveLength(1);
});
it('reports learning documents, descendant groups and resources honestly on cards', () => {
  const index = loadCatalog(manifest).organization;
  expect(
    organizationCards(index, index.listNodes('collection'))[0],
  ).toMatchObject({ learningCount: 1, resourceCount: 1, projectCount: 1 });
  expect(
    organizationCards(index, index.listNodes('group', 'book/module'))[0],
  ).toMatchObject({ learningCount: 0, resourceCount: 1 });
});
it('builds an ordered relative file tree with canonical leaves and no archive prefix', () => {
  const docs = organizationDocuments(
    loadCatalog(manifest).organization,
    'group',
    'book/project',
  ).resources;
  const tree = projectFileTree([
    ...docs,
    {
      ...docs[0]!,
      id: 'c',
      sourcePath: 'Books/project/index.html',
      title: 'Index',
      route: '/resources/books/project/index/',
    },
  ]);
  expect(tree.map((n) => n.title)).toEqual(['index.html', 'src']);
  expect(tree[1]?.children[0]).toMatchObject({
    title: 'App.js',
    route: code.route,
  });
  expect(projectFileTree([])).toEqual([]);
});
it('shared emission exactly matches populated selector traversal for actual pilots', async () => {
  const catalog = await readPreparedCatalog();
  const tree = (type: 'topic' | 'group', parent?: string): string[] =>
    catalog.organization
      .listNodes(type, parent)
      .flatMap((n) => [
        n.route,
        ...tree(
          type,
          n.type === 'group' ? n.record.collectionId + '/' + n.id : n.id,
        ),
      ]);
  const expected = [
    '/library/topics/',
    '/library/collections/',
    '/library/paths/',
    ...tree('topic'),
    ...catalog.organization
      .listNodes('collection')
      .flatMap((n) => [n.route, ...tree('group', n.id)]),
    ...catalog.organization.listNodes('path').map((n) => n.route),
  ];
  expect(catalog.organizationRoutes().sort()).toEqual(expected.sort());
  expect(catalog.organizationRoutes()).toContain(
    '/library/collections/react-complete-guide/groups/project-03-react-essentials-01-starting-project/',
  );
});

it('emission agrees with selector population for file-only, outline, supplemental and draft ancestors', () => {
  for (const fields of [
    { status: 'outline' as const },
    { status: 'draft' as const },
    { purpose: 'project-file' as const },
  ]) {
    const data = {
      ...snapshot,
      memberships: snapshot.memberships.map((m) => ({ ...m, ...fields })),
      paths: [
        {
          id: 'study',
          title: 'Study',
          summary: '',
          steps: [
            {
              id: 'one',
              title: 'One',
              summary: '',
              entryUids: [],
              topicIds: ['root'],
            },
          ],
        },
      ],
    };
    for (const entries of [
      [note, code],
      [{ ...note, role: 'supplemental' as const }, code],
      [{ ...note, draft: true }, code],
    ]) {
      const catalog = loadCatalog({ ...manifest, entries, organization: data });
      const walk = (type: 'topic' | 'group', parent?: string): string[] =>
        catalog.organization
          .listNodes(type, parent)
          .flatMap((n) => [
            n.route,
            ...walk(
              type,
              n.type === 'group' ? n.record.collectionId + '/' + n.id : n.id,
            ),
          ]);
      const expected = [
        '/library/topics/',
        '/library/collections/',
        '/library/paths/',
        ...walk('topic'),
        ...catalog.organization
          .listNodes('collection')
          .flatMap((n) => [n.route, ...walk('group', n.id)]),
        ...catalog.organization.listNodes('path').map((n) => n.route),
      ];
      expect(catalog.organizationRoutes().sort()).toEqual(expected.sort());
    }
  }
});

it('keeps path cards and topic counts separate from collection project counts', () => {
  const data = {
    ...snapshot,
    memberships: snapshot.memberships.map((m) =>
      m.entryId === note.id ? { ...m, uid: 'doc-' + 'a'.repeat(64) } : m,
    ),
    paths: [
      {
        id: 'study',
        title: 'Study',
        summary: 'Sequence',
        steps: [
          {
            id: 'one',
            title: 'One',
            summary: '',
            entryUids: ['doc-' + 'a'.repeat(64)],
            topicIds: [],
          },
        ],
      },
    ],
  };
  const index = loadCatalog({ ...manifest, organization: data }).organization;
  expect(organizationCards(index, index.listNodes('path'))).toEqual([
    {
      id: 'study',
      title: 'Study',
      route: '/library/paths/study/',
      summary: 'Sequence',
      learningCount: 1,
      resourceCount: 0,
      projectCount: 0,
    },
  ]);
  expect(organizationCards(index, index.listNodes('topic'))[0]).toMatchObject({
    learningCount: 1,
    resourceCount: 0,
    projectCount: 0,
  });
});
it('collection-level readers keep root group links without selecting an unrelated branch', () => {
  const catalog = loadCatalog({
    ...manifest,
    organization: {
      ...snapshot,
      memberships: snapshot.memberships.map((m) =>
        m.entryId === note.id
          ? {
              entryId: note.id,
              topics: [],
              collectionId: 'book',
              purpose: 'note',
              status: 'unreviewed',
              summary: '',
              relatedUids: [],
            }
          : m,
      ),
    },
  });
  const metadata = readerOrganization(catalog, note);
  expect(metadata.group).toBeUndefined();
  expect(metadata.tree[0]?.title).toBe('Module');
  expect(metadata.tree[0]?.children).toEqual([]);
});
it('file tree shares directories without duplicating nodes or losing leaf links', () => {
  const document = organizationDocuments(
    loadCatalog(manifest).organization,
    'group',
    'book/project',
  ).resources[0]!;
  const tree = projectFileTree([
    document,
    {
      ...document,
      id: 'other',
      sourcePath: 'Books/project/src/utils/format.js',
      route: '/resources/format/',
    },
    {
      ...document,
      id: 'third',
      sourcePath: 'Books/project/src/utils/parse.js',
      route: '/resources/parse/',
    },
  ]);
  expect(tree.map((n) => n.title)).toEqual(['App.js', 'utils']);
  expect(tree[1]?.children.map((n) => n.title)).toEqual([
    'format.js',
    'parse.js',
  ]);
});
