import { execFile } from 'node:child_process';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';
import {
  prepareContent,
  readPolicy,
  type PrepareOptions,
} from '../src/content/index.js';

export async function contentOptions(
  siteDir = process.cwd(),
): Promise<PrepareOptions> {
  const rootDir = resolve(siteDir, '..');
  const policyPath = join(siteDir, 'content/publication.json');
  const policy = await readPolicy(policyPath);
  const revision =
    process.env.SOURCE_REVISION ??
    policy.revision ??
    (
      await promisify(execFile)('git', ['rev-parse', 'HEAD'], { cwd: rootDir })
    ).stdout.trim();
  if (!/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/i.test(revision))
    throw new Error('Source revision must be an immutable commit hash');
  return {
    rootDir,
    outputDir: join(siteDir, '.generated'),
    policyPath,
    hosted: process.env.HOSTED === 'true',
    revision,
  };
}

export async function runContent(options: PrepareOptions): Promise<number> {
  const result = await prepareContent(options);
  if (result.diagnostics.length) {
    for (const diagnostic of result.diagnostics)
      console.error(`${diagnostic.sourcePath}: ${diagnostic.message}`);
    return 1;
  }
  console.log(
    `Prepared ${result.manifest.entries.length} entries, ${result.manifest.assets.length} assets; ${result.manifest.ledger.length} original files accounted for.`,
  );
  return 0;
}

if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  try {
    process.exitCode = await runContent(await contentOptions());
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
