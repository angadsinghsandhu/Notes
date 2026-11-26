import { expect, it } from 'vitest';
import { verifySitemap } from '../../scripts/verify-output-sitemap.js';

it('validates escaped URL locations against the canonical route list', () => {
  const site = 'https://notes.example.test';
  const xml = `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>${site}/practice/a&amp;b/</loc></url></urlset>`;
  expect(() => verifySitemap(xml, site, ['/practice/a&b/'])).not.toThrow();
  expect(() => verifySitemap(xml, site, ['/'])).toThrow('membership');
});
