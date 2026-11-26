import { createHash } from 'node:crypto';
import {
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
import { join } from 'node:path';
import { expect, it, vi } from 'vitest';
import { contentOptions, runContent } from '../../scripts/content.js';
import { exportPortfolio } from '../../scripts/export-portfolio.js';
import { runOrganization } from '../../scripts/organize.js';
import { getPortfolioNotification } from '../../scripts/portfolio-notification.js';
import { readOrganization } from '../../src/content/index.js';

const firstDiagram =
  '<svg xmlns="http://www.w3.org/2000/svg"><rect width="2" height="2"></rect></svg>';
const editedDiagram =
  '<svg xmlns="http://www.w3.org/2000/svg"><rect width="3" height="2"></rect></svg>';
const approvedEditSha = '2'.repeat(40);
const oldRoute = '/notes/books/working-note/';
const newRoute = '/notes/books/renamed-note/';

it('publishes reviewed create, edit, rename and removal from the Notes authoring files', async ({
  onTestFinished,
}) => {
  const directory = await mkdtemp(
    join(await realpath(tmpdir()), 'notes-authoring-'),
  );
  onTestFinished(async () => {
    vi.restoreAllMocks();
    vi.unstubAllEnvs();
    await rm(directory, { recursive: true, force: true });
  });
  for (const name of [
    'HOSTED',
    'SITE_URL',
    'SOURCE_REVISION',
    'REPOSITORY_URL',
  ])
    vi.stubEnv(name, undefined);

  const rootDir = join(directory, 'archive');
  const site = join(rootDir, 'site');
  const books = join(rootDir, 'Books');
  const organization = join(site, 'content/organization');
  const publishedAssets = join(site, 'public/content-assets');
  await mkdir(join(books, 'private'), { recursive: true });
  await mkdir(join(site, 'content'), { recursive: true });
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
      exclude: ['Books/private/**'],
      overrides: { 'Books/private/hidden.md': { title: 'Private override' } },
      repositoryPublic: true,
      repositoryUrl: 'https://github.com/example/notes',
    }),
  );
  await writeFile(
    join(books, 'private/hidden.md'),
    '# Private original\n\nprivate content marker',
  );
  await writeFile(
    join(books, 'draft.md'),
    '---\ntitle: Draft original\ndraft: true\n---\n\ndraft content marker',
  );
  await writeFile(join(books, 'first.svg'), firstDiagram);
  await writeFile(join(books, 'edited.svg'), editedDiagram);

  async function publish(label: string, revision: string) {
    const out = join(directory, label);
    const snapshot = await exportPortfolio({
      rootDir,
      out,
      revision,
      mode: 'preview',
    });
    const manifest = await readFile(join(out, 'manifest.json'), 'utf8');
    expect(JSON.parse(manifest)).toEqual(snapshot);
    expect(manifest).not.toMatch(
      /Private (?:original|override)|Draft original|(?:private|draft) content marker/,
    );
    expect(snapshot).toMatchObject({ mode: 'preview', sourceSha: revision });
    return { snapshot, out };
  }

  const before = await publish('before', '0'.repeat(40));
  expect(before.snapshot.entries).toEqual([]);
  expect(before.snapshot.assets).toEqual([]);

  const note = join(books, 'working-note.md');
  await writeFile(
    note,
    '---\ntitle: Working note\n---\n\nOriginal public paragraph.\n\n![Diagram](first.svg)\n',
  );
  const log = vi.spyOn(console, 'log').mockImplementation(() => {});
  expect(await runOrganization(site, ['--dry-run'])).toBe(0);
  const plan = join(directory, 'reviewed-plan.json');
  await writeFile(plan, log.mock.lastCall?.[0] as string);
  expect(await runOrganization(site, ['--apply', plan])).toBe(0);
  const registry = (await readOrganization(organization)).entries;
  expect(registry.entries).toEqual([
    expect.objectContaining({
      sourcePath: 'Books/working-note.md',
      status: 'unreviewed',
    }),
  ]);
  const enrolled = registry.entries[0]!;
  const uid = enrolled.uid;
  expect(uid).toMatch(/^doc-[a-f0-9]{64}$/);
  enrolled.status = 'reviewed';
  const entriesFile = join(organization, 'entries.json');
  await writeFile(entriesFile, JSON.stringify(registry));
  vi.stubEnv('SOURCE_REVISION', '1'.repeat(40));
  expect(await runContent(await contentOptions(site))).toBe(0);
  vi.stubEnv('SOURCE_REVISION', undefined);
  log.mockRestore();

  const created = await publish('created', '1'.repeat(40));
  expect(created.snapshot.entries).toEqual([
    expect.objectContaining({
      id: uid,
      route: oldRoute,
      aliases: [],
      bodyHtml: expect.stringContaining('Original public paragraph.'),
    }),
  ]);
  expect(created.snapshot.assets).toHaveLength(1);
  const firstAsset = created.snapshot.assets[0]!;
  expect(await readFile(join(created.out, firstAsset.exportPath), 'utf8')).toBe(
    firstDiagram,
  );

  await writeFile(
    note,
    '---\ntitle: Working note\n---\n\nRevised public paragraph.\n\n![Replacement](edited.svg)\n',
  );
  const edited = await publish('edited', approvedEditSha);
  expect(edited.snapshot.entries).toEqual([
    expect.objectContaining({
      id: uid,
      route: oldRoute,
      bodyHtml: expect.stringContaining('Revised public paragraph.'),
    }),
  ]);
  expect(edited.snapshot.entries[0]?.bodyHtml).not.toContain(
    'Original public paragraph.',
  );
  const editedHash = createHash('sha256').update(editedDiagram).digest('hex');
  expect(edited.snapshot.assets).toEqual([
    {
      publicPath: `/content-assets/${editedHash}.svg`,
      exportPath: `assets/${editedHash}.svg`,
      bytes: Buffer.byteLength(editedDiagram),
      sha256: editedHash,
    },
  ]);
  expect(edited.snapshot.entries[0]?.bodyHtml).toContain(
    `/content-assets/${editedHash}.svg`,
  );
  expect(await readdir(join(edited.out, 'assets'))).toEqual([
    `${editedHash}.svg`,
  ]);
  expect(await readdir(publishedAssets)).toEqual([`${editedHash}.svg`]);
  expect(
    await readFile(join(edited.out, `assets/${editedHash}.svg`), 'utf8'),
  ).toBe(editedDiagram);
  expect(await readFile(join(books, 'first.svg'), 'utf8')).toBe(firstDiagram);

  // Synthetic CI evidence exercises the decision independently of preview export authentication.
  const approval = {
    repository: 'example/notes',
    ref: 'refs/heads/approved-notes-fixture',
    workflow: '.github/workflows/notes-site.yml',
  };
  const candidate = {
    repository: approval.repository,
    ref: approval.ref,
    sha: edited.snapshot.sourceSha,
  };
  const evidence = {
    ...approval,
    event: 'push',
    headSha: approvedEditSha,
    verifiedSha: approvedEditSha,
  };
  const delivered = new Set<string>();
  expect(
    getPortfolioNotification(
      candidate,
      { ...evidence, conclusion: 'failure' },
      approval,
      delivered,
    ),
  ).toBeNull();
  const verifiedRun = { ...evidence, conclusion: 'success' };
  const intent = getPortfolioNotification(
    candidate,
    verifiedRun,
    approval,
    delivered,
  );
  expect(intent?.notesSha).toBe(approvedEditSha);
  delivered.add(intent!.key);
  expect(
    getPortfolioNotification(candidate, verifiedRun, approval, delivered),
  ).toBeNull();

  const moved = join(books, 'renamed-note.md');
  await rename(note, moved);
  await writeFile(
    moved,
    `---\ntitle: Renamed note\naliases: [${oldRoute}]\n---\n\nRevised public paragraph.\n\n![Replacement](edited.svg)\n`,
  );
  enrolled.sourcePath = 'Books/renamed-note.md';
  await writeFile(entriesFile, JSON.stringify(registry));
  const renamedSha = '3'.repeat(40);
  const renamed = await publish('renamed', renamedSha);
  expect(renamed.snapshot.entries).toEqual([
    expect.objectContaining({
      id: uid,
      route: newRoute,
      title: 'Renamed note',
      aliases: [oldRoute],
      sourceUrl: `https://github.com/example/notes/blob/${renamedSha}/Books/renamed-note.md`,
    }),
  ]);
  expect(renamed.snapshot.organization.memberships).toEqual([
    expect.objectContaining({ uid, entryId: uid, status: 'reviewed' }),
  ]);

  await rm(moved);
  registry.entries = [];
  await writeFile(entriesFile, JSON.stringify(registry));
  const removed = await publish('removed', '4'.repeat(40));
  expect(removed.snapshot.entries).toEqual([]);
  expect(removed.snapshot.organization.memberships).toEqual([]);
  expect(removed.snapshot.assets).toEqual([]);
  expect(await readdir(join(removed.out, 'assets'))).toEqual([]);
  expect(await readdir(publishedAssets)).toEqual([]);
});
