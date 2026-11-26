import { lstat, readFile, readdir } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { fromHtml } from 'hast-util-from-html';
import { verifySitemap } from './verify-output-sitemap.js';
import { selectCurriculumRoutes } from '../src/lib/leetcode.js';
import { buildOrganizationIndex } from '../src/lib/organization.js';
import type { Element, Nodes } from 'hast';
import { buildFolders, flattenFolders } from '../src/lib/folders.js';
import { verifyPagefind } from './verify-pagefind.js';
import { pdfAssets } from './pdf-assets.js';
import {
  publicationExclusion,
  organizationPageRoutes,
  readPolicy,
  publicationPages,
  assertCurriculumRouteOwnership,
  verifyCurriculumArtifacts,
  type Diagnostic,
  type Manifest,
} from '../src/content/index.js';

const MAX_FILES = 20_000;
const MAX_BYTES = 26_214_400;
const routeFile = (route: string) =>
  route.endsWith('/') ? `${route.slice(1)}index.html` : route.slice(1);
type Page = {
  ids: Set<string>;
  namedAnchors?: Set<string>;
  links: { url: string; tag: string; attribute?: string }[];
  nodes: Element[];
  pathSteps: { id: string; links: string[] }[];
};
const hasFragment = (page: Page, id: string) =>
  page.ids.has(id) || page.namedAnchors?.has(id);
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
  const result: Page = { ids: new Set(), links: [], nodes: [], pathSteps: [] };
  function visit(node: Nodes, step?: Page['pathSteps'][number]): void {
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
      const { id, name } = node.properties;
      if (typeof id === 'string') result.ids.add(retainedText(id));
      if (node.tagName === 'a' && typeof name === 'string')
        (result.namedAnchors ??= new Set()).add(retainedText(name));
      for (const key of ['href', 'src', 'poster', 'action', 'cite']) {
        const value = node.properties[key];
        if (typeof value === 'string') {
          if (step && node.tagName === 'a' && key === 'href')
            step.links.push(retainedText(value));
          result.links.push({
            url: retainedText(value),
            tag: node.tagName,
            attribute: key,
          });
        }
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
    if (
      node.type === 'element' &&
      node.tagName === 'ol' &&
      Array.isArray(node.properties.className) &&
      node.properties.className.includes('path-steps')
    ) {
      for (const child of node.children) {
        const item =
          child.type === 'element' && child.tagName === 'li'
            ? { id: String(child.properties.id ?? ''), links: [] as string[] }
            : undefined;
        if (item) result.pathSteps.push(item);
        visit(child, item);
      }
    } else if ('children' in node)
      for (const child of node.children) visit(child, step);
  }
  visit(fromHtml(html));
  return result;
}

/** Read-only verification of the deployed tree against the private prepared manifest. */
export async function verifyOutput(
  distDir: string,
  electedCurriculumRoutes?: readonly string[],
): Promise<Diagnostic[]> {
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
  const organizationRoutes = organizationPageRoutes(
    published,
    manifest.organization,
  );
  const folders = flattenFolders(buildFolders(published))
    .filter((folder) => folder.segments.length > 0)
    .map((folder) => folder.route);
  let curriculumRoutes: string[] = [];
  if (
    manifest.curriculumGeneration !== undefined ||
    electedCurriculumRoutes?.length
  ) {
    try {
      const snapshot =
        manifest.curriculumGeneration === undefined
          ? undefined
          : await verifyCurriculumArtifacts(
              join(site, '.generated'),
              manifest.curriculumGeneration,
            );
      const claims = snapshot?.routes ?? [];
      assertCurriculumRouteOwnership(
        [...publicationPages([], manifest.organization), ...claims],
        published,
      );
      curriculumRoutes = selectCurriculumRoutes(
        claims,
        electedCurriculumRoutes,
      );
    } catch (error) {
      fail(
        '.generated/current/manifest.json',
        error instanceof Error ? error.message : String(error),
      );
    }
  }
  const expected = new Set([
    '404.html',
    ...fixed.map(routeFile),
    ...curriculumRoutes.map(routeFile),
    ...organizationRoutes.map(routeFile),
    ...folders.map(routeFile),
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
      /(?:^|\/)(?:\.generated|content|migration-report\.json|manifest\.json|publication\.json|\.env(?:\..*)?)($|\/)|^(?:worker-assets|practice-traces)($|\/)|(?:^|\/)(?:curriculum|trace-assets|progress-registry)\.json$/.test(
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
      pages.set(file, { ids: new Set(), nodes: [], links, pathSteps: [] });
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
          !hasFragment(
            pages.get(target)!,
            decodeURIComponent(url.hash.slice(1)),
          )
        )
          fail(file, `Missing fragment: ${link.url}`);
      } catch {
        fail(file, `Unsafe URL: ${link.url}`);
      }
    }
  }
  const organization = buildOrganizationIndex(published, manifest.organization);
  for (const route of organizationRoutes) {
    const parsed = pages.get(routeFile(route));
    if (!parsed) continue;
    const canonicals = parsed.nodes.filter(
      (node) =>
        node.tagName === 'link' &&
        Array.isArray(node.properties.rel) &&
        node.properties.rel.includes('canonical'),
    );
    if (
      siteUrl
        ? canonicals.length !== 1 ||
          canonicals[0]?.properties.href !== new URL(route, siteUrl).href
        : canonicals.length > 0
    )
      fail(route, `Invalid canonical for ${route}`);
    if (parsed.nodes.some((node) => 'dataPagefindBody' in node.properties))
      fail(route, 'Organization listing contains Pagefind body');
    const path = /^\/library\/paths\/([^/]+)\/$/.exec(route);
    const node = path ? organization.getNode('path', path[1]!) : undefined;
    if (
      node?.type === 'path' &&
      JSON.stringify(parsed.pathSteps) !==
        JSON.stringify(
          node.steps.map((step) => ({
            id: step.id,
            links: [...step.entries, ...step.topics].map((link) => link.route),
          })),
        )
    )
      fail(route, `Invalid resolved path steps for ${route}`);
  }
  if (siteUrl && files.has('sitemap.xml')) {
    try {
      verifySitemap(
        await readFile(join(dist, 'sitemap.xml'), 'utf8'),
        siteUrl,
        [
          ...fixed,
          ...organizationRoutes,
          ...folders,
          ...published.map((entry) => entry.route),
          ...curriculumRoutes,
        ],
      );
    } catch {
      fail('sitemap.xml', 'Sitemap differs from canonical published routes');
    }
  }
  for (const entry of published) {
    const parsed = pages.get(routeFile(entry.route));
    if (!parsed) continue;
    const missingAnchors = [
      ...entry.headings.map(({ id }) => id).filter((id) => !parsed.ids.has(id)),
      ...(entry.anchors ?? []).filter((anchor) => !hasFragment(parsed, anchor)),
    ];
    for (const anchor of missingAnchors)
      fail(entry.sourcePath, `Reader is missing declared anchor: ${anchor}`);
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
