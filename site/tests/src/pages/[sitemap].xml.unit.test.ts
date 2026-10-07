import { expect, it, vi, afterEach } from 'vitest';
import type { APIContext } from 'astro';
import { GET, getStaticPaths } from '../../../src/pages/[sitemap].xml.js';
vi.mock('../../../src/lib/catalog.js', () => ({
  sectionLabels: { tutorials: 'Tutorials' },
  readPreparedCatalog: vi.fn(async () => ({
    listEntries: () => [{ route: '/notes/tutorials/a&b/' }],
  })),
}));
afterEach(() => vi.unstubAllEnvs());
it('emits paths only with explicit site configuration', async () => {
  vi.stubEnv('SITE', undefined);
  expect(await getStaticPaths()).toEqual([]);
  vi.stubEnv('SITE', 'https://notes.example.test');
  expect(await getStaticPaths()).toEqual([{ params: { sitemap: 'sitemap' } }]);
});
it('returns 404 without a site and XML-escapes actual catalog URLs', async () => {
  expect((await GET({ site: undefined } as APIContext)).status).toBe(404);
  const response = await GET({
    site: new URL('https://notes.example.test'),
  } as APIContext);
  expect(response.headers.get('content-type')).toBe(
    'application/xml; charset=utf-8',
  );
  const body = await response.text();
  expect(body).toContain(
    '<loc>https://notes.example.test/library/tutorials/</loc>',
  );
  expect(body).toContain('/notes/tutorials/a&amp;b/');
  expect(body).not.toContain('/notes/tutorials/a&b/');
});
