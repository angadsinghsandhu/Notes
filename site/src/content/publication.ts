import {
  lstat,
  mkdir,
  readFile,
  readdir,
  rename,
  rm,
  writeFile,
} from 'node:fs/promises';
import { basename, dirname, join, resolve } from 'node:path';
import { verifyGeneratedTree, verifyOutputDirectory } from './manifest.js';
import type { Manifest } from './types.js';

const assetName =
  /^[a-f0-9]{64}\.(?:png|jpg|gif|webp|avif|svg|ico|pdf|ppt|pptx)$/;
const removal = { recursive: true, force: true, maxRetries: 2, retryDelay: 0 };
const message = (error: unknown): string =>
  error instanceof Error ? error.message : String(error);
async function exists(path: string): Promise<boolean> {
  try {
    await lstat(path);
    return true;
  } catch (error) {
    if (error instanceof Error && 'code' in error && error.code === 'ENOENT')
      return false;
    throw error;
  }
}
async function ownedPaths(generated: string, assetsTarget?: string) {
  const output = resolve(generated);
  if (basename(output) !== '.generated' || basename(dirname(output)) !== 'site')
    throw new Error('Publication requires the owned site/.generated directory');
  const root = dirname(dirname(output));
  return {
    generated: await verifyOutputDirectory(root, generated, 'site/.generated'),
    assets: await verifyOutputDirectory(
      root,
      assetsTarget ?? join(root, 'site/public/content-assets'),
      'site/public/content-assets',
    ),
  };
}
function ownedStage(
  generated: string,
  stage: string,
  canonical: string,
): string {
  if (
    ![resolve(generated), canonical].includes(dirname(resolve(stage))) ||
    !/^\.stage-[a-f0-9-]{36}$/.test(basename(stage))
  )
    throw new Error(
      'Publication stage must be inside the owned generated directory',
    );
  return join(canonical, basename(stage));
}
function localNames(manifest: Manifest): Set<string> {
  const local = manifest.assets.filter((asset) => asset.mode === 'local');
  if (local.some((asset) => !asset.url.startsWith('/content-assets/')))
    throw new Error('Invalid generated asset URL');
  const names = local.map((asset) =>
    asset.url.slice('/content-assets/'.length),
  );
  if (names.some((name) => !assetName.test(name)))
    throw new Error('Invalid generated asset name');
  return new Set(names);
}

/** Validate the complete record and its targets before mutating any recovery files. */
async function restorePending(
  stage: string,
  current: string,
  assets: string,
): Promise<void> {
  await verifyGeneratedTree(stage);
  await verifyGeneratedTree(current);
  await verifyGeneratedTree(assets);
  const record: unknown = JSON.parse(
    await readFile(join(stage, 'rollback-pending.json'), 'utf8'),
  );
  if (
    !record ||
    typeof record !== 'object' ||
    !('installed' in record) ||
    !Array.isArray(record.installed) ||
    record.installed.some(
      (name: unknown) => typeof name !== 'string' || !assetName.test(name),
    )
  )
    throw new Error('Invalid publication rollback record');
  const installed = record.installed as string[];
  const proposed = localNames(
    JSON.parse(
      await readFile(join(stage, 'manifest.json'), 'utf8'),
    ) as Manifest,
  );
  const currentFile = join(current, 'manifest.json');
  const committed = (await exists(currentFile))
    ? localNames(JSON.parse(await readFile(currentFile, 'utf8')) as Manifest)
    : new Set<string>();
  for (const name of installed) {
    if (
      !proposed.has(name) ||
      committed.has(name) ||
      (await exists(join(stage, 'assets', name)))
    )
      throw new Error(
        'Rollback record cannot remove an unowned or committed asset',
      );
  }
  const retired = await readdir(join(stage, 'retired-assets'));
  if (retired.some((name) => !assetName.test(name)))
    throw new Error('Invalid quarantined asset name');
  for (const name of retired)
    await rename(join(stage, 'retired-assets', name), join(assets, name));
  for (const name of installed) await rm(join(assets, name), { force: true });
}

/** Pending rollback is recovered before cleanup; a failed recovery leaves its stage intact. */
export async function recoverPublications(
  generated: string,
  assetsTarget: string,
): Promise<void> {
  const owned = await ownedPaths(generated, assetsTarget);
  const current = join(owned.generated, 'current');
  await verifyGeneratedTree(current);
  for (const name of await readdir(owned.generated)) {
    if (!/^\.(?:stage|snapshot-backup|assets-backup)-[a-f0-9-]{36}$/.test(name))
      continue;
    const path = join(owned.generated, name);
    await verifyGeneratedTree(path);
    if (await exists(join(path, 'rollback-pending.json')))
      await restorePending(path, current, owned.assets);
    else if (
      (await exists(join(path, 'manifest.json'))) &&
      (await exists(join(path, 'retired-assets'))) &&
      (await readdir(join(path, 'retired-assets'))).length
    )
      throw new Error(
        'Quarantined assets lack a rollback record; recovery stage preserved',
      );
    await rm(path, removal);
  }
  const legacyBodies = join(current, 'bodies');
  if (await exists(legacyBodies)) {
    const manifest = JSON.parse(
      await readFile(join(current, 'manifest.json'), 'utf8'),
    ) as Manifest & { preparedBodies?: unknown };
    if (manifest.preparedBodies) {
      await verifyGeneratedTree(legacyBodies);
      await rm(legacyBodies, removal);
    }
  }
}

/** Failed rollback data must never be discarded by preparation's finally block. */
export async function discardPublication(
  generated: string,
  stage: string,
): Promise<void> {
  const owned = await ownedPaths(generated);
  const path = ownedStage(generated, stage, owned.generated);
  await verifyGeneratedTree(path);
  if (
    (await exists(join(path, 'rollback-pending.json'))) ||
    ((await exists(join(path, 'retired-assets'))) &&
      (await readdir(join(path, 'retired-assets'))).length)
  )
    throw new Error('Pending publication rollback preserved for recovery');
  await rm(path, removal);
}

/** One regular-file rename commits catalog+bodies; asset changes have bounded rollback. */
export async function commitPublication(
  generated: string,
  assetsTarget: string,
  stage: string,
  manifest: Manifest,
  development: boolean,
): Promise<void> {
  const owned = await ownedPaths(generated, assetsTarget);
  stage = ownedStage(generated, stage, owned.generated);
  generated = owned.generated;
  assetsTarget = owned.assets;
  const current = join(generated, 'current');
  await verifyGeneratedTree(current);
  await verifyGeneratedTree(assetsTarget);
  await verifyGeneratedTree(stage);
  await mkdir(current, { recursive: true });
  const wanted = localNames(manifest);
  const retained = new Set(wanted);
  const file = join(current, 'manifest.json');
  if (development && (await exists(file))) {
    const previous = JSON.parse(await readFile(file, 'utf8')) as Manifest;
    for (const name of localNames(previous)) retained.add(name);
  }
  const installed: string[] = [];
  await mkdir(join(stage, 'retired-assets'));
  try {
    for (const name of wanted) {
      const target = join(assetsTarget, name);
      if (await exists(target)) {
        if (
          !(await readFile(target)).equals(
            await readFile(join(stage, 'assets', name)),
          )
        )
          throw new Error(
            `Existing content-addressed asset is corrupt: ${name}`,
          );
      } else {
        await rename(join(stage, 'assets', name), target);
        installed.push(name);
      }
    }
    for (const name of await readdir(assetsTarget)) {
      if (retained.has(name)) continue;
      await rename(
        join(assetsTarget, name),
        join(stage, 'retired-assets', name),
      );
    }
    await rename(join(stage, 'manifest.json'), file);
  } catch (error) {
    try {
      await writeFile(
        join(stage, 'rollback-pending.json'),
        JSON.stringify({ installed }),
      );
      await restorePending(stage, current, assetsTarget);
      await rm(join(stage, 'rollback-pending.json'));
    } catch (rollbackError) {
      throw new Error(
        `Publication failed: ${message(error)}; rollback pending: ${message(rollbackError)}`,
        { cause: rollbackError },
      );
    }
    throw error;
  }
  // Cleanup after the commit cannot turn a changed publication into a failed rebuild.
  try {
    await recoverPublications(generated, assetsTarget);
  } catch (error) {
    console.warn(
      `Committed publication; recovery cleanup pending: ${message(error)}`,
    );
  }
}
