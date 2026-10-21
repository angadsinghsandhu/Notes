import { createHash } from 'node:crypto';
import { posix } from 'node:path';
import { CONTENT_ROOTS } from './schema.js';
import type { OrganizationSnapshot } from './organization-types.js';
import type { ContentEntry, Metadata, SourceEntry, Section } from './types.js';

const naturalOrder = new Intl.Collator('en', {
  numeric: true,
  sensitivity: 'base',
});

export function compareSourcePaths(a: string, b: string): number {
  return naturalOrder.compare(a, b) || (a < b ? -1 : a > b ? 1 : 0);
}

function digest(value: string): string {
  return createHash('sha256').update(value).digest('hex');
}

function segmentSlug(original: string): string {
  const normalized = original.normalize('NFC');
  const slug = normalized
    .toLowerCase()
    .replace(/['’]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
  return slug || `item-${digest(normalized).slice(0, 8)}`;
}

export function createEntry(
  source: SourceEntry,
  metadata: Metadata,
): ContentEntry {
  const sourcePath = source.sourcePath.replaceAll('\\', '/').normalize('NFC');
  const segments = sourcePath.split('/').slice(1);
  const filename = segments.pop() ?? '';
  const groupSegments = [...segments];
  const extension = posix.extname(filename);
  const reader = source.kind === 'markdown' || source.kind === 'notebook';
  if (!(source.kind === 'markdown' && /^readme\.md$/i.test(filename))) {
    // Resources retain their extension in identity: index.html, index.js and
    // index.css are distinct pages even when they share a directory and stem.
    segments.push(
      reader ? filename.slice(0, filename.length - extension.length) : filename,
    );
  }
  const path = metadata.slug ?? segments.map(segmentSlug).join('/');
  const prefix = reader ? '/notes/' : '/resources/';
  const route = `${prefix}${source.section}/${path ? `${path}/` : ''}`;
  return {
    ...metadata,
    id: digest(sourcePath),
    sourcePath,
    section: source.section,
    kind: source.kind,
    bytes: source.bytes,
    groupSegments,
    route,
    headings: [],
  };
}

export function assertUniqueRoutes(
  entries: ContentEntry[],
  additionalPages: readonly { route: string; owner: string }[] = [],
): void {
  const owners = new Map<string, string>();
  const files = new Map<string, string>();
  const directories = new Map<string, string>();
  function claim(route: string, owner: string, endpoint = false): void {
    const key = `${route.replace(/\/+$/, '').toLowerCase()}/`;
    const previous = owners.get(key);
    if (previous !== undefined)
      throw new Error(`Route collision at ${route}: ${previous} and ${owner}`);
    const file = endpoint ? key.slice(0, -1) : `${key}index.html`;
    const fileOwner = files.get(file) ?? directories.get(file);
    if (fileOwner !== undefined)
      throw new Error(`Output collision at ${file}: ${fileOwner} and ${owner}`);
    let directory = posix.dirname(file);
    while (directory !== '/') {
      const directoryOwner = files.get(directory);
      if (directoryOwner !== undefined)
        throw new Error(
          `Output collision at ${directory}: ${directoryOwner} and ${owner} (${route})`,
        );
      directories.set(directory, owner);
      directory = posix.dirname(directory);
    }
    owners.set(key, owner);
    files.set(file, owner);
  }
  for (const route of [
    '/',
    '/library/',
    '/library/tree/',
    '/library/topics/',
    '/library/collections/',
    '/library/paths/',
    '/search/',
    '/404.html',
    '/sitemap.xml',
    '/_headers',
    ...CONTENT_ROOTS.map((root) => `/library/${root.toLowerCase()}/`),
  ])
    claim(route, `reserved website route ${route}`, !route.endsWith('/'));
  for (const page of additionalPages) claim(page.route, page.owner);
  for (const entry of entries) {
    claim(entry.route, entry.sourcePath);
    for (const alias of entry.aliases) {
      const path = alias.replace(/\/+$/, '').toLowerCase();
      const namespace = ['/content-assets', '/pagefind', '/_astro'].find(
        (value) => path === value || path.startsWith(`${value}/`),
      );
      if (namespace)
        throw new Error(
          `${entry.sourcePath}: alias ${alias} shadows reserved website namespace ${namespace}/`,
        );
      claim(alias, entry.sourcePath);
    }
  }
}

/** Escape the escape character too: distinct source names never share a URL. */
export function sourceFolderRoute(
  section: Section,
  segments: readonly string[],
): string {
  const path = segments
    .map((segment) =>
      encodeURIComponent(segment)
        .replace(
          /[!'()*~.]/g,
          (character) =>
            `%${character.charCodeAt(0).toString(16).toUpperCase()}`,
        )
        .replaceAll('%', '~'),
    )
    .join('/');
  return `/library/${section}/${path ? `folders/${path}/` : ''}`;
}

export function publicationPages(
  entries: readonly ContentEntry[],
  organization?: OrganizationSnapshot,
): { route: string; owner: string }[] {
  const folders = new Map<string, string>();
  for (const entry of entries) {
    if (entry.draft) continue;
    entry.groupSegments.forEach((_label, index) => {
      const segments = entry.groupSegments.slice(0, index + 1);
      folders.set(
        sourceFolderRoute(entry.section, segments),
        `folder ${entry.section}/${segments.join('/')}`,
      );
    });
  }
  return [
    ...Array.from(folders, ([route, owner]) => ({ route, owner })),
    ...(organization?.topics.map((topic) => ({
      route: `/library/topics/${topic.id}/`,
      owner: `topic ${topic.id}`,
    })) ?? []),
    ...(organization?.collections.map((collection) => ({
      route: `/library/collections/${collection.id}/`,
      owner: `collection ${collection.id}`,
    })) ?? []),
    ...(organization?.groups.map((group) => ({
      route: `/library/collections/${group.collectionId}/groups/${group.id}/`,
      owner: `group ${group.collectionId}/${group.id}`,
    })) ?? []),
    ...(organization?.paths.map((path) => ({
      route: `/library/paths/${path.id}/`,
      owner: `path ${path.id}`,
    })) ?? []),
  ];
}
