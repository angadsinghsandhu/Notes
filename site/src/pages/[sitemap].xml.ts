import type { APIContext } from 'astro';
import { readPreparedCatalog, sectionLabels } from '../lib/catalog.js';

export async function getStaticPaths() {
  return import.meta.env.SITE ? [{ params: { sitemap: 'sitemap' } }] : [];
}

export async function GET({ site }: APIContext): Promise<Response> {
  if (!site) return new Response(null, { status: 404 });
  const catalog = await readPreparedCatalog();
  const routes = [
    '/',
    '/library/',
    '/search/',
    ...Object.keys(sectionLabels).map((section) => `/library/${section}/`),
    ...catalog.listEntries().map((entry) => entry.route),
  ];
  const escape = (value: string) =>
    value
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('"', '&quot;');
  const urls = routes
    .map(
      (route) => `<url><loc>${escape(new URL(route, site).href)}</loc></url>`,
    )
    .join('');
  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls}</urlset>`,
    {
      headers: { 'Content-Type': 'application/xml; charset=utf-8' },
    },
  );
}
