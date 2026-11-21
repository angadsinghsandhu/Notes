import {
  mkdir,
  mkdtemp,
  readFile,
  readdir,
  rename,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { basename, dirname, join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import { prepareContent } from '../../../src/content/index.js';
import {
  readPreparedBody,
  readPreparedCatalog,
} from '../../../src/lib/catalog.js';
import { prepareFixture } from '../content/leetcode/prepare-fixtures.js';

const faults = vi.hoisted(() => ({
  beforeRead: undefined as undefined | ((path: string) => Promise<void>),
  beforeRename: undefined as undefined | ((path: string) => void),
}));
vi.mock('node:fs/promises', async (original) => {
  const fs = await original<typeof import('node:fs/promises')>();
  return {
    ...fs,
    readFile: (async (
      path: string,
      ...options: [options?: Parameters<typeof fs.readFile>[1]]
    ) => {
      await faults.beforeRead?.(path);
      return fs.readFile(path, options[0] ?? null);
    }) as typeof fs.readFile,
    rename: async (from: string, to: string) => {
      faults.beforeRename?.(to);
      await fs.rename(from, to);
    },
  };
});
const roots: string[] = [];
afterEach(async () => {
  faults.beforeRead = undefined;
  faults.beforeRename = undefined;
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});

async function archive() {
  const rootDir = await mkdtemp(join(tmpdir(), 'notes-curriculum-catalog-'));
  roots.push(rootDir);
  const policyPath = join(rootDir, 'site/content/publication.json');
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
      repositoryPublic: true,
      repositoryUrl: 'https://github.com/owner/repo',
      revision: 'a'.repeat(40),
    }),
  );
  return {
    rootDir,
    outputDir: join(rootDir, 'site/.generated'),
    policyPath,
    hosted: false,
  };
}

async function put(root: string, path: string, value: string | Buffer) {
  const file = join(root, path);
  await mkdir(dirname(file), { recursive: true });
  await writeFile(file, value);
}

async function enrollCurriculum(
  root: string,
  config: Parameters<typeof prepareFixture>[1],
): Promise<string> {
  const fixture = await prepareFixture(root, config);
  const directory = join(root, 'site/content/leetcode');
  await rm(directory, { recursive: true, force: true });
  await rename(fixture.rootDir, directory);
  const { problems, lessons, paths } = fixture.definition;
  await put(
    directory,
    'manifest.json',
    JSON.stringify({
      version: 1,
      problems,
      lessons: lessons.map(({ problemId }) => problemId),
      paths: paths.map(({ id }) => id),
    }),
  );
  for (const lesson of lessons)
    await put(
      directory,
      `problems/${lesson.problemId.split(':')[1]}/metadata.json`,
      JSON.stringify(lesson),
    );
  for (const path of paths)
    await put(directory, `paths/${path.id}.json`, JSON.stringify(path));
  return directory;
}

it('keeps the archive manifest byte-identical when curriculum has never been enrolled', async () => {
  const options = await archive();
  await put(options.rootDir, 'Tutorials/note.md', '# Archive');
  const manifestPath = join(options.outputDir, 'current/manifest.json');
  expect((await prepareContent(options)).diagnostics).toEqual([]);
  const before = await readFile(manifestPath);
  expect(
    (
      await prepareContent({
        ...options,
        curriculumDir: join(options.rootDir, 'site/content/leetcode'),
      })
    ).diagnostics,
  ).toEqual([]);
  expect(await readFile(manifestPath)).toEqual(before);
  expect(
    (
      await readPreparedCatalog(dirname(manifestPath))
    ).curriculum.listProblems(),
  ).toEqual([]);
});

it('rejects a reserved Worker alias before replacing an archive-only publication', async () => {
  const base = await archive();
  const options = {
    ...base,
    curriculumDir: join(base.rootDir, 'site/content/leetcode'),
  };
  const source = 'Tutorials/note.md';
  const manifestPath = join(options.outputDir, 'current/manifest.json');
  await put(options.rootDir, source, '# Archive');
  expect((await prepareContent(options)).diagnostics).toEqual([]);
  const before = await readFile(manifestPath);

  await put(
    options.rootDir,
    source,
    '---\ntitle: Archive\naliases:\n  - /PRACTICE-TRACES/demo/\n---\n# Archive',
  );
  const attempted = await prepareContent(options);
  expect({
    messages: attempted.diagnostics.map(({ message }) => message),
    retainedManifest: (await readFile(manifestPath)).equals(before),
  }).toEqual({
    messages: [
      expect.stringContaining('reserved Worker namespace /practice-traces/'),
    ],
    retainedManifest: true,
  });
});

it('keeps the last good curriculum on malformed updates and pins held archive bodies and trace references', async () => {
  const base = await archive();
  await put(base.rootDir, 'Tutorials/note.md', '# Archive before');
  const curriculumDir = await enrollCurriculum(base.rootDir, {
    prose: '# Lesson before',
  });
  const options = { ...base, curriculumDir, development: true };
  const current = join(base.outputDir, 'current');
  const manifestPath = join(current, 'manifest.json');
  const first = await prepareContent(options);
  expect(first.diagnostics).toEqual([]);
  const manifest = await readFile(manifestPath);
  const old = await readPreparedCatalog(current);
  const oldEntry = old.listEntries()[0]!;
  const oldLesson = old.curriculum.getLesson('leetcode:1')!;
  const oldTrace = oldLesson.approaches[0]!.trace!;
  const oldPackage = join(
    base.outputDir,
    `curriculum-${first.manifest.curriculumGeneration}`,
    'worker-assets',
    oldTrace.url,
  );
  const oldBytes = await readFile(oldPackage);
  expect(oldLesson.bodyHtml).toContain('Lesson before');

  await writeFile(join(curriculumDir, 'problems/1/lesson.md'), '# Unreviewed');
  expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
    'SHA256',
  );
  expect(await readFile(manifestPath)).toEqual(manifest);
  expect(await readFile(oldPackage)).toEqual(oldBytes);
  expect(await readPreparedCatalog(current)).toBe(old);
  await rm(join(curriculumDir, 'manifest.json'));
  expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
    'cannot read curriculum JSON',
  );
  expect(await readFile(manifestPath)).toEqual(manifest);

  await enrollCurriculum(base.rootDir, {
    prose: '# Lesson after',
    trace: (implementationSha256) =>
      JSON.stringify({
        problemId: 'leetcode:1',
        approachId: 'hash-map',
        exampleId: 'pair',
        implementationSha256,
        result: [1, 0],
        frames: [],
      }),
  });
  await put(base.rootDir, 'Tutorials/note.md', '# Archive after');
  const second = await prepareContent(options);
  expect(second.diagnostics).toEqual([]);
  expect(second.manifest.curriculumGeneration).not.toBe(
    first.manifest.curriculumGeneration,
  );
  const next = await readPreparedCatalog(current);
  expect(await readPreparedBody(oldEntry, current)).toContain('Archive before');
  expect(old.curriculum.getLesson('leetcode:1')).toEqual(oldLesson);
  expect(await readFile(oldPackage)).toEqual(oldBytes);
  const newLesson = next.curriculum.getLesson('leetcode:1')!;
  expect(newLesson.bodyHtml).toContain('Lesson after');
  expect(newLesson.approaches[0]?.trace?.url).not.toBe(oldTrace.url);
  expect(await readPreparedBody(next.listEntries()[0]!, current)).toContain(
    'Archive after',
  );
  const verified = next.curriculum.listProblems({
    status: 'verified',
    difficulty: 'easy',
    domain: 'algorithm',
    topic: 'array',
  });
  expect(next.curriculum.listProblems({ topic: 'unknown' })).toEqual([]);
  verified[0]!.topics.length = 0;
  newLesson.approaches[0]!.trace!.exampleIds.length = 0;
  next.curriculum.getPath('all-problems')!.nodes.length = 0;
  expect(
    next.curriculum.listProblems({ status: 'verified' })[0]!.topics,
  ).toContain('array');
  expect(
    next.curriculum.getLesson('leetcode:1')!.approaches[0]!.trace!.exampleIds,
  ).toEqual(['pair']);
  expect(next.curriculum.getPath('all-problems')!.nodes).toHaveLength(2);
});

it('lists unverified identities without granting unavailable drafts a lesson', async () => {
  const options = await archive();
  const curriculumDir = await enrollCurriculum(options.rootDir, {
    draft: true,
    prose: null,
  });
  expect(
    (await prepareContent({ ...options, curriculumDir })).diagnostics,
  ).toEqual([]);
  const { curriculum } = await readPreparedCatalog(
    join(options.outputDir, 'current'),
  );
  expect(
    curriculum.listProblems({ status: 'draft' }).map(({ id }) => id),
  ).toEqual(['leetcode:1']);
  expect(curriculum.listProblems({ status: 'planned' })).toHaveLength(1999);
  expect(curriculum.listProblems({ status: 'verified' })).toEqual([]);
  expect(curriculum.getLesson('leetcode:1')).toBeUndefined();
  expect(curriculum.listPaths().map(({ id }) => id)).toEqual(['all-problems']);
});

it('restores archive assets and discards a new candidate generation if manifest commit fails', async () => {
  const base = await archive();
  const curriculumDir = await enrollCurriculum(base.rootDir, {
    prose: '# Previous',
  });
  const options = { ...base, curriculumDir };
  const image = await readFile('tests/fixtures/synthetic/task3/pixel.png');
  await put(base.rootDir, 'Tutorials/pixel.png', image);
  await put(
    base.rootDir,
    'Tutorials/note.md',
    '# With pixel\n![Pixel](pixel.png)',
  );
  const first = await prepareContent(options);
  expect(first.diagnostics).toEqual([]);
  const current = join(base.outputDir, 'current/manifest.json');
  const before = await readFile(current);
  const asset = join(
    base.rootDir,
    'site/public',
    first.manifest.assets[0]!.url,
  );
  expect(await readFile(asset)).toEqual(image);
  await put(base.rootDir, 'Tutorials/note.md', '# Remove pixel');

  await enrollCurriculum(base.rootDir, { prose: '# Candidate' });
  faults.beforeRename = (target) => {
    if (target.endsWith('/current/manifest.json'))
      throw new Error('manifest commit failed');
  };
  const failed = await prepareContent(options);
  expect(failed.diagnostics[0]?.message).toContain('manifest commit failed');
  expect(await readFile(current)).toEqual(before);
  expect(await readFile(asset)).toEqual(image);
  expect(
    (await readdir(base.outputDir)).filter((name) =>
      name.startsWith('curriculum-'),
    ),
  ).toEqual([`curriculum-${first.manifest.curriculumGeneration}`]);
});

it('reselects the manifest when production retires a generation during the initial catalog read', async () => {
  const base = await archive();
  await put(base.rootDir, 'Tutorials/note.md', '# Archive before');
  const curriculumDir = await enrollCurriculum(base.rootDir, {
    prose: '# Previous',
  });
  const options = { ...base, curriculumDir };
  const first = await prepareContent(options);
  expect(first.diagnostics).toEqual([]);
  const current = join(base.outputDir, 'current');
  const generationDir = join(
    base.outputDir,
    `curriculum-${first.manifest.curriculumGeneration}`,
  );
  let switched = false;
  faults.beforeRead = async (path) => {
    if (!path.endsWith(`/${basename(generationDir)}/curriculum.json`)) return;
    faults.beforeRead = undefined;
    await enrollCurriculum(base.rootDir, { prose: '# Replacement' });
    await put(base.rootDir, 'Tutorials/note.md', '# Archive after');
    expect((await prepareContent(options)).diagnostics).toEqual([]);
    switched = true;
  };
  const catalog = await readPreparedCatalog(current);
  expect(switched).toBe(true);
  expect(catalog.curriculum.getLesson('leetcode:1')?.bodyHtml).toContain(
    'Replacement',
  );
  expect(await readPreparedBody(catalog.listEntries()[0]!, current)).toContain(
    'Archive after',
  );
  await expect(readdir(generationDir)).rejects.toMatchObject({
    code: 'ENOENT',
  });
});

it('rejects a normalized archive alias collision and links variants without changing separate archive bytes', async () => {
  const base = await archive();
  const path = 'Tutorials/note.md';
  const archiveNote = '# Archive source';
  await put(base.rootDir, path, archiveNote);
  const noCurriculum = await prepareContent(base);
  expect(noCurriculum.diagnostics).toEqual([]);
  const curriculumDir = await enrollCurriculum(base.rootDir, {
    prose: '# Editorial lesson',
  });
  const options = {
    ...base,
    curriculumDir,
    sourceVariants: new Map([[path, 'leetcode:1' as const]]),
  };
  const result = await prepareContent(options);
  expect(result.diagnostics).toEqual([]);
  expect(result.manifest.entries).toEqual(noCurriculum.manifest.entries);
  expect(await readFile(join(base.rootDir, path), 'utf8')).toBe(archiveNote);
  const current = join(base.outputDir, 'current');
  const catalog = await readPreparedCatalog(current);
  expect(await readPreparedBody(catalog.listEntries()[0]!, current)).toContain(
    'Archive source',
  );
  const data = JSON.parse(
    await readFile(
      join(
        base.outputDir,
        `curriculum-${result.manifest.curriculumGeneration}/curriculum.json`,
      ),
      'utf8',
    ),
  );
  expect(data.sourceVariants).toEqual([
    {
      sourceId: result.manifest.entries[0]!.id,
      sourceRoute: result.manifest.entries[0]!.route,
      problemId: 'leetcode:1',
      lessonRoute: catalog.curriculum.getLesson('leetcode:1')!.route,
    },
  ]);
  const manifestPath = join(current, 'manifest.json');
  const before = await readFile(manifestPath);
  await put(
    base.rootDir,
    path,
    `---\ntitle: Archive source\naliases:\n  - ${catalog.curriculum.getLesson('leetcode:1')!.route.toUpperCase()}\n---\n${archiveNote}`,
  );
  const failed = await prepareContent(options);
  expect(failed.diagnostics[0]?.message).toMatch(/collision/i);
  expect(await readFile(manifestPath)).toEqual(before);
});

it('rejects enrolled source beneath an external symlinked parent and retains the selected manifest', async () => {
  const base = await archive();
  const curriculumDir = await enrollCurriculum(base.rootDir, {
    prose: '# Selected',
  });
  const options = { ...base, curriculumDir };
  const first = await prepareContent(options);
  expect(first.diagnostics).toEqual([]);
  const manifestPath = join(base.outputDir, 'current/manifest.json');
  const before = await readFile(manifestPath);
  const external = await mkdtemp(join(tmpdir(), 'notes-external-enrollment-'));
  roots.push(external);
  const sourceParent = dirname(curriculumDir);
  const externalContent = join(external, 'content');
  await rename(sourceParent, externalContent);
  await symlink(externalContent, sourceParent);
  const result = await prepareContent(options);
  expect(result.diagnostics[0]?.message).toContain(
    'Unsafe curriculum directory',
  );
  expect(await readFile(manifestPath)).toEqual(before);
  const outside = await prepareContent({
    ...base,
    curriculumDir: join(externalContent, 'leetcode'),
  });
  expect(outside.diagnostics[0]?.message).toContain(
    'Curriculum directory must be inside the project',
  );
  expect(await readFile(manifestPath)).toEqual(before);
});
