import { posix } from 'node:path';
import { URLSearchParams } from 'node:url';
import { publicationExclusion } from './discover.js';
import { CONTENT_ROOTS } from './schema.js';
import { assertUniqueRoutes } from './identifiers.js';
import type {
  AssetRecord,
  ContentEntry,
  PublicationPolicy,
  RouteCatalog,
} from './types.js';

function allowed(path: string, policy?: PublicationPolicy): boolean {
  const segments = path.split('/');
  return (
    segments.length > 1 &&
    CONTENT_ROOTS.some((root) => root === segments[0]) &&
    !Array.from(path).some(
      (character) =>
        character.charCodeAt(0) < 32 || character.charCodeAt(0) === 127,
    ) &&
    !segments.some((value) => !value || value === '..' || value === '.') &&
    !path.includes('\\') &&
    !publicationExclusion(
      path,
      policy ?? {
        roots: [...CONTENT_ROOTS],
        exclude: [],
        overrides: {},
        repositoryPublic: false,
      },
    ) &&
    (!policy ||
      (policy.roots.includes(segments[0] ?? '') &&
        policy.overrides[path]?.draft !== true))
  );
}

function https(value: string): URL {
  const url = new URL(value);
  if (url.protocol !== 'https:' || url.username || url.password)
    throw new Error('Expected HTTPS URL without credentials');
  return url;
}

export function publicSourceUrl(
  sourcePath: string,
  policy: PublicationPolicy,
  catalog?: RouteCatalog,
): string {
  try {
    if (!allowed(sourcePath, policy)) throw new Error('Excluded source');
    const explicit = policy.overrides[sourcePath]?.resourceUrl;
    if (explicit) {
      const url = https(explicit);
      validateRepositoryTarget(url, policy, catalog);
      return url.href;
    }
    if (
      !policy.repositoryPublic ||
      !policy.repositoryUrl ||
      !policy.revision ||
      !/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/i.test(policy.revision)
    )
      throw new Error(
        'Public repository URL and immutable commit revision are required; supply an explicit HTTPS resourceUrl otherwise',
      );
    const repository = https(policy.repositoryUrl);
    if (
      repository.search ||
      repository.hash ||
      repository.hostname !== 'github.com' ||
      !/^\/[^/]+\/[^/]+\/?$/.test(repository.pathname)
    )
      throw new Error('Expected a GitHub repository URL');
    return `${repository.origin}${repository.pathname.replace(/\/$/, '').replace(/\.git$/, '')}/blob/${policy.revision}/${sourcePath.split('/').map(encodeURIComponent).join('/')}`;
  } catch (error) {
    throw new Error(
      `${sourcePath}: unavailable public source action: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error },
    );
  }
}

export function createRouteCatalog(
  entries: ContentEntry[],
  assets: AssetRecord[],
  policy?: PublicationPolicy,
): RouteCatalog {
  const published = entries.filter(
    (entry) => !entry.draft && allowed(entry.sourcePath, policy),
  );
  assertUniqueRoutes(published);
  const catalog: RouteCatalog = {
    sources: new Map(),
    routes: new Map(),
    assets: new Map(),
    ...(policy ? { policy } : {}),
  };
  for (const entry of published) {
    if (catalog.sources.has(entry.sourcePath))
      throw new Error(`Duplicate source: ${entry.sourcePath}`);
    catalog.sources.set(entry.sourcePath, entry);
    for (const route of [entry.route, ...entry.aliases])
      catalog.routes.set(route, entry);
  }
  for (const asset of assets) {
    if (!allowed(asset.sourcePath, policy)) continue;
    if (catalog.assets.has(asset.sourcePath))
      throw new Error(`Duplicate asset: ${asset.sourcePath}`);
    catalog.assets.set(asset.sourcePath, asset);
  }
  for (const asset of catalog.assets.values()) {
    if (asset.mode === 'external')
      validateRepositoryTarget(https(asset.url), policy, catalog);
  }
  return catalog;
}

function repositoryPath(
  url: URL,
  policy?: PublicationPolicy,
): string | undefined {
  if (!policy?.repositoryUrl) return undefined;
  const repository = https(policy.repositoryUrl);
  const expected = decodeURIComponent(repository.pathname)
    .replace(/\/$/, '')
    .replace(/\.git$/, '')
    .toLowerCase();
  const parts = url.pathname.split('/').filter(Boolean);
  const owner =
    `/${decodeURIComponent(parts[0] ?? '')}/${decodeURIComponent(parts[1] ?? '')}`.toLowerCase();
  if (
    repository.hostname === 'github.com' &&
    url.hostname === 'raw.githubusercontent.com' &&
    owner === expected
  )
    return parts.slice(3).join('/');
  if (url.hostname !== repository.hostname || owner !== expected)
    return undefined;
  if (parts[2] !== 'blob' && parts[2] !== 'tree' && parts[2] !== 'raw')
    throw new Error('Unsupported internal repository URL');
  return parts.slice(4).join('/');
}

function directoryEntry(
  path: string,
  catalog: RouteCatalog,
): ContentEntry | undefined {
  const directory = path.replace(/\/$/, '');
  return [...catalog.sources.values()].find(
    (entry) =>
      posix.dirname(entry.sourcePath) === directory &&
      /^readme\.md$/i.test(posix.basename(entry.sourcePath)),
  );
}

function validateRepositoryTarget(
  url: URL,
  policy?: PublicationPolicy,
  catalog?: RouteCatalog,
): void {
  const repository = repositoryPath(url, policy);
  if (repository === undefined) return;
  const target = posix
    .normalize(decodeURIComponent(repository))
    .replace(/\/$/, '')
    .normalize('NFC');
  if (!allowed(target, policy))
    throw new Error(`Excluded repository target ${target}`);
  if (
    catalog &&
    !catalog.sources.has(target) &&
    !catalog.assets.has(target) &&
    !directoryEntry(target, catalog)
  )
    throw new Error(`Missing or unpublished repository target ${target}`);
}

function externalAssetUrl(
  configured: string,
  query: string,
  fragment: string,
): string {
  if (!query && !fragment) return configured;
  const url = new URL(configured);
  if (query) {
    const incoming = new URLSearchParams(query);
    for (const key of new Set(incoming.keys())) url.searchParams.delete(key);
    for (const [key, value] of incoming) url.searchParams.append(key, value);
  }
  if (fragment) url.hash = fragment.slice(1);
  return url.href;
}

export function resolveLink(
  href: string,
  sourcePath: string,
  catalog: RouteCatalog,
): string {
  try {
    if (
      !href ||
      Array.from(href).some(
        (character) =>
          character.charCodeAt(0) < 32 || character.charCodeAt(0) === 127,
      ) ||
      href !== href.trim() ||
      href.startsWith('//') ||
      href.includes('\\')
    )
      throw new Error('Empty or unsafe URL');
    const wiki = /^\[\[([^\]\r\n[]+)\]\]$/.exec(href)?.[1];
    let target = wiki ? (wiki.split('|')[0] ?? '') : href;
    let repository = false;
    if (/^[a-z][a-z0-9+.-]*:/i.test(target)) {
      const url = new URL(target);
      if (
        !['https:', 'http:', 'mailto:'].includes(url.protocol) ||
        url.username ||
        url.password
      )
        throw new Error('Unsafe URL scheme or credentials');
      if (url.protocol === 'mailto:') return href;
      const path = repositoryPath(url, catalog.policy);
      if (path === undefined) return href;
      target = `${path}${url.search}${url.hash}`;
      repository = true;
    }
    const match = /^([^?#]*)(\?[^#]*)?(#.*)?$/.exec(target);
    const rawPath = match?.[1] ?? '';
    const query = match?.[2] ?? '';
    const fragment = match?.[3] ?? '';
    const path = decodeURIComponent(rawPath).normalize('NFC');
    let entry: ContentEntry | undefined;
    let asset: AssetRecord | undefined;
    let resolvedPath: string;
    if (wiki) {
      const key = path.toLowerCase();
      const candidates = [...catalog.sources.values()].filter(
        (item) =>
          item.sourcePath.toLowerCase() === key ||
          item.title.toLowerCase() === key ||
          posix
            .basename(item.sourcePath, posix.extname(item.sourcePath))
            .toLowerCase() === key,
      );
      if (candidates.length !== 1)
        throw new Error(
          candidates.length
            ? `Ambiguous wiki target ${path}: ${candidates
                .map((item) => item.sourcePath)
                .sort()
                .join(', ')}`
            : `Missing wiki target ${path}`,
        );
      entry = candidates[0];
      resolvedPath = entry?.sourcePath ?? path;
    } else if (
      [...catalog.assets.values()].some(
        (record) => record.mode === 'local' && record.url === path,
      )
    ) {
      asset = [...catalog.assets.values()].find(
        (record) => record.mode === 'local' && record.url === path,
      );
      resolvedPath = asset?.sourcePath ?? path;
    } else if (catalog.routes.has(path)) {
      entry = catalog.routes.get(path);
      resolvedPath = entry?.sourcePath ?? path;
    } else {
      resolvedPath = repository
        ? posix.normalize(path)
        : path
          ? path.startsWith('/')
            ? posix.normalize(path.slice(1))
            : posix.join(posix.dirname(sourcePath), path)
          : sourcePath;
      resolvedPath = resolvedPath.replace(/\/$/, '');
      if (!allowed(resolvedPath, catalog.policy))
        throw new Error(`Excluded or escaping target ${resolvedPath}`);
      entry =
        catalog.sources.get(resolvedPath) ??
        directoryEntry(resolvedPath, catalog);
      asset = catalog.assets.get(resolvedPath);
    }
    if (!entry && !asset)
      throw new Error(`Missing or unpublished target ${resolvedPath}`);
    if (
      fragment &&
      entry &&
      !entry.headings.some(
        (heading) => heading.id === decodeURIComponent(fragment.slice(1)),
      ) &&
      !entry.anchors?.includes(decodeURIComponent(fragment.slice(1)))
    )
      throw new Error(`Missing fragment ${fragment} in ${resolvedPath}`);
    if (asset?.mode === 'external') {
      validateRepositoryTarget(https(asset.url), catalog.policy, catalog);
      return externalAssetUrl(asset.url, query, fragment);
    }
    return `${entry?.route ?? asset?.url}${query}${fragment}`;
  } catch (error) {
    throw new Error(
      `${sourcePath}: cannot resolve ${href}: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error },
    );
  }
}
