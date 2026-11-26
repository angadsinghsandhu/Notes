import {
  lstat,
  mkdir,
  mkdtemp,
  rename,
  rmdir,
  unlink,
  writeFile,
} from 'node:fs/promises';
import { join } from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import { validateOrganization } from './organization-schema.js';
import {
  organizationInventory,
  optionalBytes,
  safePath,
  sha256,
  verifiedRoot,
} from './organization-migrate-inventory.js';
import {
  migrationPlanSchema,
  SIDECARS,
  type OrganizationMigrationPlan,
} from './organization-migrate-types.js';

/** Only fixed sidecars can be written; all untrusted evidence is re-derived. */
export async function applyOrganizationMigration(
  value: OrganizationMigrationPlan,
): Promise<void> {
  const plan = migrationPlanSchema.parse(value);
  const root = await verifiedRoot(plan.rootDir);
  if (plan.rootDir !== root)
    throw new Error('Organization plan root must be canonical');
  const directory = await safePath(root, 'site/content/organization');
  const definition = validateOrganization(
    Object.fromEntries(
      SIDECARS.map((name, index) => {
        const record = plan.sidecars[index]!;
        if (record.filename !== `${name}.json`)
          throw new Error('Invalid sidecar filename or order');
        return [name, JSON.parse(record.proposedBytes) as unknown];
      }),
    ),
  );
  const paths = await Promise.all(
    plan.sidecars.map((record) =>
      safePath(root, `site/content/organization/${record.filename}`),
    ),
  );
  const previous = await Promise.all(paths.map(optionalBytes));
  async function validateEvidence(): Promise<void> {
    const evidence = await organizationInventory(root, definition);
    if (
      plan.policyHash !== evidence.policyHash ||
      !isDeepStrictEqual(plan.inventory, evidence.inventory)
    )
      throw new Error('Organization source evidence changed after planning');
    if (
      !isDeepStrictEqual(plan.coverage, evidence.coverage) ||
      !isDeepStrictEqual(plan.candidates, evidence.candidates)
    )
      throw new Error('Invalid organization audit evidence');
  }
  await validateEvidence();
  if (
    previous.every(
      (bytes, index) =>
        bytes !== null &&
        bytes.toString('utf8') === plan.sidecars[index]!.proposedBytes,
    )
  )
    return;
  for (const [index, bytes] of previous.entries()) {
    if (
      (bytes === null ? null : sha256(bytes)) !==
      plan.sidecars[index]!.previousHash
    )
      throw new Error(
        `Organization destination changed: ${plan.sidecars[index]!.filename}`,
      );
  }
  const oldDefinition = previous.every((bytes) => bytes !== null)
    ? validateOrganization(
        Object.fromEntries(
          SIDECARS.map((name, index) => [
            name,
            JSON.parse(previous[index]!.toString('utf8')) as unknown,
          ]),
        ),
      )
    : undefined;
  for (const record of oldDefinition?.entries.entries ?? []) {
    if (
      !definition.entries.entries.some(
        (next) =>
          next.sourcePath === record.sourcePath && next.uid === record.uid,
      )
    )
      throw new Error(`${record.sourcePath}: registered UID must be retained`);
  }
  const backups = await safePath(root, '.superpowers/organization-migrations');
  await mkdir(backups, { recursive: true });
  await safePath(root, '.superpowers/organization-migrations');
  const recovery = await mkdtemp(join(backups, 'apply-'));
  let directoryExisted = true;
  try {
    await lstat(directory);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error;
    directoryExisted = false;
  }
  const stage = join(recovery, 'stage');
  await mkdir(stage);
  await writeFile(
    join(recovery, 'recovery.json'),
    `${JSON.stringify({ version: 1, rootDir: root, organizationDirectoryExisted: directoryExisted, sidecars: plan.sidecars.map((record, index) => ({ filename: record.filename, previousHash: record.previousHash, previousBytes: previous[index]?.toString('base64') ?? null, proposedHash: sha256(record.proposedBytes) })) }, null, 2)}\n`,
    { flag: 'wx' },
  );
  for (const record of plan.sidecars)
    await writeFile(join(stage, record.filename), record.proposedBytes, {
      flag: 'wx',
    });
  let createdDirectory = false;
  const replaced: number[] = [];
  try {
    await validateEvidence();
    createdDirectory =
      (await mkdir(directory, { recursive: true })) !== undefined;
    for (const [index, record] of plan.sidecars.entries()) {
      await safePath(root, `site/content/organization/${record.filename}`);
      const current = await optionalBytes(paths[index]!);
      if ((current === null ? null : sha256(current)) !== record.previousHash)
        throw new Error(`Organization destination changed: ${record.filename}`);
      await rename(join(stage, record.filename), paths[index]!);
      replaced.push(index);
    }
  } catch (error) {
    const failures: unknown[] = [];
    for (const index of replaced.reverse()) {
      try {
        await safePath(
          root,
          `site/content/organization/${plan.sidecars[index]!.filename}`,
        );
        const current = await optionalBytes(paths[index]!);
        if (
          current === null ||
          !current.equals(Buffer.from(plan.sidecars[index]!.proposedBytes))
        )
          throw new Error(
            `${plan.sidecars[index]!.filename}: destination changed during rollback; preserving current state`,
            { cause: error },
          );
        const bytes = previous[index]!;
        if (bytes === null) await unlink(paths[index]!);
        else {
          const restore = join(
            recovery,
            `restore-${plan.sidecars[index]!.filename}`,
          );
          await writeFile(restore, bytes, { flag: 'wx' });
          await rename(restore, paths[index]!);
        }
      } catch (failure) {
        failures.push(failure);
      }
    }
    if (createdDirectory) {
      try {
        await safePath(root, 'site/content/organization');
        await rmdir(directory);
      } catch (failure) {
        failures.push(failure);
      }
    }
    throw new AggregateError(
      [error, ...failures],
      `Organization apply failed (${error instanceof Error ? error.message : String(error)}); ${failures.length ? 'rollback incomplete' : 'previous sidecars restored'}; recovery evidence: ${recovery}`,
      { cause: error },
    );
  }
  await writeFile(
    join(recovery, 'applied.json'),
    JSON.stringify({
      version: 1,
      files: plan.sidecars.map((record) => record.filename),
    }),
    { flag: 'wx' },
  );
}
