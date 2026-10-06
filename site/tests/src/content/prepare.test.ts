import { createHash } from 'node:crypto';
import {
  mkdtemp,
  mkdir,
  writeFile,
  readFile,
  rm,
  rename,
  readdir,
  symlink,
  copyFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';

const faults = vi.hoisted(() => ({
  afterRename: undefined as
    undefined | ((from: string, to: string) => Promise<void>),
  cleanup: false,
  verification: false,
}));
vi.mock('node:fs/promises', async (original) => {
  const fs = await original<typeof import('node:fs/promises')>();
  return {
    ...fs,
    lstat: async (path: string) => {
      if (faults.verification && path.includes('/.stage-'))
        throw new Error('injected verification cleanup failure');
      return fs.lstat(path);
    },
    rename: async (from: string, to: string) => {
      await fs.rename(from, to);
      await faults.afterRename?.(from, to);
    },
    rm: async (path: string, options: Parameters<typeof fs.rm>[1]) => {
      if (faults.cleanup && /\.(?:snapshot|assets)-backup-|\.stage-/.test(path))
        throw new Error('injected verified cleanup failure');
      return fs.rm(path, options);
    },
  };
});
import { prepareContent } from '../../../src/content/prepare.js';
import type { PublicationPolicy } from '../../../src/content/index.js';

const roots: string[] = [];
const policy: PublicationPolicy = {
  roots: ['Books', 'Classes', 'Courses', 'Interview', 'Languages', 'Tutorials'],
  exclude: ['**/hidden/**'],
  overrides: {},
  repositoryPublic: true,
  repositoryUrl: 'https://github.com/angadsinghsandhu/Notes',
  revision: 'a'.repeat(40),
};
async function archive() {
  const root = await mkdtemp(join(tmpdir(), 'notes-prepare-'));
  roots.push(root);
  await mkdir(join(root, 'site/content'), { recursive: true });
  const policyPath = join(root, 'site/content/publication.json');
  await writeFile(policyPath, JSON.stringify(policy));
  return {
    rootDir: root,
    outputDir: join(root, 'site/.generated'),
    policyPath,
    hosted: false,
  };
}
async function put(root: string, path: string, value: string | Buffer) {
  await mkdir(dirname(join(root, path)), { recursive: true });
  await writeFile(join(root, path), value);
}
afterEach(async () => {
  faults.afterRename = undefined;
  faults.cleanup = false;
  faults.verification = false;
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});

it('prepare_real_mixed_archive_subset with deterministic bodies, routes, metadata and full ledger', async () => {
  const options = await archive();
  const originals = [
    [
      'Courses/Programming with Mosh - Docker Tutorial for Beginners/5 Linux Basics/README.md',
      'tests/fixtures/real/task3/linux.md',
    ],
    [
      'Courses/Programming with Mosh - Docker Tutorial for Beginners/5 Linux Basics/imgs/Ubuntu-Reference.jpg',
      'tests/fixtures/real/task3/Ubuntu-Reference.jpg',
    ],
    [
      'Interview/leetcode/78_Subsets.py',
      'tests/fixtures/real/task4/78_Subsets.py',
    ],
    [
      'Books/PyTorch/example.ipynb',
      'tests/fixtures/real/task4/pytorch-excerpt.json',
    ],
  ];
  for (const [path, fixture] of originals)
    await put(options.rootDir, path!, await readFile(fixture!));
  const resources = [
    'Courses/Programming with Mosh - Docker Tutorial for Beginners/5 Linux Basics/imgs/Linux-Reference.jpg',
    'Classes/Johns Hopkins/Sem 1/NLP/Week 4/recitation/5-semantics-answers.pdf',
    'Classes/Johns Hopkins/Sem 1/NLP/Week 5/lect15-neural.pptx',
  ];
  // Real archive files copied unchanged; the actual slide filename is pinned below.
  for (const path of resources) {
    await mkdir(dirname(join(options.rootDir, path)), { recursive: true });
    await copyFile(join('..', path), join(options.rootDir, path));
  }
  await put(options.rootDir, 'Languages/Japanese/empty.md', '');
  await put(options.rootDir, 'Tutorials/data.bin', 'unpublished data');
  const first = await prepareContent(options);
  expect(first.diagnostics).toEqual([]);
  expect(first.manifest.entries.map((entry) => entry.kind)).toEqual(
    expect.arrayContaining(['markdown', 'notebook', 'code', 'pdf', 'slides']),
  );
  expect(first.manifest.ledger).toHaveLength(
    originals.length + resources.length + 2,
  );
  const note = first.manifest.entries.find(
    (entry) => entry.sourcePath === originals[0]![0],
  )!;
  expect(note.route).toBe(
    '/notes/courses/programming-with-mosh-docker-tutorial-for-beginners/5-linux-basics/',
  );
  expect(
    (
      JSON.parse(
        await readFile(
          join(options.outputDir, 'current/manifest.json'),
          'utf8',
        ),
      ) as { preparedBodies: Record<string, string> }
    ).preparedBodies[note.bodyFile!],
  ).toContain('content-assets/');
  const pdf = first.manifest.entries.find((entry) => entry.kind === 'pdf')!;
  expect(pdf.assetUrl).toMatch(/^\/content-assets\/[a-f0-9]{64}\.pdf$/);
  expect(pdf.sourceUrl).toContain(policy.revision);
  const bytes = await readFile(
    join(options.outputDir, 'current/manifest.json'),
  );
  await put(
    options.rootDir,
    'site/.generated/current/bodies/obsolete.html',
    'obsolete legacy body',
  );
  const second = await prepareContent(options);
  expect(second).toEqual(first);
  await expect(
    readFile(join(options.outputDir, 'current/bodies/obsolete.html')),
  ).rejects.toMatchObject({ code: 'ENOENT' });
  expect(
    await readFile(join(options.outputDir, 'current/manifest.json')),
  ).toEqual(bytes);
});
it('do_not_publish_draft_bodies_or_internal_ledger and fail links before author sanitization', async () => {
  const options = await archive();
  await put(
    options.rootDir,
    'Tutorials/draft.md',
    '---\ntitle: Hidden\ndraft: true\n---\n![secret](private.png)',
  );
  await put(
    options.rootDir,
    'Tutorials/private.png',
    'not referenced by published content',
  );
  await put(options.rootDir, 'Tutorials/public.md', '# Public');
  const first = await prepareContent(options);
  expect(first.diagnostics).toEqual([]);
  expect(first.manifest.entries.map((entry) => entry.sourcePath)).toEqual([
    'Tutorials/public.md',
  ]);
  expect(
    await readdir(join(options.rootDir, 'site/public/content-assets')),
  ).toEqual([]);
  expect(
    Object.keys(
      (
        JSON.parse(
          await readFile(
            join(options.outputDir, 'current/manifest.json'),
            'utf8',
          ),
        ) as { preparedBodies: Record<string, string> }
      ).preparedBodies,
    ),
  ).toHaveLength(1);
  await expect(
    readFile(join(options.rootDir, 'site/dist/manifest.json')),
  ).rejects.toMatchObject({ code: 'ENOENT' });
  const snapshot = await readFile(
    join(options.outputDir, 'current/manifest.json'),
  );
  await put(
    options.rootDir,
    'Tutorials/public.md',
    '# Public\n[hidden](draft.md)',
  );
  expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
    'draft.md',
  );
  expect(
    await readFile(join(options.outputDir, 'current/manifest.json')),
  ).toEqual(snapshot);
  await put(
    options.rootDir,
    'Tutorials/public.md',
    '# Public\n<a href="javascript:bad()">unsafe</a>',
  );
  expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
    'Unsafe URL',
  );
});
it('remove_deleted_pages_assets_and_aliases while preserving the explicit rename alias', async () => {
  const options = await archive();
  const image = await readFile('tests/fixtures/synthetic/task3/pixel.png');
  await put(options.rootDir, 'Tutorials/old.md', '# Old\n![pixel](pixel.png)');
  await put(options.rootDir, 'Tutorials/pixel.png', image);
  const first = await prepareContent(options);
  expect(first.diagnostics).toEqual([]);
  const old = first.manifest.entries[0]!;
  await rename(
    join(options.rootDir, 'Tutorials/old.md'),
    join(options.rootDir, 'Tutorials/new.md'),
  );
  await put(
    options.rootDir,
    'Tutorials/new.md',
    '---\ntitle: New\naliases: [/notes/tutorials/old/]\n---\n# New',
  );
  const second = await prepareContent(options);
  expect(second.diagnostics).toEqual([]);
  expect(second.manifest.entries[0]?.aliases).toEqual([
    '/notes/tutorials/old/',
  ]);
  await expect(
    readFile(join(options.outputDir, 'current', old.bodyFile!)),
  ).rejects.toMatchObject({ code: 'ENOENT' });
  expect(
    await readdir(join(options.rootDir, 'site/public/content-assets')),
  ).toEqual([]);
  expect(second.manifest.entries[0]?.route).toBe('/notes/tutorials/new/');
});
it('rejects cleanup outside exact owned directories and symlink snapshots without losing unrelated data', async () => {
  const options = await archive();
  await put(options.rootDir, 'Tutorials/a.md', '# A');
  await put(options.rootDir, 'outside/keep', 'preserve');
  expect(
    (
      await prepareContent({
        ...options,
        outputDir: join(options.rootDir, 'outside'),
      })
    ).diagnostics[0]?.message,
  ).toContain('site/.generated');
  expect(await readFile(join(options.rootDir, 'outside/keep'), 'utf8')).toBe(
    'preserve',
  );
  await mkdir(options.outputDir);
  await symlink(
    join(options.rootDir, 'outside'),
    join(options.outputDir, 'current'),
  );
  expect((await prepareContent(options)).diagnostics[0]?.message).toMatch(
    /symbolic|symlink/i,
  );
  expect(await readFile(join(options.rootDir, 'outside/keep'), 'utf8')).toBe(
    'preserve',
  );
});
it('collects notebook headings across cells before resolving cross-document fragments and stages extracted rasters', async () => {
  const options = await archive();
  const png = await readFile('tests/fixtures/synthetic/task3/pixel.png');
  await put(
    options.rootDir,
    'Tutorials/a.md',
    '# A\n[second](book.ipynb#actual-heading-1)',
  );
  await put(
    options.rootDir,
    'Tutorials/book.ipynb',
    JSON.stringify({
      nbformat: 4,
      nbformat_minor: 5,
      metadata: {},
      cells: [
        {
          cell_type: 'markdown',
          source: '$$\nx\n---\n$$\n\n# Actual heading',
          metadata: {},
        },
        {
          cell_type: 'markdown',
          source: '# Actual heading\n![plot](attachment:plot.png)',
          metadata: {},
          attachments: { 'plot.png': { 'image/png': png.toString('base64') } },
        },
      ],
    }),
  );
  const result = await prepareContent(options);
  expect(result.diagnostics).toEqual([]);
  const notebook = result.manifest.entries.find(
    (entry) => entry.kind === 'notebook',
  )!;
  expect(notebook.headings.map((heading) => heading.id)).toEqual([
    'actual-heading',
    'actual-heading-1',
  ]);
  expect(result.manifest.assets).toHaveLength(1);
  expect(
    await readFile(
      join(
        options.rootDir,
        'site/public',
        result.manifest.assets[0]!.url.slice(1),
      ),
    ),
  ).toEqual(png);
});
it('fails invalid hosted policy and malformed notebooks with source/cell diagnostics', async () => {
  const options = await archive();
  expect(
    (await prepareContent({ ...options, hosted: true })).diagnostics[0]
      ?.message,
  ).toContain('siteUrl');
  await put(
    options.rootDir,
    'Tutorials/bad.ipynb',
    JSON.stringify({
      nbformat: 4,
      nbformat_minor: 5,
      metadata: {},
      cells: [{ cell_type: 'unknown', source: '', metadata: {} }],
    }),
  );
  const result = await prepareContent(options);
  expect(result.diagnostics[0]).toMatchObject({
    sourcePath: 'Tutorials/bad.ipynb',
    cellIndex: 0,
  });
});

it('reproduces the real malformed empty notebook template and verifies its minimal archive repair', async () => {
  const options = await archive();
  const path =
    'Courses/Coursera/Deep Learning AI course/TensorFlow Deployment/Course 3 - TensorFlow Datasets/Week 1/Examples/tfds_horse-or-human.ipynb';
  const original = await readFile(
    'tests/fixtures/real/task5/empty-template.invalid.txt',
    'utf8',
  );
  await put(options.rootDir, path, original);
  expect((await prepareContent(options)).diagnostics[0]).toMatchObject({
    sourcePath: path,
  });
  const repaired = await readFile(join('..', path), 'utf8');
  expect(repaired).toBe(original.replace('  ],\n}', '  ]\n}'));
  await put(options.rootDir, path, repaired);
  expect((await prepareContent(options)).diagnostics).toEqual([]);
});

const sourceRepairs = JSON.parse(
  await readFile('tests/fixtures/real/task5/source-repairs.json', 'utf8'),
) as {
  sourcePath: string;
  fixture: string;
  replacements: [string, string][];
}[];
it.each(sourceRepairs)(
  'preserves all original source bytes except reviewed repairs: $sourcePath',
  async ({ sourcePath, fixture, replacements }) => {
    let expected = await readFile(
      join('tests/fixtures/real/task5', fixture),
      'utf8',
    );
    for (const [original, replacement] of replacements)
      expected = expected.replaceAll(original, replacement);
    expect(await readFile(join('..', sourcePath), 'utf8')).toBe(expected);
  },
);

it('extracts real inline notebook PNGs but rejects generic data URLs and draft source overrides', async () => {
  const options = await archive();
  const notebook = await readFile(
    'tests/fixtures/real/task5/inline-raster-excerpt.json',
  );
  await put(options.rootDir, 'Tutorials/inline.ipynb', notebook);
  expect((await prepareContent(options)).diagnostics).toEqual([]);
  const png = await readFile('tests/fixtures/synthetic/task3/pixel.png');
  await put(
    options.rootDir,
    'Tutorials/note.md',
    `![bad](data:image/png;base64,${png.toString('base64')})`,
  );
  expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
    'Unsafe URL',
  );
  await put(options.rootDir, 'Tutorials/note.md', '# Public');
  await put(
    options.rootDir,
    'Tutorials/draft.md',
    '---\ntitle: Draft\ndraft: true\n---\n# Secret',
  );
  await writeFile(
    options.policyPath,
    JSON.stringify({
      ...policy,
      overrides: {
        'Tutorials/note.md': {
          resourceUrl: `https://github.com/angadsinghsandhu/Notes/blob/${policy.revision}/Tutorials/draft.md`,
        },
      },
    }),
  );
  expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
    'unpublished repository target',
  );
});

const notebookRepairs = JSON.parse(
  await readFile('tests/fixtures/real/task5/notebook-repairs.json', 'utf8'),
) as {
  sourcePath: string;
  originalSha256: string;
  rawReplacements: { original: string; replacement: string }[];
}[];
it.each(notebookRepairs)(
  'preserves notebook bytes outside reviewed Markdown source tokens: $sourcePath',
  async ({ sourcePath, originalSha256, rawReplacements }) => {
    const actual = await readFile(join('..', sourcePath), 'utf8');
    let restored = actual;
    for (const { original, replacement } of rawReplacements) {
      expect(actual).toContain(replacement);
      restored = restored.replaceAll(replacement, original);
    }
    expect(createHash('sha256').update(restored).digest('hex')).toBe(
      originalSha256,
    );
  },
);

it.each(['removal', 'verification'])(
  'reports committed success after postcommit %s cleanup failure and recovers without accumulating backups',
  async (failure) => {
    const options = await archive();
    await put(options.rootDir, 'Tutorials/note.md', '# Old');
    expect((await prepareContent(options)).diagnostics).toEqual([]);
    await put(options.rootDir, 'Tutorials/note.md', '# New');
    if (failure === 'removal') faults.cleanup = true;
    else
      faults.afterRename = async (_from, to) => {
        if (to.endsWith('/current/manifest.json')) faults.verification = true;
      };
    const warning = vi.spyOn(console, 'warn').mockImplementation(() => {});
    try {
      const result = await prepareContent(options);
      expect(result.diagnostics).toEqual([]);
      const committed = JSON.parse(
        await readFile(
          join(options.outputDir, 'current/manifest.json'),
          'utf8',
        ),
      ) as { entries: { title: string }[] };
      expect(committed.entries[0]?.title).toBe('New');
      expect(warning.mock.calls.flat().join(' ')).toContain('cleanup');
      faults.afterRename = undefined;
      expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
        'cleanup failure',
      );
      expect(
        (await readdir(options.outputDir)).filter((name) =>
          name.startsWith('.stage-'),
        ),
      ).toHaveLength(1);
      faults.cleanup = false;
      faults.verification = false;
      expect((await prepareContent(options)).diagnostics).toEqual([]);
      expect(
        (await readdir(options.outputDir)).filter(
          (name) => name.startsWith('.stage-') || name.includes('-backup-'),
        ),
      ).toEqual([]);
    } finally {
      warning.mockRestore();
    }
  },
);
