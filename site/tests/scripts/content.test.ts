import {
  mkdtemp,
  mkdir,
  writeFile,
  readFile,
  rm,
  symlink,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, delimiter } from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { afterEach, expect, it, vi } from 'vitest';
import { contentOptions, runContent } from '../../scripts/content.js';
const roots: string[] = [];
afterEach(async () => {
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function archive() {
  vi.stubEnv('SOURCE_REVISION', undefined);
  vi.stubEnv('SITE_URL', undefined);
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
  expect(options.revision).toBe('b'.repeat(40));
  expect(options.organizationDir).toBe(join(site, 'content/organization'));
  expect(options.curriculumDir).toBe(join(site, 'content/leetcode'));
  expect(await runContent(options)).toBe(1);
  expect(error.mock.calls.flat().join(' ')).toContain('Tutorials/note.md');
  await writeFile(join(root, 'Tutorials/note.md'), '# Note');
  expect(await runContent(options)).toBe(0);
});
it('uses immutable local HEAD when neither policy nor environment supplies a revision', async () => {
  vi.stubEnv('SOURCE_REVISION', undefined);
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
  expect(packageJson.scripts.dev).toBe(
    'npm run pdf:assets && tsx scripts/dev.ts',
  );
  expect(packageJson.scripts['pdf:assets']).toBe('tsx scripts/pdf-assets.ts');
  expect(packageJson.scripts['content:check']).toBe('tsx scripts/content.ts');
  expect(packageJson.scripts.build).toBe(
    'npm run pdf:assets && npm run content:check && astro build && pagefind --site dist && npm run check:output',
  );
});

it('wires reviewed dry-run migration and output verification commands', async () => {
  const value = JSON.parse(await readFile('package.json', 'utf8'));
  expect(value.scripts['content:migrate']).toBe('tsx scripts/migrate.ts');
  expect(value.scripts['content:organize']).toBe('tsx scripts/organize.ts');
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

it('executes verification with build fixtures first, final output validation and failure propagation', async () => {
  const { scripts } = JSON.parse(await readFile('package.json', 'utf8')) as {
    scripts: Record<string, string>;
  };
  const root = await mkdtemp(join(tmpdir(), 'notes-verify-order-'));
  roots.push(root);
  const log = join(root, 'order.log');
  await writeFile(
    join(root, 'npm'),
    `#!/bin/sh
printf '%s\n' "$*" >> "$TASK_8_ORDER_LOG"
if [ "$*" = "$TASK_8_FAIL_COMMAND" ]; then exit 23; fi
`,
    { mode: 0o755 },
  );
  const order = ['run build', 'run check', 'run test:e2e', 'run check:output'];
  for (const failAt of [-1, 0, 1, 2, 3]) {
    await writeFile(log, '');
    let code = 0;
    try {
      await promisify(execFile)('sh', ['-c', scripts.verify!], {
        env: {
          ...process.env,
          PATH: `${root}${delimiter}${process.env['PATH'] ?? ''}`,
          TASK_8_ORDER_LOG: log,
          TASK_8_FAIL_COMMAND: order[failAt] ?? '',
        },
      });
    } catch (error) {
      code = (error as { code: number }).code;
    }
    expect(code).toBe(failAt === -1 ? 0 : 23);
    expect((await readFile(log, 'utf8')).trim().split('\n')).toEqual(
      order.slice(0, failAt === -1 ? order.length : failAt + 1),
    );
  }
});

it('runs archive parity and curriculum verification in check and stops at a failed Python command', async () => {
  const { scripts } = JSON.parse(await readFile('package.json', 'utf8')) as {
    scripts: Record<string, string>;
  };
  const parity = '-B scripts/check_polars.py';
  const discovery =
    '-B -m unittest discover -s tests/scripts -p test_curriculum*.py';
  const problems =
    '-B -m unittest tests/content/leetcode/problems/*/test_problem_*_solutions.py';
  const evidence = '-B scripts/curriculum.py check';
  expect(scripts['test:polars']).toBe(`python3 ${parity}`);
  const order = [
    'run format:check',
    'run lint',
    'run check:boundaries',
    'run typecheck',
    'run test:polars',
    'run test:curriculum',
    'run test:unit',
  ];
  expect(scripts.check).toBe(
    order.map((command) => `npm ${command}`).join(' && '),
  );
  const root = await mkdtemp(join(tmpdir(), 'notes-python-gates-'));
  roots.push(root);
  const log = join(root, 'order.log');
  await writeFile(
    join(root, 'npm'),
    `#!/bin/sh
printf '%s\\n' "$*" >> "$TASK_CHECK_ORDER_LOG"
case "$*" in
  "run test:polars") exec sh -c "$TASK_CHECK_PARITY_COMMAND" ;;
  "run test:curriculum") exec sh -c "$TASK_CHECK_CURRICULUM_COMMAND" ;;
esac
`,
    { mode: 0o755 },
  );
  await writeFile(
    join(root, 'python3'),
    `#!/bin/sh
printf 'python3 %s\\n' "$*" >> "$TASK_CHECK_ORDER_LOG"
if [ "$*" = "$TASK_CHECK_FAIL_COMMAND" ]; then exit 31; fi
`,
    { mode: 0o755 },
  );
  const executed = [
    ...order.slice(0, 5),
    `python3 ${parity}`,
    order[5],
    `python3 ${discovery}`,
    `python3 ${problems}`,
    `python3 ${evidence}`,
    order[6],
  ];
  for (const failingCommand of ['', parity, discovery, problems, evidence]) {
    await writeFile(log, '');
    let code = 0;
    try {
      await promisify(execFile)('sh', ['-c', scripts.check!], {
        cwd: root,
        env: {
          ...process.env,
          PATH: `${root}${delimiter}${process.env['PATH'] ?? ''}`,
          TASK_CHECK_ORDER_LOG: log,
          TASK_CHECK_PARITY_COMMAND: scripts['test:polars']!,
          TASK_CHECK_CURRICULUM_COMMAND: scripts['test:curriculum']!,
          TASK_CHECK_FAIL_COMMAND: failingCommand,
        },
      });
    } catch (error) {
      code = (error as { code: number }).code;
    }
    expect(code).toBe(failingCommand ? 31 : 0);
    expect((await readFile(log, 'utf8')).trim().split('\n')).toEqual(
      failingCommand
        ? executed.slice(0, executed.indexOf(`python3 ${failingCommand}`) + 1)
        : executed,
    );
  }
});

it('accepts genuine curriculum absence and retains publication for an invalid curriculum enrollment', async () => {
  const { site } = await archive();
  const error = vi.spyOn(console, 'error').mockImplementation(() => {});
  vi.spyOn(console, 'log').mockImplementation(() => {});
  const options = await contentOptions(site);
  const directory = options.curriculumDir!;
  const manifest = join(options.outputDir, 'current/manifest.json');
  expect(await runContent(options)).toBe(0);
  const baseline = await readFile(manifest);

  await mkdir(directory);
  expect(await runContent(options)).toBe(1);
  expect(error).toHaveBeenLastCalledWith(
    expect.stringContaining('cannot read curriculum JSON'),
  );
  expect(await readFile(manifest)).toEqual(baseline);

  await rm(directory, { recursive: true });
  await writeFile(directory, '{}');
  expect(await runContent(options)).toBe(1);
  expect(error).toHaveBeenLastCalledWith(
    expect.stringContaining('Unsafe curriculum directory'),
  );
  expect(await readFile(manifest)).toEqual(baseline);

  await rm(directory);
  await symlink(join(site, 'missing'), directory);
  expect(await runContent(options)).toBe(1);
  expect(error).toHaveBeenLastCalledWith(
    expect.stringContaining('Unsafe curriculum directory'),
  );
  expect(await readFile(manifest)).toEqual(baseline);
});
