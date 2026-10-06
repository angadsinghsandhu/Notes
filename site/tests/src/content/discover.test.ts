import { afterEach, describe, expect, it } from 'vitest';
import {
  copyFile,
  mkdir,
  mkdtemp,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import {
  discoverEntries,
  publicationExclusion,
} from '../../../src/content/discover.js';
import type { PublicationPolicy } from '../../../src/content/types.js';
const dirs: string[] = [];
const policy: PublicationPolicy = {
  roots: ['Books', 'Classes', 'Courses', 'Interview', 'Languages', 'Tutorials'],
  exclude: [],
  overrides: {},
  repositoryPublic: false,
};
async function root(): Promise<string> {
  const dir = await mkdtemp(join(tmpdir(), 'notes-discover-'));
  dirs.push(dir);
  return dir;
}
async function file(
  dir: string,
  path: string,
  body = '# Title',
): Promise<void> {
  const target = join(dir, path);
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, body);
}
afterEach(async () => {
  await Promise.all(
    dirs.splice(0).map((dir) => rm(dir, { recursive: true, force: true })),
  );
});
describe('automatic content discovery', () => {
  it('discover_new_markdown_without_registration', async () => {
    const dir = await root();
    await file(dir, 'Interview/Applied Science/breadth/1-basics.md');
    await copyFile(
      new URL('../../fixtures/real/interview-1-basics.md', import.meta.url),
      join(dir, 'Interview/Applied Science/breadth/1-basics.md'),
    );
    await file(dir, 'Interview/Applied Science/breadth/2-new.md');
    const first = await discoverEntries(dir, policy);
    expect(first.sources.map((source) => source.sourcePath)).toEqual([
      'Interview/Applied Science/breadth/1-basics.md',
      'Interview/Applied Science/breadth/2-new.md',
    ]);
    expect(await discoverEntries(dir, policy)).toEqual(first);
  });
  it('reject_symlink_escape_and_excluded_targets', async () => {
    const dir = await root();
    const outside = await root();
    await file(outside, 'secret.md');
    const excluded = [
      'Books/.kiro/hidden.md',
      'Books/env.json',
      'Books/.ipynb_checkpoints/note.md',
      'Books/node_modules/vendor.md',
      'Books/__pycache__/cached.py',
      'Books/.cache/note.md',
      'Books/dist/compiled.js',
    ];
    for (const path of excluded) await file(dir, path);
    await file(dir, 'Books/allowed.md');
    await symlink(join(outside, 'secret.md'), join(dir, 'Books/escape.md'));
    await symlink(join(dir, 'Books/.kiro'), join(dir, 'Books/indirect'));
    await symlink(join(dir, 'Books/allowed.md'), join(dir, 'Books/alias.md'));
    const result = await discoverEntries(dir, policy);
    expect(result.sources.map((source) => source.sourcePath)).toEqual([
      'Books/allowed.md',
    ]);
    for (const path of [
      ...excluded,
      'Books/escape.md',
      'Books/indirect',
      'Books/alias.md',
    ])
      expect(result.ledger).toContainEqual(
        expect.objectContaining({ sourcePath: path, disposition: 'excluded' }),
      );
  });
  it('accounts for draft, unsupported, supporting assets, and out-of-root files', async () => {
    const dir = await root();
    const paths = [
      'Books/note.md',
      'Books/draft.md',
      'Books/plot.png',
      'Books/data.csv',
      'Books/config.json',
      'Books/file.pdf',
      'Books/deck.pptx',
      'Books/code.py',
      'Books/lab.ipynb',
    ];
    for (const path of paths)
      await file(
        dir,
        path,
        path.endsWith('draft.md')
          ? '---\ntitle: Draft\ndraft: true\n---\n'
          : '# Title',
      );
    const result = await discoverEntries(dir, {
      ...policy,
      overrides: { 'Books/draft.md': { draft: false } },
    });
    expect(result.ledger.map((row) => row.sourcePath).sort()).toEqual(
      paths.sort(),
    );
    expect(result.sources.map((source) => source.kind).sort()).toEqual([
      'code',
      'markdown',
      'notebook',
      'pdf',
      'slides',
    ]);
    expect(result.ledger).toContainEqual(
      expect.objectContaining({
        sourcePath: 'Books/draft.md',
        disposition: 'excluded',
        reason: expect.stringContaining('draft'),
      }),
    );
    expect(result.ledger).toContainEqual(
      expect.objectContaining({
        sourcePath: 'Books/plot.png',
        disposition: 'supporting-asset',
      }),
    );
    expect(result.ledger).toContainEqual(
      expect.objectContaining({
        sourcePath: 'Books/data.csv',
        disposition: 'unsupported',
      }),
    );
    await file(dir, 'README.md');
    expect((await discoverEntries(dir, policy)).ledger).toHaveLength(
      paths.length,
    );
  });
  it('policy exclusions always win, including explicit metadata and resource URLs', async () => {
    const dir = await root();
    await file(dir, 'Books/private/note.md');
    await file(dir, 'Books/keep.md');
    const result = await discoverEntries(dir, {
      ...policy,
      exclude: ['Books/private/**'],
      overrides: {
        'Books/private/note.md': {
          title: 'Publish',
          draft: false,
          resourceUrl: 'https://example.com/note',
        },
      },
    });
    expect(result.sources.map((source) => source.sourcePath)).toEqual([
      'Books/keep.md',
    ]);
  });
  it('keeps course content in a nested site directory and rejects linked roots', async () => {
    const dir = await root();
    const outside = await root();
    await file(dir, 'Courses/project/site/example.html');
    await file(outside, 'note.md');
    await symlink(outside, join(dir, 'Books'));
    const result = await discoverEntries(dir, policy);
    expect(result.sources.map((source) => source.sourcePath)).toEqual([
      'Courses/project/site/example.html',
    ]);
    expect(result.ledger).toContainEqual(
      expect.objectContaining({ sourcePath: 'Books', disposition: 'excluded' }),
    );
  });

  it('sorts traversal numerically and classifies every supported code extension', async () => {
    const dir = await root();
    const extensions = [
      'py',
      'js',
      'jsx',
      'ts',
      'tsx',
      'css',
      'html',
      'java',
      'kt',
      'cpp',
    ];
    for (const ext of extensions) await file(dir, `Courses/code.${ext}`);
    for (const number of [10, 2, 1]) await file(dir, `Books/${number}.MD`);
    const result = await discoverEntries(dir, policy);
    expect(
      result.sources.slice(0, 3).map((source) => source.sourcePath),
    ).toEqual(['Books/1.MD', 'Books/2.MD', 'Books/10.MD']);
    expect(
      result.sources.filter((source) => source.kind === 'code'),
    ).toHaveLength(extensions.length);
  });
});

it('shares ancestor policy exclusions for direct source actions', () => {
  const policy: PublicationPolicy = {
    roots: [
      'Books',
      'Classes',
      'Courses',
      'Interview',
      'Languages',
      'Tutorials',
    ],
    exclude: ['Tutorials/hidden'],
    overrides: {},
    repositoryPublic: false,
  };
  expect(publicationExclusion('Tutorials/hidden/image.png', policy)).toContain(
    'Tutorials/hidden',
  );
  expect(
    publicationExclusion('Tutorials/visible/image.png', policy),
  ).toBeUndefined();
  expect(publicationExclusion('Tutorials/.env', policy)).toContain(
    'credential',
  );
});

it('applies built-in credential exclusions to ancestor directories', () => {
  expect(publicationExclusion('Tutorials/secrets/image.png', policy)).toContain(
    'credential',
  );
});
