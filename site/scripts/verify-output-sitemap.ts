import { SaxesParser } from 'saxes';

export function verifySitemap(
  xml: string,
  siteUrl: string,
  routes: readonly string[],
): void {
  const expectedUrls = new Set(
    routes.map((route) => new URL(route, siteUrl).href),
  );
  const urls: string[] = [];
  let location: string | undefined;
  const namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9';
  const tags: string[] = [];
  const parser = new SaxesParser({ xmlns: true });
  parser.on('opentag', ({ local, uri }) => {
    const tag = uri === namespace ? local : '';
    tags.push(tag);
    const path = tags.join('/');
    if (tags.length === 1 && tag !== 'urlset')
      throw new Error('Invalid sitemap root');
    if (path === 'urlset/url/loc') {
      if (location !== undefined) throw new Error('Repeated location');
      location = '';
    } else if (path.startsWith('urlset/url/loc/'))
      throw new Error('Nested location content');
  });
  const append = (value: string) => {
    if (tags.join('/') === 'urlset/url/loc') location += value;
  };
  parser.on('text', append);
  parser.on('cdata', append);
  parser.on('closetag', () => {
    if (tags.join('/') === 'urlset/url') {
      if (!location) throw new Error('Missing location');
      urls.push(location);
      location = undefined;
    }
    tags.pop();
  });
  parser.write(xml).close();
  if (
    urls.length !== expectedUrls.size ||
    new Set(urls).size !== urls.length ||
    urls.some((url) => !expectedUrls.has(url))
  )
    throw new Error('Sitemap membership mismatch');
}
