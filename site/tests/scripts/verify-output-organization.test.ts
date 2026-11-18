import { createIndex, close } from 'pagefind';
import { mkdtemp, mkdir, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import { verifyOutput } from '../../scripts/verify-output.js';
import {
  organizationPageRoutes,
  type Manifest,
} from '../../src/content/index.js';

const roots: string[] = [];
afterEach(async () => {
  vi.unstubAllEnvs();
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function put(path: string, text: string | Uint8Array) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, text);
}
// Synthetic published output uses the same native index producer as production.
async function fixture(
  configured = false,
  editReader?: (html: string) => string,
) {
  vi.stubEnv('SITE_URL', configured ? 'https://notes.example.test' : undefined);
  const root = await mkdtemp(join(tmpdir(), 'notes-organization-output-'));
  roots.push(root);
  const site = join(root, 'site');
  const dist = join(site, 'dist');
  const uid = 'doc-' + 'b'.repeat(64);
  const entry = {
    id: 'a'.repeat(64),
    sourcePath: 'Tutorials/note.md',
    section: 'tutorials' as const,
    kind: 'markdown' as const,
    bytes: 1,
    title: 'Acceptance note',
    description: '',
    tags: [],
    draft: false,
    aliases: ['/old-note/'],
    groupSegments: [],
    route: '/notes/tutorials/note/',
    headings: [{ id: 'description', text: 'Description', depth: 3 }],
    anchors: ['explicit'],
  };
  const manifest: Manifest = {
    version: 1,
    entries: [entry],
    assets: [],
    ledger: [],
    organization: {
      topics: [{ id: 'topic', title: 'Topic', summary: '' }],
      collections: [
        { id: 'collection', title: 'Collection', summary: '', type: 'book' },
      ],
      groups: [
        {
          id: 'group',
          collectionId: 'collection',
          title: 'Group',
          summary: '',
          type: 'chapter',
        },
      ],
      memberships: [
        {
          entryId: entry.id,
          uid,
          topics: ['topic'],
          collectionId: 'collection',
          groupId: 'group',
          purpose: 'note',
          status: 'reviewed',
          summary: '',
          relatedUids: [],
        },
      ],
      paths: [
        {
          id: 'path',
          title: 'Path',
          summary: '',
          steps: [
            {
              id: 'read',
              title: 'Read',
              summary: '',
              entryUids: [uid],
              topicIds: [],
            },
            {
              id: 'explore',
              title: 'Explore',
              summary: '',
              entryUids: [],
              topicIds: ['topic'],
            },
          ],
        },
      ],
    },
  };
  await put(
    join(site, '.generated/current/manifest.json'),
    JSON.stringify(manifest),
  );
  await put(
    join(site, 'content/publication.json'),
    JSON.stringify({
      roots: [
        'Books',
        'Classes',
        'Courses',
        'Interview',
        'Languages',
        'Tutorials',
      ],
    }),
  );
  const organization = organizationPageRoutes(
    manifest.entries,
    manifest.organization,
  );
  const routes = [
    '/',
    '/library/',
    '/library/tree/',
    '/search/',
    ...organization,
    ...[
      'books',
      'classes',
      'courses',
      'interview',
      'languages',
      'tutorials',
    ].map((s) => `/library/${s}/`),
    entry.route,
  ];
  const canonical = (route: string) =>
    configured
      ? `<link rel="canonical" href="https://notes.example.test${route}">`
      : '';
  for (const route of routes)
    await put(
      join(dist, route, 'index.html'),
      `<html lang="en"><head>${canonical(route)}</head><body><main data-pagefind-ignore>Listing</main></body></html>`,
    );
  const reader = `<html lang="en"><head>${canonical(entry.route)}<meta name="description" content="Read Leadership Principle in Interview."></head><body><article data-pagefind-body data-kind="markdown" data-pagefind-filter="kind[data-kind]" data-pagefind-meta="kind[data-kind]"><h1 data-pagefind-meta="title">Acceptance note</h1><h3 id="description">Description</h3><a name="explicit">Explicit</a><a href="#description">Description</a><a href="#explicit">Explicit</a></article></body></html>`;
  await put(
    join(dist, entry.route, 'index.html'),
    editReader?.(reader) ?? reader,
  );
  await put(
    join(dist, 'old-note/index.html'),
    `<html><head>${canonical(entry.route)}<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=${entry.route}"></head><body><a href="${entry.route}">Continue</a></body></html>`,
  );
  const steps = `<ol class="path-steps"><li id="read"><a href="${entry.route}">Read</a></li><li id="explore"><a href="/library/topics/topic/">Explore</a></li></ol>`;
  await put(
    join(dist, 'library/paths/path/index.html'),
    `<html><head>${canonical('/library/paths/path/')}</head><body><main data-pagefind-ignore>${steps}</main></body></html>`,
  );
  await put(join(dist, '404.html'), '<html><body>Not found</body></html>');
  const sitemap = `<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${routes.map((r) => `<url><loc>https://notes.example.test${r}</loc></url>`).join('')}</urlset>`;
  if (configured) await put(join(dist, 'sitemap.xml'), sitemap);
  const created = await createIndex();
  if (!created.index) throw new Error(created.errors.join(';'));
  try {
    await created.index.addDirectory({ path: dist });
    for (const f of (await created.index.getFiles()).files)
      await put(join(dist, 'pagefind', f.path), f.content);
  } finally {
    await created.index.deleteIndex();
    await close();
  }
  return { site, dist, manifest, entry, organization, sitemap, steps };
}

it.each([false, true])(
  'accepts every populated category and ordered UID/topic path with configured=%s',
  async (configured) => {
    expect(await verifyOutput((await fixture(configured)).dist)).toEqual([]);
  },
);
it.each([
  'topics/',
  'collections/',
  'paths/',
  'topics/topic/',
  'collections/collection/',
  'collections/collection/groups/group/',
  'paths/path/',
])('rejects wrong category canonical for %s', async (suffix) => {
  const f = await fixture(true);
  const file = join(f.dist, 'library', suffix, 'index.html');
  await put(
    file,
    (await readFile(file, 'utf8')).replace(
      /<link rel="canonical"[^>]+>/,
      '<link rel="canonical" href="https://notes.example.test/wrong/">',
    ),
  );
  expect(await verifyOutput(f.dist)).toContainEqual(
    expect.objectContaining({
      message: `Invalid canonical for /library/${suffix}`,
    }),
  );
});
it('rejects a canonical on an unconfigured category and duplicate configured canonicals', async () => {
  const f = await fixture();
  const file = join(f.dist, 'library/topics/index.html');
  const html = await readFile(file, 'utf8');
  await put(
    file,
    html.replace(
      '</head>',
      '<link rel="canonical" href="https://notes.example.test/library/topics/"></head>',
    ),
  );
  expect(await verifyOutput(f.dist)).toContainEqual(
    expect.objectContaining({
      message: 'Invalid canonical for /library/topics/',
    }),
  );
  vi.stubEnv('SITE_URL', 'https://notes.example.test');
  await put(
    file,
    html.replace(
      '</head>',
      '<link rel="canonical" href="https://notes.example.test/library/topics/"><link rel="canonical" href="https://notes.example.test/library/topics/"></head>',
    ),
  );
  await put(join(f.dist, 'sitemap.xml'), f.sitemap);
  expect(await verifyOutput(f.dist)).toContainEqual(
    expect.objectContaining({
      message: 'Invalid canonical for /library/topics/',
    }),
  );
});
it('rejects a listing Pagefind body even when ignored by the native index', async () => {
  const f = await fixture();
  const file = join(f.dist, 'library/topics/index.html');
  await put(
    file,
    (await readFile(file, 'utf8')).replace(
      'data-pagefind-ignore',
      'data-pagefind-ignore data-pagefind-body',
    ),
  );
  expect(await verifyOutput(f.dist)).toContainEqual(
    expect.objectContaining({
      message: 'Organization listing contains Pagefind body',
    }),
  );
});
it.each(['missing', 'wrong-target', 'wrong-order', 'duplicate', 'extra'])(
  'rejects %s resolved path-step evidence',
  async (fault) => {
    const f = await fixture();
    const file = join(f.dist, 'library/paths/path/index.html');
    let steps = f.steps;
    if (fault === 'missing') steps = '<ol class="path-steps"></ol>';
    if (fault === 'wrong-target')
      steps = steps.replace(f.entry.route, '/library/');
    if (fault === 'wrong-order')
      steps = `<ol class="path-steps"><li id="explore"><a href="/library/topics/topic/">Explore</a></li><li id="read"><a href="${f.entry.route}">Read</a></li></ol>`;
    if (fault === 'duplicate')
      steps = steps.replace(
        '</ol>',
        `<li id="read"><a href="${f.entry.route}">Duplicate</a></li></ol>`,
      );
    if (fault === 'extra')
      steps = steps.replace('</li>', '<a href="/library/">Extra</a></li>');
    await put(
      file,
      `<html><body><main data-pagefind-ignore>${steps}</main></body></html>`,
    );
    expect(await verifyOutput(f.dist)).toContainEqual(
      expect.objectContaining({
        message: 'Invalid resolved path steps for /library/paths/path/',
      }),
    );
  },
);
it('accepts a sitemap image extension plus a location with text, CDATA and character references', async () => {
  const f = await fixture(true);
  const xml = f.sitemap.replace(
    '<loc>https://notes.example.test/</loc>',
    '<loc>https://notes.example<![CDATA[.test]]>&#47;</loc><image:image xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><image:loc>https://notes.example.test/image.png</image:loc></image:image>',
  );
  await put(join(f.dist, 'sitemap.xml'), xml);
  expect(await verifyOutput(f.dist)).toEqual([]);
});
it.each([
  'missing',
  'extra',
  'alias',
  'duplicate',
  'malformed',
  'wrong-origin',
  'wrong root',
  'missing namespace',
  'extension shadow',
  'nested location',
  'two locations in one URL',
  'element inside location',
])('rejects %s sitemap membership', async (fault) => {
  const f = await fixture(true);
  let xml = f.sitemap;
  if (fault === 'missing')
    xml = xml.replace(
      '<url><loc>https://notes.example.test/library/topics/topic/</loc></url>',
      '',
    );
  if (fault === 'extra' || fault === 'alias')
    xml = xml.replace(
      '</urlset>',
      `<url><loc>https://notes.example.test/${fault === 'alias' ? 'old-note' : 'unexpected'}/</loc></url></urlset>`,
    );
  if (fault === 'duplicate')
    xml = xml.replace(
      '</urlset>',
      '<url><loc>https://notes.example.test/</loc></url></urlset>',
    );
  if (fault === 'malformed') xml = '<urlset><url>';
  if (fault === 'wrong-origin')
    xml = xml.replace(
      'https://notes.example.test/library/topics/topic/',
      'https://other.example/library/topics/topic/',
    );
  if (fault === 'wrong root') xml = xml.replaceAll('urlset', 'feed');
  if (fault === 'missing namespace')
    xml = xml.replace(
      ' xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
      '',
    );
  const location =
    '<loc>https://notes.example.test/library/topics/topic/</loc>';
  if (fault === 'extension shadow')
    xml = xml.replace(
      location,
      '<image:image xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><image:loc>https://notes.example.test/library/topics/topic/</image:loc></image:image>',
    );
  if (fault === 'nested location')
    xml = xml.replace(location, `<lastmod>${location}</lastmod>`);
  if (fault === 'two locations in one URL')
    xml = xml
      .replace(`<url>${location}</url>`, '')
      .replace(
        '<loc>https://notes.example.test/</loc>',
        `<loc>https://notes.example.test/</loc>${location}`,
      );
  if (fault === 'element inside location')
    xml = xml.replace(location, location.replace('</loc>', '<ignored/></loc>'));
  await put(join(f.dist, 'sitemap.xml'), xml);
  expect(await verifyOutput(f.dist)).toContainEqual(
    expect.objectContaining({
      message: 'Sitemap differs from canonical published routes',
    }),
  );
});
it.each(['description', 'explicit'])(
  'rejects a missing declared reader %s anchor even when a non-anchor element shares its name',
  async (anchor) => {
    const f = await fixture(false, (reader) =>
      anchor === 'description'
        ? reader.replace(' id="description"', '')
        : reader
            .replace(' name="explicit"', '')
            .replace('</article>', '<input name="explicit"></article>'),
    );
    expect(await verifyOutput(f.dist)).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          message: `Reader is missing declared anchor: ${anchor}`,
        }),
        expect.objectContaining({ message: `Missing fragment: #${anchor}` }),
      ]),
    );
  },
);
it('requires an ID for a declared reader heading even if a legacy named anchor resolves its fragment', async () => {
  const f = await fixture(false, (reader) =>
    reader
      .replace(' id="description"', '')
      .replace('</article>', '<a name="description"></a></article>'),
  );
  expect(await verifyOutput(f.dist)).toEqual([
    expect.objectContaining({
      message: 'Reader is missing declared anchor: description',
    }),
  ]);
});
