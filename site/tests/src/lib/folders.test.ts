import { expect, it } from 'vitest';
import {
  assertUniqueRoutes,
  createEntry,
  readMetadata,
  readPolicy,
} from '../../../src/content/index.js';
import type { ContentEntry, SourceEntry } from '../../../src/content/index.js';
import { sectionLabels } from '../../../src/lib/catalog.js';
import {
  buildFolders,
  flattenFolders,
  folderRoute,
} from '../../../src/lib/folders.js';

let fixtureId = 0;
const entry = (
  groupSegments: string[],
  fields: Partial<ContentEntry> = {},
): ContentEntry => {
  const section = fields.section ?? 'books';
  const kind = fields.kind ?? 'markdown';
  const extension = {
    markdown: 'md',
    notebook: 'ipynb',
    code: 'py',
    pdf: 'pdf',
    slides: 'pptx',
  }[kind];
  const sourcePath = [
    sectionLabels[section],
    ...groupSegments,
    `fixture-${fixtureId++}.${extension}`,
  ].join('/');
  return {
    ...createEntry(
      {
        sourcePath,
        absolutePath: `/unused/${sourcePath}`,
        section,
        kind,
        bytes: 1,
      },
      {
        title: 'Fixture',
        description: '',
        tags: [],
        aliases: [],
        draft: false,
      },
    ),
    ...fields,
  };
};

async function authoredCodeEntry(
  sourcePath: string,
  aliases: string[] = [],
): Promise<ContentEntry> {
  const input: SourceEntry = {
    sourcePath,
    absolutePath: `/unused/${sourcePath}`,
    section: 'books',
    kind: 'code',
    bytes: 1,
  };
  const policy = await readPolicy('content/publication.json');
  policy.overrides[sourcePath] = { aliases };
  const metadata = await readMetadata(input, policy);
  expect(metadata.aliases).toEqual(aliases);
  return createEntry(input, metadata);
}

it('encodes each original segment reversibly without slug, separator or reserved-path collisions', () => {
  const segments = ['a b', 'a-b', 'a/b', 'a%2Fb', '~20', '.', '..', 'é?#'];
  const routes = segments.map((segment) => folderRoute('books', [segment]));
  expect(new Set(routes).size).toBe(segments.length);
  expect(folderRoute('books', [])).toBe('/library/books/');
  expect(folderRoute('books', ['a b', 'Chapter 1'])).toBe(
    '/library/books/folders/a~20b/Chapter~201/',
  );
  for (const route of routes)
    expect(new URL(route, 'https://example.test').pathname).toBe(route);
});

it('builds all section roots, ancestors, direct files and counts from published actual segments', () => {
  const note = entry(['Book', 'Chapter']);
  const resource = entry(['Book'], { kind: 'code' });
  const supplemental = entry([], { role: 'supplemental' });
  const roots = buildFolders([
    note,
    resource,
    supplemental,
    entry(['Hidden'], { draft: true }),
    entry(['Other'], { section: 'languages' }),
  ]);
  expect(roots).toHaveLength(6);
  expect(flattenFolders(roots)).toHaveLength(9);
  const books = roots.find((folder) => folder.section === 'books')!;
  expect(books.entries).toEqual([supplemental]);
  expect([books.noteCount, books.resourceCount]).toEqual([1, 2]);
  expect(books.children.map((child) => child.label)).toEqual(['Book']);
  expect(books.children[0]!.entries).toEqual([resource]);
  expect(books.children[0]!.children[0]!.entries).toEqual([note]);
  expect(
    roots.find((folder) => folder.section === 'languages')!.children[0]!.label,
  ).toBe('Other');
});

it('keeps similar names and sibling branches distinct and sorts folders consistently', () => {
  const books = buildFolders([
    entry(['z']),
    entry(['a-b', 'same']),
    entry(['a b', 'same']),
    entry(['a-b', 'same'], { kind: 'pdf' }),
  ])[0]!;
  expect(books.children.map((folder) => folder.label)).toEqual([
    'a b',
    'a-b',
    'z',
  ]);
  expect(books.children[0]!.children[0]!.route).not.toBe(
    books.children[1]!.children[0]!.route,
  );
  expect(books.children[1]!.children[0]!.entries).toHaveLength(2);
});

it('rejects case-only folders from supported different source files with both folder owners', async () => {
  const entries = await Promise.all([
    authoredCodeEntry('Books/Foo/one.py'),
    authoredCodeEntry('Books/foo/two.py'),
  ]);
  expect(entries.map((item) => item.route)).toEqual([
    '/resources/books/foo/one-py/',
    '/resources/books/foo/two-py/',
  ]);
  expect(() => assertUniqueRoutes(entries)).not.toThrow();
  const check = () => buildFolders(entries);
  expect(check).toThrow('folder Books/Foo');
  expect(check).toThrow('folder Books/foo');
});

it.each([
  '/library/tree/',
  '/library/books/folders/Foo/',
  '/LIBRARY/BOOKS/FOLDERS/FOO/',
  '/library/books/folders/Foo/index.html',
])(
  'rejects supported alias %s before returning navigation pages',
  async (alias) => {
    const actual = await authoredCodeEntry('Books/Foo/one.py', [alias]);
    const check = () => buildFolders([actual]);
    expect(check).toThrow('Books/Foo/one.py');
    expect(check).toThrow(
      alias === '/library/tree/'
        ? 'reserved website route /library/tree/'
        : 'folder Books/Foo',
    );
  },
);

it('retains non-conflicting aliases and excludes draft route owners', async () => {
  const actual = await authoredCodeEntry('Books/Foo/one.py', [
    '/legacy-book-one/',
  ]);
  const draft = {
    ...(await authoredCodeEntry('Books/foo/two.py', ['/library/tree/'])),
    draft: true,
  };
  const roots = buildFolders([actual, draft]);
  expect(roots[0]!.children.map((folder) => folder.label)).toEqual(['Foo']);
  expect(roots[0]!.children[0]!.entries[0]!.aliases).toEqual([
    '/legacy-book-one/',
  ]);
});
