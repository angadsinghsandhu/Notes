import { decode, encode } from 'cbor-x';
import { createIndex, close } from 'pagefind';
import { gunzipSync, gzipSync } from 'node:zlib';
import {
  mkdtemp,
  mkdir,
  readFile,
  writeFile,
  readdir,
  rm,
  symlink,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
const nativeFault = vi.hoisted(() => ({ mode: '' }));
vi.mock('pagefind', async (original) => {
  const native = await original<typeof import('pagefind')>();
  return {
    ...native,
    createIndex: async () => {
      if (nativeFault.mode === 'missing-index') return { errors: [] };
      const result = await native.createIndex();
      if (nativeFault.mode === 'create-error')
        return { ...result, errors: ['Native create failure'] };
      if (result.index && nativeFault.mode === 'add-throw')
        result.index.addDirectory = async () => {
          throw 'Native directory failure';
        };
      if (result.index && nativeFault.mode === 'add-error') {
        const add = result.index.addDirectory.bind(result.index);
        result.index.addDirectory = async (options) => ({
          ...(await add(options)),
          errors: ['Native add failure'],
        });
      }
      return result;
    },
  };
});
import { verifyPagefind } from '../../scripts/verify-pagefind.js';
import type { Manifest } from '../../src/content/index.js';
const dirs: string[] = [];
afterEach(async () => {
  nativeFault.mode = '';
  for (const dir of dirs.splice(0))
    await rm(dir, { recursive: true, force: true });
});
async function fixture() {
  const manifest = JSON.parse(
    await readFile('.generated/current/manifest.json', 'utf8'),
  ) as Manifest;
  const entry = manifest.entries.find(
    (entry) =>
      entry.sourcePath ===
      'Courses/Scrimba/Learn React/src/projects/01-first-react/README.md',
  )!;
  const dist = await mkdtemp(join(tmpdir(), 'notes-native-pagefind-'));
  dirs.push(dist);
  const path = join(dist, entry.route, 'index.html');
  await mkdir(dirname(path), { recursive: true });
  const html = await readFile(join('dist', entry.route, 'index.html'), 'utf8');
  await writeFile(path, html);
  const { index } = await createIndex();
  if (!index) throw new Error('Native Pagefind unavailable');
  try {
    await index.addDirectory({ path: dist });
    const generated = await index.getFiles();
    for (const file of generated.files) {
      const path = join(dist, 'pagefind', file.path);
      await mkdir(dirname(path), { recursive: true });
      await writeFile(path, file.content);
    }
  } finally {
    await index.deleteIndex();
    await close();
  }
  const metadata = (await readdir(join(dist, 'pagefind'))).find((path) =>
    path.endsWith('.pf_meta'),
  )!;
  return {
    dist,
    entry,
    path,
    html,
    metadata: join(dist, 'pagefind', metadata),
  };
}
it('accepts a real built Vite document indexed by the installed native producer', async () => {
  const { dist, entry } = await fixture();
  expect(await verifyPagefind(dist, [entry])).toEqual([]);
});
it.each([
  'membership',
  'frame',
  'shape',
  'version',
  'truncated',
  'orphan',
  'word-index',
  'body',
])('rejects actual native %s corruption', async (fault) => {
  const { dist, entry, metadata, path, html } = await fixture();
  if (fault === 'membership') {
    const file = join(
      dist,
      'pagefind/filter',
      (await readdir(join(dist, 'pagefind/filter')))[0]!,
    );
    const record = decode(gunzipSync(await readFile(file)).subarray(12)) as [
      string,
      [string, number[]][],
    ];
    record[1][0]![0] = 'wrong-member';
    await writeFile(
      file,
      gzipSync(Buffer.concat([Buffer.from('pagefind_dcd'), encode(record)])),
    );
  } else if (fault === 'frame')
    await writeFile(metadata, gzipSync(Buffer.from('wrong')));
  else if (fault === 'shape')
    await writeFile(
      metadata,
      gzipSync(Buffer.concat([Buffer.from('pagefind_dcd'), encode(['1.5.2'])])),
    );
  else if (fault === 'version') {
    const record = decode(
      gunzipSync(await readFile(metadata)).subarray(12),
    ) as unknown[];
    record[0] = 'old';
    await writeFile(
      metadata,
      gzipSync(Buffer.concat([Buffer.from('pagefind_dcd'), encode(record)])),
    );
  } else if (fault === 'truncated')
    await writeFile(
      metadata,
      gzipSync(gunzipSync(await readFile(metadata)).subarray(0, 16)),
    );
  else if (fault === 'orphan')
    await writeFile(
      join(dist, 'pagefind/pagefind.en_orphan.pf_meta'),
      await readFile(metadata),
    );
  else if (fault === 'word-index')
    await writeFile(
      join(
        dist,
        'pagefind/index',
        (await readdir(join(dist, 'pagefind/index')))[0]!,
      ),
      Buffer.from('broken'),
    );
  else
    await writeFile(
      path,
      html.replace(
        '</article>',
        '<p>Added actual body sentinel.</p></article>',
      ),
    );
  expect((await verifyPagefind(dist, [entry])).length).toBeGreaterThan(0);
});

it('accepts no index for an empty publication and rejects unsafe native artifacts', async () => {
  const { dist, entry } = await fixture();
  const missing = join(dist, 'missing');
  expect(await verifyPagefind(missing, [])).toEqual([]);
  await symlink(
    join(dist, 'pagefind/pagefind.js'),
    join(dist, 'pagefind/unsafe.js'),
  );
  expect(await verifyPagefind(dist, [entry])).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        message: 'Unsafe Pagefind symbolic link or non-file',
      }),
    ]),
  );
});
it.each([
  'url',
  'title',
  'fragment-json',
  'duplicate-fragment',
  'entry-missing',
  'language',
  'configuration',
  'meta-missing',
  'filter-missing',
  'filter-name',
  'filter-values',
  'filter-ids',
  'duplicate-ids',
  'duplicate-filters',
  'wasm',
  'count',
  'native-js-missing',
])(
  'rejects %s corruption of real native references and membership',
  async (fault) => {
    const { dist, entry, metadata } = await fixture();
    const framed = (value: unknown) =>
      gzipSync(Buffer.concat([Buffer.from('pagefind_dcd'), encode(value)]));
    const entryPath = join(dist, 'pagefind/pagefind-entry.json');
    const index = JSON.parse(await readFile(entryPath, 'utf8')) as {
      languages: Record<
        string,
        { hash: string; wasm: string; page_count: number }
      >;
      include_characters?: string[];
    };
    const language = Object.values(index.languages)[0]!;
    if (
      ['url', 'title', 'fragment-json', 'duplicate-fragment'].includes(fault)
    ) {
      const fragmentDir = join(dist, 'pagefind/fragment');
      const file = join(fragmentDir, (await readdir(fragmentDir))[0]!);
      if (fault === 'duplicate-fragment')
        await writeFile(
          join(fragmentDir, 'duplicate.pf_fragment'),
          await readFile(file),
        );
      else if (fault === 'fragment-json')
        await writeFile(file, gzipSync(Buffer.from('pagefind_dcd{invalid')));
      else {
        const record = JSON.parse(
          gunzipSync(await readFile(file))
            .subarray(12)
            .toString(),
        ) as { url: string; meta: { title: string } };
        if (fault === 'url') record.url = '/notes/excluded/';
        else record.meta.title = 'Stale title';
        await writeFile(
          file,
          gzipSync(Buffer.from(`pagefind_dcd${JSON.stringify(record)}`)),
        );
      }
    } else if (fault === 'entry-missing') await rm(entryPath);
    else if (fault === 'language') {
      index.languages['ja'] = language;
      await writeFile(entryPath, JSON.stringify(index));
    } else if (fault === 'configuration') {
      index.include_characters = ['!'];
      await writeFile(entryPath, JSON.stringify(index));
    } else if (fault === 'meta-missing') await rm(metadata);
    else if (fault === 'wasm' || fault === 'count') {
      if (fault === 'wasm') language.wasm = 'wrong';
      else language.page_count++;
      await writeFile(entryPath, JSON.stringify(index));
    } else if (fault === 'native-js-missing')
      await rm(join(dist, 'pagefind/pagefind.js'));
    else {
      const record = decode(
        gunzipSync(await readFile(metadata)).subarray(12),
      ) as [
        string,
        [string, number][],
        unknown[],
        [string, string][],
        unknown[],
        string[],
      ];
      const file = join(
        dist,
        'pagefind/filter',
        `${record[3][0]![1]}.pf_filter`,
      );
      if (fault === 'filter-missing') await rm(file);
      else if (fault === 'duplicate-filters') {
        record[3].push(record[3][0]!);
        await writeFile(metadata, framed(record));
      } else {
        const filter = decode(
          gunzipSync(await readFile(file)).subarray(12),
        ) as [string, [string, number[]][]];
        if (fault === 'filter-name') filter[0] = 'wrong';
        else if (fault === 'filter-values') filter[1].push(filter[1][0]!);
        else if (fault === 'filter-ids') filter[1][0]![1] = [record[1].length];
        else filter[1][0]![1] = [0, 0];
        await writeFile(file, framed(filter));
      }
    }
    const diagnostics = await verifyPagefind(dist, [entry]);
    expect(diagnostics.length).toBeGreaterThan(0);
    expect(diagnostics.map((x) => x.message).join(' ')).toMatch(
      /Stale|Malformed|semantic|count|artifact/,
    );
  },
);

it.each(['missing-index', 'create-error', 'add-error', 'add-throw'])(
  'fails closed and releases owned native indexes on %s producer failure',
  async (mode) => {
    const { dist, entry } = await fixture();
    nativeFault.mode = mode;
    const diagnostics = await verifyPagefind(dist, [entry]);
    expect(diagnostics).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          sourcePath: 'pagefind/.',
          message: expect.stringContaining('Cannot verify Pagefind'),
        }),
      ]),
    );
  },
);
