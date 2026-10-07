import { decode } from 'cbor-x';
import { createIndex, close } from 'pagefind';
import { lstat, readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { gunzipSync } from 'node:zlib';
import { z } from 'zod';
import type { ContentEntry, Diagnostic } from '../src/content/index.js';

const hash = z.string().regex(/^[a-z0-9_-]+$/);
const integer = z.number().int().nonnegative();
const metadata = z.tuple([
  z.literal('1.5.2'),
  z.array(z.tuple([hash, integer])),
  z.array(z.tuple([z.string(), z.string(), hash])),
  z.array(z.tuple([z.string(), hash])),
  z.array(z.never()),
  z.array(z.string()),
]);
const filter = z.tuple([
  z.string(),
  z.array(z.tuple([z.string(), z.array(integer)])),
]);
const entrySchema = z
  .object({
    version: z.literal('1.5.2'),
    languages: z.record(
      z.string(),
      z.object({ hash, wasm: hash, page_count: integer }).strict(),
    ),
    include_characters: z.array(z.string()).optional(),
  })
  .strict();
const fragmentSchema = z
  .object({
    url: z.string(),
    meta: z.object({ title: z.string(), kind: z.string() }).passthrough(),
  })
  .passthrough();
function unpack(bytes: Uint8Array): Buffer {
  const decoded = gunzipSync(bytes);
  if (decoded.subarray(0, 12).toString() !== 'pagefind_dcd')
    throw new Error('Invalid Pagefind framing');
  return decoded.subarray(12);
}

/** Regenerate in memory with the native producer; never write or replace deployed files. */
export async function verifyPagefind(
  dist: string,
  entries: ContentEntry[],
): Promise<Diagnostic[]> {
  const diagnostics: Diagnostic[] = [];
  const fail = (file: string, message: string) =>
    diagnostics.push({ sourcePath: `pagefind/${file}`, message });
  const files = new Map<string, Uint8Array>();
  async function visit(directory: string, prefix = ''): Promise<void> {
    for (const name of await readdir(directory)) {
      const path = join(directory, name);
      const stat = await lstat(path);
      if (stat.isDirectory()) await visit(path, `${prefix}${name}/`);
      else if (stat.isFile())
        files.set(`${prefix}${name}`, await readFile(path));
      else
        fail(`${prefix}${name}`, 'Unsafe Pagefind symbolic link or non-file');
    }
  }
  try {
    await visit(join(dist, 'pagefind'));
  } catch (error) {
    if (
      entries.length ||
      !(error instanceof Error && 'code' in error && error.code === 'ENOENT')
    )
      fail('.', 'Missing Pagefind directory');
    return diagnostics;
  }
  const routes = new Map(entries.map((entry) => [entry.route, entry]));
  const urls = new Set<string>();
  for (const [path, bytes] of files)
    if (path.startsWith('fragment/')) {
      try {
        const record = fragmentSchema.parse(
          JSON.parse(unpack(bytes).toString()),
        );
        const entry = routes.get(record.url);
        if (!entry || urls.has(record.url))
          fail(path, `Stale Pagefind URL: ${record.url}`);
        else if (
          record.meta.title !== entry.title.replace(/\s+/g, ' ').trim() ||
          record.meta.kind !== entry.kind
        )
          fail(path, `Stale Pagefind metadata: ${record.url}`);
        urls.add(record.url);
      } catch {
        fail(path, 'Malformed Pagefind fragment');
      }
    }
  const created = await createIndex();
  try {
    if (!created.index || created.errors.length)
      throw new Error(
        created.errors.join('; ') || 'Native Pagefind unavailable',
      );
    const added = await created.index.addDirectory({ path: dist });
    const generated = await created.index.getFiles();
    if (added.errors.length || generated.errors.length)
      throw new Error([...added.errors, ...generated.errors].join('; '));
    const expected = new Map(
      generated.files.map((file) => [file.path, file.content]),
    );
    for (const [path, bytes] of expected)
      if (
        path !== 'pagefind-entry.json' &&
        !path.endsWith('.pf_meta') &&
        !path.startsWith('filter/')
      ) {
        if (!files.has(path) || !Buffer.from(bytes).equals(files.get(path)!))
          fail(
            path,
            'Stale Pagefind artifact: content does not match generated HTML',
          );
      }
    for (const path of files.keys())
      if (
        !path.endsWith('.pf_meta') &&
        !path.startsWith('filter/') &&
        !expected.has(path)
      )
        fail(path, 'Stale Pagefind artifact: obsolete fragment or word index');
    try {
      const entry = entrySchema.parse(
        JSON.parse(
          Buffer.from(files.get('pagefind-entry.json') ?? []).toString(),
        ),
      );
      const proposed = entrySchema.parse(
        JSON.parse(
          Buffer.from(expected.get('pagefind-entry.json') ?? []).toString(),
        ),
      );
      const count = Object.values(entry.languages).reduce(
        (sum, language) => sum + language.page_count,
        0,
      );
      if (count !== entries.length || urls.size !== entries.length)
        fail(
          'pagefind-entry.json',
          `Pagefind count mismatch: ${count} indexed/${urls.size} fragments/${entries.length} published`,
        );
      if (
        JSON.stringify(Object.keys(entry.languages).sort()) !==
          JSON.stringify(Object.keys(proposed.languages).sort()) ||
        JSON.stringify(entry.include_characters) !==
          JSON.stringify(proposed.include_characters)
      )
        throw new Error('Language/configuration mismatch');
      const referenced = new Set(['pagefind-entry.json']);
      const semantics = (
        bytes: Uint8Array,
        source: Map<string, Uint8Array>,
        referenced?: Set<string>,
      ) => {
        const record = metadata.parse(decode(unpack(bytes)) as unknown);
        const filters = record[3]
          .map(([name, hash]) => {
            const path = `filter/${hash}.pf_filter`;
            referenced?.add(path);
            const data = source.get(path);
            if (!data) throw new Error(`Missing filter ${path}`);
            const parsed = filter.parse(decode(unpack(data)) as unknown);
            if (
              parsed[0] !== name ||
              new Set(parsed[1].map(([value]) => value)).size !==
                parsed[1].length
            )
              throw new Error('Invalid filter identity');
            for (const [, ids] of parsed[1])
              if (
                ids.some((id) => id >= record[1].length) ||
                new Set(ids).size !== ids.length
              )
                throw new Error('Invalid filter page membership');
            return [
              name,
              parsed[1]
                .map(([value, ids]) => [value, [...ids].sort((a, b) => a - b)])
                .sort((a, b) => String(a[0]).localeCompare(String(b[0]))),
            ];
          })
          .sort((a, b) => String(a[0]).localeCompare(String(b[0])));
        if (new Set(record[3].map(([name]) => name)).size !== record[3].length)
          throw new Error('Duplicate filter identity');
        return JSON.stringify([
          record[0],
          record[1],
          record[2],
          filters,
          record[4],
          record[5],
        ]);
      };
      for (const [language, actual] of Object.entries(entry.languages)) {
        const target = `pagefind.${actual.hash}.pf_meta`;
        referenced.add(target);
        const proposedLanguage = proposed.languages[language]!;
        const expectedMeta = expected.get(
          `pagefind.${proposedLanguage.hash}.pf_meta`,
        )!;
        const bytes = files.get(target);
        if (!bytes) throw new Error(`Missing metadata ${target}`);
        if (
          actual.wasm !== proposedLanguage.wasm ||
          actual.page_count !== proposedLanguage.page_count ||
          semantics(bytes, files, referenced) !==
            semantics(expectedMeta, expected)
        )
          throw new Error(`Stale metadata/filter memberships for ${language}`);
        for (const path of [`wasm.${actual.wasm}.pagefind`, 'pagefind.js'])
          if (
            !files.has(path) ||
            !Buffer.from(expected.get(path) ?? []).equals(files.get(path)!)
          )
            throw new Error(`Missing/corrupt native artifact ${path}`);
      }
      for (const path of files.keys())
        if (
          (path.endsWith('.pf_meta') || path.startsWith('filter/')) &&
          !referenced.has(path)
        )
          fail(path, 'Orphan Pagefind metadata/filter artifact');
    } catch (error) {
      fail(
        'pagefind-entry.json',
        `Pagefind semantic verification failed: ${error instanceof Error ? error.message : String(error)}`,
      );
    }
  } catch (error) {
    fail(
      '.',
      `Cannot verify Pagefind: ${error instanceof Error ? error.message : String(error)}`,
    );
  } finally {
    if (created.index) await created.index.deleteIndex();
    await close();
  }
  return diagnostics;
}
