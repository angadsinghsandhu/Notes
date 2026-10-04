import { lstat, readdir, realpath } from 'node:fs/promises';
import {
  extname,
  isAbsolute,
  join,
  matchesGlob,
  relative,
  sep,
} from 'node:path';
import { compareSourcePaths, createEntry } from './identifiers.js';
import { CONTENT_ROOTS, readMetadata } from './schema.js';
import type {
  ContentKind,
  MigrationRow,
  PublicationPolicy,
  Section,
  SourceEntry,
} from './types.js';

const SUPPORTED_EXTENSIONS: Readonly<Record<string, ContentKind>> = {
  '.md': 'markdown',
  '.ipynb': 'notebook',
  '.py': 'code',
  '.js': 'code',
  '.jsx': 'code',
  '.ts': 'code',
  '.tsx': 'code',
  '.css': 'code',
  '.html': 'code',
  '.java': 'code',
  '.kt': 'code',
  '.cpp': 'code',
  '.pdf': 'pdf',
  '.ppt': 'slides',
  '.pptx': 'slides',
};
const SUPPORTING_EXTENSIONS = new Set([
  '.png',
  '.jpg',
  '.jpeg',
  '.gif',
  '.webp',
  '.avif',
  '.svg',
  '.ico',
]);
const EXCLUDED_DIRECTORIES = new Set([
  '.git',
  '.kiro',
  'node_modules',
  '__pycache__',
  '.cache',
  '.pytest_cache',
  '.mypy_cache',
  '.ruff_cache',
  '.ipynb_checkpoints',
  '.venv',
  'venv',
  'env',
  'dist',
  'build',
  '.next',
  '.astro',
  '.generated',
  'coverage',
  '.tox',
  '.DS_Store',
]);
const EXCLUDED_ARCHIVES = new Set([
  '.zip',
  '.tar',
  '.gz',
  '.bz2',
  '.xz',
  '.7z',
  '.rar',
]);

function exclusion(
  sourcePath: string,
  policy: PublicationPolicy,
): string | undefined {
  const segments = sourcePath.split('/');
  if (segments.some((segment) => EXCLUDED_DIRECTORIES.has(segment)))
    return 'Excluded dependency, cache, build, or internal path';
  const filename = segments.at(-1) ?? '';
  if (
    /^(?:\.env(?:\..*)?|env\.json|credentials?(?:[._-].*)?|secrets?(?:[._-].*)?|\.ds_store)$/i.test(
      filename,
    )
  )
    return 'Excluded environment or credential file';
  if (EXCLUDED_ARCHIVES.has(extname(filename).toLowerCase()))
    return 'Excluded binary archive';
  const pattern = policy.exclude.find((glob) => matchesGlob(sourcePath, glob));
  return pattern ? `Excluded by publication policy: ${pattern}` : undefined;
}

function contained(root: string, target: string): boolean {
  const path = relative(root, target);
  return (
    path === '' ||
    (!isAbsolute(path) && path !== '..' && !path.startsWith(`..${sep}`))
  );
}

export async function discoverEntries(
  rootDir: string,
  policy: PublicationPolicy,
): Promise<{ sources: SourceEntry[]; ledger: MigrationRow[] }> {
  const root = await realpath(rootDir);
  const sources: SourceEntry[] = [];
  const ledger: MigrationRow[] = [];

  async function visit(
    absolutePath: string,
    sourcePath: string,
    section: Section,
    allowedRoot: string,
    inheritedExclusion?: string,
  ): Promise<void> {
    const stat = await lstat(absolutePath);
    const reason = inheritedExclusion ?? exclusion(sourcePath, policy);
    if (stat.isSymbolicLink()) {
      // Never follow links, including links to excluded in-root content.
      ledger.push({
        sourcePath,
        disposition: 'excluded',
        reason: 'Excluded symbolic link; targets are never traversed',
      });
      return;
    }
    if (!contained(allowedRoot, await realpath(absolutePath))) {
      ledger.push({
        sourcePath,
        disposition: 'excluded',
        reason: 'Source escapes the allowed content root',
      });
      return;
    }
    if (stat.isDirectory()) {
      for (const name of (await readdir(absolutePath)).sort(
        compareSourcePaths,
      )) {
        await visit(
          join(absolutePath, name),
          `${sourcePath}/${name.normalize('NFC')}`,
          section,
          allowedRoot,
          reason,
        );
      }
      return;
    }
    if (!stat.isFile()) {
      ledger.push({
        sourcePath,
        disposition: 'excluded',
        reason: 'Excluded non-regular filesystem entry',
      });
      return;
    }
    if (reason) {
      ledger.push({ sourcePath, disposition: 'excluded', reason });
      return;
    }
    const extension = extname(sourcePath).toLowerCase();
    if (SUPPORTING_EXTENSIONS.has(extension)) {
      const override = policy.overrides[sourcePath];
      ledger.push({
        sourcePath,
        disposition: override?.draft === true ? 'excluded' : 'supporting-asset',
        reason:
          override?.draft === true
            ? 'Excluded draft asset'
            : 'Eligible image; copy only when referenced',
      });
      return;
    }
    const kind = SUPPORTED_EXTENSIONS[extension];
    if (!kind) {
      ledger.push({
        sourcePath,
        disposition: 'unsupported',
        reason: `Unsupported extension: ${extension || '(none)'}`,
      });
      return;
    }
    const source: SourceEntry = {
      sourcePath,
      absolutePath,
      section,
      kind,
      bytes: stat.size,
    };
    const metadata = await readMetadata(source, policy);
    if (metadata.draft) {
      ledger.push({
        sourcePath,
        disposition: 'excluded',
        reason: 'Excluded draft content',
      });
      return;
    }
    sources.push(source);
    const resourceUrl = policy.overrides[sourcePath]?.resourceUrl;
    ledger.push(
      resourceUrl && kind !== 'markdown' && kind !== 'notebook'
        ? {
            sourcePath,
            disposition: 'external-resource',
            reason: 'Explicit public resource URL',
            destination: resourceUrl,
          }
        : {
            sourcePath,
            disposition: 'page',
            reason: `Publishable ${kind}`,
            destination: createEntry(source, metadata).route,
          },
    );
  }

  for (const contentRoot of [...policy.roots].sort(compareSourcePaths)) {
    if (!CONTENT_ROOTS.some((allowed) => allowed === contentRoot))
      throw new Error(`${contentRoot}: invalid content root`);
    const absolutePath = join(root, contentRoot);
    try {
      await lstat(absolutePath);
    } catch (error) {
      if (error instanceof Error && 'code' in error && error.code === 'ENOENT')
        continue;
      throw error;
    }
    await visit(
      absolutePath,
      contentRoot,
      contentRoot.toLowerCase() as Section,
      absolutePath,
    );
  }
  sources.sort((a, b) => compareSourcePaths(a.sourcePath, b.sourcePath));
  ledger.sort((a, b) => compareSourcePaths(a.sourcePath, b.sourcePath));
  return { sources, ledger };
}
