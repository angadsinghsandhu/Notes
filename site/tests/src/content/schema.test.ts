import { afterEach, describe, expect, it } from 'vitest';
import { copyFile, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { readMetadata, readPolicy } from '../../../src/content/schema.js';
import type {
  PublicationPolicy,
  SourceEntry,
} from '../../../src/content/types.js';

const dirs: string[] = [];
const policy: PublicationPolicy = {
  roots: ['Books', 'Classes', 'Courses', 'Interview', 'Languages', 'Tutorials'],
  exclude: [],
  overrides: {},
  repositoryPublic: false,
};
async function note(body: string): Promise<SourceEntry> {
  const dir = await mkdtemp(join(tmpdir(), 'notes-schema-'));
  dirs.push(dir);
  const absolutePath = join(dir, 'note.md');
  await writeFile(absolutePath, body);
  return {
    absolutePath,
    sourcePath: 'Books/note.md',
    section: 'books',
    kind: 'markdown',
    bytes: Buffer.byteLength(body),
  };
}
afterEach(async () => {
  await Promise.all(
    dirs.splice(0).map((dir) => rm(dir, { recursive: true, force: true })),
  );
});
describe('metadata schema', () => {
  it('requires title in frontmatter even when an override supplies one', async () => {
    const source = await note('---\ntags: [ml]\n---\n# Legacy title');
    await expect(
      readMetadata(source, {
        ...policy,
        overrides: { [source.sourcePath]: { title: 'Override' } },
      }),
    ).rejects.toThrow('Books/note.md');
  });
  it('uses real legacy H1, overrides descriptive fields, and lets frontmatter win', async () => {
    const source = await note('');
    await copyFile(
      new URL('../../fixtures/real/interview-1-basics.md', import.meta.url),
      source.absolutePath,
    );
    expect((await readMetadata(source, policy)).title).toBe(
      '1. Fundamentals & Learning Paradigms',
    );
    expect(
      (
        await readMetadata(source, {
          ...policy,
          overrides: { [source.sourcePath]: { title: 'Curated' } },
        })
      ).title,
    ).toBe('Curated');
    const authored = await note(
      '---\ntitle: Authored\ndescription: Description\ntags: [ml]\n---\n',
    );
    expect(
      await readMetadata(authored, {
        ...policy,
        overrides: {
          [authored.sourcePath]: { title: 'Override', description: 'Other' },
        },
      }),
    ).toMatchObject({
      title: 'Authored',
      description: 'Description',
      tags: ['ml'],
      draft: false,
      aliases: [],
    });
  });
  it('uses the first real H1 including setext and ignores fenced examples', async () => {
    const source = await note(
      '```md\n# Example\n```\n\nLegacy setext title\n===================\n\n# Later title',
    );
    expect((await readMetadata(source, policy)).title).toBe(
      'Legacy setext title',
    );
  });

  it.each(['japanese', 'french'])(
    'preserves real empty %s placeholder behavior',
    async (language) => {
      const source = await note('');
      await copyFile(
        new URL(
          `../../fixtures/real/${language}-unit-1-4-README.md`,
          import.meta.url,
        ),
        source.absolutePath,
      );
      source.sourcePath = `Languages/${language === 'japanese' ? 'Japanese' : 'French'}/unit 1-4/README.md`;
      expect((await readMetadata(source, policy)).title).toBe('unit 1-4');
    },
  );
  it('allows the explicitly synthetic Unicode H1', async () => {
    const source = await note('');
    await copyFile(
      new URL('../../fixtures/synthetic/unicode.md', import.meta.url),
      source.absolutePath,
    );
    expect((await readMetadata(source, policy)).title).toBe('日本語の例');
  });
  it.each([
    ['title: Present\ndraft: true', false],
    ['title: Present\ndraft: false', true],
  ])('draft true always wins', async (fields, overrideDraft) => {
    const source = await note(`---\n${fields}\n---\n`);
    expect(
      (
        await readMetadata(source, {
          ...policy,
          overrides: { [source.sourcePath]: { draft: overrideDraft } },
        })
      ).draft,
    ).toBe(true);
  });
  it.each([
    'title: ""',
    'title: 42',
    'title: OK\ndescription: 4',
    'title: OK\ntags: [a, a]',
    'title: OK\ntags: [1]',
    'title: OK\ndraft: yes',
    'title: OK\nupdated: 2026-02-30',
    'title: OK\nupdated: yesterday',
    'title: OK\nslug: ../secret',
    'title: OK\nslug: Upper',
    'title: OK\norder: .inf',
    'title: OK\naliases: [https://example.com]',
    'title: OK\naliases: [/notes/../secret/]',
  ])('rejects invalid fields with source diagnostics: %s', async (fields) => {
    const source = await note(`---\n${fields}\n---\n`);
    await expect(readMetadata(source, policy)).rejects.toThrow('Books/note.md');
  });
  it('rejects invalid overrides even if frontmatter replaces the field', async () => {
    const source = await note('---\ntitle: Authored\n---\n');
    await expect(
      readMetadata(source, {
        ...policy,
        overrides: { [source.sourcePath]: { order: Infinity } },
      }),
    ).rejects.toThrow('Books/note.md');
  });
  it('loads policy with safe defaults and validates roots, URL, and overrides', async () => {
    const source = await note('');
    const path = join(source.absolutePath, '..', 'publication.json');
    await writeFile(path, JSON.stringify({ roots: policy.roots }));
    expect(await readPolicy(path)).toEqual(policy);
    for (const invalid of [
      { roots: ['../Books'] },
      { roots: policy.roots, repositoryUrl: 'http://github.com/example' },
      { roots: policy.roots, overrides: { 'Books/a.md': { draft: 'false' } } },
      { roots: policy.roots, exclude: [42] },
      { roots: policy.roots, overrides: { '../secret.md': {} } },
    ]) {
      await writeFile(path, JSON.stringify(invalid));
      await expect(readPolicy(path)).rejects.toThrow(path);
    }
  });
});

it('preserves literal trailing hashes while removing Markdown closing hashes', async () => {
  for (const [body, title] of [
    ['# C#\n', 'C#'],
    ['# C# ###\n', 'C#'],
    ['# Topic###\n', 'Topic###'],
  ]) {
    expect((await readMetadata(await note(body!), policy)).title).toBe(title);
  }
});
it('accepts only the supplemental role and preserves the real upstream title', async () => {
  const source = await note('');
  await copyFile(
    new URL(
      '../../../../Courses/Scrimba/Learn React/src/projects/01-first-react/README.md',
      import.meta.url,
    ),
    source.absolutePath,
  );
  expect(
    await readMetadata(source, {
      ...policy,
      overrides: { [source.sourcePath]: { role: 'supplemental' } },
    }),
  ).toMatchObject({ title: 'React + Vite', role: 'supplemental' });
  await expect(
    readMetadata(await note('---\ntitle: Note\nrole: primary\n---\n'), policy),
  ).rejects.toThrow('role');
});

it.each(['---\ntitle: Missing close', '---\ntitle: One\ntitle: Two\n---\n'])(
  'rejects actual malformed YAML frontmatter %j',
  async (body) => {
    await expect(readMetadata(await note(body), policy)).rejects.toThrow(
      /frontmatter|unique/i,
    );
  },
);
