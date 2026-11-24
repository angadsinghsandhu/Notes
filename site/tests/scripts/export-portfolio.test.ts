import { createHash } from 'node:crypto';
import {
  cp,
  mkdir,
  mkdtemp,
  readFile,
  readdir,
  realpath,
  rename,
  rm,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import {
  hashLessonForReview,
  type CurriculumSnapshot,
  type LessonRecord,
  type ProblemRecord,
} from '../../src/content/index.js';

const faults = vi.hoisted(() => ({
  open: undefined as undefined | ((filename: string) => Promise<void>),
}));
vi.mock('node:fs/promises', async (original) => {
  const fs = await original<typeof import('node:fs/promises')>();
  return {
    ...fs,
    open: async (...args: Parameters<typeof fs.open>) => {
      if (typeof args[0] === 'string') await faults.open?.(args[0]);
      return fs.open(...args);
    },
  };
});

const roots: string[] = [];
const revision = 'a'.repeat(40);
afterEach(async () => {
  faults.open = undefined;
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});

async function put(root: string, path: string, bytes: string | Buffer) {
  const file = join(root, path);
  await mkdir(dirname(file), { recursive: true });
  await writeFile(file, bytes);
}

async function fixture() {
  for (const name of ['SITE_URL', 'SOURCE_REVISION', 'REPOSITORY_URL'])
    vi.stubEnv(name, undefined);
  const directory = await mkdtemp(
    join(await realpath(tmpdir()), 'notes-portfolio-'),
  );
  roots.push(directory);
  const rootDir = join(directory, 'archive');
  const out = join(directory, 'export');
  await put(
    rootDir,
    'site/content/publication.json',
    JSON.stringify({
      roots: [
        'Books',
        'Classes',
        'Courses',
        'Interview',
        'Languages',
        'Tutorials',
      ],
      exclude: [],
      overrides: {},
      repositoryPublic: true,
      repositoryUrl: 'https://github.com/example/notes',
      siteUrl: 'https://notes.example.test',
    }),
  );
  await put(
    rootDir,
    'Books/Original.md',
    '---\ntitle: Original\n---\n# Approved\n\n![Dot](dot.png)\n\n<script>not-public()</script>\n',
  );
  await put(
    rootDir,
    'Books/Draft.md',
    '---\ntitle: Draft\ndraft: true\n---\nTwo Sum draft body\n',
  );
  await put(
    rootDir,
    'Books/dot.png',
    Buffer.from(
      'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aTRsAAAAASUVORK5CYII=',
      'base64',
    ),
  );
  return { directory, rootDir, out, revision, mode: 'preview' as const };
}

it('exports only reviewed publication entries', async () => {
  const options = await fixture();
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  const manifest = await exportPortfolio(options);
  expect(manifest.mode).toBe('preview');
  expect(manifest.sourceSha).toBe(revision);
  expect(manifest.entries.map(({ title }) => title)).toEqual(['Original']);
  expect(manifest.verifiedCurriculumIds).toEqual([]);
  expect(manifest.curriculum.lessons).toEqual([]);
  expect(manifest.curriculum.traceAssets).toEqual([]);
  const generated = JSON.parse(
    await readFile(
      join(options.rootDir, 'site/.generated/current/manifest.json'),
      'utf8',
    ),
  ) as { preparedBodies: Record<string, string> };
  expect(manifest.entries[0]?.bodyHtml).toBe(
    Object.values(generated.preparedBodies)[0],
  );
  expect(JSON.stringify(manifest)).not.toMatch(
    /Two Sum draft body|not-public\(\)/,
  );
  expect(manifest.assets).toHaveLength(1);
  for (const asset of manifest.assets) {
    const bytes = await readFile(join(options.out, asset.exportPath));
    expect(asset.bytes).toBe(bytes.length);
    expect(asset.sha256).toBe(createHash('sha256').update(bytes).digest('hex'));
    expect(asset.publicPath).toBe(`/content-assets/${asset.sha256}.png`);
  }
});

it('rejects a mismatched checkout revision', async () => {
  const options = await fixture();
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  await expect(
    exportPortfolio({
      ...options,
      rootDir: resolve('..'),
      mode: 'production',
    }),
  ).rejects.toThrow(/revision.*checkout/i);
  expect(await readdir(options.directory)).toEqual(['archive']);
});

it('leaves no partial export after failure', async () => {
  const options = await fixture();
  await put(options.rootDir, 'Books/Original.md', '[Broken](missing.pdf)');
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  await expect(exportPortfolio(options)).rejects.toThrow('missing.pdf');
  expect(await readdir(options.directory)).toEqual(['archive']);

  await put(options.directory, 'export/manifest.json', 'verified');
  await expect(exportPortfolio(options)).rejects.toThrow(/already exists/i);
  expect(await readFile(join(options.out, 'manifest.json'), 'utf8')).toBe(
    'verified',
  );
  expect((await readdir(options.directory)).sort()).toEqual([
    'archive',
    'export',
  ]);
});

const stableId = `doc-${'7'.repeat(64)}`;
async function organization(root: string, sourcePath: string) {
  const records = {
    taxonomy: { version: 1, topics: [] },
    collections: { version: 1, collections: [], groups: [] },
    entries: {
      version: 1,
      entries: [
        {
          uid: stableId,
          sourcePath,
          topics: [],
          purpose: 'note',
          status: 'reviewed',
        },
      ],
    },
    paths: { version: 1, paths: [] },
  };
  for (const [name, contents] of Object.entries(records))
    await put(
      root,
      `site/content/organization/${name}.json`,
      JSON.stringify(contents),
    );
}

it('keeps the stable organization ID and alias target after a rename', async () => {
  const options = await fixture();
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  await organization(options.rootDir, 'Books/Original.md');
  const before = await exportPortfolio(options);
  await rename(
    join(options.rootDir, 'Books/Original.md'),
    join(options.rootDir, 'Books/Renamed.md'),
  );
  await put(
    options.rootDir,
    'Books/Renamed.md',
    '---\ntitle: Renamed\naliases: [/notes/books/original/]\n---\n# Renamed\n',
  );
  await organization(options.rootDir, 'Books/Renamed.md');
  const current = await exportPortfolio({
    ...options,
    out: join(options.directory, 'renamed'),
  });
  const byAlias = current.entries.find(({ aliases }) =>
    aliases.includes(before.entries[0]!.route),
  );
  expect(byAlias).toMatchObject({
    id: stableId,
    route: '/notes/books/renamed/',
    title: 'Renamed',
  });
  expect(before.entries[0]?.id).toBe(stableId);
  expect(current.organization.memberships[0]).toMatchObject({
    uid: stableId,
    entryId: stableId,
  });
});

const solver = 'Interview/leetcode/Solutions/1_two_sum.py';
async function realCurriculum(root: string) {
  const input = resolve('content/leetcode');
  const target = join(root, 'site/content/leetcode');
  await cp(join(input, 'manifest.json'), join(target, 'manifest.json'));
  await cp(join(input, 'manifest'), join(target, 'manifest'), {
    recursive: true,
  });
  await cp(join(input, 'paths'), join(target, 'paths'), { recursive: true });
  await cp(join(input, 'problems'), join(target, 'problems'), {
    recursive: true,
  });
  const bytes = 'def archived_solver():\n    return [0, 1]\n';
  await put(root, solver, bytes);
  await organization(root, solver);
  await put(
    target,
    'source-map.json',
    JSON.stringify({
      version: 1,
      records: [
        {
          sourcePath: solver,
          sha256: createHash('sha256').update(bytes).digest('hex'),
          filenameNumber: 1,
          disposition: 'solver_variant',
          reason: 'An enrolled archive source variant for the isolated export.',
          problemId: 'leetcode:1',
          officialSource: {
            url: 'https://leetcode.com/problems/two-sum/',
            checkedAt: '2026-11-23T00:00:00Z',
          },
        },
      ],
    }),
  );
  return target;
}

async function promotePreview(target: string) {
  const registryPath = join(target, 'manifest.json');
  const registry = JSON.parse(await readFile(registryPath, 'utf8')) as {
    problems: { shards: string[] };
  };
  const shardPath = join(target, 'manifest', registry.problems.shards[0]!);
  const problems = JSON.parse(
    await readFile(shardPath, 'utf8'),
  ) as ProblemRecord[];
  const problem = problems.find(({ id }) => id === 'leetcode:1')!;
  problem.status = 'verified';
  await writeFile(shardPath, JSON.stringify(problems));
  const lessonPath = join(target, 'problems/1/metadata.json');
  const { review, ...content } = JSON.parse(
    await readFile(lessonPath, 'utf8'),
  ) as LessonRecord;
  expect(review).toBeNull();
  await writeFile(
    lessonPath,
    JSON.stringify({
      ...content,
      review: {
        reviewer: 'Disposable preview fixture',
        reviewedOn: '2026-11-23',
        contentSha256: hashLessonForReview(problem, content),
      },
    }),
  );
}

it('keeps the actual draft packages private and exports them only in an isolated verified preview', async () => {
  const options = await fixture();
  const { exportPortfolio, runExport } =
    await import('../../scripts/export-portfolio.js');
  const target = join(options.rootDir, 'site/content/leetcode');
  await mkdir(target, { recursive: true });
  await realCurriculum(options.rootDir);
  const draft = await exportPortfolio(options);
  expect(draft.verifiedCurriculumIds).toEqual([]);
  expect(draft.curriculum.lessons).toEqual([]);
  expect(draft.curriculum.problems).toEqual([]);
  expect(draft.curriculum.sourceVariants).toEqual([]);
  expect(draft.curriculum.traceAssets).toEqual([]);
  expect(draft.curriculum.pendingPathLabels).toHaveLength(2000);
  expect(draft.curriculum.pendingPathLabels).toContainEqual({
    pathId: 'all-problems',
    nodeId: 'problem-1',
    problemId: 'leetcode:1',
    title: 'Two Sum',
  });
  expect(
    await readdir(join(options.out, 'worker-assets/practice-traces')),
  ).toEqual([]);
  const generation = join(
    options.rootDir,
    `site/.generated/curriculum-${draft.curriculum.generation}`,
  );
  const prepared = JSON.parse(
    await readFile(join(generation, 'curriculum.json'), 'utf8'),
  ) as CurriculumSnapshot;
  expect(prepared.lessons).toContainEqual(
    expect.objectContaining({
      problemId: 'leetcode:20',
      status: 'draft',
      approaches: [
        expect.objectContaining({
          id: 'unmatched-openings',
          trace: expect.objectContaining({
            exampleIds: [
              'unfinished-stack',
              'leading-closer',
              'crossed-pairs',
              'nested-success',
            ],
          }),
        }),
      ],
    }),
  );
  expect(prepared.lessons).toContainEqual(
    expect.objectContaining({
      problemId: 'leetcode:3',
      status: 'draft',
      approaches: ['set-eviction', 'last-seen-jump'].map((id) =>
        expect.objectContaining({
          id,
          trace: expect.objectContaining({
            exampleIds: [
              'empty',
              'inside-repeat',
              'outside-repeat',
              'spaces-and-symbols',
            ],
          }),
        }),
      ),
    }),
  );
  const privatePackages = prepared.lessons.flatMap(({ approaches }) =>
    approaches.flatMap(({ trace }) => (trace ? [`${trace.sha256}.json`] : [])),
  );
  expect(
    (await readdir(join(generation, 'worker-assets/practice-traces'))).sort(),
  ).toEqual(privatePackages.sort());

  await promotePreview(target);
  const output = join(options.directory, 'verified-preview');
  const receipt = vi.spyOn(console, 'log').mockImplementation(() => {});
  expect(
    await runExport(
      ['--out', output, '--revision', revision, '--preview'],
      join(options.rootDir, 'site'),
    ),
  ).toBe(0);
  const bytes = await readFile(join(output, 'manifest.json'));
  expect(JSON.parse(String(receipt.mock.lastCall?.[0]))).toEqual({
    mode: 'preview',
    sourceSha: revision,
    manifestSha256: createHash('sha256').update(bytes).digest('hex'),
  });
  const verified = JSON.parse(bytes.toString('utf8')) as typeof draft;
  expect(verified.mode).toBe('preview');
  expect(verified.verifiedCurriculumIds).toEqual([1]);
  expect(verified.curriculum.lessons[0]).toMatchObject({
    problemId: 'leetcode:1',
    route: '/practice/leetcode/1/',
    status: 'verified',
  });
  expect(verified.curriculum.pendingPathLabels).toHaveLength(1999);
  expect(verified.curriculum.sourceVariants[0]).toMatchObject({
    sourceId: stableId,
    problemId: 'leetcode:1',
  });
  expect(verified.curriculum.traceAssets).toHaveLength(3);
  for (const asset of verified.curriculum.traceAssets) {
    const payload = await readFile(join(output, asset.exportPath));
    expect(createHash('sha256').update(payload).digest('hex')).toBe(
      asset.sha256,
    );
    expect(payload).toHaveLength(asset.bytes);
  }
  for (const approach of verified.curriculum.lessons[0]!.approaches) {
    expect(approach.transcripts).toHaveLength(3);
    expect(approach.codeHtml).toContain('shiki');
  }
});

it.each([
  ['SOURCE_REVISION', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'],
  ['REPOSITORY_URL', 'https://github.com/example/another'],
  ['SITE_URL', 'https://another.example.test'],
])(
  'rejects an ambient %s override without leaving staging output',
  async (name, value) => {
    const options = await fixture();
    vi.stubEnv(name, value);
    const { exportPortfolio } =
      await import('../../scripts/export-portfolio.js');
    await expect(exportPortfolio(options)).rejects.toThrow(
      'Publication environment overrides',
    );
    expect(await readdir(options.directory)).toEqual(['archive']);
  },
);

it('fails explicit production and malformed CLI requests without a preview fallback', async () => {
  const options = await fixture();
  const { runExport } = await import('../../scripts/export-portfolio.js');
  const log = vi.spyOn(console, 'error').mockImplementation(() => {});
  const site = join(options.rootDir, 'site');
  expect(await runExport(['--out', options.out], site)).toBe(1);
  expect(log.mock.lastCall?.[0]).toContain('Usage:');
  expect(
    await runExport(
      ['--out', options.out, '--revision', 'abcdef', '--preview'],
      site,
    ),
  ).toBe(1);
  expect(log.mock.lastCall?.[0]).toContain('exact lowercase checkout SHA');
  expect(
    await runExport(['--out', options.out, '--revision', revision], site),
  ).toBe(1);
  expect(log.mock.lastCall?.[0]).toContain('not a git repository');
  expect(await readdir(options.directory)).toEqual(['archive']);
});

it('exports a resource representation and stores duplicate content-addressed assets once', async () => {
  const options = await fixture();
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  const dot = await readFile(join(options.rootDir, 'Books/dot.png'));
  await put(options.rootDir, 'Books/same.png', dot);
  await put(
    options.rootDir,
    'Books/More.md',
    '# More\n\n![Same bytes](same.png)',
  );
  await put(options.rootDir, 'Books/Grid.pdf', '%PDF-1.4\n');
  const localStage = join(options.rootDir, '.superpowers');
  await mkdir(localStage);
  const out = join(localStage, 'resource-export');
  const snapshot = await exportPortfolio({ ...options, out });
  const resource = snapshot.entries.find(({ kind }) => kind === 'pdf');
  expect(resource?.bodyHtml).toBeUndefined();
  expect(resource?.assetUrl).toMatch(/^\/content-assets\/[a-f0-9]{64}\.pdf$/);
  expect(snapshot.assets).toHaveLength(2);
  expect(
    snapshot.assets.filter(({ publicPath }) => publicPath.endsWith('.png')),
  ).toHaveLength(1);
  expect(await readdir(join(out, 'assets'))).toHaveLength(2);
});

it('rejects a symbolic publication policy and any output under the archive inputs', async () => {
  const options = await fixture();
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  await expect(
    exportPortfolio({
      ...options,
      out: join(options.rootDir, 'Books/no-write'),
    }),
  ).rejects.toThrow('outside the checkout');
  const policy = join(options.rootDir, 'site/content/publication.json');
  const original = join(options.directory, 'policy.json');
  await rename(policy, original);
  const { symlink } = await import('node:fs/promises');
  await symlink(original, policy);
  await expect(exportPortfolio(options)).rejects.toThrow(
    'Unsafe publication policy',
  );
  expect(await readdir(options.directory)).toEqual(['archive', 'policy.json']);
});

it.each([
  [
    'changed asset bytes',
    /does not match its registered digest/,
    async (file: string) => writeFile(file, 'changed'),
  ],
  [
    'a nonregular asset',
    /Unsafe generated file/,
    async (file: string) => {
      await rm(file);
      await mkdir(file);
    },
  ],
] as const)(
  'refuses %s after generation and removes its staging directory',
  async (_name, error, change) => {
    const options = await fixture();
    const { exportPortfolio } =
      await import('../../scripts/export-portfolio.js');
    faults.open = async (file) => {
      if (file.startsWith(join(options.rootDir, 'site/public/content-assets/')))
        await change(file);
    };
    await expect(exportPortfolio(options)).rejects.toThrow(error);
    expect(await readdir(options.directory)).toEqual(['archive']);
  },
);

it.each([
  [
    'archive selection',
    /no longer matches the selected publication/,
    (manifest: {
      entries: { title: string }[];
      preparedBodies: Record<string, string>;
    }) => {
      manifest.entries[0]!.title = 'Mismatched';
    },
  ],
  [
    'prepared body',
    /prepared archive bodies/i,
    (manifest: {
      entries: { title: string }[];
      preparedBodies: Record<string, string>;
    }) => {
      manifest.preparedBodies = {};
    },
  ],
] as const)(
  'rejects an altered %s at the publication handoff',
  async (_name, error, change) => {
    const options = await fixture();
    const { exportPortfolio } =
      await import('../../scripts/export-portfolio.js');
    const path = join(options.rootDir, 'site/.generated/current/manifest.json');
    faults.open = async (file) => {
      if (file !== path) return;
      const manifest = JSON.parse(await readFile(file, 'utf8'));
      change(manifest);
      await writeFile(file, JSON.stringify(manifest));
    };
    await expect(exportPortfolio(options)).rejects.toThrow(error);
    expect(await readdir(options.directory)).toEqual(['archive']);
  },
);

it('keeps the export private if the final tracked checkout check fails', async () => {
  const options = await fixture();
  const checkout = await import('../../scripts/portfolio-export/checkout.js');
  const check = vi
    .spyOn(checkout, 'verifyCheckout')
    .mockResolvedValueOnce(undefined)
    .mockResolvedValueOnce(undefined)
    .mockRejectedValueOnce(
      new Error('Dirty tracked checkout during preparation'),
    );
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  await expect(
    exportPortfolio({ ...options, mode: 'production' }),
  ).rejects.toThrow('Dirty tracked checkout during preparation');
  expect(check).toHaveBeenCalledTimes(3);
  expect(check.mock.calls[0]).toEqual([options.rootDir, revision]);
  expect(check.mock.calls[2]?.[2]?.roots).toContain('Books');
  expect(await readdir(options.directory)).toEqual(['archive']);
});

it('surfaces unexpected staging filesystem errors without trying to write elsewhere', async () => {
  const options = await fixture();
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  await expect(
    exportPortfolio({
      ...options,
      out: join(options.directory, 'x'.repeat(256)),
    }),
  ).rejects.toMatchObject({ code: 'ENAMETOOLONG' });
  expect(await readdir(options.directory)).toEqual(['archive']);
});

it('rejects a replaced HTML body that keeps its original generated key', async () => {
  const options = await fixture();
  const { exportPortfolio } = await import('../../scripts/export-portfolio.js');
  const path = join(options.rootDir, 'site/.generated/current/manifest.json');
  faults.open = async (file) => {
    if (file !== path) return;
    const manifest = JSON.parse(await readFile(file, 'utf8')) as {
      preparedBodies: Record<string, string>;
    };
    const key = Object.keys(manifest.preparedBodies)[0]!;
    manifest.preparedBodies[key] = '<p>Replacement body</p>';
    await writeFile(file, JSON.stringify(manifest));
  };
  await expect(exportPortfolio(options)).rejects.toThrow(
    /prepared archive bodies/i,
  );
  expect(await readdir(options.directory)).toEqual(['archive']);
});
