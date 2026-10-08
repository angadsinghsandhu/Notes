import { defineConfig } from 'astro/config';
import { fileURLToPath } from 'node:url';
import { watchFile, unwatchFile } from 'node:fs';
import { lstat, readFile, realpath } from 'node:fs/promises';
import { resolve } from 'node:path';

const site = process.env['SITE_URL'];
if (site) {
  const url = new URL(site);
  if (
    url.protocol !== 'https:' ||
    url.username ||
    url.password ||
    url.search ||
    url.hash
  )
    throw new Error(
      'SITE_URL must be an explicit HTTPS URL without credentials, query, or fragment',
    );
}

export default defineConfig({
  output: 'static',
  ...(site ? { site } : {}),
  // Astro7 captures inlined script bytes before Vite8 resolves dynamic-import
  // preload markers. External modules complete that pass and cache across readers.
  vite: {
    build: { assetsInlineLimit: 0 },
    plugins: [
      {
        name: 'notes-prepared-snapshot',
        apply: 'serve',
        configureServer(server) {
          const manifest = fileURLToPath(
            new URL('./.generated/current/manifest.json', import.meta.url),
          );
          const catalog = fileURLToPath(
            new URL('./src/lib/catalog.ts', import.meta.url),
          );
          // The snapshot is an explicit facade dependency. Vite's normal
          // source-change path invalidates the facade and its SSR importers.
          // Atomic manifest replacements must remain observable after inode changes.
          const refresh = (current) => {
            if (current.isFile()) server.watcher.emit('change', catalog);
          };
          watchFile(manifest, { interval: 1000, persistent: false }, refresh);
          const indexRoot = fileURLToPath(
            new URL('./dist/pagefind', import.meta.url),
          );
          server.middlewares.use(
            '/pagefind',
            async (request, response, next) => {
              if (!['GET', 'HEAD'].includes(request.method ?? ''))
                return next();
              try {
                const path = decodeURIComponent(
                  (request.url ?? '').split('?')[0],
                );
                if (
                  !/^\/[a-zA-Z0-9_./-]+$/.test(path) ||
                  path.split('/').some((part) => part === '.' || part === '..')
                )
                  throw new Error('Invalid index path');
                const file = resolve(indexRoot, `.${path}`);
                const rootStat = await lstat(indexRoot);
                const stat = await lstat(file);
                if (
                  !rootStat.isDirectory() ||
                  rootStat.isSymbolicLink() ||
                  !stat.isFile() ||
                  stat.isSymbolicLink() ||
                  !file.startsWith(`${indexRoot}/`) ||
                  (await realpath(file)) !== file
                )
                  throw new Error('Unavailable index file');
                const mime = path.startsWith('/wasm.')
                  ? 'application/wasm'
                  : path.endsWith('.js')
                    ? 'text/javascript'
                    : path.endsWith('.json')
                      ? 'application/json'
                      : path.endsWith('.css')
                        ? 'text/css'
                        : 'application/octet-stream';
                response.setHeader('Content-Type', mime);
                response.setHeader('Cache-Control', 'no-store');
                response.end(
                  request.method === 'HEAD' ? undefined : await readFile(file),
                );
              } catch {
                response.statusCode = 404;
                response.end(
                  'Search index unavailable. Run npm run build and npm run preview.',
                );
              }
            },
          );
          server.httpServer?.once('close', () => {
            unwatchFile(manifest, refresh);
          });
        },
      },
    ],
  },
});
