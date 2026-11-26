import { createHash } from 'node:crypto';
import { lstat, readFile, readdir } from 'node:fs/promises';
import { join, posix } from 'node:path';
import { assertUniqueRoutes, publicationPages } from '../identifiers.js';
import type { ContentEntry } from '../types.js';
import type {
  CurriculumSnapshot,
  ProgressRegistry,
  TraceAssetInventory,
} from './prepare.js';
import { readPublishedCurriculum } from './publication.js';

const sha256 = /^[a-f0-9]{64}$/;
const maxFiles = 20_000;
const maxBytes = 25 * 1024 * 1024;
const traceNamespace = 'practice-traces';
const digest = (bytes: string | Uint8Array) =>
  createHash('sha256').update(bytes).digest('hex');

async function requireDirectory(path: string): Promise<void> {
  if (!(await lstat(path)).isDirectory())
    throw new Error(`Unsafe curriculum directory: ${path}`);
}

async function regularFile(path: string) {
  const stats = await lstat(path);
  if (!stats.isFile())
    throw new Error(`Expected regular curriculum file: ${path}`);
  return stats;
}

async function readSidecar<T>(path: string): Promise<T> {
  await regularFile(path);
  return JSON.parse(await readFile(path, 'utf8')) as T;
}

function checkNames(actual: string[], expected: ReadonlySet<string>): void {
  for (const name of actual)
    if (!expected.has(name))
      throw new Error(`Unexpected curriculum artifact: ${name}`);
  const names = new Set(actual);
  for (const name of expected)
    if (!names.has(name))
      throw new Error(`Missing curriculum artifact: ${name}`);
}

export async function verifyCurriculumArtifacts(
  generated: string,
  generation: string,
) {
  if (typeof generation !== 'string' || !sha256.test(generation))
    throw new Error('Invalid curriculum generation');
  const directory = join(generated, `curriculum-${generation}`);
  const worker = join(directory, 'worker-assets');
  const traces = join(worker, traceNamespace);
  await requireDirectory(generated);
  await requireDirectory(directory);
  checkNames(
    await readdir(directory),
    new Set([
      'curriculum.json',
      'progress-registry.json',
      'trace-assets.json',
      'worker-assets',
    ]),
  );

  const snapshot = await readPublishedCurriculum(generated, generation);
  const registry = await readSidecar<ProgressRegistry>(
    join(directory, 'progress-registry.json'),
  );
  const inventory = await readSidecar<TraceAssetInventory>(
    join(directory, 'trace-assets.json'),
  );
  if (
    registry?.version !== 1 ||
    registry.generation !== generation ||
    !Array.isArray(registry.problems) ||
    Object.keys(registry).length !== 3
  )
    throw new Error('Invalid curriculum progress registry');
  if (
    inventory?.version !== 1 ||
    inventory.generation !== generation ||
    !Array.isArray(inventory.assets) ||
    Object.keys(inventory).length !== 3
  )
    throw new Error('Invalid curriculum trace inventory');

  const verified = new Set(
    snapshot.problems
      .filter(({ status }) => status === 'verified')
      .map(({ id }) => id),
  );
  const verifiedLessons = snapshot.lessons
    .filter(({ status }) => status === 'verified')
    .map(({ problemId }) => problemId);
  if (
    verified.size !== verifiedLessons.length ||
    verifiedLessons.some((id) => !verified.delete(id))
  )
    throw new Error('Verified problem and lesson IDs differ');
  const progress = registry.problems;
  if (progress.some((problem) => !problem || Object.keys(problem).length !== 2))
    throw new Error('Invalid curriculum progress registry entry');
  if (
    progress.length !== verifiedLessons.length ||
    progress.some(
      ({ problemId }, index) => problemId !== verifiedLessons[index],
    )
  )
    throw new Error('Progress registry does not match verified problem IDs');
  if (
    progress.some(
      ({ revision }) => typeof revision !== 'string' || !sha256.test(revision),
    )
  )
    throw new Error('Invalid progress registry revision digest');

  const assets = inventory.assets;
  if (assets.length > maxFiles)
    throw new Error('Worker trace assets exceed 20,000 files');
  const filenames = new Set<string>();
  for (const asset of assets) {
    const filename = `${asset.sha256}.json`;
    if (
      typeof asset.sha256 !== 'string' ||
      !sha256.test(asset.sha256) ||
      asset.url !== `/${traceNamespace}/${filename}`
    )
      throw new Error('Invalid canonical public trace package path');
    if (!Number.isSafeInteger(asset.bytes) || asset.bytes <= 0)
      throw new Error(`Invalid trace package byte count: ${filename}`);
    if (asset.bytes > maxBytes)
      throw new Error(`Trace package exceeds 25 MiB: ${filename}`);
    if (filenames.has(filename))
      throw new Error(`Duplicate trace package: ${filename}`);
    filenames.add(filename);
  }
  const references = snapshot.lessons.flatMap(({ approaches }) =>
    approaches.flatMap(({ trace }) => (trace ? [trace] : [])),
  );
  if (JSON.stringify(references) !== JSON.stringify(assets))
    throw new Error(
      'Trace inventory does not match lesson approach references',
    );

  const { generation: selected, ...payload } = snapshot;
  if (digest(JSON.stringify({ payload, progress, assets })) !== selected)
    throw new Error('Curriculum content-derived generation mismatch');

  await requireDirectory(worker);
  checkNames(await readdir(worker), new Set([traceNamespace]));
  await requireDirectory(traces);
  const actual = await readdir(traces);
  if (actual.length > maxFiles)
    throw new Error('Worker trace assets exceed 20,000 files');
  checkNames(actual, filenames);
  for (const { sha256: hash, bytes } of assets) {
    const path = join(traces, `${hash}.json`);
    const stats = await regularFile(path);
    if (stats.size > maxBytes)
      throw new Error(`Trace package exceeds 25 MiB: ${path}`);
    if (stats.size !== bytes)
      throw new Error(`Trace package byte count mismatch: ${path}`);
    const contents = await readFile(path);
    if (contents.length !== bytes)
      throw new Error(`Trace package byte count mismatch: ${path}`);
    if (digest(contents) !== hash)
      throw new Error(`Trace package SHA-256 mismatch: ${path}`);
  }
  return snapshot;
}

export function assertCurriculumRouteOwnership(
  claims: CurriculumSnapshot['routes'],
  entries: ContentEntry[],
): void {
  const routeKey = (route: string) =>
    posix.normalize(route.normalize('NFC')).replace(/\/+$/, '').toLowerCase();
  const sources = entries.map((entry) => ({
    ...entry,
    route: routeKey(entry.route),
    aliases: entry.aliases.map(routeKey),
  }));
  const pages = [...publicationPages(entries), ...claims].map(
    ({ route, owner }) => ({ route: routeKey(route), owner }),
  );
  assertUniqueRoutes(sources, pages);
}
