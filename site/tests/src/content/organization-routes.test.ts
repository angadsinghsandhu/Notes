import { expect, it } from 'vitest';
import {
  createEntry,
  organizationPageRoutes,
} from '../../../src/content/index.js';
import type {
  Membership,
  OrganizationSnapshot,
} from '../../../src/content/index.js';

const note = createEntry(
  {
    sourcePath: 'Books/note.md',
    absolutePath: '/private/note.md',
    section: 'books',
    kind: 'markdown',
    bytes: 1,
  },
  { title: 'Note', description: '', tags: [], aliases: [], draft: false },
);
const file = {
  ...note,
  id: 'b'.repeat(64),
  kind: 'code' as const,
  route: '/resources/books/file/',
};
const member = (
  entryId: string,
  fields: Partial<Membership> = {},
): Membership => ({
  entryId,
  topics: [],
  purpose: 'note',
  status: 'unreviewed',
  summary: '',
  relatedUids: [],
  ...fields,
});
const snapshot = (): OrganizationSnapshot => ({
  topics: [
    { id: 'root', title: 'Root', summary: '' },
    { id: 'leaf', title: 'Leaf', summary: '', parentId: 'root' },
    { id: 'empty', title: 'Empty', summary: '' },
  ],
  collections: [
    { id: 'book', title: 'Book', summary: '', type: 'book' },
    { id: 'empty', title: 'Empty', summary: '', type: 'book' },
  ],
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
    {
      id: 'empty',
      collectionId: 'book',
      title: 'Empty',
      summary: '',
      type: 'chapter',
    },
  ],
  memberships: [
    member(note.id, { uid: 'doc-' + 'a'.repeat(64), topics: ['leaf'] }),
    member(file.id, {
      topics: ['leaf'],
      collectionId: 'book',
      groupId: 'project',
      purpose: 'project-file',
    }),
  ],
  paths: [
    {
      id: 'study',
      title: 'Study',
      summary: '',
      steps: [
        {
          id: 'topic',
          title: 'Topic',
          summary: '',
          entryUids: [],
          topicIds: ['root'],
        },
      ],
    },
    {
      id: 'direct',
      title: 'Direct',
      summary: '',
      steps: [
        {
          id: 'entry',
          title: 'Entry',
          summary: '',
          entryUids: ['doc-' + 'a'.repeat(64)],
          topicIds: [],
        },
      ],
    },
    { id: 'empty', title: 'Empty', summary: '', steps: [] },
  ],
});
it('emits fixed indexes without organization data', () => {
  expect(organizationPageRoutes([note])).toEqual([
    '/library/topics/',
    '/library/collections/',
    '/library/paths/',
  ]);
});
it('emits populated ancestors, nested groups and learning paths while omitting empty claims', () => {
  expect(organizationPageRoutes([note, file], snapshot())).toEqual([
    '/library/topics/',
    '/library/collections/',
    '/library/paths/',
    '/library/topics/root/',
    '/library/topics/leaf/',
    '/library/collections/book/',
    '/library/collections/book/groups/module/',
    '/library/collections/book/groups/project/',
    '/library/paths/study/',
    '/library/paths/direct/',
  ]);
});
it('keeps public outline/file topic and group routes but omits ineligible path steps and drafts', () => {
  const data = snapshot();
  data.memberships[0]!.status = 'outline';
  expect(organizationPageRoutes([note, file], data)).not.toContain(
    '/library/paths/study/',
  );
  expect(organizationPageRoutes([note, file], data)).not.toContain(
    '/library/paths/direct/',
  );
  data.memberships[0]!.status = 'draft';
  expect(
    organizationPageRoutes([note, { ...file, draft: true }], data),
  ).toEqual(['/library/topics/', '/library/collections/', '/library/paths/']);
  data.memberships = [];
  expect(organizationPageRoutes([note], data)).toEqual([
    '/library/topics/',
    '/library/collections/',
    '/library/paths/',
  ]);
});
it('treats supplemental entries as files without eligible learning path population', () => {
  const data = snapshot();
  expect(
    organizationPageRoutes([{ ...note, role: 'supplemental' }, file], data),
  ).toContain('/library/topics/leaf/');
  expect(
    organizationPageRoutes([{ ...note, role: 'supplemental' }, file], data),
  ).not.toContain('/library/paths/direct/');
});
