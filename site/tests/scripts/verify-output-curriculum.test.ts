import { mkdir, mkdtemp, rename, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import { verifyOutput } from '../../scripts/verify-output.js';
import { prepareCurriculum } from '../../src/content/leetcode/prepare.js';
import {
  prepareFixture,
  sourceEntry,
} from '../src/content/leetcode/prepare-fixtures.js';

// Curriculum Pagefind coverage is owned by its renderer task.
vi.mock('../../scripts/verify-pagefind.js', () => ({
  verifyPagefind: async () => [],
}));

const roots: string[] = [];
afterEach(async () => {
  vi.unstubAllEnvs();
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});

async function put(path: string, contents: string) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, contents);
}

const siteUrl = 'https://notes.example.test';
const organization = [
  '/library/topics/',
  '/library/collections/',
  '/library/paths/',
];
const sections = [
  'Books',
  'Classes',
  'Courses',
  'Interview',
  'Languages',
  'Tutorials',
];
const baseRoutes = [
  '/',
  '/library/',
  '/library/tree/',
  '/search/',
  ...organization,
  ...sections.map((section) => `/library/${section.toLowerCase()}/`),
];
const elected = '/practice/leetcode/1/';

async function output() {
  vi.stubEnv('SITE_URL', siteUrl);
  const site = await mkdtemp(join(tmpdir(), 'notes-output-curriculum-'));
  roots.push(site);
  const dist = join(site, 'dist');
  const generated = join(site, '.generated');
  const { definition, outputDir, ...context } = await prepareFixture(site);
  const snapshot = await prepareCurriculum(definition, {
    ...context,
    outputDir,
  });
  const directory = join(generated, `curriculum-${snapshot.generation}`);
  await mkdir(generated);
  await rename(outputDir, directory);
  const manifest = {
    version: 1,
    entries: [],
    assets: [],
    ledger: [],
    curriculumGeneration: snapshot.generation,
  };
  const writeManifest = (
    entries = manifest.entries as ReturnType<typeof sourceEntry>[],
  ) =>
    put(
      join(generated, 'current/manifest.json'),
      JSON.stringify({ ...manifest, entries }),
    );
  const page = (route: string, body = 'Fixture') =>
    put(
      join(dist, route, 'index.html'),
      `<html><head><link rel="canonical" href="${siteUrl}${route}"></head><body>${body}</body></html>`,
    );
  const sitemap = (...routes: string[]) =>
    put(
      join(dist, 'sitemap.xml'),
      `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${[...baseRoutes, ...routes].map((route) => `<url><loc>${siteUrl}${route}</loc></url>`).join('')}</urlset>`,
    );
  await writeManifest();
  await put(
    join(site, 'content/publication.json'),
    JSON.stringify({ roots: sections }),
  );
  await put(
    join(dist, '404.html'),
    '<html><head><meta name="robots" content="noindex"></head><body>Not found</body></html>',
  );
  for (const route of baseRoutes) await page(route);
  await sitemap();
  return { dist, directory, writeManifest, page, sitemap };
}

it('checks a selected Worker separately and accepts only explicitly elected fixture pages and sitemap locations', async () => {
  const { dist, directory, page, sitemap } = await output();
  expect(await verifyOutput(dist)).toEqual([]);
  expect(await verifyOutput(dist, [elected])).toContainEqual({
    sourcePath: 'practice/leetcode/1/index.html',
    message: 'Missing expected output file',
  });
  await page(elected);
  expect(await verifyOutput(dist)).toContainEqual({
    sourcePath: 'practice/leetcode/1/index.html',
    message: 'Unexpected output file: stale page, asset, or excluded content',
  });
  expect(await verifyOutput(dist, [elected])).toContainEqual({
    sourcePath: 'sitemap.xml',
    message: 'Sitemap differs from canonical published routes',
  });
  await sitemap(elected);
  expect(await verifyOutput(dist, [elected])).toEqual([]);
  await rm(join(directory, 'trace-assets.json'));
  expect(await verifyOutput(dist, [elected])).toContainEqual(
    expect.objectContaining({
      message: expect.stringMatching(/trace-assets\.json/),
    }),
  );
});

it('rejects a normalized alias collision even when neither curriculum renderer is enabled', async () => {
  const { dist, writeManifest } = await output();
  await writeManifest([sourceEntry({ aliases: ['/PRACTICE/LEETCODE/1//'] })]);
  expect(await verifyOutput(dist)).toContainEqual(
    expect.objectContaining({
      message: expect.stringMatching(/Route collision.*practice\/leetcode\/1/i),
    }),
  );
});

it('rejects leaked Worker assets and metadata even under otherwise permitted Pages paths', async () => {
  const { dist } = await output();
  const leaks = [
    'practice-traces/test.json',
    'pagefind/progress-registry.json',
    'pagefind/trace-assets.json',
    'pagefind/curriculum.json',
    'worker-assets/private.json',
  ];
  for (const file of leaks) await put(join(dist, file), '{}');
  const diagnostics = await verifyOutput(dist);
  for (const sourcePath of leaks)
    expect(diagnostics).toContainEqual(
      expect.objectContaining({
        sourcePath,
        message: 'Deployed internal publication data',
      }),
    );
});

it('keeps the Worker namespace reservation at the site root', async () => {
  const { dist, page, sitemap, writeManifest } = await output();
  const entry = sourceEntry({ route: '/resources/interview/practice-traces/' });
  await writeManifest([entry]);
  await page(entry.route, '<main data-pagefind-body>Fixture</main>');
  await sitemap(entry.route);
  expect(await verifyOutput(dist)).toEqual([]);
});
