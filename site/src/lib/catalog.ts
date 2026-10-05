import { lstat, readFile } from 'node:fs/promises';
import { basename, dirname, join, resolve } from 'node:path';
import { compareSourcePaths } from '../content/identifiers.js';
import type {
  ContentEntry,
  ContentKind,
  Manifest,
  Section,
} from '../content/index.js';

export type Catalog = {
  getEntry(route: string): ContentEntry | undefined;
  listEntries(filters?: {
    section?: Section;
    kind?: ContentKind;
  }): ContentEntry[];
  getAdjacentNotes(id: string): {
    previous?: ContentEntry;
    next?: ContentEntry;
  };
};

/** The internal ledger/assets never become page props. Select public fields explicitly. */
function publicEntry(entry: ContentEntry): ContentEntry {
  const {
    id,
    title,
    description,
    tags,
    draft,
    slug,
    order,
    updated,
    aliases,
    sourcePath,
    section,
    kind,
    bytes,
    groupSegments,
    route,
    headings,
    anchors,
    bodyFile,
    assetUrl,
    sourceUrl,
  } = entry;
  if (
    sourcePath.startsWith('/') ||
    sourcePath.includes('\\') ||
    bodyFile?.startsWith('/') ||
    bodyFile?.split('/').includes('..')
  )
    throw new Error('Catalog entries must contain repository-relative paths');
  return {
    id,
    title,
    description,
    tags: [...tags],
    draft,
    aliases: [...aliases],
    sourcePath,
    section,
    kind,
    bytes,
    groupSegments: [...groupSegments],
    route,
    headings: headings.map((heading) => ({ ...heading })),
    ...(slug !== undefined ? { slug } : {}),
    ...(order !== undefined ? { order } : {}),
    ...(updated !== undefined ? { updated } : {}),
    ...(anchors ? { anchors: [...anchors] } : {}),
    ...(bodyFile ? { bodyFile } : {}),
    ...(assetUrl ? { assetUrl } : {}),
    ...(sourceUrl ? { sourceUrl } : {}),
  };
}

export function loadCatalog(manifest: Manifest): Catalog {
  const entries = manifest.entries
    .filter((entry) => !entry.draft)
    .map(publicEntry)
    .sort(
      (a, b) =>
        compareSourcePaths(a.section, b.section) ||
        compareSourcePaths(
          a.groupSegments.join('/'),
          b.groupSegments.join('/'),
        ) ||
        (a.order ?? Infinity) - (b.order ?? Infinity) ||
        compareSourcePaths(a.sourcePath, b.sourcePath),
    );
  const routes = new Map<string, ContentEntry>();
  for (const entry of entries)
    for (const route of [entry.route, ...entry.aliases])
      routes.set(route, entry);
  return {
    getEntry: (route) => {
      const entry = routes.get(route);
      return entry ? publicEntry(entry) : undefined;
    },
    listEntries: (filters = {}) =>
      entries
        .filter(
          (entry) =>
            (!filters.section || entry.section === filters.section) &&
            (!filters.kind || entry.kind === filters.kind),
        )
        .map(publicEntry),
    getAdjacentNotes: (id) => {
      const entry = entries.find((item) => item.id === id);
      if (!entry || !['markdown', 'notebook'].includes(entry.kind)) return {};
      const notes = entries.filter(
        (item) =>
          item.section === entry.section &&
          item.groupSegments.join('/') === entry.groupSegments.join('/') &&
          ['markdown', 'notebook'].includes(item.kind),
      );
      const index = notes.findIndex((item) => item.id === id);
      const previous = notes[index - 1];
      const next = notes[index + 1];
      return {
        ...(previous ? { previous: publicEntry(previous) } : {}),
        ...(next ? { next: publicEntry(next) } : {}),
      };
    },
  };
}

async function snapshotPath(snapshotDir: string): Promise<string> {
  const snapshot = resolve(snapshotDir);
  const generated = dirname(snapshot);
  if (
    basename(snapshot) !== 'current' ||
    basename(generated) !== '.generated' ||
    basename(dirname(generated)) !== 'site'
  )
    throw new Error('Catalog reads require a site/.generated/current snapshot');
  for (const path of [dirname(generated), generated, snapshot]) {
    const stat = await lstat(path);
    if (stat.isSymbolicLink() || !stat.isDirectory())
      throw new Error(
        'Unsafe symbolic link or non-directory generated snapshot',
      );
  }
  return snapshot;
}

/** Server-side facade: pages never import the internal manifest or scan the archive. */
export async function readPreparedCatalog(
  snapshotDir = resolve('.generated/current'),
): Promise<Catalog> {
  const snapshot = await snapshotPath(snapshotDir);
  const file = join(snapshot, 'manifest.json');
  const stat = await lstat(file);
  if (!stat.isFile() || stat.isSymbolicLink())
    throw new Error('Unsafe generated manifest');
  return loadCatalog(JSON.parse(await readFile(file, 'utf8')) as Manifest);
}

export async function readPreparedBody(
  entry: ContentEntry,
  snapshotDir = resolve('.generated/current'),
): Promise<string> {
  if (entry.draft) throw new Error('Draft bodies are unavailable');
  if (!entry.bodyFile) return '';
  if (
    !/^[a-f0-9]{64}$/.test(entry.id) ||
    entry.bodyFile !== `bodies/${entry.id}.html`
  )
    throw new Error('Invalid generated body path');
  const snapshot = await snapshotPath(snapshotDir);
  const directory = join(snapshot, 'bodies');
  const stat = await lstat(directory);
  if (!stat.isDirectory() || stat.isSymbolicLink())
    throw new Error('Unsafe symbolic link body directory');
  const file = join(snapshot, entry.bodyFile);
  const body = await lstat(file);
  if (!body.isFile() || body.isSymbolicLink())
    throw new Error('Unsafe symbolic link body file');
  return readFile(file, 'utf8');
}
