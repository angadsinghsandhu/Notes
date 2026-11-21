import {
  mkdtemp,
  mkdir,
  readFile,
  rename,
  rm,
  symlink,
  truncate,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterEach, expect, it } from 'vitest';
import {
  assertCurriculumRouteOwnership,
  verifyCurriculumArtifacts,
} from '../../../../src/content/leetcode/artifacts.js';
import { prepareCurriculum } from '../../../../src/content/leetcode/prepare.js';
import { digest, prepareFixture, sourceEntry } from './prepare-fixtures.js';

const roots: string[] = [];
afterEach(async () => {
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function artifact(draft = false, traceCount = 1) {
  const root = await mkdtemp(join(tmpdir(), 'notes-worker-artifact-'));
  roots.push(root);
  const { definition, outputDir, ...context } = await prepareFixture(root, {
    draft,
    traceCount,
  });
  const snapshot = await prepareCurriculum(definition, {
    ...context,
    outputDir,
  });
  const generated = join(root, '.generated');
  const directory = join(generated, `curriculum-${snapshot.generation}`);
  await mkdir(generated);
  await rename(outputDir, directory);
  const trace = snapshot.lessons[0]!.approaches[0]!.trace;
  const traceFile = join(
    directory,
    'worker-assets',
    trace?.url ?? 'practice-traces/not-emitted.json',
  );
  const registryFile = join(directory, 'progress-registry.json');
  const inventoryFile = join(directory, 'trace-assets.json');
  const registry = JSON.parse(await readFile(registryFile, 'utf8'));
  const inventory = JSON.parse(await readFile(inventoryFile, 'utf8'));
  return {
    verify: () => verifyCurriculumArtifacts(generated, snapshot.generation),
    root,
    generated,
    directory,
    snapshot,
    trace: trace!,
    traceFile,
    registryFile,
    inventoryFile,
    registry,
    inventory,
  };
}

it('verifies only the selected generation and leaves its bytes untouched', async () => {
  const { generated, snapshot, traceFile, verify } = await artifact();
  await mkdir(join(generated, `curriculum-${'0'.repeat(64)}`));
  const bytes = await readFile(traceFile);
  await expect(verify()).resolves.toEqual(snapshot);
  expect(await readFile(traceFile)).toEqual(bytes);
  await expect(
    verifyCurriculumArtifacts(generated, '../stray'),
  ).rejects.toThrow(/generation/i);
  await expect(
    verifyCurriculumArtifacts(generated, '1'.repeat(64)),
  ).rejects.toThrow();
});

it('supports a draft trace without enrolling a draft revision', async () => {
  const { registry, snapshot, verify } = await artifact(true);
  expect(registry.problems).toEqual([]);
  await expect(verify()).resolves.toEqual(snapshot);
});

it.each([
  ['missing package', 'Missing', async ({ traceFile }) => rm(traceFile)],
  [
    'unbound registry property',
    'registry',
    async ({ registryFile, registry }) =>
      writeFile(
        registryFile,
        JSON.stringify({ ...registry, private: 'unexpected' }),
      ),
  ],
  [
    'unbound inventory property',
    'inventory',
    async ({ inventoryFile, inventory }) =>
      writeFile(
        inventoryFile,
        JSON.stringify({ ...inventory, private: 'unexpected' }),
      ),
  ],
  [
    'extra registry entry property',
    'registry',
    async ({ registryFile, registry }) =>
      writeFile(
        registryFile,
        JSON.stringify({
          ...registry,
          problems: [{ ...registry.problems[0], private: 'unexpected' }],
        }),
      ),
  ],
  [
    'invalid package declaration',
    'byte',
    async ({ inventoryFile, inventory, trace }) =>
      writeFile(
        inventoryFile,
        JSON.stringify({ ...inventory, assets: [{ ...trace, bytes: 0 }] }),
      ),
  ],
  [
    'oversized package declaration',
    '25 MiB',
    async ({ inventoryFile, inventory, trace }) =>
      writeFile(
        inventoryFile,
        JSON.stringify({
          ...inventory,
          assets: [{ ...trace, bytes: 25 * 1024 * 1024 + 1 }],
        }),
      ),
  ],
  [
    'duplicate package declaration',
    'Duplicate',
    async ({ inventoryFile, inventory, trace }) =>
      writeFile(
        inventoryFile,
        JSON.stringify({ ...inventory, assets: [trace, trace] }),
      ),
  ],

  [
    'extra package',
    'Unexpected',
    async ({ traceFile }) =>
      writeFile(join(dirname(traceFile), 'extra.json'), ''),
  ],
  [
    'extra asset root file',
    'Unexpected',
    async ({ directory }) =>
      writeFile(join(directory, 'worker-assets/private.json'), ''),
  ],
  [
    'sidecar directory',
    'regular',
    async ({ registryFile }) => {
      await rm(registryFile);
      await mkdir(registryFile);
    },
  ],
  [
    'symlinked package',
    'regular',
    async ({ root, traceFile }) => {
      const target = join(root, 'outside.json');
      await rename(traceFile, target);
      await symlink(target, traceFile);
    },
  ],
  [
    'symlinked Worker directory',
    'directory',
    async ({ root, directory }) => {
      const worker = join(directory, 'worker-assets');
      const target = join(root, 'outside');
      await rename(worker, target);
      await symlink(target, worker);
    },
  ],
  [
    'symlinked selected generation',
    'directory',
    async ({ root, directory }) => {
      const target = join(root, 'outside');
      await rename(directory, target);
      await symlink(target, directory);
    },
  ],
  [
    'symlinked generated root',
    'directory',
    async ({ root, generated }) => {
      const target = join(root, 'outside');
      await rename(generated, target);
      await symlink(target, generated);
    },
  ],
  [
    'size mismatch',
    'byte',
    async ({ traceFile, trace }) => truncate(traceFile, trace.bytes - 1),
  ],
  [
    'package limit',
    '25 MiB',
    async ({ traceFile }) => truncate(traceFile, 25 * 1024 * 1024 + 1),
  ],
  [
    'digest mismatch',
    'SHA-256',
    async ({ traceFile, trace }) =>
      writeFile(traceFile, Buffer.alloc(trace.bytes)),
  ],
  [
    'registry version mismatch',
    'registry',
    async ({ registryFile, registry }) =>
      writeFile(registryFile, JSON.stringify({ ...registry, version: 2 })),
  ],
  [
    'inventory generation mismatch',
    'inventory',
    async ({ inventoryFile, inventory }) =>
      writeFile(
        inventoryFile,
        JSON.stringify({ ...inventory, generation: '0'.repeat(64) }),
      ),
  ],
  [
    'missing verified revision',
    'verified',
    async ({ registryFile, registry }) =>
      writeFile(registryFile, JSON.stringify({ ...registry, problems: [] })),
  ],
  [
    'invalid revision digest',
    'revision',
    async ({ registryFile, registry }) =>
      writeFile(
        registryFile,
        JSON.stringify({
          ...registry,
          problems: [{ ...registry.problems[0], revision: 'bogus' }],
        }),
      ),
  ],
  [
    'different valid revision',
    'content-derived generation',
    async ({ registryFile, registry }) =>
      writeFile(
        registryFile,
        JSON.stringify({
          ...registry,
          problems: [
            { ...registry.problems[0], revision: digest('modified revision') },
          ],
        }),
      ),
  ],
  [
    'missing approach reference',
    'approach',
    async ({ inventoryFile, inventory }) =>
      writeFile(inventoryFile, JSON.stringify({ ...inventory, assets: [] })),
  ],
  [
    'oversized inventory',
    '20,000',
    async ({ inventoryFile, inventory, trace }) =>
      writeFile(
        inventoryFile,
        JSON.stringify({
          ...inventory,
          assets: Array.from({ length: 20_001 }, () => trace),
        }),
      ),
  ],
  [
    'noncanonical public path',
    'canonical',
    async ({ inventoryFile, inventory, trace }) =>
      writeFile(
        inventoryFile,
        JSON.stringify({
          ...inventory,
          assets: [
            { ...trace, url: `/practice-traces/../${trace.sha256}.json` },
          ],
        }),
      ),
  ],
] satisfies [
  string,
  string,
  (fixture: Awaited<ReturnType<typeof artifact>>) => Promise<unknown>,
][])('rejects %s', async (_name, message, tamper) => {
  const fixture = await artifact();
  await tamper(fixture);
  await expect(fixture.verify()).rejects.toThrow(message);
});

it('accepts a generation with no public trace packages', async () => {
  const { verify, inventory } = await artifact(true, 0);
  expect(inventory.assets).toEqual([]);
  await expect(verify()).resolves.toBeDefined();
});

it('enforces the physical Worker file limit separately from its inventory', async () => {
  const { traceFile, verify } = await artifact();
  for (let offset = 0; offset < 20_000; offset += 250)
    await Promise.all(
      Array.from({ length: 250 }, (_, index) =>
        writeFile(join(dirname(traceFile), String(offset + index)), ''),
      ),
    );
  await expect(verify()).rejects.toThrow('20,000');
}, 20_000);

it.each([
  ['/library/', [], 'reserved website route'],
  [
    '/library/interview/folders/arrays/',
    [sourceEntry({ groupSegments: ['Arrays'] })],
    'folder',
  ],
  [
    '/practice/café/',
    [sourceEntry({ aliases: ['/PRACTICE/CAFÉ/'] })],
    'Route collision',
  ],
  ['/PRACTICE-TRACES/', [], 'reserved Worker namespace'],
  ['/practice-traces/pkg/', [], 'reserved Worker namespace'],
] as const)(
  'reserves %s for its canonical owner',
  (route, entries, diagnostic) => {
    expect(() =>
      assertCurriculumRouteOwnership(
        [{ route, owner: 'curriculum fixture' }],
        [...entries],
      ),
    ).toThrow(diagnostic);
  },
);
