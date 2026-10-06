import { readFile } from 'node:fs/promises';
import { describe, expect, it } from 'vitest';
import {
  collectHeadings,
  collectExplicitAnchors,
  collectMarkdownLinks,
} from '../../../src/content/headings.js';
import { createEntry } from '../../../src/content/identifiers.js';
import {
  createRouteCatalog,
  resolveLink,
  publicSourceUrl,
} from '../../../src/content/links.js';
import type {
  ContentEntry,
  PublicationPolicy,
} from '../../../src/content/types.js';

const policy: PublicationPolicy = {
  roots: ['Books', 'Classes', 'Courses', 'Interview', 'Languages', 'Tutorials'],
  exclude: ['**/hidden/**'],
  overrides: {},
  repositoryPublic: true,
  repositoryUrl: 'https://github.com/owner/repo',
  revision: 'a'.repeat(40),
};
function entry(sourcePath: string, title = 'Title'): ContentEntry {
  return createEntry(
    {
      sourcePath,
      absolutePath: `/archive/${sourcePath}`,
      section: 'tutorials',
      kind: 'markdown',
      bytes: 0,
    },
    { title, description: '', tags: [], aliases: [], draft: false },
  );
}
const referring = 'Tutorials/Group/README.md';

describe('published link resolution', () => {
  it('rewrite_real_relative_links_and_fragments', async () => {
    const sourcePath =
      'Courses/Programming with Mosh - Docker Tutorial for Beginners/5 Linux Basics/README.md';
    const body = await readFile('tests/fixtures/real/task3/linux.md', 'utf8');
    const note = { ...entry(sourcePath), headings: collectHeadings(body) };
    const picture = `${sourcePath.slice(0, -9)}imgs/Ubuntu-Reference.jpg`;
    const target = {
      ...entry('Tutorials/Group/A B.md'),
      headings: collectHeadings('# Repeat\n# Repeat'),
    };
    const directory = entry('Tutorials/Other/ReadMe.MD');
    const catalog = createRouteCatalog(
      [note, target, directory],
      [
        {
          sourcePath: picture,
          bytes: 1,
          mode: 'local',
          url: '/content-assets/hash.jpg',
        },
      ],
      policy,
    );
    const image = collectMarkdownLinks(body).find((link) => link.image);
    expect(image).toBeDefined();
    expect(resolveLink(image!.href, sourcePath, catalog)).toBe(
      '/content-assets/hash.jpg',
    );
    expect(
      resolveLink('/content-assets/hash.jpg?size=1#view', sourcePath, catalog),
    ).toBe('/content-assets/hash.jpg?size=1#view');
    expect(resolveLink('A%20B.md?view=one#repeat-1', referring, catalog)).toBe(
      `${target.route}?view=one#repeat-1`,
    );
    expect(resolveLink('../Other/', referring, catalog)).toBe(directory.route);
    expect(resolveLink(`${target.route}#repeat`, referring, catalog)).toBe(
      `${target.route}#repeat`,
    );
    expect(() => resolveLink('missing.md', referring, catalog)).toThrow(
      /Tutorials\/Group\/README.md.*missing.md/,
    );
    expect(() => resolveLink('A B.md#absent', referring, catalog)).toThrow(
      /README.md.*A B.md.*absent/,
    );
  });
  it('validates real explicit author anchor fragments', async () => {
    const body = await readFile(
      'tests/fixtures/real/task3/course-update-guide-udemy.md',
      'utf8',
    );
    const note = {
      ...entry(referring),
      headings: collectHeadings(body),
      anchors: collectExplicitAnchors(body),
    };
    const catalog = createRouteCatalog([note], []);
    for (const { href } of collectMarkdownLinks(body).filter((link) =>
      link.href.startsWith('#'),
    )) {
      expect(resolveLink(href, referring, catalog)).toBe(
        `${note.route}${href}`,
      );
    }
  });
  it('resolve_wikilink_only_when_unique', () => {
    const a = entry('Tutorials/Group/a.md', 'Unique');
    const b = entry('Tutorials/Other/b.md', 'Other');
    const catalog = createRouteCatalog([a, b], []);
    expect(resolveLink('[[Unique|Label]]', referring, catalog)).toBe(a.route);
    expect(resolveLink('[[Tutorials/Other/b.md]]', referring, catalog)).toBe(
      b.route,
    );
    const duplicate = createRouteCatalog([a, { ...b, title: 'Unique' }], []);
    expect(() => resolveLink('[[Unique]]', referring, duplicate)).toThrow(
      /a.md.*b.md/,
    );
    expect(() => resolveLink('[[Missing]]', referring, catalog)).toThrow(
      'Missing',
    );
  });
  it.each([
    'https://example.org/path?q=1#frag',
    'http://example.org',
    'mailto:hello@example.org',
  ])('preserves external %s', (href) => {
    expect(resolveLink(href, referring, createRouteCatalog([], []))).toBe(href);
  });
  it.each([
    'javascript:alert(1)',
    'data:image/png;base64,AAAA',
    '\u0000javascript:alert(1)',
    '//example.org',
    '../../../secret.md',
    'file:///etc/passwd',
    'ftp://example.org',
  ])('rejects unsafe or escaping %s', (href) => {
    expect(() =>
      resolveLink(href, referring, createRouteCatalog([], [], policy)),
    ).toThrow(referring);
  });
  it('known repository URLs cannot bypass draft/excluded targets', () => {
    const published = entry('Tutorials/Group/A B.md');
    const draft = { ...entry('Tutorials/draft.md'), draft: true };
    const hidden = entry('Tutorials/hidden/private.md');
    const catalog = createRouteCatalog([published, draft, hidden], [], policy);
    expect(
      resolveLink(
        'https://github.com/owner/repo/blob/main/Tutorials/Group/A%20B.md?q=1',
        referring,
        catalog,
      ),
    ).toBe(`${published.route}?q=1`);
    expect(
      resolveLink(
        'https://github.com/another/repo/blob/main/Tutorials/draft.md',
        referring,
        catalog,
      ),
    ).toContain('another/repo');
    for (const path of [
      'Tutorials/draft.md',
      'Tutorials/hidden/private.md',
      'Tutorials/link.md',
    ]) {
      expect(() =>
        resolveLink(
          `https://github.com/owner/repo/blob/master/${path}`,
          referring,
          catalog,
        ),
      ).toThrow(path);
      expect(() =>
        resolveLink(
          `https://raw.githubusercontent.com/owner/repo/master/${path}`,
          referring,
          catalog,
        ),
      ).toThrow(path);
    }
  });
  it('does not invent a directory target when there is no README', () => {
    expect(() =>
      resolveLink(
        '../Other',
        referring,
        createRouteCatalog([entry('Tutorials/Other/code.py')], []),
      ),
    ).toThrow('Other');
  });
  it('rejects duplicate aliases and source ownership', () => {
    const a = entry('Tutorials/a.md');
    expect(() => createRouteCatalog([a, a], [])).toThrow();
  });
});

describe('public external resource actions', () => {
  it('require_accessible_source_url_for_external_resource', () => {
    expect(publicSourceUrl('Tutorials/A B/日本語.pdf', policy)).toBe(
      `https://github.com/owner/repo/blob/${'a'.repeat(40)}/Tutorials/A%20B/%E6%97%A5%E6%9C%AC%E8%AA%9E.pdf`,
    );
    for (const config of [
      { ...policy, repositoryPublic: false },
      { ...policy, repositoryUrl: undefined },
      { ...policy, revision: 'main' },
    ]) {
      expect(() =>
        publicSourceUrl('Tutorials/a.pdf', config as PublicationPolicy),
      ).toThrow('Tutorials/a.pdf');
    }
    expect(
      publicSourceUrl('Tutorials/a.pdf', {
        ...policy,
        repositoryPublic: false,
        overrides: {
          'Tutorials/a.pdf': { resourceUrl: 'https://cdn.example.org/a.pdf' },
        },
      }),
    ).toBe('https://cdn.example.org/a.pdf');
    expect(() =>
      publicSourceUrl('Tutorials/a.pdf', {
        ...policy,
        overrides: {
          'Tutorials/a.pdf': { resourceUrl: 'javascript:alert(1)' },
        },
      }),
    ).toThrow();
  });
});

describe('publication identity and encoded source safety', () => {
  it('decodes repository filenames exactly once and checks encoded repository identity', () => {
    const percent = entry('Tutorials/literal%20name.md');
    const catalog = createRouteCatalog([percent], [], policy);
    expect(
      resolveLink(
        'https://github.com/owner/repo/blob/main/Tutorials/literal%2520name.md',
        referring,
        catalog,
      ),
    ).toBe(percent.route);
    expect(() =>
      resolveLink(
        'https://github.com/%6fwner/repo/blob/main/Tutorials/hidden/private.md',
        referring,
        catalog,
      ),
    ).toThrow('hidden/private.md');
  });
  it('excludes descendant content when the policy matches a directory', () => {
    const hidden = entry('Tutorials/hidden/a.md');
    const catalog = createRouteCatalog([hidden], [], {
      ...policy,
      exclude: ['Tutorials/hidden'],
    });
    expect(() =>
      resolveLink('/Tutorials/hidden/a.md', referring, catalog),
    ).toThrow('hidden/a.md');
    expect(() =>
      publicSourceUrl('Tutorials/hidden/a.pdf', {
        ...policy,
        exclude: ['Tutorials/hidden'],
      }),
    ).toThrow('hidden/a.pdf');
  });
  it('rejects direct public source actions outside allowed content roots and credential directories', () => {
    for (const path of [
      '.git/config',
      'Tutorials/.env',
      'Tutorials/node_modules/private.pdf',
    ]) {
      expect(() => publicSourceUrl(path, policy)).toThrow(path);
    }
  });
});

it('rewrites the exact historical repository link between two real PyTorch chapter notes', async () => {
  const first =
    'Books/Programming PyTorch for Deep Learning - Ian Pointer/Chapter 1 - Getting Started with Pytorch/ReadMe.md';
  const second =
    'Books/Programming PyTorch for Deep Learning - Ian Pointer/Chapter 2 - Image Clasification with Pytorch/ReadMe.md';
  const body = await readFile(
    'tests/fixtures/real/task3/pytorch-chapter-1.md',
    'utf8',
  );
  const targetBody = await readFile(
    'tests/fixtures/real/task3/pytorch-chapter-2.md',
    'utf8',
  );
  const target = { ...entry(second), headings: collectHeadings(targetBody) };
  const catalog = createRouteCatalog(
    [{ ...entry(first), headings: collectHeadings(body) }, target],
    [],
    { ...policy, repositoryUrl: 'https://github.com/angadsinghsandhu/Notes' },
  );
  const link = collectMarkdownLinks(body).find(
    ({ href }) =>
      href.includes('Notes/tree/master/Books/') && href.includes('Chapter%202'),
  );
  expect(link).toBeDefined();
  expect(resolveLink(link!.href, first, catalog)).toBe(target.route);
});

it('rejects resource overrides to excluded or draft known repository targets', () => {
  const resource = entry('Tutorials/Group/a.pdf');
  const draft = { ...entry('Tutorials/draft.pdf'), draft: true };
  const catalog = createRouteCatalog([resource, draft], [], policy);
  const override = (target: string): PublicationPolicy => ({
    ...policy,
    overrides: {
      [resource.sourcePath]: {
        resourceUrl: `https://github.com/owner/repo/blob/main/${target}`,
      },
    },
  });
  expect(() =>
    publicSourceUrl(resource.sourcePath, override('Tutorials/hidden/a.pdf')),
  ).toThrow('hidden/a.pdf');
  expect(() =>
    publicSourceUrl(resource.sourcePath, override(draft.sourcePath), catalog),
  ).toThrow('draft.pdf');
  expect(() =>
    createRouteCatalog(
      [resource, draft],
      [
        {
          sourcePath: resource.sourcePath,
          bytes: 1,
          mode: 'external',
          url: `https://github.com/owner/repo/blob/main/${draft.sourcePath}`,
        },
      ],
      policy,
    ),
  ).toThrow('draft.pdf');
});

it('preserves a valid self-referencing external asset URL without recursion', () => {
  const sourcePath = 'Tutorials/Group/a.pdf';
  const url = `https://github.com/owner/repo/blob/${'a'.repeat(40)}/${sourcePath}`;
  const catalog = createRouteCatalog(
    [],
    [{ sourcePath, url, bytes: 26_214_401, mode: 'external' }],
    policy,
  );
  expect(resolveLink('a.pdf', referring, catalog)).toBe(url);
  expect(
    publicSourceUrl(
      sourcePath,
      { ...policy, overrides: { [sourcePath]: { resourceUrl: url } } },
      catalog,
    ),
  ).toBe(url);
});

describe('external asset suffix composition', () => {
  function catalog(url: string) {
    return createRouteCatalog(
      [],
      [
        {
          sourcePath: 'Tutorials/Group/a.pdf',
          mode: 'external',
          bytes: 1,
          url,
        },
      ],
      policy,
    );
  }
  it.each([
    [
      'https://cdn.example.org/a.pdf?token=abc',
      'a.pdf?download=1',
      'https://cdn.example.org/a.pdf?token=abc&download=1',
    ],
    [
      'https://cdn.example.org/a.pdf#default',
      'a.pdf#page=2',
      'https://cdn.example.org/a.pdf#page=2',
    ],
    [
      'https://cdn.example.org/a.pdf?token=abc#default',
      'a.pdf?download=1#page=2',
      'https://cdn.example.org/a.pdf?token=abc&download=1#page=2',
    ],
    [
      'https://cdn.example.org/a.pdf?token=abc#default',
      'a.pdf?download=1',
      'https://cdn.example.org/a.pdf?token=abc&download=1#default',
    ],
    [
      'https://cdn.example.org/a.pdf?token=abc#default',
      'a.pdf#page=2',
      'https://cdn.example.org/a.pdf?token=abc#page=2',
    ],
    [
      'https://cdn.example.org/a.pdf?token=abc#default',
      'a.pdf#',
      'https://cdn.example.org/a.pdf?token=abc',
    ],
  ])(
    'composes configured %s with incoming %s',
    (configured, href, expected) => {
      expect(resolveLink(href, referring, catalog(configured))).toBe(expected);
    },
  );
  it('replaces collided query keys while retaining other keys and incoming repeated values', () => {
    const result = new URL(
      resolveLink(
        'a.pdf?mode=one&mode=two&extra=a&extra=b',
        referring,
        catalog(
          'https://cdn.example.org/a.pdf?token=abc&mode=old&mode=older&keep=1&keep=2#default',
        ),
      ),
    );
    expect([...result.searchParams]).toEqual([
      ['token', 'abc'],
      ['keep', '1'],
      ['keep', '2'],
      ['mode', 'one'],
      ['mode', 'two'],
      ['extra', 'a'],
      ['extra', 'b'],
    ]);
    expect(result.hash).toBe('#default');
  });
  it('preserves the exact configured URL when no incoming suffix exists', () => {
    const configured =
      'https://CDN.example.org/%7efile.pdf?token=a%20b&mode=1&mode=2#default';
    expect(resolveLink('a.pdf', referring, catalog(configured))).toBe(
      configured,
    );
  });
});
