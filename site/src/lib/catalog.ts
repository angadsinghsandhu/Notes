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

const preparedBodies = new WeakMap<
  ContentEntry,
  { snapshot: string; id: string; bodyFile: string; html: string }
>();

export function loadCatalog(manifest: Manifest): Catalog {
  return createCatalog(manifest);
}

function createCatalog(manifest: Manifest, select = publicEntry): Catalog {
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
      return entry ? select(entry) : undefined;
    },
    listEntries: (filters = {}) =>
      entries
        .filter(
          (entry) =>
            (!filters.section || entry.section === filters.section) &&
            (!filters.kind || entry.kind === filters.kind),
        )
        .map(select),
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
        ...(previous ? { previous: select(previous) } : {}),
        ...(next ? { next: select(next) } : {}),
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
  const manifest = JSON.parse(await readFile(file, 'utf8')) as Manifest & {
    preparedBodies?: Record<string, string>;
  };
  const bodies = new Map<string, string>();
  for (const entry of manifest.entries) {
    if (entry.draft || !entry.bodyFile) continue;
    assertBodyPath(entry);
    const html = manifest.preparedBodies
      ? manifest.preparedBodies[entry.bodyFile]
      : await readPreparedBody(entry, snapshot);
    if (typeof html !== 'string') throw new Error('Missing generated body');
    bodies.set(entry.bodyFile, html);
  }
  return createCatalog(manifest, (entry) => {
    const selected = publicEntry(entry);
    if (selected.bodyFile)
      preparedBodies.set(selected, {
        snapshot,
        id: selected.id,
        bodyFile: selected.bodyFile,
        html: bodies.get(selected.bodyFile)!,
      });
    return selected;
  });
}

function assertBodyPath(entry: ContentEntry): void {
  if (
    !/^[a-f0-9]{64}$/.test(entry.id) ||
    entry.bodyFile !== `bodies/${entry.id}.html`
  )
    throw new Error('Invalid generated body path');
}

/** Keep the selected entry object: its body stays bound to the catalog read that selected it. */
export async function readPreparedBody(
  entry: ContentEntry,
  snapshotDir = resolve('.generated/current'),
): Promise<string> {
  if (entry.draft) throw new Error('Draft bodies are unavailable');
  if (!entry.bodyFile) return '';
  assertBodyPath(entry);
  const bound = preparedBodies.get(entry);
  if (bound) {
    if (
      bound.snapshot !== resolve(snapshotDir) ||
      bound.id !== entry.id ||
      bound.bodyFile !== entry.bodyFile
    )
      throw new Error('Selected body does not belong to this catalog snapshot');
    return bound.html;
  }
  const snapshot = await snapshotPath(snapshotDir);
  const manifestFile = join(snapshot, 'manifest.json');
  const manifestStat = await lstat(manifestFile);
  if (!manifestStat.isFile() || manifestStat.isSymbolicLink())
    throw new Error('Unsafe generated manifest');
  const manifest = JSON.parse(
    await readFile(manifestFile, 'utf8'),
  ) as Manifest & { preparedBodies?: Record<string, string> };
  if (manifest.preparedBodies) {
    const published = manifest.entries.find(
      (item) =>
        item.id === entry.id && !item.draft && item.bodyFile === entry.bodyFile,
    );
    const html = published && manifest.preparedBodies[entry.bodyFile];
    if (typeof html !== 'string')
      throw new Error(
        'Body is unavailable in the current snapshot; retain the catalog-selected entry',
      );
    return html;
  }
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
