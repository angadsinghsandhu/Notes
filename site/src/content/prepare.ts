import { randomUUID } from 'node:crypto';
import {
  lstat,
  mkdir,
  readFile,
  rename,
  rm,
  writeFile,
  realpath,
} from 'node:fs/promises';
import { extname, join } from 'node:path';
import { discoverEntries } from './discover.js';
import { readMetadata, readPolicy } from './schema.js';
import { compareSourcePaths, createEntry } from './identifiers.js';
import {
  collectExplicitAnchors,
  collectHeadings,
  collectMarkdownLinks,
  createHeadingSlugger,
  type MarkdownLink,
} from './headings.js';
import { createRouteCatalog, publicSourceUrl, resolveLink } from './links.js';
import { planAssets, readPlannedLocalAsset } from './assets.js';
import {
  verifyGeneratedTree,
  verifyOutputDirectory,
  writeManifest,
} from './manifest.js';
import { renderMarkdown } from './render/markdown.js';
import { renderNotebook } from './render/notebook.js';
import { renderSource } from './render/source.js';
import type {
  AssetRecord,
  ContentEntry,
  Diagnostic,
  Manifest,
  PreparationResult,
  PublicationPolicy,
} from './types.js';

export type PrepareOptions = {
  rootDir: string;
  outputDir: string;
  policyPath: string;
  hosted: boolean;
  revision?: string;
};
type Document = {
  entry: ContentEntry;
  text: string;
  json?: unknown;
  links: MarkdownLink[];
};

function diagnostic(sourcePath: string, error: unknown): Diagnostic {
  const original = error instanceof Error ? error.message : String(error);
  const message =
    original.length > 1000
      ? `${original.slice(0, 600)}…[truncated]…${original.slice(-300)}`
      : original;
  const cell = /: cell (\d+)/.exec(message)?.[1];
  return { sourcePath, message, ...(cell ? { cellIndex: Number(cell) } : {}) };
}

function notebookMarkdown(json: unknown): string[] {
  // Full nbformat/cell validation stays with the reviewed renderer. Collection never drops malformed cells.
  if (
    !json ||
    typeof json !== 'object' ||
    !('cells' in json) ||
    !Array.isArray(json.cells)
  )
    return [];
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
      throw new Error(`: cell ${index}: invalid notebook Markdown source`);
    return [
      typeof cell.source === 'string' ? cell.source : cell.source.join(''),
    ];
  });
}

function notebookExtraction(entry: ContentEntry, link: MarkdownLink): boolean {
  return (
    entry.kind === 'notebook' &&
    (link.href.startsWith('attachment:') ||
      (link.image && /^data:image\/(?:png|jpeg);base64,/.test(link.href)))
  );
}

async function exists(path: string): Promise<boolean> {
  try {
    await lstat(path);
    return true;
  } catch (error) {
    if (error instanceof Error && 'code' in error && error.code === 'ENOENT')
      return false;
    throw error;
  }
}

/** Stage both trees first; swap the manifest last and roll back every completed rename on error. */
async function commitSnapshot(
  generated: string,
  assetsTarget: string,
  stage: string,
): Promise<void> {
  const token = randomUUID();
  const current = join(generated, 'current');
  const oldSnapshot = join(generated, `.snapshot-backup-${token}`);
  const oldAssets = join(generated, `.assets-backup-${token}`);
  await verifyGeneratedTree(current);
  await verifyGeneratedTree(assetsTarget);
  const hadSnapshot = await exists(current);
  let movedAssets = false;
  let installedAssets = false;
  let movedSnapshot = false;
  try {
    await rename(assetsTarget, oldAssets);
    movedAssets = true;
    await rename(join(stage, 'assets'), assetsTarget);
    installedAssets = true;
    if (hadSnapshot) {
      await rename(current, oldSnapshot);
      movedSnapshot = true;
    }
    await rename(stage, current);
  } catch (error) {
    if (movedSnapshot) await rename(oldSnapshot, current);
    if (installedAssets) await rename(assetsTarget, join(stage, 'assets'));
    if (movedAssets) await rename(oldAssets, assetsTarget);
    throw error;
  }
  // Only names created by this transaction can be cleaned, after checking their complete trees.
  for (const backup of [oldSnapshot, oldAssets]) {
    await verifyGeneratedTree(backup);
    await rm(backup, { recursive: true, force: true });
  }
}

export async function prepareContent(
  options: PrepareOptions,
): Promise<PreparationResult> {
  const manifest: Manifest = {
    version: 1,
    entries: [],
    assets: [],
    ledger: [],
  };
  const diagnostics: Diagnostic[] = [];
  const result = { manifest, diagnostics };
  let stage: string | undefined;
  try {
    const root = await realpath(options.rootDir);
    const generated = await verifyOutputDirectory(
      options.rootDir,
      options.outputDir,
      'site/.generated',
    );
    const assetsTarget = await verifyOutputDirectory(
      root,
      join(root, 'site/public/content-assets'),
      'site/public/content-assets',
    );
    await verifyGeneratedTree(join(generated, 'current'));
    await verifyGeneratedTree(assetsTarget);
    const policy: PublicationPolicy = {
      ...(await readPolicy(options.policyPath)),
      ...(process.env.REPOSITORY_URL
        ? { repositoryUrl: process.env.REPOSITORY_URL }
        : {}),
      ...(options.revision ? { revision: options.revision } : {}),
      ...(process.env.SOURCE_REVISION
        ? { revision: process.env.SOURCE_REVISION }
        : {}),
      ...(process.env.SITE_URL ? { siteUrl: process.env.SITE_URL } : {}),
    };
    if (
      options.hosted &&
      (!policy.siteUrl ||
        new URL(policy.siteUrl).protocol !== 'https:' ||
        new URL(policy.siteUrl).username ||
        new URL(policy.siteUrl).password)
    )
      throw new Error(
        'Hosted preparation requires an HTTPS siteUrl without credentials',
      );
    const discovery = await discoverEntries(root, policy);
    manifest.ledger = discovery.ledger;
    const documents: Document[] = [];
    for (const source of discovery.sources) {
      try {
        const entry = createEntry(source, await readMetadata(source, policy));
        const text = ['markdown', 'notebook', 'code'].includes(source.kind)
          ? await readFile(source.absolutePath, 'utf8')
          : '';
        const json: unknown =
          source.kind === 'notebook' ? JSON.parse(text) : undefined;
        const markdown =
          source.kind === 'markdown'
            ? [text]
            : source.kind === 'notebook'
              ? notebookMarkdown(json)
              : [];
        const slugger = createHeadingSlugger();
        entry.headings = markdown.flatMap((cell) =>
          collectHeadings(cell, slugger),
        );
        entry.anchors = [...new Set(markdown.flatMap(collectExplicitAnchors))];
        manifest.entries.push(entry);
        documents.push({
          entry,
          text,
          ...(json !== undefined ? { json } : {}),
          links: markdown.flatMap(collectMarkdownLinks),
        });
      } catch (error) {
        diagnostics.push(diagnostic(source.sourcePath, error));
      }
    }
    if (diagnostics.length) return result;
    const candidates: AssetRecord[] = manifest.ledger
      .filter((row) => row.disposition === 'supporting-asset')
      .map((row, index) => ({
        sourcePath: row.sourcePath,
        bytes: 0,
        mode: 'local',
        url: `/planned-assets/${index}`,
      }));
    const preliminary = createRouteCatalog(
      manifest.entries,
      candidates,
      policy,
    );
    const selected = new Set(
      manifest.entries
        .filter((entry) => ['pdf', 'slides'].includes(entry.kind))
        .map((entry) => entry.sourcePath),
    );
    for (const document of documents) {
      for (const link of document.links) {
        if (notebookExtraction(document.entry, link)) continue;
        try {
          const resolved = resolveLink(
            link.href,
            document.entry.sourcePath,
            preliminary,
          );
          const asset = candidates.find(
            (asset) => asset.url === resolved.split(/[?#]/)[0],
          );
          if (asset) selected.add(asset.sourcePath);
        } catch (error) {
          diagnostics.push(diagnostic(document.entry.sourcePath, error));
        }
      }
    }
    if (diagnostics.length) return result;
    manifest.assets = await planAssets(root, [...selected], policy);
    const catalog = createRouteCatalog(
      manifest.entries,
      manifest.assets,
      policy,
    );
    const bodies = new Map<string, string>();
    const derived = new Map<string, Uint8Array>();
    for (const document of documents) {
      const entry = document.entry;
      try {
        // Validate every original URL before sanitization can remove an unsafe author URL.
        for (const link of document.links)
          if (!notebookExtraction(entry, link))
            resolveLink(link.href, entry.sourcePath, catalog);
        const asset = catalog.assets.get(entry.sourcePath);
        if (asset) entry.assetUrl = asset.url;
        entry.sourceUrl =
          !policy.repositoryPublic &&
          !policy.overrides[entry.sourcePath]?.resourceUrl &&
          asset?.mode === 'local'
            ? asset.url
            : publicSourceUrl(entry.sourcePath, policy, catalog);
        const context = {
          sourcePath: entry.sourcePath,
          catalog,
          extractAsset: (asset: AssetRecord, bytes: Uint8Array) => {
            derived.set(asset.url, bytes);
          },
        };
        const rendered =
          entry.kind === 'markdown'
            ? await renderMarkdown(document.text, context)
            : entry.kind === 'notebook'
              ? await renderNotebook(document.json, context)
              : entry.kind === 'code'
                ? await renderSource(
                    document.text,
                    extname(entry.sourcePath).slice(1),
                  )
                : undefined;
        if (rendered) {
          entry.bodyFile = `bodies/${entry.id}.html`;
          bodies.set(entry.bodyFile, rendered.html);
        }
      } catch (error) {
        diagnostics.push(diagnostic(entry.sourcePath, error));
      }
    }
    if (diagnostics.length) return result;
    manifest.assets = [...catalog.assets.values()].sort((a, b) =>
      compareSourcePaths(a.sourcePath, b.sourcePath),
    );
    const deployedFiles = new Set(
      manifest.assets
        .filter((asset) => asset.mode === 'local')
        .map((asset) => asset.url),
    );
    if (bodies.size + deployedFiles.size + manifest.entries.length + 1 > 20_000)
      throw new Error('Generated publication exceeds the 20,000-file limit');
    stage = join(generated, `.stage-${randomUUID()}`);
    await mkdir(join(stage, 'bodies'), { recursive: true });
    await mkdir(join(stage, 'assets'));
    for (const [name, html] of bodies) await writeFile(join(stage, name), html);
    for (const asset of manifest.assets) {
      if (asset.mode !== 'local') continue;
      const bytes =
        derived.get(asset.url) ?? (await readPlannedLocalAsset(root, asset));
      await writeFile(
        join(stage, 'assets', asset.url.slice('/content-assets/'.length)),
        bytes,
      );
    }
    await writeManifest(manifest, stage);
    await commitSnapshot(generated, assetsTarget, stage);
    stage = undefined;
  } catch (error) {
    diagnostics.push(diagnostic('publication', error));
  } finally {
    if (stage) {
      await verifyGeneratedTree(stage);
      await rm(stage, { recursive: true, force: true });
    }
  }
  return result;
}
