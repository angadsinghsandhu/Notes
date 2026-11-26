import { createHash } from 'node:crypto';
import { lstat, readFile, readdir, realpath } from 'node:fs/promises';
import { isAbsolute, join, resolve } from 'node:path';
import { discoverEntries } from './discover.js';
import {
  collectExplicitAnchors,
  collectHeadings,
  createHeadingSlugger,
  parseMarkdown,
} from './headings.js';
import {
  assertUniqueRoutes,
  createEntry,
  publicationPages,
} from './identifiers.js';
import { resolveOrganization } from './organization.js';
import { readMetadata, readPolicy } from './schema.js';
import type { ContentEntry } from './types.js';
import type { OrganizationDefinition } from './organization-types.js';
import type { OrganizationMigrationPlan } from './organization-migrate-types.js';

export const sha256 = (bytes: string | Uint8Array): string =>
  createHash('sha256').update(bytes).digest('hex');

/** Inspect every existing path component, including parents of an absent target. */
export async function safePath(root: string, path: string): Promise<string> {
  const parts = path.split('/');
  if (
    isAbsolute(path) ||
    parts.some(
      (part) => !part || part === '.' || part === '..' || part.includes('\\'),
    )
  )
    throw new Error(`Unsafe organization path: ${path}`);
  let target = root;
  for (const [index, part] of parts.entries()) {
    target = join(target, part);
    try {
      const info = await lstat(target);
      if (
        info.isSymbolicLink() ||
        (index < parts.length - 1
          ? !info.isDirectory()
          : !info.isDirectory() && !info.isFile())
      )
        throw new Error(
          `Unsafe organization path: ${path}; expected regular paths without symlinks`,
        );
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error;
    }
  }
  return target;
}
export async function verifiedRoot(rootDir: string): Promise<string> {
  const root = await realpath(rootDir);
  if (root !== resolve(rootDir))
    throw new Error('Organization root must be canonical without symlinks');
  await safePath(root, 'site/content/publication.json');
  return root;
}
export async function optionalBytes(path: string): Promise<Buffer | null> {
  try {
    return await readFile(path);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error;
    return null;
  }
}
function markdownCells(text: string): string[] {
  const json: unknown = JSON.parse(text);
  if (
    !json ||
    typeof json !== 'object' ||
    !('cells' in json) ||
    !Array.isArray(json.cells)
  )
    throw new Error('Invalid notebook cells');
  return json.cells.flatMap((cell: unknown, index: number) => {
    if (
      !cell ||
      typeof cell !== 'object' ||
      !('cell_type' in cell) ||
      cell.cell_type !== 'markdown'
    )
      return [];
    if (
      !('source' in cell) ||
      !(
        typeof cell.source === 'string' ||
        (Array.isArray(cell.source) &&
          cell.source.every((line: unknown) => typeof line === 'string'))
      )
    )
      throw new Error(`Invalid notebook Markdown source at cell ${index}`);
    return [
      typeof cell.source === 'string' ? cell.source : cell.source.join(''),
    ];
  });
}

/** Fresh archive evidence; no renderer, generated manifest, or program execution. */
export async function organizationInventory(
  root: string,
  definition: OrganizationDefinition,
) {
  const policyPath = await safePath(root, 'site/content/publication.json');
  const policyHash = sha256(await readFile(policyPath));
  const policy = await readPolicy(policyPath);
  const { sources, ledger } = await discoverEntries(root, policy);
  const entries: ContentEntry[] = [];
  const bodies = new Map<string, string[]>();
  const records = new Map(
    definition.entries.entries.map((record) => [record.sourcePath, record]),
  );
  for (const source of sources) {
    const entry = createEntry(source, await readMetadata(source, policy));
    const organizationalDraft =
      records.get(source.sourcePath)?.status === 'draft';
    const text =
      !organizationalDraft && ['markdown', 'notebook'].includes(source.kind)
        ? await readFile(source.absolutePath, 'utf8')
        : '';
    const markdown = organizationalDraft
      ? []
      : source.kind === 'markdown'
        ? [text]
        : source.kind === 'notebook'
          ? markdownCells(text)
          : [];
    const slugger = createHeadingSlugger();
    entry.headings = markdown.flatMap((cell) => collectHeadings(cell, slugger));
    entry.anchors = [...new Set(markdown.flatMap(collectExplicitAnchors))];
    bodies.set(source.sourcePath, markdown);
    entries.push(entry);
    if (organizationalDraft) {
      entry.draft = true;
      const row = ledger.find((row) => row.sourcePath === source.sourcePath)!;
      row.disposition = 'excluded';
      row.reason = 'Excluded organizational draft content';
      delete row.destination;
    }
  }
  // Match preparation: excluded existing records survive in storage, missing records remain errors.
  const excluded = new Set(
    ledger
      .filter((row) => row.disposition === 'excluded')
      .map((row) => row.sourcePath),
  );
  const snapshot = resolveOrganization(entries, {
    ...definition,
    entries: {
      version: 1,
      entries: definition.entries.entries.filter(
        (record) =>
          !excluded.has(record.sourcePath) ||
          entries.some((entry) => entry.sourcePath === record.sourcePath),
      ),
    },
  });
  const publics = entries.filter((entry) => !entry.draft);
  assertUniqueRoutes(publics, publicationPages(publics, snapshot));
  const indexed = new Map(entries.map((entry) => [entry.sourcePath, entry]));
  const inventory: OrganizationMigrationPlan['inventory'] = [];
  const directories = new Map<string, string[]>();
  const physical = new Map(
    sources.map((source) => [source.sourcePath, source.absolutePath]),
  );
  async function actualPath(sourcePath: string): Promise<string> {
    const known = physical.get(sourcePath);
    if (known) return known;
    let path = root;
    for (const segment of sourcePath.split('/')) {
      let names = directories.get(path);
      if (!names) {
        names = await readdir(path);
        directories.set(path, names);
      }
      const matches = names.filter((name) => name.normalize('NFC') === segment);
      if (matches.length !== 1)
        throw new Error(`Ambiguous or missing source path: ${sourcePath}`);
      path = join(path, matches[0]!);
    }
    return path;
  }
  for (const row of ledger) {
    const entry = indexed.get(row.sourcePath);
    // Symlinks and non-regular exclusions have no readable source bytes.
    const path = await actualPath(row.sourcePath);
    const info = await lstat(path);
    inventory.push({
      ...row,
      sha256: info.isFile() ? sha256(await readFile(path)) : null,
      ...(entry ? { entryId: entry.id, route: entry.route } : {}),
      headings: entry?.headings ?? [],
      anchors: entry?.anchors ?? [],
    });
  }
  const unclassified = publics
    .filter(
      (entry) =>
        !records.get(entry.sourcePath)?.topics.length &&
        !records.get(entry.sourcePath)?.collectionId,
    )
    .map((entry) => entry.sourcePath);
  const duplicates = new Map<string, string[]>();
  const outlines: string[] = [];
  for (const entry of publics) {
    const digest = inventory.find(
      (row) => row.sourcePath === entry.sourcePath,
    )!.sha256!;
    const group = duplicates.get(digest) ?? [];
    group.push(entry.sourcePath);
    duplicates.set(digest, group);
    const markdown = bodies.get(entry.sourcePath)!;
    if (
      markdown.length &&
      markdown.every((cell) =>
        parseMarkdown(cell).children.every(
          (node) => node.type === 'heading' || node.type === 'thematicBreak',
        ),
      )
    )
      outlines.push(entry.sourcePath);
  }
  return {
    policyHash,
    inventory,
    publics,
    snapshot,
    coverage: {
      publicEntries: publics.length,
      registered: definition.entries.entries.length,
      reviewed: snapshot.memberships.filter(
        (member) => member.status === 'reviewed',
      ).length,
      unclassified: unclassified.length,
    },
    candidates: {
      duplicates: [...duplicates.values()].filter((group) => group.length > 1),
      outlines,
      unclassified,
    },
  };
}
