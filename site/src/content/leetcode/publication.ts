import { lstat, readFile, readdir, rename, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { verifyGeneratedTree } from '../manifest.js';
import type { CurriculumSnapshot } from './prepare.js';

const generationName = /^curriculum-[a-f0-9]{64}$/;

function generationDirectory(generated: string, generation: string): string {
  const name = `curriculum-${generation}`;
  if (typeof generation !== 'string' || !generationName.test(name))
    throw new Error('Invalid curriculum generation');
  return join(generated, name);
}

/** Missing enrollment is optional. An existing invalid target is a publication error. */
export async function hasCurriculumDirectory(path: string): Promise<boolean> {
  try {
    const stat = await lstat(path);
    if (!stat.isDirectory())
      throw new Error(`Unsafe curriculum directory: ${path}`);
    return true;
  } catch (error) {
    if (error instanceof Error && 'code' in error && error.code === 'ENOENT')
      return false;
    throw error;
  }
}

async function compareTrees(
  staged: string,
  installed: string,
): Promise<boolean> {
  const stagedEntries = await readdir(staged, { withFileTypes: true });
  const installedEntries = await readdir(installed, { withFileTypes: true });
  if (stagedEntries.length !== installedEntries.length) return false;
  const byName = new Map(installedEntries.map((entry) => [entry.name, entry]));
  for (const entry of stagedEntries) {
    const existing = byName.get(entry.name);
    const from = join(staged, entry.name);
    const to = join(installed, entry.name);
    if (entry.isDirectory() && existing?.isDirectory()) {
      if (!(await compareTrees(from, to))) return false;
    } else if (entry.isFile() && existing?.isFile()) {
      if (!(await readFile(from)).equals(await readFile(to))) return false;
    } else return false;
  }
  return true;
}

/** The transaction verifies the generated root and the staging tree before calling this. */
export async function installCurriculum(
  generated: string,
  staged: string,
  generation: string,
): Promise<string | undefined> {
  const target = generationDirectory(generated, generation);
  if (!(await hasCurriculumDirectory(target))) {
    await rename(staged, target);
    return target;
  }
  await verifyGeneratedTree(target);
  if (!(await compareTrees(staged, target)))
    throw new Error(`Existing curriculum generation is corrupt: ${generation}`);
  return undefined;
}

/** Called after the manifest commits, inside the verified generated root. */
export async function pruneCurriculum(
  generated: string,
  selected?: string,
  preceding?: string,
): Promise<void> {
  let failure: unknown;
  for (const name of await readdir(generated)) {
    if (
      !generationName.test(name) ||
      name === `curriculum-${selected}` ||
      name === `curriculum-${preceding}`
    )
      continue;
    const path = join(generated, name);
    try {
      if (!(await hasCurriculumDirectory(path))) continue;
      await verifyGeneratedTree(path);
      await rm(path, {
        recursive: true,
        force: true,
        maxRetries: 2,
        retryDelay: 0,
      });
    } catch (error) {
      failure ??= error;
    }
  }
  if (failure !== undefined) throw failure;
}

export async function readPublishedCurriculum(
  generated: string,
  generation: string,
): Promise<CurriculumSnapshot> {
  const directory = generationDirectory(generated, generation);
  if (!(await hasCurriculumDirectory(directory)))
    throw new Error(`Selected curriculum generation is missing: ${generation}`);
  const file = join(directory, 'curriculum.json');
  if (!(await lstat(file)).isFile())
    throw new Error('Unsafe generated curriculum file');
  const snapshot = JSON.parse(
    await readFile(file, 'utf8'),
  ) as CurriculumSnapshot | null;
  if (
    snapshot?.version !== 1 ||
    snapshot.generation !== generation ||
    !Array.isArray(snapshot.problems) ||
    !Array.isArray(snapshot.lessons) ||
    !Array.isArray(snapshot.paths) ||
    !Array.isArray(snapshot.routes) ||
    !Array.isArray(snapshot.sourceVariants)
  )
    throw new Error('Invalid curriculum snapshot');
  return snapshot;
}
