import { readFile, realpath } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  applyOrganizationMigration,
  planOrganizationMigration,
  readOrganization,
  type OrganizationMigrationPlan,
} from '../src/content/index.js';

/** The executable supplies its own site directory, never a plan-selected root. */
export async function runOrganization(
  siteDir: string,
  args: string[] = [],
): Promise<number> {
  const dryRun =
    args.length === 0 || (args.length === 1 && args[0] === '--dry-run');
  if (
    !dryRun &&
    !(
      args.length === 2 &&
      args[0] === '--apply' &&
      args[1] &&
      !args[1].startsWith('--')
    )
  )
    throw new Error(
      'Usage: content:organize [--dry-run | --apply <reviewed-plan.json>]',
    );
  const root = await realpath(resolve(siteDir, '..'));
  if (dryRun) {
    const definition = await readOrganization(
      join(root, 'site/content/organization'),
    );
    console.log(
      JSON.stringify(
        await planOrganizationMigration(root, definition),
        null,
        2,
      ),
    );
  } else {
    const plan: unknown = JSON.parse(
      await readFile(resolve(siteDir, args[1]!), 'utf8'),
    );
    if (
      !plan ||
      typeof plan !== 'object' ||
      !('rootDir' in plan) ||
      plan.rootDir !== root
    )
      throw new Error(
        'Reviewed organization plan root must match this worktree root',
      );
    await applyOrganizationMigration(plan as OrganizationMigrationPlan);
  }
  return 0;
}
if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  try {
    process.exitCode = await runOrganization(
      fileURLToPath(new URL('..', import.meta.url)),
      process.argv.slice(2),
    );
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
