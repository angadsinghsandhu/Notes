import { constants } from 'node:fs';
import { open } from 'node:fs/promises';
import { join, posix } from 'node:path';
import { z } from 'zod';
import { problem, sha256 } from './schema.js';
import type { ProblemId, ProblemRecord } from './types.js';

const archivePrefix = 'Interview/leetcode/Solutions/';
const filenameNumber = z.number().int().nonnegative();
const sourcePath = z.string().refine(
  (path) =>
    path.startsWith(archivePrefix) &&
    path === path.normalize('NFC') &&
    !path.includes('\\') &&
    Array.from(path).every((character) => {
      const code = character.charCodeAt(0);
      return code >= 32 && code !== 127;
    }) &&
    path
      .split('/')
      .every((part) => part !== '' && part !== '.' && part !== '..'),
  'Expected a normalized repository-relative LeetCode archive path',
);
const canonicalUrl = problem.shape.officialUrl.unwrap();
const articleIndexUrl =
  /^https:\/\/leetcode\.com\/articles\/\?page=[1-9]\d*(?:&tag=[a-z0-9]+(?:-[a-z0-9]+)*)?$/;
const descriptionUrl =
  /^https:\/\/leetcode\.com\/problems\/[a-z0-9]+(?:-[a-z0-9]+)*\/description\/$/;
const sourceRecord = z.strictObject({
  sourcePath,
  sha256,
  filenameNumber: filenameNumber.nullable(),
  duplicateFilenameNumber: filenameNumber.optional(),
  disposition: z.enum([
    'solver_variant',
    'statement_only',
    'link_only',
    'practice',
    'pending_reconciliation',
    'out_of_range',
    'archive_support',
    'empty',
  ]),
  reason: z.string().trim().min(1),
  problemId: problem.shape.id.optional(),
  officialSource: z
    .strictObject({
      url: z.string(),
      checkedAt: z.iso.datetime({ precision: 0 }),
    })
    .optional(),
});
const sourceMap = z.strictObject({
  version: z.literal(1),
  records: z.array(sourceRecord),
});

type SolverSource = {
  sha256: string;
  problemId: ProblemId;
  officialUrl: string;
};

export async function readSourceMap(
  root: string,
): Promise<ReadonlyMap<string, SolverSource> | undefined> {
  const filename = join(root, 'source-map.json');
  try {
    const file = await open(
      filename,
      constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK,
    ).catch((error: unknown) => {
      if (error instanceof Error && 'code' in error && error.code === 'ENOENT')
        return undefined;
      throw error;
    });
    if (!file) return undefined;
    let text: string;
    try {
      if (!(await file.stat()).isFile())
        throw new Error('Expected a regular file');
      text = await file.readFile('utf8');
    } finally {
      await file.close();
    }
    const { records } = sourceMap.parse(JSON.parse(text));
    const seen = new Set<string>();
    const solvers = new Map<string, SolverSource>();
    for (const record of records) {
      const {
        sourcePath: path,
        problemId,
        officialSource,
        disposition,
      } = record;
      if (seen.has(path)) throw new Error(`Duplicate source path ${path}`);
      seen.add(path);
      const prefix = /^(\d+)[ _.-]/.exec(posix.basename(path));
      if (
        record.filenameNumber !== (prefix ? Number(prefix[1]) : null) ||
        (record.duplicateFilenameNumber !== undefined &&
          record.duplicateFilenameNumber !== record.filenameNumber)
      )
        throw new Error(`${path}: inconsistent filename number`);

      if (problemId && officialSource) {
        const { url } = officialSource;
        const canonical = canonicalUrl.safeParse(url).success;
        if (disposition === 'solver_variant') {
          if (!canonical)
            throw new Error(`${path}: solver requires a canonical problem URL`);
          solvers.set(path, {
            sha256: record.sha256,
            problemId,
            officialUrl: url,
          });
        } else if (
          !canonical &&
          !descriptionUrl.test(url) &&
          !articleIndexUrl.test(url)
        ) {
          throw new Error(`${path}: invalid official source URL`);
        }
      } else if (
        problemId ||
        officialSource ||
        disposition === 'solver_variant'
      ) {
        throw new Error(
          `${path}: expected both problem ID and official source evidence`,
        );
      }
    }
    return solvers;
  } catch (error) {
    throw new Error(`${filename}: invalid source map: ${String(error)}`, {
      cause: error,
    });
  }
}

export function resolveSourceVariants(
  solvers: ReadonlyMap<string, SolverSource>,
  problems: readonly ProblemRecord[],
  sourceDigests: ReadonlyMap<string, string>,
): ReadonlyMap<string, ProblemId> {
  const officialUrls = new Map(
    problems.map(({ id, officialUrl }) => [id, officialUrl]),
  );
  const variants = new Map<string, ProblemId>();
  for (const [path, { sha256, problemId, officialUrl }] of solvers) {
    if (officialUrls.get(problemId) !== officialUrl)
      throw new Error(
        `source-map.json: ${path} disagrees with official curriculum problem ${problemId}`,
      );
    const actual = sourceDigests.get(path);
    if (actual === undefined) continue;
    if (actual !== sha256)
      throw new Error(`source-map.json: SHA-256 mismatch for ${path}`);
    variants.set(path, problemId);
  }
  return variants;
}
