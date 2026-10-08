import { createHash } from 'node:crypto';
import { constants } from 'node:fs';
import { lstat, open, readFile, realpath } from 'node:fs/promises';
import { join } from 'node:path';
import { discoverEntries } from './discover.js';
import { readMetadata, CONTENT_ROOTS } from './schema.js';
import type { MigrationRow, PublicationPolicy } from './types.js';

export type MigrationPlan = {
  rootDir: string;
  changes: { sourcePath: string; originalHash: string; proposedText: string }[];
  ledger: MigrationRow[];
};
const hash = (text: string) => createHash('sha256').update(text).digest('hex');

/** Planning reads the complete inventory, never mutates source or generated output. */
export async function planMigration(
  rootDir: string,
  policy: PublicationPolicy,
): Promise<MigrationPlan> {
  const root = await realpath(rootDir);
  const { sources, ledger } = await discoverEntries(root, policy);
  const changes: MigrationPlan['changes'] = [];
  for (const source of sources) {
    if (source.kind !== 'markdown') continue;
    const text = await readFile(source.absolutePath, 'utf8');
    const metadata = await readMetadata(source, policy);
    const row = ledger.find((item) => item.sourcePath === source.sourcePath)!;
    if (metadata.role === 'supplemental') {
      row.reason =
        'Publish supplemental document using policy metadata; source preserved';
      continue;
    }
    if (
      /^\uFEFF?---[ \t]*(?:\r?\n|$)/.test(text) ||
      /^---[ \t]*(?:\r?\n|$)/.test(text)
    ) {
      row.reason =
        'Publish authored Markdown with existing metadata; source preserved';
      continue;
    }
    const newline = text.includes('\r\n') ? '\r\n' : '\n';
    changes.push({
      sourcePath: source.sourcePath,
      originalHash: hash(text),
      proposedText: `---${newline}title: ${JSON.stringify(metadata.title)}${newline}---${newline}${text}`,
    });
    row.reason = text.length
      ? 'Add authored title metadata; original body preserved'
      : 'Add placeholder title metadata; original empty body preserved';
  }
  return { rootDir: root, changes, ledger };
}

async function openSource(plan: MigrationPlan, sourcePath: string) {
  const parts = sourcePath.split('/');
  if (
    !CONTENT_ROOTS.some((root) => root === parts[0]) ||
    parts.length < 2 ||
    parts.some((part) => !part || part === '.' || part === '..') ||
    sourcePath.includes('\\')
  )
    throw new Error(`Unsafe migration source path: ${sourcePath}`);
  let path = await realpath(plan.rootDir);
  for (const [index, part] of parts.entries()) {
    path = join(path, part);
    const stat = await lstat(path);
    if (
      stat.isSymbolicLink() ||
      (index === parts.length - 1 ? !stat.isFile() : !stat.isDirectory())
    )
      throw new Error(
        `${sourcePath}: migration requires regular source paths without symbolic links`,
      );
  }
  return open(path, constants.O_RDWR | constants.O_NOFOLLOW);
}

/** Preflight every hash before any write, then recheck on the actual opened file. */
export async function applyMigration(plan: MigrationPlan): Promise<void> {
  if (
    new Set(plan.changes.map((change) => change.sourcePath)).size !==
    plan.changes.length
  )
    throw new Error('Duplicate migration source path');
  for (const change of plan.changes) {
    const file = await openSource(plan, change.sourcePath);
    try {
      if (hash(await file.readFile('utf8')) !== change.originalHash)
        throw new Error(
          `${change.sourcePath}: source changed after migration planning`,
        );
    } finally {
      await file.close();
    }
  }
  for (const change of plan.changes) {
    const file = await openSource(plan, change.sourcePath);
    try {
      if (hash(await file.readFile('utf8')) !== change.originalHash)
        throw new Error(
          `${change.sourcePath}: source changed after migration planning`,
        );
      await file.write(change.proposedText, 0, 'utf8');
      await file.truncate(Buffer.byteLength(change.proposedText));
    } finally {
      await file.close();
    }
  }
}
