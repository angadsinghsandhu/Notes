import { lstat, mkdir, realpath, readdir, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import type { Manifest } from './types.js';

function missing(error: unknown): boolean {
  return error instanceof Error && 'code' in error && error.code === 'ENOENT';
}

/** Only these two owned directories may participate in generated cleanup. */
export async function verifyOutputDirectory(
  rootDir: string,
  targetDir: string,
  location: 'site/.generated' | 'site/public/content-assets',
): Promise<string> {
  const root = await realpath(rootDir);
  const expected = join(root, location);
  if (
    resolve(targetDir) !== expected &&
    resolve(targetDir) !== join(resolve(rootDir), location)
  )
    throw new Error(`Output must be the verified ${location} directory`);
  let current = root;
  for (const part of location.split('/')) {
    current = join(current, part);
    try {
      const stat = await lstat(current);
      if (stat.isSymbolicLink() || !stat.isDirectory())
        throw new Error(
          `Unsafe symbolic link or non-directory output: ${current}`,
        );
    } catch (error) {
      if (!missing(error)) throw error;
      await mkdir(current);
    }
  }
  return expected;
}

/** Before a swap/cleanup, reject symlinks and non-file entries throughout the owned tree. */
export async function verifyGeneratedTree(path: string): Promise<void> {
  try {
    const stat = await lstat(path);
    if (stat.isSymbolicLink() || (!stat.isDirectory() && !stat.isFile()))
      throw new Error(`Unsafe symbolic link or generated entry: ${path}`);
    if (stat.isDirectory())
      for (const name of await readdir(path))
        await verifyGeneratedTree(join(path, name));
  } catch (error) {
    if (!missing(error)) throw error;
  }
}

export async function writeManifest(
  manifest: Manifest,
  outputDir: string,
): Promise<void> {
  const output = resolve(outputDir);
  const base = dirname(output);
  if (
    dirname(base).split('/').at(-1) !== 'site' ||
    base.split('/').at(-1) !== '.generated' ||
    !/^(?:current|\.stage-[a-f0-9-]{36})$/.test(output.split('/').at(-1) ?? '')
  )
    throw new Error(
      'Manifest output must be an internal site/.generated snapshot',
    );
  await verifyOutputDirectory(dirname(dirname(base)), base, 'site/.generated');
  await verifyGeneratedTree(output);
  await mkdir(output, { recursive: true });
  const path = join(output, 'manifest.json');
  await verifyGeneratedTree(path);
  await writeFile(path, `${JSON.stringify(manifest, null, 2)}\n`);
}
