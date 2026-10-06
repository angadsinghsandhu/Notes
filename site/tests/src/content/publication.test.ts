import {
  mkdtemp,
  mkdir,
  readFile,
  writeFile,
  readdir,
  rm,
  symlink,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import { randomUUID } from 'node:crypto';
import {
  commitPublication,
  discardPublication,
  recoverPublications,
} from '../../../src/content/publication.js';
import { writeManifest } from '../../../src/content/manifest.js';
import type { Manifest } from '../../../src/content/index.js';
import { prepareContent } from '../../../src/content/prepare.js';

const faults = vi.hoisted(() => ({ commit: false, restore: false }));
vi.mock('node:fs/promises', async (original) => {
  const fs = await original<typeof import('node:fs/promises')>();
  return {
    ...fs,
    rename: async (from: string, to: string) => {
      if (faults.commit && to.endsWith('/current/manifest.json'))
        throw new Error('injected commit failure');
      if (faults.restore && from.includes('/retired-assets/'))
        throw new Error('injected restoration failure');
      await fs.rename(from, to);
    },
  };
});
const roots: string[] = [];
afterEach(async () => {
  faults.commit = false;
  faults.restore = false;
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function archive() {
  const root = await mkdtemp(join(tmpdir(), 'notes-publication-'));
  roots.push(root);
  await mkdir(join(root, 'Tutorials'));
  await mkdir(join(root, 'site/content'), { recursive: true });
  const policyPath = join(root, 'site/content/publication.json');
  await writeFile(
    policyPath,
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
    rootDir: root,
    outputDir: join(root, 'site/.generated'),
    policyPath,
    hosted: false,
  };
}

it('preserves quarantined last-good assets across commit plus restoration failure and retries recovery without accumulating stages', async () => {
  const options = await archive();
  const note = join(options.rootDir, 'Tutorials/note.md');
  const imagePath = join(options.rootDir, 'Tutorials/pixel.png');
  const image = await readFile('tests/fixtures/synthetic/task3/pixel.png');
  await writeFile(note, '# Old\n![pixel](pixel.png)');
  await writeFile(imagePath, image);
  const first = await prepareContent(options);
  expect(first.diagnostics).toEqual([]);
  const snapshot = join(options.outputDir, 'current/manifest.json');
  const before = await readFile(snapshot);
  await writeFile(note, '# New\n![pixel](pixel.png)');
  await writeFile(imagePath, Buffer.concat([image, Buffer.from('new')]));
  faults.commit = true;
  faults.restore = true;
  const result = await prepareContent(options);
  expect(result.diagnostics[0]?.message).toContain('restoration failure');
  const stages = (await readdir(options.outputDir)).filter((name) =>
    name.startsWith('.stage-'),
  );
  expect(stages).toHaveLength(1);
  const backup = join(
    options.outputDir,
    stages[0]!,
    'retired-assets',
    first.manifest.assets[0]!.url.split('/').at(-1)!,
  );
  expect(await readFile(backup)).toEqual(image);
  expect(await readFile(snapshot)).toEqual(before);
  faults.commit = false;
  expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
    'restoration failure',
  );
  expect(await readFile(backup)).toEqual(image);
  expect(
    (await readdir(options.outputDir)).filter((name) =>
      name.startsWith('.stage-'),
    ),
  ).toEqual(stages);
  faults.restore = false;
  await writeFile(note, '# Broken\n[missing](missing.md)');
  expect((await prepareContent(options)).diagnostics[0]?.message).toContain(
    'missing.md',
  );
  expect(await readFile(snapshot)).toEqual(before);
  const assetDirectory = join(options.rootDir, 'site/public/content-assets');
  expect(await readdir(assetDirectory)).toEqual([
    first.manifest.assets[0]!.url.split('/').at(-1),
  ]);
  expect(
    await readFile(
      join(assetDirectory, first.manifest.assets[0]!.url.split('/').at(-1)!),
    ),
  ).toEqual(image);
  await writeFile(note, '# New\n![pixel](pixel.png)');
  expect((await prepareContent(options)).diagnostics).toEqual([]);
  expect(
    (await readdir(options.outputDir)).filter((name) =>
      name.startsWith('.stage-'),
    ),
  ).toEqual([]);
  expect(JSON.parse(await readFile(snapshot, 'utf8')).entries[0].title).toBe(
    'New',
  );
});

async function pending() {
  const options = await archive();
  const assets = join(options.rootDir, 'site/public/content-assets');
  await mkdir(assets, { recursive: true });
  const stage = join(options.outputDir, `.stage-${randomUUID()}`);
  await mkdir(join(stage, 'assets'), { recursive: true });
  await mkdir(join(stage, 'retired-assets'));
  const name = `${'a'.repeat(64)}.png`;
  const committed: Manifest = {
    version: 1,
    entries: [],
    assets: [
      {
        sourcePath: 'Tutorials/pixel.png',
        bytes: 3,
        mode: 'local',
        url: `/content-assets/${name}`,
      },
    ],
    ledger: [],
  };
  await writeFile(join(assets, name), 'old');
  await writeManifest(committed, join(options.outputDir, 'current'));
  await writeManifest(committed, stage);
  await writeFile(
    join(stage, 'rollback-pending.json'),
    JSON.stringify({ installed: [] }),
  );
  return { options, assets, stage, name };
}

it.each([
  '../outside',
  '/tmp/outside',
  `sub/${'b'.repeat(64)}.png`,
  'not-a-generated-asset',
  `${'a'.repeat(64)}.png`,
  `${'b'.repeat(64)}.png`,
])(
  'rejects forged pending removal %s before touching committed or unrelated data',
  async (installed) => {
    const { options, assets, stage, name } = await pending();
    const outside = join(options.rootDir, 'outside');
    await writeFile(outside, 'unrelated');
    await writeFile(
      join(stage, 'rollback-pending.json'),
      JSON.stringify({ installed: [installed] }),
    );
    await expect(
      recoverPublications(options.outputDir, assets),
    ).rejects.toThrow(/record|asset/i);
    expect(await readFile(join(assets, name), 'utf8')).toBe('old');
    expect(await readFile(outside, 'utf8')).toBe('unrelated');
    expect(
      await readFile(join(stage, 'rollback-pending.json'), 'utf8'),
    ).toContain(installed);
  },
);

it('rejects symlink rollback records and out-of-bound recovery targets while preserving both trees', async () => {
  const { options, assets, stage, name } = await pending();
  const outside = join(options.rootDir, 'outside');
  await mkdir(outside);
  await writeFile(join(outside, 'record'), JSON.stringify({ installed: [] }));
  await rm(join(stage, 'rollback-pending.json'));
  await symlink(join(outside, 'record'), join(stage, 'rollback-pending.json'));
  await expect(recoverPublications(options.outputDir, assets)).rejects.toThrow(
    /symbolic|symlink/i,
  );
  await expect(recoverPublications(options.outputDir, outside)).rejects.toThrow(
    /verified|output/i,
  );
  await expect(discardPublication(options.outputDir, outside)).rejects.toThrow(
    /stage/i,
  );
  expect(await readFile(join(assets, name), 'utf8')).toBe('old');
  expect(await readFile(join(outside, 'record'), 'utf8')).toContain(
    'installed',
  );
});

it('preserves quarantined files if the rollback record is missing or malformed', async () => {
  const { options, assets, stage, name } = await pending();
  await writeFile(join(stage, 'retired-assets', name), 'backup');
  await rm(join(stage, 'rollback-pending.json'));
  await expect(recoverPublications(options.outputDir, assets)).rejects.toThrow(
    /lack.*record/i,
  );
  await expect(discardPublication(options.outputDir, stage)).rejects.toThrow(
    /preserved/i,
  );
  await writeFile(
    join(stage, 'rollback-pending.json'),
    JSON.stringify({ installed: 'invalid' }),
  );
  await expect(recoverPublications(options.outputDir, assets)).rejects.toThrow(
    /record/i,
  );
  expect(await readFile(join(stage, 'retired-assets', name), 'utf8')).toBe(
    'backup',
  );
  expect(await readFile(join(assets, name), 'utf8')).toBe('old');
});

it('rejects an out-of-bound commit stage without replacing the prior manifest or assets', async () => {
  const { options, assets, name } = await pending();
  const outside = join(options.rootDir, 'outside');
  await mkdir(outside);
  const before = await readFile(
    join(options.outputDir, 'current/manifest.json'),
  );
  await expect(
    commitPublication(
      options.outputDir,
      assets,
      outside,
      { version: 1, entries: [], assets: [], ledger: [] },
      false,
    ),
  ).rejects.toThrow(/stage/i);
  expect(
    await readFile(join(options.outputDir, 'current/manifest.json')),
  ).toEqual(before);
  expect(await readFile(join(assets, name), 'utf8')).toBe('old');
});

it.each(['retired-name', 'proposed-url'])(
  'rejects forged %s before recovering or deleting any pending files',
  async (fault) => {
    const { options, assets, stage, name } = await pending();
    if (fault === 'retired-name')
      await writeFile(
        join(stage, 'retired-assets/unowned-file'),
        'private backup',
      );
    else {
      const proposed = JSON.parse(
        await readFile(join(stage, 'manifest.json'), 'utf8'),
      ) as Manifest;
      proposed.assets[0]!.url = `/external/${name}`;
      await writeManifest(proposed, stage);
    }
    await expect(
      recoverPublications(options.outputDir, assets),
    ).rejects.toThrow(/asset/i);
    expect(await readFile(join(assets, name), 'utf8')).toBe('old');
    expect(
      await readFile(join(stage, 'rollback-pending.json'), 'utf8'),
    ).toContain('installed');
  },
);
