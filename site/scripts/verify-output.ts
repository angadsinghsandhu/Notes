import { lstat, readFile, readdir } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { fromHtml } from 'hast-util-from-html';
import type { Element, Nodes } from 'hast';
import { buildFolders, flattenFolders } from '../src/lib/folders.js';
import { verifyPagefind } from './verify-pagefind.js';
import { pdfAssets } from './pdf-assets.js';
import {
  publicationExclusion,
  organizationPageRoutes,
  readPolicy,
  type Diagnostic,
  type Manifest,
} from '../src/content/index.js';

const MAX_FILES = 20_000;
const MAX_BYTES = 26_214_400;
const routeFile = (route: string) =>
  route.endsWith('/') ? `${route.slice(1)}index.html` : route.slice(1);
type Page = {
  ids: Set<string>;
  links: { url: string; tag: string; attribute?: string }[];
  nodes: Element[];
};
const text = (node: Nodes): string =>
  node.type === 'text'
    ? node.value
    : 'children' in node
      ? node.children.map(text).join('')
      : '';
// Flatten parser attribute ropes retained across pages; preserve exact UTF-16 code units.
const retainedText = (value: string): string =>
  Buffer.from(value, 'utf16le').toString('utf16le');
function page(html: string): Page {
  const result: Page = { ids: new Set(), links: [], nodes: [] };
  function visit(node: Nodes): void {
    if (node.type === 'element') {
      // Links/IDs remain complete; only source actions need retained anchor text.
      const sourceAction =
        node.tagName === 'a' && text(node).trim() === 'View original source';
      if (
        sourceAction ||
        ['meta', 'link', 'iframe'].includes(node.tagName) ||
        'dataPdfViewer' in node.properties ||
        'dataPagefindBody' in node.properties
      )
        result.nodes.push({
          type: 'element',
          tagName: node.tagName,
          properties: node.properties,
          children: sourceAction ? [{ type: 'text', value: text(node) }] : [],
        });
      for (const key of ['id', 'name']) {
        const value = node.properties[key];
        if (typeof value === 'string') result.ids.add(retainedText(value));
      }
      for (const key of ['href', 'src', 'poster', 'action', 'cite']) {
        const value = node.properties[key];
        if (typeof value === 'string')
          result.links.push({
            url: retainedText(value),
            tag: node.tagName,
            attribute: key,
          });
      }
      const set = node.properties['srcSet'];
      if (typeof set === 'string')
        for (const candidate of set.split(','))
          result.links.push({
            url: retainedText(candidate.trim().split(/\s+/)[0] ?? ''),
            tag: node.tagName,
          });
      if (
        node.tagName === 'meta' &&
        String(node.properties['httpEquiv']).toLowerCase() === 'refresh'
      ) {
        const target = /url=(.*)$/i.exec(
          String(node.properties['content']),
        )?.[1];
        if (target)
          result.links.push({ url: retainedText(target), tag: 'meta' });
      }
    }
    if ('children' in node) for (const child of node.children) visit(child);
  }
  visit(fromHtml(html));
  return result;
}

/** Read-only verification of the deployed tree against the private prepared manifest. */
export async function verifyOutput(distDir: string): Promise<Diagnostic[]> {
  const diagnostics: Diagnostic[] = [];
  const fail = (sourcePath: string, message: string) =>
    diagnostics.push({ sourcePath, message });
  const dist = resolve(distDir);
  const site = dirname(dist);
  const manifest = JSON.parse(
    await readFile(join(site, '.generated/current/manifest.json'), 'utf8'),
  ) as Manifest;
  const policy = await readPolicy(join(site, 'content/publication.json'));
  const siteUrl = process.env['SITE_URL'] ?? policy.siteUrl;
  const files = new Map<string, number>();
  async function walk(directory: string, prefix = ''): Promise<void> {
    const stat = await lstat(directory);
    if (stat.isSymbolicLink() || !stat.isDirectory()) {
      fail(prefix || '.', 'Unsafe symbolic link or non-directory output');
      return;
    }
    for (const name of await readdir(directory)) {
      const path = join(directory, name);
      const relative = `${prefix}${name}`;
      const stat = await lstat(path);
      if (stat.isSymbolicLink())
        fail(relative, 'Unsafe symbolic link in output');
      else if (stat.isDirectory()) await walk(path, `${relative}/`);
      else if (stat.isFile()) {
        files.set(relative, stat.size);
        if (stat.size > MAX_BYTES)
          fail(
            relative,
            `Deployed asset is ${stat.size} bytes; maximum is ${MAX_BYTES}`,
          );
      } else fail(relative, 'Unsafe non-regular output');
    }
  }
  await walk(dist);
  if (files.size > MAX_FILES)
    fail('.', `Output has ${files.size} files; maximum is ${MAX_FILES}`);
  const published = manifest.entries.filter((entry) => {
    const excluded = publicationExclusion(entry.sourcePath, policy);
    if (excluded)
      fail(
        entry.sourcePath,
        `Excluded entry leaked into prepared publication: ${excluded}`,
      );
    return !entry.draft && !excluded;
  });
  const publishedAssets = manifest.assets.filter((asset) => {
    const excluded = publicationExclusion(asset.sourcePath, policy);
    if (excluded)
      fail(
        asset.sourcePath,
        `Excluded asset leaked into prepared publication: ${excluded}`,
      );
    return !excluded;
  });
  for (const entry of manifest.entries.filter((entry) => entry.draft))
    fail(entry.sourcePath, 'Draft entry leaked into prepared publication');
  const fixed = [
    '/',
    '/library/',
    '/library/tree/',
    '/search/',
    ...policy.roots.map((root) => `/library/${root.toLowerCase()}/`),
  ];
  const expected = new Set([
    '404.html',
    ...fixed.map(routeFile),
    ...organizationPageRoutes(published, manifest.organization).map(routeFile),
    ...flattenFolders(buildFolders(published))
      .filter((folder) => folder.segments.length > 0)
      .map((folder) => routeFile(folder.route)),
    ...published.flatMap((entry) =>
      [entry.route, ...entry.aliases].map(routeFile),
    ),
  ]);
  if (siteUrl) expected.add('sitemap.xml');
  const assets = new Set(
    publishedAssets
      .filter((asset) => asset.mode === 'local')
      .map((asset) => asset.url.slice(1)),
  );
  const pages = new Map<string, Page>();
  for (const [file, bytes] of files) {
    if (
      /(?:^|\/)(?:\.generated|content|migration-report\.json|manifest\.json|publication\.json|\.env(?:\..*)?)($|\/)/.test(
        file,
      )
    )
      fail(file, 'Deployed internal publication data');
    const allowed =
      expected.has(file) ||
      assets.has(file) ||
      /^_astro\/[^/]+\.(?:js|css|woff2?|ttf|otf)$/.test(file) ||
      /^pagefind\/[a-zA-Z0-9_./-]+$/.test(file) ||
      file.startsWith('pdfjs/') ||
      file === '_headers' ||
      file === '_redirects';
    if (!allowed)
      fail(
        file,
        'Unexpected output file: stale page, asset, or excluded content',
      );
    if (file.endsWith('.html'))
      pages.set(file, page(await readFile(join(dist, file), 'utf8')));
    if (bytes <= MAX_BYTES && file.endsWith('.css')) {
      const css = await readFile(join(dist, file), 'utf8');
      const links = [
        ...css.matchAll(/url\(\s*(?:"([^"]*)"|'([^']*)'|([^\s)]*))\s*\)/g),
      ].map((match) => ({
        url: match[1] ?? match[2] ?? match[3] ?? '',
        tag: 'style',
      }));
      pages.set(file, { ids: new Set(), nodes: [], links });
    }
  }
  const hasPdfViewer = [...pages.values()].some((parsed) =>
    parsed.nodes.some((node) => 'dataPdfViewer' in node.properties),
  );
  const pdfFiles = [...files.keys()].filter((file) =>
    file.startsWith('pdfjs/'),
  );
  if (hasPdfViewer || pdfFiles.length) {
    const support = await pdfAssets();
    for (const file of pdfFiles) {
      const original = support.get(file.slice('pdfjs/'.length));
      if (!original) fail(file, 'Unexpected PDF.js support file');
      else if (!(await readFile(join(dist, file))).equals(original))
        fail(file, 'PDF.js support file differs from pinned distribution');
    }
    for (const file of support.keys())
      if (!files.has(`pdfjs/${file}`))
        fail(`pdfjs/${file}`, 'Missing PDF.js support file');
  }
  for (const file of [...expected, ...assets])
    if (!files.has(file)) fail(file, 'Missing expected output file');
  for (const [file, parsed] of pages) {
    for (const link of parsed.links) {
      if (/^(?:https?:|mailto:|tel:)/i.test(link.url)) continue;
      if (/^data:/i.test(link.url) && ['img', 'style'].includes(link.tag))
        continue;
      try {
        const url = new URL(link.url, `https://output.invalid/${file}`);
        if (
          url.origin !== 'https://output.invalid' ||
          link.url.includes('\\') ||
          Array.from(link.url).some(
            (character) => character.charCodeAt(0) <= 32,
          )
        ) {
          fail(file, `Unsafe URL: ${link.url}`);
          continue;
        }
        const path = decodeURIComponent(url.pathname);
        if (path.includes('\\') || path.includes('\0')) {
          fail(file, `Unsafe URL: ${link.url}`);
          continue;
        }
        const target = path.endsWith('/')
          ? `${path.slice(1)}index.html`
          : path.slice(1);
        if (!files.has(target)) fail(file, `Missing local target: ${link.url}`);
        else if (
          url.hash &&
          pages.has(target) &&
          !pages.get(target)!.ids.has(decodeURIComponent(url.hash.slice(1)))
        )
          fail(file, `Missing fragment: ${link.url}`);
      } catch {
        fail(file, `Unsafe URL: ${link.url}`);
      }
    }
  }
  for (const entry of published) {
    const parsed = pages.get(routeFile(entry.route));
    if (!parsed) continue;
    const actions = parsed.nodes.filter(
      (node) =>
        node.tagName === 'a' && text(node).trim() === 'View original source',
    );
    const localSource = publishedAssets.some(
      (asset) =>
        asset.mode === 'local' &&
        asset.sourcePath === entry.sourcePath &&
        asset.url === entry.sourceUrl &&
        asset.url === entry.assetUrl &&
        /^\/content-assets\/[a-f0-9]{64}\.(?:pdf|ppt|pptx)$/.test(asset.url) &&
        files.has(asset.url.slice(1)),
    );
    if (
      entry.sourceUrl &&
      (actions.length !== 1 ||
        actions[0]?.properties['href'] !== entry.sourceUrl ||
        (!/^https:\/\//.test(entry.sourceUrl) && !localSource))
    )
      fail(entry.sourcePath, 'Malformed or missing original source action');
    if (!parsed.nodes.some((node) => 'dataPagefindBody' in node.properties))
      fail(entry.sourcePath, 'Reader is missing Pagefind body');
    for (const alias of entry.aliases) {
      const parsed = pages.get(routeFile(alias));
      if (!parsed) continue;
      const robots = parsed.nodes.some(
        (node) =>
          node.tagName === 'meta' &&
          node.properties['name'] === 'robots' &&
          node.properties['content'] === 'noindex',
      );
      const refresh = parsed.nodes.some(
        (node) =>
          node.tagName === 'meta' &&
          String(node.properties['httpEquiv']) === 'refresh' &&
          node.properties['content'] === `0;url=${entry.route}`,
      );
      if (
        !robots ||
        !refresh ||
        !parsed.links.some(
          (link) => link.tag === 'a' && link.url === entry.route,
        )
      )
        fail(entry.sourcePath, `Malformed alias: ${alias}`);
    }
    for (const route of [entry.route, ...entry.aliases]) {
      const canonicals =
        pages
          .get(routeFile(route))
          ?.nodes.filter(
            (node) =>
              node.tagName === 'link' &&
              node.properties['rel'] instanceof Array &&
              node.properties['rel'].includes('canonical'),
          ) ?? [];
      const target = siteUrl ? new URL(entry.route, siteUrl).href : undefined;
      if (
        target
          ? canonicals.length !== 1 ||
            canonicals[0]?.properties['href'] !== target
          : canonicals.length > 0
      )
        fail(entry.sourcePath, `Invalid canonical for ${route}`);
    }
    if (
      entry.assetUrl?.startsWith('/content-assets/') &&
      !assets.has(entry.assetUrl.slice(1))
    )
      fail(entry.sourcePath, 'Resource asset is missing from manifest');
    if (
      entry.bytes > MAX_BYTES &&
      ['pdf', 'slides'].includes(entry.kind) &&
      (parsed.nodes.some((node) => node.tagName === 'iframe') ||
        parsed.links.some(
          (link) =>
            link.tag === 'a' &&
            link.attribute === 'href' &&
            link.url === entry.assetUrl &&
            entry.assetUrl?.startsWith('/'),
        ))
    )
      fail(entry.sourcePath, 'Oversized resource has a local source action');
  }
  diagnostics.push(...(await verifyPagefind(dist, published)));
  return diagnostics;
}

if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  try {
    const diagnostics = await verifyOutput(resolve(process.argv[2] ?? 'dist'));
    for (const diagnostic of diagnostics)
      console.error(`${diagnostic.sourcePath}: ${diagnostic.message}`);
    process.exitCode = diagnostics.length ? 1 : 0;
    if (!diagnostics.length)
      console.log(
        'Verified production file limits, routes, assets, fragments, source actions and Pagefind.',
      );
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
