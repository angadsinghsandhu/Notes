import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { lstat, readFile, writeFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';
import {
  applyMigration,
  planMigration,
  createEntry,
  createRouteCatalog,
  readMetadata,
  readPolicy,
  renderMarkdown,
  type Manifest,
  type Section,
} from '../src/content/index.js';

const digest = (text: string) =>
  createHash('sha256').update(text).digest('hex');
async function buildSite(site: string): Promise<string> {
  const result = await promisify(execFile)(
    'npm',
    ['exec', '--', 'astro', 'build'],
    { cwd: site, maxBuffer: 8 * 1024 * 1024 },
  );
  return result.stdout.slice(-1500);
}

/** Apply one inspected metadata-only source at a time; validate/build before the next. */
export async function runMigration(
  siteDir = process.cwd(),
  args: string[] = [],
  build: (site: string) => Promise<string | void> = buildSite,
): Promise<number> {
  if (
    args.length > 1 ||
    (args.length === 1 && !['--dry-run', '--apply'].includes(args[0] ?? ''))
  )
    throw new Error('Migration mode must be --dry-run or --apply');
  const mode = args[0] === '--apply' ? 'apply' : 'dry-run';
  const site = resolve(siteDir);
  const policy = await readPolicy(join(site, 'content/publication.json'));
  const plan = await planMigration(resolve(site, '..'), policy);
  const report = {
    mode,
    changes: plan.changes.map((change) => {
      const row = plan.ledger.find(
        (row) => row.sourcePath === change.sourcePath,
      )!;
      return {
        sourcePath: change.sourcePath,
        originalHash: change.originalHash,
        proposedHash: digest(change.proposedText),
        proposedMetadata: {
          title: JSON.parse(
            /^---\r?\ntitle: (.*?)\r?\n/.exec(change.proposedText)?.[1] ??
              'null',
          ) as string,
        },
        reason: row.reason,
        disposition: row.disposition,
      };
    }),
    classification: {
      supplementalPaths: Object.entries(policy.overrides)
        .filter(([, value]) => value.role === 'supplemental')
        .map(([path]) => path),
      semantics:
        'Supplemental documents retain reader routes, full body search and source access; primary learning-note browse and adjacency exclude them.',
    },
    authorReviews: [
      {
        sourcePath:
          'Courses/Programming with Mosh - Docker Tutorial for Beginners/README.md',
        reason:
          'Docker introduction describes Reinforcement Learning and Stanford CS234; original wording/title preserved for author review.',
      },
      ...['6 Consensus', '7 Threshold Cryptography', '8 Rollups'].map(
        (topic) => ({
          sourcePath: `Classes/Johns Hopkins/Sem 3/Crypto/${topic}/readme.md`,
          reason:
            'Crypto introduction and Bitcoin heading repeat another topic; original wording/title preserved for author review.',
        }),
      ),
    ].filter((record) =>
      plan.ledger.some((row) => row.sourcePath === record.sourcePath),
    ),
    validations: [] as {
      sourcePath: string;
      bodyPreserved: boolean;
      metadataPreserved: boolean;
      renderPreserved: boolean;
      buildPassed: boolean;
      buildExitCode?: number;
      buildSummary?: string;
      failure?: string;
    }[],
    ledger: plan.ledger,
  };
  const save = () =>
    writeFile(
      join(site, 'content/migration-report.json'),
      `${JSON.stringify(report, null, 2)}\n`,
    );
  if (mode === 'apply') {
    const reviewed = JSON.parse(
      await readFile(join(site, 'content/migration-report.json'), 'utf8'),
    ) as { mode: string; changes: unknown };
    if (
      reviewed.mode !== 'dry-run' ||
      JSON.stringify(reviewed.changes) !== JSON.stringify(report.changes)
    )
      throw new Error(
        'Reviewed migration plan changed; rerun and inspect --dry-run before applying',
      );
  }
  await save();
  if (mode === 'dry-run') {
    console.log(
      JSON.stringify({
        mode,
        proposedChanges: report.changes.length,
        originalFiles: plan.ledger.length,
        changes: report.changes,
      }),
    );
    return 0;
  }
  // Validate all hashes before the first source write, including later sources.
  for (const change of plan.changes)
    if (
      digest(await readFile(join(plan.rootDir, change.sourcePath), 'utf8')) !==
      change.originalHash
    )
      throw new Error(
        `${change.sourcePath}: source changed after migration planning`,
      );
  const manifest = JSON.parse(
    await readFile(join(site, '.generated/current/manifest.json'), 'utf8'),
  ) as Manifest;
  const catalog = createRouteCatalog(manifest.entries, manifest.assets, policy);
  for (const change of plan.changes) {
    const absolutePath = join(plan.rootDir, change.sourcePath);
    const source = {
      sourcePath: change.sourcePath,
      absolutePath,
      section: change.sourcePath.split('/')[0]!.toLowerCase() as Section,
      kind: 'markdown' as const,
      bytes: (await lstat(absolutePath)).size,
    };
    const original = await readFile(absolutePath, 'utf8');
    const before = await readMetadata(source, policy);
    const rendered = await renderMarkdown(original, {
      sourcePath: source.sourcePath,
      catalog,
    });
    const record = {
      sourcePath: change.sourcePath,
      bodyPreserved: false,
      metadataPreserved: false,
      renderPreserved: false,
      buildPassed: false,
    } as (typeof report.validations)[number];
    report.validations.push(record);
    try {
      await applyMigration({ ...plan, changes: [change] });
      const changed = await readFile(absolutePath, 'utf8');
      const after = await readMetadata(source, policy);
      const current = await renderMarkdown(changed, {
        sourcePath: source.sourcePath,
        catalog,
      });
      record.bodyPreserved =
        changed.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '') === original;
      record.metadataPreserved =
        JSON.stringify(before) === JSON.stringify(after) &&
        createEntry(source, before).route === createEntry(source, after).route;
      record.renderPreserved =
        current.html === rendered.html &&
        JSON.stringify(current.headings) === JSON.stringify(rendered.headings);
      if (
        !record.bodyPreserved ||
        !record.metadataPreserved ||
        !record.renderPreserved
      )
        throw new Error(
          `${change.sourcePath}: migration body/metadata/render equality failed; further apply stopped`,
        );
      record.buildSummary = (await build(site)) ?? '';
      record.buildPassed = true;
      record.buildExitCode = 0;
    } catch (error) {
      record.failure = error instanceof Error ? error.message : String(error);
      await save();
      console.log(JSON.stringify(record));
      throw error;
    }
    await save();
    console.log(JSON.stringify(record));
  }
  console.log(
    JSON.stringify({
      mode,
      applied: report.validations.length,
      originalFiles: plan.ledger.length,
    }),
  );
  return 0;
}

if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  try {
    process.exitCode = await runMigration(process.cwd(), process.argv.slice(2));
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
