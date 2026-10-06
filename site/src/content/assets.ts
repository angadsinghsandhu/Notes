import { createHash } from 'node:crypto';
import {
  lstat,
  mkdir,
  readFile,
  readdir,
  realpath,
  rm,
  writeFile,
} from 'node:fs/promises';
import { extname, join, resolve } from 'node:path';
import { SaxesParser } from 'saxes';
import sharp from 'sharp';
import { discoverEntries } from './discover.js';
import { compareSourcePaths } from './identifiers.js';
import { publicSourceUrl } from './links.js';
import { CONTENT_ROOTS } from './schema.js';
import type { AssetRecord, PublicationPolicy } from './types.js';

export const MAX_LOCAL_ASSET_BYTES = 26_214_400;
const extensions = new Set([
  '.png',
  '.jpg',
  '.jpeg',
  '.gif',
  '.webp',
  '.avif',
  '.svg',
  '.ico',
  '.pdf',
  '.ppt',
  '.pptx',
]);
const svgElements = new Set([
  'svg',
  'g',
  'defs',
  'title',
  'desc',
  'path',
  'rect',
  'circle',
  'ellipse',
  'line',
  'polyline',
  'polygon',
  'text',
  'tspan',
  'textPath',
  'use',
  'symbol',
  'clipPath',
  'mask',
  'linearGradient',
  'radialGradient',
  'stop',
]);
const svgAttributes = new Set([
  'id',
  'viewBox',
  'preserveAspectRatio',
  'width',
  'height',
  'x',
  'y',
  'x1',
  'y1',
  'x2',
  'y2',
  'cx',
  'cy',
  'r',
  'rx',
  'ry',
  'd',
  'points',
  'transform',
  'fill',
  'fill-opacity',
  'fill-rule',
  'stroke',
  'stroke-width',
  'stroke-opacity',
  'stroke-linecap',
  'stroke-linejoin',
  'stroke-dasharray',
  'stroke-dashoffset',
  'opacity',
  'clip-path',
  'clip-rule',
  'mask',
  'offset',
  'stop-color',
  'stop-opacity',
  'gradientUnits',
  'gradientTransform',
  'spreadMethod',
  'font-family',
  'font-size',
  'font-weight',
  'text-anchor',
  'dominant-baseline',
  'dx',
  'dy',
  'href',
]);
const svgNamespace = 'http://www.w3.org/2000/svg';
function escape(value: string): string {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function sanitizeSvg(bytes: Buffer): Buffer {
  const parser = new SaxesParser({ xmlns: true });
  let output = '';
  const stack: boolean[] = [];
  let rootSeen = false;
  parser.on('doctype', () => {
    throw new Error('SVG DOCTYPE/entities are forbidden');
  });
  parser.on('opentag', (tag) => {
    if (!rootSeen) {
      rootSeen = true;
      if (tag.local !== 'svg' || (tag.uri && tag.uri !== svgNamespace))
        throw new Error('Expected SVG root element');
    }
    const keep =
      stack.every(Boolean) &&
      svgElements.has(tag.local) &&
      (!tag.uri || tag.uri === svgNamespace);
    stack.push(keep);
    if (!keep) return;
    output += `<${tag.local}`;
    if (stack.length === 1) output += ` xmlns="${svgNamespace}"`;
    for (const attribute of Object.values(tag.attributes)) {
      const name = attribute.local;
      if (
        !svgAttributes.has(name) ||
        (attribute.uri && attribute.uri !== 'http://www.w3.org/1999/xlink')
      )
        continue;
      const value = attribute.value;
      if (name === 'href' && !/^#[A-Za-z0-9_:-]+$/.test(value)) continue;
      // No CSS expressions, escaped CSS, external URLs or executable values.
      if (/javascript:|data:|https?:|expression|[\\<>]/i.test(value)) continue;
      if (/url\s*\(/i.test(value) && !/^url\(#[A-Za-z0-9_:-]+\)$/.test(value))
        continue;
      output += ` ${name}="${escape(value)}"`;
    }
    output += '>';
  });
  parser.on('text', (value) => {
    if (stack.every(Boolean)) output += escape(value);
  });
  parser.on('cdata', (value) => {
    if (stack.every(Boolean)) output += escape(value);
  });
  parser.on('closetag', (tag) => {
    if (stack.pop()) output += `</${tag.local}>`;
  });
  parser.write(bytes.toString('utf8')).close();
  if (!rootSeen) throw new Error('Missing SVG document');
  return Buffer.from(output);
}

async function verifiedSource(
  root: string,
  sourcePath: string,
): Promise<string> {
  const parts = sourcePath.split('/');
  if (
    !CONTENT_ROOTS.some((allowed) => allowed === parts[0]) ||
    parts.some((part) => !part || part === '.' || part === '..') ||
    sourcePath.includes('\\')
  )
    throw new Error(`${sourcePath}: asset path escapes content roots`);
  let current = root;
  for (const part of parts) {
    current = join(current, part);
    if ((await lstat(current)).isSymbolicLink())
      throw new Error(`${sourcePath}: symbolic link assets are forbidden`);
  }
  if (!(await lstat(current)).isFile())
    throw new Error(`${sourcePath}: asset must be a regular file`);
  return current;
}

async function localBytes(
  root: string,
  sourcePath: string,
): Promise<{ bytes: Buffer; originalSize: number }> {
  const path = await verifiedSource(root, sourcePath);
  const size = (await lstat(path)).size;
  if (size > MAX_LOCAL_ASSET_BYTES)
    throw new Error(`${sourcePath}: asset exceeds local size limit`);
  const original = await readFile(path);
  if (original.length !== size)
    throw new Error(`${sourcePath}: asset changed while reading`);
  try {
    const bytes =
      extname(sourcePath).toLowerCase() === '.svg'
        ? sanitizeSvg(original)
        : original;
    if (bytes.length > MAX_LOCAL_ASSET_BYTES)
      throw new Error('Sanitized asset exceeds local size limit');
    return { bytes, originalSize: size };
  } catch (error) {
    throw new Error(
      `${sourcePath}: invalid asset: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error },
    );
  }
}

function assetUrl(sourcePath: string, bytes: Buffer): string {
  return `/content-assets/${createHash('sha256').update(bytes).digest('hex')}${extname(sourcePath).toLowerCase().replace('.jpeg', '.jpg')}`;
}

export async function planAssets(
  rootDir: string,
  sources: string[],
  policy: PublicationPolicy,
): Promise<AssetRecord[]> {
  const root = await realpath(rootDir);
  const discovery = await discoverEntries(root, policy);
  const approved = new Set(
    discovery.ledger
      .filter(
        (row) =>
          row.disposition === 'supporting-asset' ||
          row.disposition === 'page' ||
          row.disposition === 'external-resource',
      )
      .map((row) => row.sourcePath),
  );
  const assets: AssetRecord[] = [];
  for (const sourcePath of [...new Set(sources)].sort(compareSourcePaths)) {
    if (
      !approved.has(sourcePath) ||
      !extensions.has(extname(sourcePath).toLowerCase())
    )
      throw new Error(
        `${sourcePath}: missing, excluded, symlink or unsupported asset`,
      );
    const path = await verifiedSource(root, sourcePath);
    const size = (await lstat(path)).size;
    if (
      size > MAX_LOCAL_ASSET_BYTES ||
      policy.overrides[sourcePath]?.resourceUrl
    ) {
      assets.push({
        sourcePath,
        bytes: size,
        mode: 'external',
        url: publicSourceUrl(sourcePath, policy),
      });
    } else {
      const content = await localBytes(root, sourcePath);
      assets.push({
        sourcePath,
        bytes: content.originalSize,
        mode: 'local',
        url: assetUrl(sourcePath, content.bytes),
      });
    }
  }
  return assets;
}

async function generatedDirectory(
  root: string,
  targetDir: string,
  rootDir: string,
): Promise<string> {
  const expected = join(root, 'site/public/content-assets');
  if (
    resolve(targetDir) !== expected &&
    resolve(targetDir) !== join(resolve(rootDir), 'site/public/content-assets')
  )
    throw new Error(
      'Asset target must be the verified site/public/content-assets directory',
    );
  let current = root;
  for (const part of ['site', 'public', 'content-assets']) {
    current = join(current, part);
    try {
      const stat = await lstat(current);
      if (stat.isSymbolicLink() || !stat.isDirectory())
        throw new Error(
          `Unsafe symbolic link or non-directory asset target: ${current}`,
        );
    } catch (error) {
      if (error instanceof Error && 'code' in error && error.code === 'ENOENT')
        await mkdir(current);
      else throw error;
    }
  }
  return expected;
}

export async function readPlannedLocalAsset(
  rootDir: string,
  asset: AssetRecord,
): Promise<Buffer> {
  const root = await realpath(rootDir);
  if (
    asset.mode !== 'local' ||
    !/^\/content-assets\/[a-f0-9]{64}\.(?:png|jpg|gif|webp|avif|svg|ico|pdf|ppt|pptx)$/.test(
      asset.url,
    ) ||
    !extensions.has(extname(asset.sourcePath).toLowerCase())
  )
    throw new Error(`${asset.sourcePath}: invalid generated asset URL`);
  const data = await localBytes(root, asset.sourcePath);
  if (
    data.originalSize !== asset.bytes ||
    assetUrl(asset.sourcePath, data.bytes) !== asset.url
  )
    throw new Error(
      `${asset.sourcePath}: asset changed or hash mismatch; re-plan assets`,
    );
  return data.bytes;
}

export async function copyLocalAssets(
  rootDir: string,
  assets: AssetRecord[],
  targetDir: string,
): Promise<void> {
  const root = await realpath(rootDir);
  const target = await generatedDirectory(root, targetDir, rootDir);
  const local = assets.filter((asset) => asset.mode === 'local');
  // Validate all sources and existing outputs before replacing or deleting output.
  for (const asset of local) await readPlannedLocalAsset(root, asset);
  const previous = await readdir(target);
  for (const name of previous) {
    const stat = await lstat(join(target, name));
    if (!stat.isFile() || stat.isSymbolicLink())
      throw new Error(`Unsafe generated asset entry: ${name}`);
  }
  const written = new Set<string>();
  for (const asset of local) {
    const name = asset.url.slice('/content-assets/'.length);
    if (written.has(name)) continue;
    await writeFile(
      join(target, name),
      await readPlannedLocalAsset(root, asset),
    );
    written.add(name);
  }
  for (const name of previous)
    if (!written.has(name)) await rm(join(target, name));
}

export type RasterAsset = { asset: AssetRecord; width: number; height: number };

/** Validate extracted notebook raster bytes; the preparation sink owns writing. */
export async function planRasterAsset(
  sourcePath: string,
  bytes: Uint8Array,
  mime: 'image/png' | 'image/jpeg',
): Promise<RasterAsset> {
  try {
    if (!bytes.byteLength || bytes.byteLength > MAX_LOCAL_ASSET_BYTES)
      throw new Error('Extracted image exceeds the bounded image size');
    if (mime !== 'image/png' && mime !== 'image/jpeg')
      throw new Error('Unsupported raster MIME');
    const data = Buffer.from(bytes);
    const image = sharp(data, {
      limitInputPixels: 40_000_000,
      failOn: 'warning',
    });
    const metadata = await image.metadata();
    if (
      metadata.format !== (mime === 'image/png' ? 'png' : 'jpeg') ||
      !metadata.width ||
      !metadata.height
    )
      throw new Error('Image bytes do not match the declared raster MIME');
    // Decode all pixels to catch truncated/corrupt payloads after valid headers.
    await image.stats();
    return {
      asset: {
        sourcePath,
        bytes: data.length,
        mode: 'local',
        url: `/content-assets/${createHash('sha256').update(data).digest('hex')}.${mime === 'image/png' ? 'png' : 'jpg'}`,
      },
      width: metadata.width,
      height: metadata.height,
    };
  } catch (error) {
    throw new Error(
      `${sourcePath}: invalid extracted raster: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error },
    );
  }
}
