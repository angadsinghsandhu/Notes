import { mkdtemp, mkdir, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import { contentOptions, runContent } from '../../scripts/content.js';
const roots: string[] = [];
afterEach(async () => {
  vi.restoreAllMocks();
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function archive() {
  const root = await mkdtemp(join(tmpdir(), 'notes-cli-'));
  roots.push(root);
  const site = join(root, 'site');
  await mkdir(join(site, 'content'), { recursive: true });
  await mkdir(join(root, 'Tutorials'));
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
      revision: 'b'.repeat(40),
    }),
  );
  return { root, site };
}
it('returns nonzero for source diagnostics and zero for a repaired source', async () => {
  const { root, site } = await archive();
  const error = vi.spyOn(console, 'error').mockImplementation(() => {});
  vi.spyOn(console, 'log').mockImplementation(() => {});
  await writeFile(
    join(root, 'Tutorials/note.md'),
    '# Note\n[broken](missing.md)',
  );
  const options = await contentOptions(site);
  expect(await runContent(options)).toBe(1);
  expect(error.mock.calls.flat().join(' ')).toContain('Tutorials/note.md');
  await writeFile(join(root, 'Tutorials/note.md'), '# Note');
  expect(await runContent(options)).toBe(0);
});
it('uses immutable local HEAD when neither policy nor environment supplies a revision', async () => {
  const options = await contentOptions(process.cwd());
  expect(options.revision).toMatch(/^[a-f0-9]{40}$/);
  expect(options.rootDir).toBe(
    join(process.cwd(), '..').replace(/\/site\/\.\.$/, ''),
  );
});

it('prepares archive content before dev and production build through explicit package commands', async () => {
  const packageJson = JSON.parse(await readFile('package.json', 'utf8')) as {
    scripts: Record<string, string>;
  };
  expect(packageJson.scripts.dev).toBe('tsx scripts/dev.ts');
  expect(packageJson.scripts['content:check']).toBe('tsx scripts/content.ts');
  expect(packageJson.scripts.build).toBe(
    'npm run content:check && astro build && pagefind --site dist && npm run check:output',
  );
});

it('wires reviewed dry-run migration and output verification commands', async () => {
  const value = JSON.parse(await readFile('package.json', 'utf8'));
  expect(value.scripts['content:migrate']).toBe('tsx scripts/migrate.ts');
  expect(value.scripts['check:output']).toBe('tsx scripts/verify-output.ts');
});

it('rejects mutable revision configuration and the actual CLI reports a failing policy with nonzero status', async () => {
  const { site } = await archive();
  vi.stubEnv('SOURCE_REVISION', 'master');
  await expect(contentOptions(site)).rejects.toThrow('immutable commit hash');
  vi.unstubAllEnvs();
  const argv = process.argv;
  const exitCode = process.exitCode;
  vi.spyOn(console, 'error').mockImplementation(() => {});
  vi.spyOn(process, 'cwd').mockReturnValue(join(site, 'missing'));
  process.argv = [process.execPath, join(process.cwd(), 'scripts/content.ts')];
  // Use the real module URL for its executable guard, with an isolated failing cwd.
  process.argv[1] = new URL(
    '../../scripts/content.ts',
    import.meta.url,
  ).pathname;
  vi.resetModules();
  try {
    await import('../../scripts/content.js');
    expect(process.exitCode).toBe(1);
    expect(console.error).toHaveBeenCalledWith(
      expect.stringContaining('publication.json'),
    );
  } finally {
    process.argv = argv;
    process.exitCode = exitCode;
  }
});
