import { decode, encode } from 'cbor-x';
import { gzipSync, gunzipSync } from 'node:zlib';
import { createIndex, close } from 'pagefind';
import {
  mkdtemp,
  mkdir,
  writeFile,
  readdir,
  readFile,
  rm,
  truncate,
  symlink,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import { execFileSync } from 'node:child_process';
import { verifyOutput } from '../../scripts/verify-output.js';
import type { ContentEntry, Manifest } from '../../src/content/index.js';
const roots: string[] = [];
afterEach(async () => {
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function put(path: string, text: string | Buffer) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, text);
}
// Explicitly synthetic output fixture for validator boundaries and corruptions.
async function output(entries: ContentEntry[] = []) {
  const root = await mkdtemp(join(tmpdir(), 'notes-output-'));
  roots.push(root);
  const site = join(root, 'site');
  const dist = join(site, 'dist');
  const manifest: Manifest = { version: 1, entries, assets: [], ledger: [] };
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
  for (const route of [
    '/',
    '/library/',
    '/search/',
    ...[
      'books',
      'classes',
      'courses',
      'interview',
      'languages',
      'tutorials',
    ].map((section) => `/library/${section}/`),
  ])
    await put(
      join(dist, route, 'index.html'),
      '<html><body><main>Fixture</main></body></html>',
    );
  await put(
    join(dist, '404.html'),
    '<html><head><meta name="robots" content="noindex"></head><body>Not found</body></html>',
  );
  return { root, site, dist, manifest };
}
function note(fields: Partial<ContentEntry> = {}): ContentEntry {
  return {
    id: 'a'.repeat(64),
    sourcePath: 'Books/note.md',
    section: 'books',
    kind: 'markdown',
    bytes: 1,
    title: 'Synthetic validation note',
    description: '',
    tags: [],
    draft: false,
    aliases: [],
    headings: [{ id: 'target', text: 'Target', depth: 2 }],
    groupSegments: [],
    route: '/notes/books/note/',
    sourceUrl: `https://github.com/owner/repo/blob/${'a'.repeat(40)}/Books/note.md`,
    ...fields,
  };
}
async function pageFixture(fields: Partial<ContentEntry> = {}) {
  const entry = note(fields);
  const fixture = await output([entry]);
  const html = `<html lang="en"><body><article data-pagefind-body data-kind="${entry.kind}" data-pagefind-filter="kind[data-kind]" data-pagefind-meta="kind[data-kind]"><h1 data-pagefind-meta="title">${entry.title}</h1><h2 id="target">Target</h2><div data-pagefind-ignore><a href="${entry.sourceUrl}">View original source</a></div></article></body></html>`;
  await put(join(fixture.dist, entry.route, 'index.html'), html);
  const created = await createIndex();
  if (!created.index) throw new Error(created.errors.join(';'));
  try {
    await created.index.addDirectory({ path: fixture.dist });
    const generated = await created.index.getFiles();
    for (const file of generated.files)
      await put(
        join(fixture.dist, 'pagefind', file.path),
        Buffer.from(file.content),
      );
  } finally {
    await created.index.deleteIndex();
    await close();
  }
  return { ...fixture, entry, html };
}
it('accepts the actual complete built archive and keeps the ledger internal', async () => {
  expect(await verifyOutput(join(process.cwd(), 'dist'))).toEqual([]);
}, 120000);
it('accepts exactly 20000 files and rejects 20001', async () => {
  const { dist } = await output();
  await mkdir(join(dist, '_astro'));
  for (let index = 10; index < 20000; index++)
    await writeFile(join(dist, `_astro/fixture-${index}.js`), '');
  expect(await verifyOutput(dist)).toEqual([]);
  await writeFile(join(dist, '_astro/fixture-20000.js'), '');
  expect(await verifyOutput(dist)).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ message: expect.stringContaining('20001') }),
    ]),
  );
}, 120000);
it('accepts exactly 26214400 bytes and rejects 26214401', async () => {
  const { dist } = await output();
  const path = join(dist, '_astro/fixture.js');
  await put(path, '');
  await truncate(path, 26214400);
  expect(await verifyOutput(dist)).toEqual([]);
  await truncate(path, 26214401);
  expect(await verifyOutput(dist)).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ message: expect.stringContaining('26214401') }),
    ]),
  );
}, 120000);
it.each([
  ['<img src="/content-assets/missing.png">', 'Missing local target'],
  ['<a href="#absent">Missing fragment</a>', 'Missing fragment'],
  ['<a href="/missing/?q=1">Missing page</a>', 'Missing local target'],
  ['<img srcset="/missing.png 1x, /other.png 2x">', 'Missing local target'],
  ['<iframe src="/missing.pdf"></iframe>', 'Missing local target'],
  ['<a href="javascript:alert(1)">Bad</a>', 'Unsafe URL'],
])('rejects local URL/fragment defects: %s', async (extra, message) => {
  const { dist, entry, html } = await pageFixture();
  await put(
    join(dist, entry.route, 'index.html'),
    html.replace('</article>', `${extra}</article>`),
  );
  expect(
    (await verifyOutput(dist)).some((item) => item.message.includes(message)),
  ).toBe(true);
});
it('validates aliases, canonical targets and immutable source-action structure', async () => {
  const { site, dist, entry, html } = await pageFixture({ aliases: ['/old/'] });
  await put(
    join(dist, 'old/index.html'),
    `<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=${entry.route}"><a href="${entry.route}">Continue</a>`,
  );
  expect(await verifyOutput(dist)).toEqual([]);
  await put(
    join(dist, entry.route, 'index.html'),
    html
      .replace('View original source', 'Lost source')
      .replace(
        '</article>',
        '<link rel="canonical" href="https://other.example/wrong/"/></article>',
      ),
  );
  const diagnostics = await verifyOutput(dist);
  expect(
    diagnostics.some((item) => item.message.includes('source action')),
  ).toBe(true);
  expect(diagnostics.some((item) => item.message.includes('canonical'))).toBe(
    true,
  );
  expect(
    await readFile(join(site, '.generated/current/manifest.json'), 'utf8'),
  ).toContain('Books/note.md');
});
it('rejects stale pages, unknown assets, excluded sources, draft remnants and deployed internal ledger', async () => {
  const { site, dist, manifest } = await output();
  manifest.entries = [note({ draft: true })];
  manifest.ledger = [
    {
      sourcePath: 'Books/private.md',
      disposition: 'excluded',
      reason: 'draft',
    },
  ];
  await put(
    join(site, '.generated/current/manifest.json'),
    JSON.stringify(manifest),
  );
  await put(
    join(dist, 'notes/books/note/index.html'),
    '<article data-pagefind-body>Draft</article>',
  );
  await put(join(dist, 'notes/books/private/index.html'), '<p>Excluded</p>');
  await put(
    join(dist, 'content/migration-report.json'),
    JSON.stringify(manifest.ledger),
  );
  const diagnostics = await verifyOutput(dist);
  expect(diagnostics.some((item) => item.message.includes('Draft'))).toBe(true);
  expect(
    diagnostics.some((item) => item.message.includes('Unexpected output')),
  ).toBe(true);
  expect(diagnostics.some((item) => item.message.includes('internal'))).toBe(
    true,
  );
});
it('detects stale Pagefind URLs, count mismatches and malformed fragments', async () => {
  const { dist } = await pageFixture();
  await put(
    join(dist, 'pagefind/fragment/en_stale.pf_fragment'),
    gzipSync(
      'pagefind_dcd{"url":"/notes/books/deleted/","content":"Deleted","meta":{}}',
    ),
  );
  expect(
    (await verifyOutput(dist)).some((item) =>
      item.message.includes('Stale Pagefind'),
    ),
  ).toBe(true);
  const fragment = (await readdir(join(dist, 'pagefind/fragment'))).find(
    (file) => file !== 'en_stale.pf_fragment',
  )!;
  await put(join(dist, 'pagefind/fragment', fragment), 'not gzip');
  expect(
    (await verifyOutput(dist)).some((item) =>
      item.message.includes('Pagefind fragment'),
    ),
  ).toBe(true);
  const indexPath = join(dist, 'pagefind/pagefind-entry.json');
  const index = JSON.parse(await readFile(indexPath, 'utf8'));
  index.languages.en.page_count = 2;
  await put(indexPath, JSON.stringify(index));
  expect(
    (await verifyOutput(dist)).some((item) =>
      item.message.includes('Pagefind count'),
    ),
  ).toBe(true);
});
it('checks CSS resource URLs and rejects symlinks without removing unrelated files', async () => {
  const { root, dist } = await output();
  await put(
    join(dist, '_astro/styles.css'),
    'body{background:url("/missing.png")}',
  );
  expect(
    (await verifyOutput(dist)).some((item) =>
      item.message.includes('Missing local target'),
    ),
  ).toBe(true);
  const original = join(root, 'keep.txt');
  await writeFile(original, 'Keep');
  await symlink(original, join(dist, 'unsafe.txt'));
  expect(
    (await verifyOutput(dist)).some((item) =>
      item.message.includes('symbolic'),
    ),
  ).toBe(true);
  expect(await readFile(original, 'utf8')).toBe('Keep');
});

it('detects a same-title stale Pagefind body against actual generated HTML', async () => {
  const { dist, entry, html } = await pageFixture();
  await put(
    join(dist, entry.route, 'index.html'),
    html.replace('</article>', '<p>Changed orchard sentinel.</p></article>'),
  );
  expect(
    (await verifyOutput(dist)).some((item) =>
      item.message.includes('Stale Pagefind artifact'),
    ),
  ).toBe(true);
});

it('rejects same-count native Pagefind filter membership corruption', async () => {
  const { dist } = await pageFixture();
  const name = (await readdir(join(dist, 'pagefind/filter')))[0]!;
  const file = join(dist, 'pagefind/filter', name);
  const original = gunzipSync(await readFile(file));
  const record = decode(original.subarray(12)) as [
    string,
    [string, number[]][],
  ];
  record[1][0]![0] = 'wrong-membership';
  await writeFile(
    file,
    gzipSync(Buffer.concat([Buffer.from('pagefind_dcd'), encode(record)])),
  );
  expect(
    (await verifyOutput(dist)).some((item) =>
      item.message.includes('Pagefind semantic'),
    ),
  ).toBe(true);
});
it.each(['frame', 'truncated', 'shape', 'version', 'orphan'])(
  'rejects native Pagefind metadata %s corruption',
  async (fault) => {
    const { dist } = await pageFixture();
    const name = (await readdir(join(dist, 'pagefind'))).find((file) =>
      file.endsWith('.pf_meta'),
    )!;
    const file = join(dist, 'pagefind', name);
    const original = gunzipSync(await readFile(file));
    if (fault === 'frame')
      await writeFile(file, gzipSync(Buffer.from('wrong-frame')));
    else if (fault === 'truncated')
      await writeFile(file, gzipSync(original.subarray(0, 16)));
    else if (fault === 'shape')
      await writeFile(
        file,
        gzipSync(
          Buffer.concat([Buffer.from('pagefind_dcd'), encode(['1.5.2'])]),
        ),
      );
    else if (fault === 'version') {
      const record = decode(original.subarray(12)) as unknown[];
      record[0] = 'old';
      await writeFile(
        file,
        gzipSync(Buffer.concat([Buffer.from('pagefind_dcd'), encode(record)])),
      );
    } else
      await writeFile(
        join(dist, 'pagefind/pagefind.en_orphan.pf_meta'),
        await readFile(file),
      );
    expect(
      (await verifyOutput(dist)).some((item) =>
        /Pagefind semantic|Orphan Pagefind/.test(item.message),
      ),
    ).toBe(true);
  },
);

it('rejects a symlink output root and an actual non-regular FIFO without reading or modifying them', async () => {
  const { dist, root } = await output();
  const target = join(root, 'private');
  await mkdir(target);
  await writeFile(join(target, 'preserve.txt'), 'Private retained');
  await rm(dist, { recursive: true });
  await symlink(target, dist);
  expect(await verifyOutput(dist)).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        message: 'Unsafe symbolic link or non-directory output',
      }),
    ]),
  );
  expect(await readFile(join(target, 'preserve.txt'), 'utf8')).toBe(
    'Private retained',
  );
  const other = await output();
  execFileSync('mkfifo', [join(other.dist, 'pipe')]);
  expect(await verifyOutput(other.dist)).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        sourcePath: 'pipe',
        message: 'Unsafe non-regular output',
      }),
    ]),
  );
});
it('rejects encoded unsafe local URLs, missing reader markers and absent route/alias output', async () => {
  const { dist, entry, html } = await pageFixture({ aliases: ['/old-note/'] });
  await put(
    join(dist, entry.route, 'index.html'),
    html
      .replace('data-pagefind-body', 'data-ignored')
      .replace(
        '</article>',
        '<a href="/%5cunsafe">slash</a><a href="/%00unsafe">null</a><a href="/%ZZ">bad encoding</a><img src="data:image/png;base64,AA=="></article>',
      ),
  );
  const errors = await verifyOutput(dist);
  expect(errors.map((x) => x.message)).toEqual(
    expect.arrayContaining([
      expect.stringContaining('Reader is missing'),
      expect.stringContaining('Unsafe URL: /%5c'),
      expect.stringContaining('Unsafe URL: /%00'),
      expect.stringContaining('Unsafe URL: /%ZZ'),
    ]),
  );
  await rm(join(dist, entry.route), { recursive: true });
  expect(await verifyOutput(dist)).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        sourcePath: 'notes/books/note/index.html',
        message: 'Missing expected output file',
      }),
    ]),
  );
});
it.each(['robots', 'refresh', 'link'])(
  'rejects an alias missing its %s contract',
  async (fault) => {
    const { dist, entry } = await pageFixture({ aliases: ['/old-note/'] });
    await put(
      join(dist, '/old-note/index.html'),
      `<html><head>${fault === 'robots' ? '' : '<meta name="robots" content="noindex">'}${fault === 'refresh' ? '' : `<meta http-equiv="refresh" content="0;url=${entry.route}">`}</head><body>${fault === 'link' ? '' : `<a href="${entry.route}">Read note</a>`}</body></html>`,
    );
    expect(await verifyOutput(dist)).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          sourcePath: entry.sourcePath,
          message: 'Malformed alias: /old-note/',
        }),
      ]),
    );
  },
);
it('validates exact canonical targets for configured output without altering indexed article content', async () => {
  const { dist, entry, html } = await pageFixture();
  vi.stubEnv('SITE_URL', 'https://notes.example.test');
  try {
    await put(join(dist, 'sitemap.xml'), '<?xml version="1.0"?><urlset/>');
    const canonical = `<head><link rel="canonical" href="https://notes.example.test${entry.route}"></head>`;
    await put(
      join(dist, entry.route, 'index.html'),
      html.replace('<body>', `${canonical}<body>`),
    );
    expect(await verifyOutput(dist)).toEqual([]);
    await put(
      join(dist, entry.route, 'index.html'),
      html.replace(
        '<body>',
        '<head><link rel="canonical" href="https://notes.example.test/wrong/"></head><body>',
      ),
    );
    expect(await verifyOutput(dist)).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          message: `Invalid canonical for ${entry.route}`,
        }),
      ]),
    );
  } finally {
    vi.unstubAllEnvs();
  }
});
it.each(['iframe', 'download'])(
  'rejects an oversized PDF with a local %s action and an untracked resource asset',
  async (kind) => {
    const { dist, entry, html } = await pageFixture({
      kind: 'pdf',
      bytes: 26_214_401,
      assetUrl: '/content-assets/untracked.pdf',
    });
    const action =
      kind === 'iframe'
        ? '<iframe src="/content-assets/untracked.pdf"></iframe>'
        : '<a href="/content-assets/untracked.pdf">Download</a>';
    await put(
      join(dist, entry.route, 'index.html'),
      html.replace('</article>', `${action}</article>`),
    );
    expect(await verifyOutput(dist)).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          message: 'Resource asset is missing from manifest',
        }),
        expect.objectContaining({
          message: 'Oversized resource has a local source action',
        }),
      ]),
    );
  },
);
it('validates draft absence, named anchors and HTTPS source actions through parsed output', async () => {
  const { site, dist, entry, html, manifest } = await pageFixture({
    sourceUrl: 'http://example.test/source',
  });
  await put(
    join(dist, entry.route, 'index.html'),
    html
      .replace(
        'View original source',
        '<!--Label comment-->View original source',
      )
      .replace(
        '</article>',
        '<a name="named">Named anchor</a><a href="#named">Read</a></article>',
      ),
  );
  manifest.entries.push(note({ draft: true, sourcePath: 'Books/draft.md' }));
  await writeFile(
    join(site, '.generated/current/manifest.json'),
    JSON.stringify(manifest),
  );
  expect(await verifyOutput(dist)).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        message: 'Draft entry leaked into prepared publication',
      }),
      expect.objectContaining({
        message: 'Malformed or missing original source action',
      }),
    ]),
  );
});
it.each(['success', 'diagnostic', 'exception'])(
  'executes actual output CLI %s with isolated fixture paths',
  async (mode) => {
    const { dist } = await output();
    if (mode === 'diagnostic')
      await put(join(dist, 'stale.html'), '<p>Stale</p>');
    const argv = process.argv;
    const exitCode = process.exitCode;
    const error = vi.spyOn(console, 'error').mockImplementation(() => {});
    const log = vi.spyOn(console, 'log').mockImplementation(() => {});
    process.argv = [
      process.execPath,
      new URL('../../scripts/verify-output.ts', import.meta.url).pathname,
      mode === 'exception' ? join(dist, 'missing') : dist,
    ];
    vi.resetModules();
    try {
      await import('../../scripts/verify-output.js');
      expect(process.exitCode).toBe(mode === 'success' ? 0 : 1);
      if (mode === 'success')
        expect(log).toHaveBeenCalledWith(
          expect.stringContaining('Verified production'),
        );
      else expect(error).toHaveBeenCalled();
    } finally {
      process.argv = argv;
      process.exitCode = exitCode;
      vi.restoreAllMocks();
    }
  },
);

async function privateResourceFixture(kind: 'pdf' | 'slides') {
  const actual = JSON.parse(
    await readFile('.generated/current/manifest.json', 'utf8'),
  ) as Manifest;
  const resource = actual.entries.find(
    (entry) =>
      entry.kind === kind && entry.assetUrl?.startsWith('/content-assets/'),
  )!;
  const asset = {
    ...actual.assets.find((asset) => asset.sourcePath === resource.sourcePath)!,
  };
  const fixture = await pageFixture({ ...resource, sourceUrl: asset.url });
  fixture.manifest.assets = [asset];
  await put(
    join(fixture.site, '.generated/current/manifest.json'),
    JSON.stringify(fixture.manifest),
  );
  const policyPath = join(fixture.site, 'content/publication.json');
  const policy = JSON.parse(await readFile(policyPath, 'utf8'));
  await put(policyPath, JSON.stringify({ ...policy, repositoryPublic: false }));
  await put(
    join(fixture.dist, asset.url.slice(1)),
    await readFile(join(process.cwd(), 'dist', asset.url.slice(1))),
  );
  return { ...fixture, asset };
}

it.each(['pdf', 'slides'] as const)(
  'accepts a private %s source action pointing to its real published local asset',
  async (kind) => {
    const { dist } = await privateResourceFixture(kind);
    expect(await verifyOutput(dist)).toEqual([]);
  },
);

it.each([
  'different-source',
  'external-mode',
  'missing-file',
  'unhashed-url',
  'reader-asset-mismatch',
])(
  'rejects a local original-source action with an invalid matching asset: %s',
  async (fault) => {
    const { site, dist, entry, html, manifest, asset } =
      await privateResourceFixture('pdf');
    if (fault === 'different-source') asset.sourcePath = 'Books/another.pdf';
    else if (fault === 'external-mode') asset.mode = 'external';
    else if (fault === 'missing-file') await rm(join(dist, asset.url.slice(1)));
    else if (fault === 'unhashed-url') {
      await put(
        join(dist, 'content-assets/unhashed.pdf'),
        await readFile(join(dist, asset.url.slice(1))),
      );
      const originalUrl = asset.url;
      asset.url = '/content-assets/unhashed.pdf';
      entry.sourceUrl = asset.url;
      entry.assetUrl = asset.url;
      await put(
        join(dist, entry.route, 'index.html'),
        html.replaceAll(originalUrl, asset.url),
      );
    } else entry.assetUrl = '/content-assets/' + 'f'.repeat(64) + '.pdf';
    await put(
      join(site, '.generated/current/manifest.json'),
      JSON.stringify(manifest),
    );
    expect(await verifyOutput(dist)).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          sourcePath: entry.sourcePath,
          message: 'Malformed or missing original source action',
        }),
      ]),
    );
  },
);

it('rejects retained real reader, alias and native search records when current exclusions win over an override', async () => {
  const actual = JSON.parse(
    await readFile('.generated/current/manifest.json', 'utf8'),
  ) as Manifest;
  const resource = actual.entries.find((entry) => entry.kind === 'markdown')!;
  const { site, dist, entry } = await pageFixture({
    ...resource,
    aliases: ['/excluded-real-note/'],
  });
  await put(
    join(dist, 'excluded-real-note/index.html'),
    `<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=${entry.route}"><a href="${entry.route}">Continue</a>`,
  );
  expect(await verifyOutput(dist)).toEqual([]);
  const policyPath = join(site, 'content/publication.json');
  const policy = JSON.parse(await readFile(policyPath, 'utf8'));
  await put(
    policyPath,
    JSON.stringify({
      ...policy,
      exclude: [entry.sourcePath],
      overrides: {
        [entry.sourcePath]: { title: entry.title, aliases: entry.aliases },
      },
    }),
  );
  const diagnostics = await verifyOutput(dist);
  expect(diagnostics).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        sourcePath: entry.sourcePath,
        message: expect.stringContaining('Excluded entry'),
      }),
      expect.objectContaining({
        sourcePath: entry.route.slice(1) + 'index.html',
        message: expect.stringContaining('Unexpected output'),
      }),
      expect.objectContaining({
        sourcePath: 'excluded-real-note/index.html',
        message: expect.stringContaining('Unexpected output'),
      }),
      expect.objectContaining({
        message: expect.stringContaining('Stale Pagefind URL'),
      }),
      expect.objectContaining({
        message: expect.stringContaining('Pagefind count mismatch'),
      }),
    ]),
  );
});

it.each(['policy', 'mandatory'])(
  'rejects a retained local manifest asset excluded by %s even with an override',
  async (kind) => {
    const actual = JSON.parse(
      await readFile('.generated/current/manifest.json', 'utf8'),
    ) as Manifest;
    const originalAsset = actual.assets.find(
      (asset) => asset.mode === 'local' && asset.url.endsWith('.png'),
    )!;
    const { site, dist, manifest } = await pageFixture();
    const asset = {
      ...originalAsset,
      sourcePath:
        kind === 'mandatory'
          ? 'Books/node_modules/retained.png'
          : originalAsset.sourcePath,
    };
    manifest.assets = [asset];
    await put(
      join(site, '.generated/current/manifest.json'),
      JSON.stringify(manifest),
    );
    await put(
      join(dist, asset.url.slice(1)),
      await readFile(join(process.cwd(), 'dist', originalAsset.url.slice(1))),
    );
    if (kind === 'policy') expect(await verifyOutput(dist)).toEqual([]);
    const policyPath = join(site, 'content/publication.json');
    const policy = JSON.parse(await readFile(policyPath, 'utf8'));
    await put(
      policyPath,
      JSON.stringify({
        ...policy,
        exclude: kind === 'policy' ? [asset.sourcePath] : [],
        overrides: {
          [asset.sourcePath]: {
            resourceUrl: 'https://cdn.example.test/retained.png',
          },
        },
      }),
    );
    expect(await verifyOutput(dist)).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          sourcePath: asset.sourcePath,
          message: expect.stringContaining('Excluded asset'),
        }),
        expect.objectContaining({
          sourcePath: asset.url.slice(1),
          message: expect.stringContaining('Unexpected output'),
        }),
      ]),
    );
  },
);
