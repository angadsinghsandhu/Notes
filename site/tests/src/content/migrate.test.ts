import { createHash } from 'node:crypto';
import {
  mkdtemp,
  mkdir,
  readFile,
  writeFile,
  rm,
  symlink,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterEach, expect, it } from 'vitest';
import { planMigration, applyMigration } from '../../../src/content/migrate.js';
import { readPolicy, readMetadata } from '../../../src/content/schema.js';
import type { PublicationPolicy } from '../../../src/content/types.js';
const dirs: string[] = [];
const policy: PublicationPolicy = {
  roots: ['Books', 'Classes', 'Courses', 'Interview', 'Languages', 'Tutorials'],
  exclude: [],
  overrides: {},
  repositoryPublic: false,
};
const authored = 'Interview/Applied Science/breadth/6.6.2-transformers.md';
const vendor =
  'Courses/Scrimba/Learn React/src/projects/01-first-react/README.md';
const empty = 'Languages/Japanese/unit 1-4/README.md';
afterEach(async () => {
  for (const dir of dirs.splice(0))
    await rm(dir, { recursive: true, force: true });
});
async function archive(paths = [authored, vendor, empty]) {
  const root = await mkdtemp(join(tmpdir(), 'notes-migrate-'));
  dirs.push(root);
  for (const path of paths) {
    await mkdir(dirname(join(root, path)), { recursive: true });
    await writeFile(
      join(root, path),
      (await readFile(join(process.cwd(), '..', path), 'utf8')).replace(
        /^---\r?\ntitle: "[^\n]*"\r?\n---\r?\n/,
        '',
      ),
    );
  }
  return root;
}
it('plans real authored metadata without source writes, preserves exact bodies including empty placeholders, and applies idempotently', async () => {
  const root = await archive();
  const scoped = {
    ...policy,
    overrides: { [vendor]: { role: 'supplemental' as const } },
  };
  const originals = new Map(
    await Promise.all(
      [authored, vendor, empty].map(
        async (path) =>
          [path, await readFile(join(root, path), 'utf8')] as const,
      ),
    ),
  );
  const plan = await planMigration(root, scoped);
  expect(plan.changes.map((change) => change.sourcePath)).toEqual([
    authored,
    empty,
  ]);
  for (const change of plan.changes) {
    const original = originals.get(change.sourcePath)!;
    expect(await readFile(join(root, change.sourcePath), 'utf8')).toBe(
      original,
    );
    expect(change.originalHash).toBe(
      createHash('sha256').update(original).digest('hex'),
    );
    expect(
      change.proposedText.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, ''),
    ).toBe(original);
  }
  expect(plan.ledger.find((row) => row.sourcePath === vendor)).toMatchObject({
    disposition: 'page',
    reason: expect.stringContaining('supplemental'),
  });
  await applyMigration(plan);
  expect(await readFile(join(root, vendor), 'utf8')).toBe(
    originals.get(vendor),
  );
  expect((await planMigration(root, scoped)).changes).toEqual([]);
  const title = await readMetadata(
    {
      sourcePath: authored,
      absolutePath: join(root, authored),
      section: 'interview',
      kind: 'markdown',
      bytes: 0,
    },
    scoped,
  );
  expect(title.title).toBe('6.6.2 Transformer Architecture');
});
it('rejects all writes when a later real source changed after planning', async () => {
  const root = await archive([authored, empty]);
  const plan = await planMigration(root, policy);
  const first = await readFile(join(root, authored), 'utf8');
  await writeFile(join(root, empty), 'Concurrent author edit');
  await expect(applyMigration(plan)).rejects.toThrow(empty);
  expect(await readFile(join(root, authored), 'utf8')).toBe(first);
  expect(await readFile(join(root, empty), 'utf8')).toBe(
    'Concurrent author edit',
  );
});
it('rejects replaced symlink sources and unsafe forged paths without overwriting targets', async () => {
  const root = await archive([authored]);
  const plan = await planMigration(root, policy);
  const target = join(root, 'outside.txt');
  await writeFile(target, 'Preserve');
  await rm(join(root, authored));
  await symlink(target, join(root, authored));
  await expect(applyMigration(plan)).rejects.toThrow(/symbolic|regular/);
  expect(await readFile(target, 'utf8')).toBe('Preserve');
  await expect(
    applyMigration({
      ...plan,
      changes: [{ ...plan.changes[0]!, sourcePath: '../outside.txt' }],
    }),
  ).rejects.toThrow(/path/);
});
it('keeps existing frontmatter and excluded sources untouched and accounts unsupported artifacts', async () => {
  const root = await archive([authored]);
  await mkdir(join(root, 'Books'));
  await writeFile(
    join(root, 'Books/ready.md'),
    '---\ntitle: Existing\n---\n# Body',
  );
  await writeFile(
    join(root, 'Books/draft.md'),
    '---\ntitle: Draft\ndraft: true\n---\n',
  );
  await writeFile(join(root, 'Books/data.csv'), 'a,b\n1,2');
  const plan = await planMigration(root, policy);
  expect(plan.changes.map((change) => change.sourcePath)).toEqual([authored]);
  expect(plan.ledger).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        sourcePath: 'Books/data.csv',
        disposition: 'unsupported',
      }),
      expect.objectContaining({
        sourcePath: 'Books/draft.md',
        disposition: 'excluded',
      }),
    ]),
  );
});
it('preserves Task5 actual-target link repairs while adding only metadata', async () => {
  const path = "Tutorials/AI/Andrej Karpathy/Let's build GPT/notes/README.md";
  const root = await archive([path]);
  const original = await readFile(join(root, path), 'utf8');
  expect(original).toContain('../papers/attention%20is%20all%20you%20need.pdf');
  expect(
    (
      await readFile(
        join(
          process.cwd(),
          '..',
          path,
          '..',
          '../papers/attention is all you need.pdf',
        ),
      )
    ).length,
  ).toBeGreaterThan(0);
  const plan = await planMigration(root, policy);
  expect(plan.changes[0]?.proposedText.endsWith(original)).toBe(true);
  expect(original).not.toContain('../papers/1706.03762.pdf');
});
it('plans the current archive policy without changing source', async () => {
  const current = await readPolicy('content/publication.json');
  const plan = await planMigration(join(process.cwd(), '..'), current);
  expect(new Set(plan.ledger.map((row) => row.sourcePath)).size).toBe(
    plan.ledger.length,
  );
  expect(plan.ledger.length).toBeGreaterThan(10000);
}, 120000);
