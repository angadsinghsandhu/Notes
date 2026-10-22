import { join } from 'node:path';
import {
  readOrganization,
  validateOrganization,
} from './organization-schema.js';
import {
  organizationInventory,
  optionalBytes,
  safePath,
  sha256,
  verifiedRoot,
} from './organization-migrate-inventory.js';
import {
  SIDECARS,
  type OrganizationMigrationPlan,
} from './organization-migrate-types.js';
import type { OrganizationDefinition } from './organization-types.js';

/** Enroll public sources mechanically; classification remains an explicit review. */
export async function planOrganizationMigration(
  rootDir: string,
  value: OrganizationDefinition,
): Promise<OrganizationMigrationPlan> {
  const root = await verifiedRoot(rootDir);
  await safePath(root, 'site/content/organization');
  for (const name of SIDECARS)
    await safePath(root, `site/content/organization/${name}.json`);
  const previous = await readOrganization(
    join(root, 'site/content/organization'),
  );
  const definition = validateOrganization(value);
  const proposed = new Map(
    definition.entries.entries.map((record) => [record.sourcePath, record]),
  );
  for (const record of previous.entries.entries) {
    const replacement = proposed.get(record.sourcePath);
    if (replacement && replacement.uid !== record.uid)
      throw new Error(`${record.sourcePath}: registered UID cannot change`);
    if (!replacement) definition.entries.entries.push(record);
  }
  const discovery = await organizationInventory(root, definition);
  const registered = new Set(
    definition.entries.entries.map((record) => record.sourcePath),
  );
  for (const entry of discovery.publics)
    if (!registered.has(entry.sourcePath)) {
      definition.entries.entries.push({
        uid: `doc-${entry.id}`,
        sourcePath: entry.sourcePath,
        topics: [],
        purpose:
          entry.kind === 'code'
            ? 'project-file'
            : !entry.role && ['markdown', 'notebook'].includes(entry.kind)
              ? 'note'
              : 'reference',
        status: 'unreviewed',
      });
    }
  validateOrganization(definition);
  const evidence = discovery;
  evidence.coverage.registered = definition.entries.entries.length;
  const sidecars: OrganizationMigrationPlan['sidecars'] = [];
  for (const name of SIDECARS) {
    const bytes = await optionalBytes(
      join(root, `site/content/organization/${name}.json`),
    );
    sidecars.push({
      filename: `${name}.json`,
      previousHash: bytes === null ? null : sha256(bytes),
      proposedBytes: `${JSON.stringify(definition[name], null, 2)}\n`,
    });
  }
  return {
    version: 1,
    rootDir: root,
    policyHash: evidence.policyHash,
    inventory: evidence.inventory,
    sidecars,
    coverage: evidence.coverage,
    candidates: evidence.candidates,
  };
}
export { applyOrganizationMigration } from './organization-migrate-apply.js';
export type { OrganizationMigrationPlan } from './organization-migrate-types.js';
