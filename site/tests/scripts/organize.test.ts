import {
  mkdtemp,
  mkdir,
  readFile,
  readdir,
  realpath,
  rm,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import * as organize from '../../scripts/organize.js';
import {
  planOrganizationMigration,
  readOrganization,
} from '../../src/content/index.js';
vi.mock('node:url', async (importOriginal) => ({
  ...(await importOriginal<typeof import('node:url')>()),
}));
const roots: string[] = [];
afterEach(async () => {
  vi.restoreAllMocks();
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function fixture() {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'organize-cli-')));
  roots.push(root);
  await mkdir(join(root, 'site/content'), { recursive: true });
  await mkdir(join(root, 'Tutorials'));
  await writeFile(
    join(root, 'site/content/publication.json'),
    JSON.stringify({
      roots: [
        'Books',
        'Classes',
        'Courses',
        'Interview',
        'Languages',
        'Tutorials',
      ],
    }),
  );
  await writeFile(join(root, 'Tutorials/note.md'), '# Note');
  return { root, site: join(root, 'site') };
}
it('prints complete default and explicit dry-run plans without writes', async () => {
  const { root, site } = await fixture();
  const before = await readdir(root, { recursive: true });
  const output = vi.spyOn(console, 'log').mockImplementation(() => {});
  expect(await organize.runOrganization(site)).toBe(0);
  const plan = JSON.parse(output.mock.calls[0]![0] as string);
  expect(plan).toMatchObject({
    version: 1,
    rootDir: root,
    coverage: { publicEntries: 1 },
  });
  expect(plan.sidecars).toHaveLength(4);
  expect(await organize.runOrganization(site, ['--dry-run'])).toBe(0);
  expect(await readdir(root, { recursive: true })).toEqual(before);
});
it('applies a reviewed JSON plan only to the known worktree root', async () => {
  const { root, site } = await fixture();
  const definition = await readOrganization(join(site, 'content/organization'));
  const plan = await planOrganizationMigration(root, definition);
  const filename = join(root, 'reviewed.json');
  await writeFile(filename, JSON.stringify(plan));
  expect(await organize.runOrganization(site, ['--apply', filename])).toBe(0);
  expect(
    JSON.parse(
      await readFile(join(site, 'content/organization/entries.json'), 'utf8'),
    ).entries,
  ).toHaveLength(1);
  const other = await fixture();
  await writeFile(filename, JSON.stringify({ ...plan, rootDir: other.root }));
  await expect(
    organize.runOrganization(site, ['--apply', filename]),
  ).rejects.toThrow('root');
});
it.each([
  ['--unknown'],
  ['--apply'],
  ['--dry-run', 'extra'],
  ['--apply', 'plan', 'extra'],
  ['--dry-run', '--apply', 'plan'],
])('rejects unknown or ambiguous arguments %j', async (...args) => {
  await expect(organize.runOrganization('/unused', args)).rejects.toThrow(
    'Usage',
  );
});

it('executes the CLI guard against its module directory and reports nonzero failures', async () => {
  const { site } = await fixture();
  const url = await import('node:url');
  const actual = await vi.importActual<typeof import('node:url')>('node:url');
  vi.spyOn(url, 'fileURLToPath').mockImplementation((value, options) =>
    value instanceof URL && value.pathname.endsWith('/site/')
      ? site
      : actual.fileURLToPath(value, options),
  );
  const originalArgv = process.argv;
  const originalExit = process.exitCode;
  const error = vi.spyOn(console, 'error').mockImplementation(() => {});
  const output = vi.spyOn(console, 'log').mockImplementation(() => {});
  try {
    for (const args of [[], ['--unknown']]) {
      process.argv = [
        process.execPath,
        actual.fileURLToPath(
          new URL('../../scripts/organize.ts', import.meta.url),
        ),
        ...args,
      ];
      vi.resetModules();
      await import('../../scripts/organize.js');
      expect(process.exitCode).toBe(args.length ? 1 : 0);
    }
    expect(
      JSON.parse(output.mock.calls[0]![0] as string).coverage.publicEntries,
    ).toBe(1);
    expect(error.mock.calls[0]![0]).toContain('Usage');
    process.argv = [process.execPath];
    vi.resetModules();
    await import('../../scripts/organize.js');
  } finally {
    process.argv = originalArgv;
    process.exitCode = originalExit;
  }
});
it.each(['null', '{}', 'not JSON'])(
  'rejects malformed reviewed JSON %s without writes',
  async (text) => {
    const { root, site } = await fixture();
    await writeFile(join(root, 'reviewed.json'), text);
    await expect(
      organize.runOrganization(site, ['--apply', join(root, 'reviewed.json')]),
    ).rejects.toThrow();
    expect(await readdir(join(site, 'content'))).toEqual(['publication.json']);
  },
);
