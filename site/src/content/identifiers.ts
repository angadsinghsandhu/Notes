import { createHash } from 'node:crypto';
import { posix } from 'node:path';
import type { ContentEntry, Metadata, SourceEntry } from './types.js';

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

export function assertUniqueRoutes(entries: ContentEntry[]): void {
  const owners = new Map<string, string>();
  for (const entry of entries) {
    for (const route of [entry.route, ...entry.aliases]) {
      const key = `${route.replace(/\/+$/, '').toLowerCase()}/`;
      const previous = owners.get(key);
      if (previous !== undefined) {
        throw new Error(
          `Route collision at ${route}: ${previous} and ${entry.sourcePath}`,
        );
      }
      owners.set(key, entry.sourcePath);
    }
  }
}
