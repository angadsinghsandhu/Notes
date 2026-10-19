import {
  mkdtemp,
  mkdir,
  readFile,
  writeFile,
  rm,
  chmod,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import { runMigration } from '../../scripts/migrate.js';
import { prepareContent } from '../../src/content/index.js';
const roots: string[] = [];
afterEach(async () => {
  vi.restoreAllMocks();
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function archive() {
  const root = await mkdtemp(join(tmpdir(), 'notes-migration-cli-'));
  roots.push(root);
  const site = join(root, 'site');
  await mkdir(join(site, 'content'), { recursive: true });
  const path = 'Interview/Applied Science/breadth/6.6.2-transformers.md';
  await mkdir(dirname(join(root, path)), { recursive: true });
  const current = await readFile(join(process.cwd(), '..', path), 'utf8');
  expect(current).toMatch(
    /^---\ntitle: "6.6.2 Transformer Architecture"\n---\n/,
  );
  const original = current.replace(
    /^---\ntitle: "6.6.2 Transformer Architecture"\n---\n/,
    '',
  );
  await writeFile(join(root, path), original);
  await writeFile(
    join(site, 'content/publication.json'),
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
  const prepared = await prepareContent({
    rootDir: root,
    outputDir: join(site, '.generated'),
    policyPath: join(site, 'content/publication.json'),
    hosted: false,
  });
  expect(prepared.diagnostics).toEqual([]);
  return { root, site, path, original };
}
it('writes internal dry-run dispositions and hashes without touching the real note copy, then validates each apply before building', async () => {
  vi.spyOn(console, 'log').mockImplementation(() => {});
  const { root, site, path, original } = await archive();
  const build = vi.fn(async () => {});
  expect(await runMigration(site, ['--dry-run'], build)).toBe(0);
  expect(await readFile(join(root, path), 'utf8')).toBe(original);
  expect(build).not.toHaveBeenCalled();
  const report = JSON.parse(
    await readFile(join(site, 'content/migration-report.json'), 'utf8'),
  );
  expect(report.changes).toEqual([
    expect.objectContaining({
      sourcePath: path,
      originalHash: expect.stringMatching(/^[a-f0-9]{64}$/),
      reason: expect.stringContaining('body preserved'),
      disposition: 'page',
    }),
  ]);
  expect(await runMigration(site, ['--apply'], build)).toBe(0);
  expect(build).toHaveBeenCalledTimes(1);
  const applied = JSON.parse(
    await readFile(join(site, 'content/migration-report.json'), 'utf8'),
  );
  expect(applied.validations[0]).toMatchObject({
    sourcePath: path,
    bodyPreserved: true,
    metadataPreserved: true,
    renderPreserved: true,
    buildPassed: true,
  });
  expect((await readFile(join(root, path), 'utf8')).endsWith(original)).toBe(
    true,
  );
  expect(await runMigration(site, ['--dry-run'], build)).toBe(0);
  expect(build).toHaveBeenCalledTimes(1);
  expect(
    JSON.parse(
      await readFile(join(site, 'content/migration-report.json'), 'utf8'),
    ).changes,
  ).toEqual([]);
});
it('fails closed on unknown mode and a failing per-source build', async () => {
  vi.spyOn(console, 'log').mockImplementation(() => {});
  const { site } = await archive();
  await expect(runMigration(site, ['--force'])).rejects.toThrow('mode');
  await runMigration(site, ['--dry-run']);
  await expect(
    runMigration(site, ['--apply'], async () => {
      throw new Error('Build rejected');
    }),
  ).rejects.toThrow('Build rejected');
  const report = JSON.parse(
    await readFile(join(site, 'content/migration-report.json'), 'utf8'),
  );
  expect(report.validations[0].buildPassed).toBe(false);
});

it('rejects drift from the reviewed dry run before any real source copy is overwritten', async () => {
  vi.spyOn(console, 'log').mockImplementation(() => {});
  const { root, site, path, original } = await archive();
  await runMigration(site, ['--dry-run']);
  const changed = `${original}\nConcurrent author text.\n`;
  await writeFile(join(root, path), changed);
  await expect(runMigration(site, ['--apply'], async () => {})).rejects.toThrow(
    'Reviewed migration plan',
  );
  expect(await readFile(join(root, path), 'utf8')).toBe(changed);
});
it('flags all four actual copied introductions for author review without rewriting them', async () => {
  vi.spyOn(console, 'log').mockImplementation(() => {});
  const { root, site } = await archive();
  const paths = [
    'Courses/Programming with Mosh - Docker Tutorial for Beginners/README.md',
    'Classes/Johns Hopkins/Sem 3/Crypto/6 Consensus/readme.md',
    'Classes/Johns Hopkins/Sem 3/Crypto/7 Threshold Cryptography/readme.md',
    'Classes/Johns Hopkins/Sem 3/Crypto/8 Rollups/readme.md',
  ];
  for (const path of paths) {
    await mkdir(dirname(join(root, path)), { recursive: true });
    const original = await readFile(join(process.cwd(), '..', path));
    await writeFile(join(root, path), original);
  }
  await runMigration(site, ['--dry-run']);
  const report = JSON.parse(
    await readFile(join(site, 'content/migration-report.json'), 'utf8'),
  );
  expect(
    report.authorReviews
      .map((record: { sourcePath: string }) => record.sourcePath)
      .sort(),
  ).toEqual([...paths].sort());
  expect(
    report.authorReviews.every((record: { reason: string }) =>
      record.reason.includes('introduction'),
    ),
  ).toBe(true);
  for (const path of paths)
    expect(await readFile(join(root, path))).toEqual(
      await readFile(join(process.cwd(), '..', path)),
    );
});

it('defaults to dry run and records supplemental upstream documents without changes', async () => {
  const { root, site } = await archive();
  const path =
    'Courses/Scrimba/Learn React/src/projects/01-first-react/README.md';
  await mkdir(dirname(join(root, path)), { recursive: true });
  await writeFile(
    join(root, path),
    await readFile(join(process.cwd(), '..', path)),
  );
  const policyPath = join(site, 'content/publication.json');
  const policy = JSON.parse(await readFile(policyPath, 'utf8'));
  await writeFile(
    policyPath,
    JSON.stringify({
      ...policy,
      overrides: { [path]: { role: 'supplemental' } },
    }),
  );
  vi.spyOn(console, 'log').mockImplementation(() => {});
  expect(await runMigration(site)).toBe(0);
  const report = JSON.parse(
    await readFile(join(site, 'content/migration-report.json'), 'utf8'),
  );
  expect(report.mode).toBe('dry-run');
  expect(report.classification.supplementalPaths).toEqual([path]);
  expect(
    report.changes.map((x: { sourcePath: string }) => x.sourcePath),
  ).not.toContain(path);
  await expect(runMigration(site, ['--apply', '--force'])).rejects.toThrow(
    'mode',
  );
});
it('invokes the default native build command for an isolated owned executable fixture', async () => {
  const { root, site } = await archive();
  const bin = join(site, 'node_modules/.bin');
  await mkdir(bin, { recursive: true });
  const marker = join(root, 'build-arguments.json');
  await writeFile(
    join(bin, 'astro'),
    `#!/usr/bin/env node\nconst fs = require('node:fs'); fs.writeFileSync(${JSON.stringify(marker)},JSON.stringify(process.argv.slice(2))); console.log('Owned native builder fixture completed.');\n`,
  );
  await chmod(join(bin, 'astro'), 0o755);
  vi.spyOn(console, 'log').mockImplementation(() => {});
  await runMigration(site, ['--dry-run']);
  expect(await runMigration(site, ['--apply'])).toBe(0);
  expect(JSON.parse(await readFile(marker, 'utf8'))).toEqual(['build']);
  const report = JSON.parse(
    await readFile(join(site, 'content/migration-report.json'), 'utf8'),
  );
  expect(report.validations[0].buildSummary).toContain(
    'Owned native builder fixture completed',
  );
  expect(report.validations[0].buildPassed).toBe(true);
});
it('executes the real CLI guard and returns nonzero for an unknown mode', async () => {
  const argv = process.argv;
  const exitCode = process.exitCode;
  const error = vi.spyOn(console, 'error').mockImplementation(() => {});
  process.argv = [
    process.execPath,
    new URL('../../scripts/migrate.ts', import.meta.url).pathname,
    '--force',
  ];
  vi.resetModules();
  try {
    await import('../../scripts/migrate.js');
    expect(process.exitCode).toBe(1);
    expect(error).toHaveBeenCalledWith(
      'Migration mode must be --dry-run or --apply',
    );
  } finally {
    process.argv = argv;
    process.exitCode = exitCode;
  }
});

it('rejects a sparse argument vector and records primitive build failures without overwriting the source body', async () => {
  const { site } = await archive();
  vi.spyOn(console, 'log').mockImplementation(() => {});
  await expect(runMigration(site, new Array<string>(1))).rejects.toThrow(
    'mode',
  );
  await runMigration(site, ['--dry-run']);
  await expect(
    runMigration(site, ['--apply'], async () => {
      throw 'Builder refused';
    }),
  ).rejects.toBe('Builder refused');
  const report = JSON.parse(
    await readFile(join(site, 'content/migration-report.json'), 'utf8'),
  );
  expect(report.validations[0]).toMatchObject({
    failure: 'Builder refused',
    bodyPreserved: true,
    buildPassed: false,
  });
});
