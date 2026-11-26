import { z } from 'zod';

export const SIDECARS = [
  'taxonomy',
  'collections',
  'entries',
  'paths',
] as const;
const hash = z.string().regex(/^[a-f0-9]{64}$/);
const strings = z.array(z.string());
const inventoryRow = z
  .object({
    sourcePath: z.string(),
    sha256: hash.nullable(),
    disposition: z.enum([
      'page',
      'external-resource',
      'supporting-asset',
      'excluded',
      'unsupported',
    ]),
    reason: z.string(),
    destination: z.string().optional(),
    entryId: hash.optional(),
    route: z.string().optional(),
    headings: z.array(
      z
        .object({
          id: z.string(),
          text: z.string(),
          depth: z.number().int().min(1).max(6),
        })
        .strict(),
    ),
    anchors: strings,
  })
  .strict();
export const migrationPlanSchema = z
  .object({
    version: z.literal(1),
    rootDir: z.string(),
    policyHash: hash,
    inventory: z.array(inventoryRow),
    sidecars: z
      .array(
        z
          .object({
            filename: z.enum([
              'taxonomy.json',
              'collections.json',
              'entries.json',
              'paths.json',
            ]),
            previousHash: hash.nullable(),
            proposedBytes: z.string(),
          })
          .strict(),
      )
      .length(4),
    coverage: z
      .object({
        publicEntries: z.number().int().nonnegative(),
        registered: z.number().int().nonnegative(),
        reviewed: z.number().int().nonnegative(),
        unclassified: z.number().int().nonnegative(),
      })
      .strict(),
    candidates: z
      .object({
        duplicates: z.array(strings),
        outlines: strings,
        unclassified: strings,
      })
      .strict(),
  })
  .strict();
export type OrganizationMigrationPlan = z.infer<typeof migrationPlanSchema>;
