import {
  mkdtemp,
  mkdir,
  writeFile,
  readFile,
  rm,
  symlink,
  open,
  readdir,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { afterEach, describe, expect, it } from 'vitest';
import {
  planAssets,
  copyLocalAssets,
  planRasterAsset,
  readPlannedLocalAsset,
} from '../../../src/content/assets.js';
import type { PublicationPolicy } from '../../../src/content/types.js';

const policy: PublicationPolicy = {
  roots: ['Books', 'Classes', 'Courses', 'Interview', 'Languages', 'Tutorials'],
  exclude: ['**/hidden/**'],
  overrides: {},
  repositoryPublic: true,
  repositoryUrl: 'https://github.com/owner/repo',
  revision: 'b'.repeat(40),
};
const roots: string[] = [];
async function archive(): Promise<string> {
  const root = await mkdtemp(join(tmpdir(), 'notes-task3-'));
  roots.push(root);
  await mkdir(join(root, 'Tutorials/images'), { recursive: true });
  return root;
}
async function sparse(path: string, bytes: number): Promise<void> {
  const file = await open(path, 'w');
  await file.truncate(bytes);
  await file.close();
}
afterEach(async () => {
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});

describe('approved asset planning and copy', () => {
  it('copies referenced real image bytes only and deduplicates content hashes', async () => {
    const root = await archive();
    const bytes = await readFile(
      'tests/fixtures/real/task3/Ubuntu-Reference.jpg',
    );
    for (const name of ['a.jpg', 'b.jpg', 'unreferenced.jpg'])
      await writeFile(join(root, `Tutorials/images/${name}`), bytes);
    const assets = await planAssets(
      root,
      [
        'Tutorials/images/a.jpg',
        'Tutorials/images/b.jpg',
        'Tutorials/images/a.jpg',
      ],
      policy,
    );
    expect(assets).toHaveLength(2);
    expect(assets[0]?.url).toBe(
      `/content-assets/${createHash('sha256').update(bytes).digest('hex')}.jpg`,
    );
    expect(assets[1]?.url).toBe(assets[0]?.url);
    const target = join(root, 'site/public/content-assets');
    await mkdir(target, { recursive: true });
    await writeFile(join(target, 'stale.jpg'), 'old generated output');
    await copyLocalAssets(root, assets, target);
    expect(await readdir(target)).toEqual([assets[0]!.url.split('/').at(-1)]);
    expect(
      await readFile(join(target, assets[0]!.url.split('/').at(-1)!)),
    ).toEqual(bytes);
  });
  it('uses sparse inputs at the exact 25 MiB boundary', async () => {
    const root = await archive();
    await sparse(join(root, 'Tutorials/images/boundary.png'), 26_214_400);
    await sparse(join(root, 'Tutorials/images/oversize.png'), 26_214_401);
    const assets = await planAssets(
      root,
      ['Tutorials/images/boundary.png', 'Tutorials/images/oversize.png'],
      policy,
    );
    expect(assets[0]).toMatchObject({ bytes: 26_214_400, mode: 'local' });
    expect(assets[1]).toMatchObject({
      bytes: 26_214_401,
      mode: 'external',
      url: `https://github.com/owner/repo/blob/${'b'.repeat(40)}/Tutorials/images/oversize.png`,
    });
    const target = join(root, 'site/public/content-assets');
    await copyLocalAssets(root, assets, target);
    expect(await readdir(target)).toHaveLength(1);
    await expect(
      planAssets(root, ['Tutorials/images/oversize.png'], {
        ...policy,
        repositoryPublic: false,
      }),
    ).rejects.toThrow('oversize.png');
  });
  it('rejects excluded/draft/unsupported/symlink and escaping inputs', async () => {
    const root = await archive();
    await mkdir(join(root, 'Tutorials/hidden'));
    await writeFile(join(root, 'Tutorials/hidden/a.png'), 'secret');
    await writeFile(join(root, 'Tutorials/images/draft.png'), 'draft');
    await writeFile(
      join(root, 'Tutorials/images/source.html'),
      '<script>bad()</script>',
    );
    await symlink(
      join(root, 'Tutorials/hidden'),
      join(root, 'Tutorials/images/link'),
    );
    for (const path of [
      'Tutorials/hidden/a.png',
      'Tutorials/images/link/a.png',
      '../outside.png',
      'Tutorials/images/missing.png',
      'Tutorials/images/source.html',
    ]) {
      await expect(planAssets(root, [path], policy)).rejects.toThrow(path);
    }
    await expect(
      planAssets(root, ['Tutorials/images/draft.png'], {
        ...policy,
        overrides: { 'Tutorials/images/draft.png': { draft: true } },
      }),
    ).rejects.toThrow('draft.png');
  });
  it('sanitizes SVG scripts, foreignObject, event handlers, styles and remote URL attributes before hashing/copy', async () => {
    const root = await archive();
    await writeFile(
      join(root, 'Tutorials/images/a.svg'),
      '<svg xmlns="http://www.w3.org/2000/svg" onload="bad()"><script>bad()</script><foreignObject><div>evil</div></foreignObject><rect width="10" height="10" style="background:url(https://evil.org)" fill="url(https://evil.org)"/><a href="javascript:bad()"><text>safe text</text></a><use href="https://evil.org/x.svg#x"/><path id="safe" d="M0 0"/><use href="#safe"/></svg>',
    );
    const assets = await planAssets(root, ['Tutorials/images/a.svg'], policy);
    const target = join(root, 'site/public/content-assets');
    await copyLocalAssets(root, assets, target);
    const svg = await readFile(
      join(target, assets[0]!.url.split('/').at(-1)!),
      'utf8',
    );
    expect(svg).not.toMatch(
      /script|foreignObject|onload|style|evil\.org|javascript/,
    );
    expect(svg).toContain('d="M0 0"');
    expect(svg).toContain('href="#safe"');
    expect(assets[0]?.url).toContain(
      createHash('sha256').update(svg).digest('hex'),
    );
  });
  it.each([
    '<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><svg>&xxe;</svg>',
    '<svg><unclosed></svg>',
    '<svg xmlns="http://evil.example"><rect width="10"/></svg>',
  ])('rejects unsafe or malformed XML: %s', async (xml) => {
    const root = await archive();
    await writeFile(join(root, 'Tutorials/images/a.svg'), xml);
    await expect(
      planAssets(root, ['Tutorials/images/a.svg'], policy),
    ).rejects.toThrow('a.svg');
  });
  it('cannot clean or copy outside the verified generated asset directory', async () => {
    const root = await archive();
    await writeFile(join(root, 'Tutorials/images/a.png'), 'image');
    const assets = await planAssets(root, ['Tutorials/images/a.png'], policy);
    const outside = join(root, 'outside');
    await mkdir(outside);
    await writeFile(join(outside, 'keep.txt'), 'must survive');
    await expect(copyLocalAssets(root, assets, outside)).rejects.toThrow(
      'content-assets',
    );
    expect(await readFile(join(outside, 'keep.txt'), 'utf8')).toBe(
      'must survive',
    );
    await mkdir(join(root, 'site'));
    await symlink(outside, join(root, 'site/public'));
    await expect(
      copyLocalAssets(root, assets, join(root, 'site/public/content-assets')),
    ).rejects.toThrow(/symbolic|symlink/i);
  });
  it('revalidates asset bytes and path before replacing generated output', async () => {
    const root = await archive();
    await writeFile(join(root, 'Tutorials/images/a.png'), 'image');
    const assets = await planAssets(root, ['Tutorials/images/a.png'], policy);
    const target = join(root, 'site/public/content-assets');
    await mkdir(target, { recursive: true });
    await writeFile(join(target, 'keep.txt'), 'prior output');
    await writeFile(join(root, 'Tutorials/images/a.png'), 'other');
    await expect(copyLocalAssets(root, assets, target)).rejects.toThrow(
      /changed|hash/i,
    );
    expect(await readFile(join(target, 'keep.txt'), 'utf8')).toBe(
      'prior output',
    );
    await expect(
      copyLocalAssets(
        root,
        [{ ...assets[0]!, url: '/content-assets/../../outside.png' }],
        target,
      ),
    ).rejects.toThrow();
  });
  it('keeps explicit external resource overrides external even for small PDFs', async () => {
    const root = await archive();
    await writeFile(join(root, 'Tutorials/a.pdf'), 'pdf');
    expect(
      await planAssets(root, ['Tutorials/a.pdf'], {
        ...policy,
        overrides: {
          'Tutorials/a.pdf': { resourceUrl: 'https://cdn.example.org/a.pdf' },
        },
      }),
    ).toMatchObject([
      { mode: 'external', url: 'https://cdn.example.org/a.pdf' },
    ]);
  });
});

describe('bounded extracted notebook raster assets', () => {
  it('creates a hashed asset from valid real JPEG bytes with dimensions', async () => {
    const bytes = await readFile(
      'tests/fixtures/real/task3/Ubuntu-Reference.jpg',
    );
    const result = await planRasterAsset(
      'Tutorials/example.ipynb#cell-2',
      bytes,
      'image/jpeg',
    );
    expect(result.asset).toMatchObject({
      sourcePath: 'Tutorials/example.ipynb#cell-2',
      bytes: bytes.length,
      mode: 'local',
      url: `/content-assets/${createHash('sha256').update(bytes).digest('hex')}.jpg`,
    });
    expect(result.width).toBeGreaterThan(0);
    expect(result.height).toBeGreaterThan(0);
  });
  it('accepts bounded valid PNG bytes and rejects incorrect MIME, corrupt or oversized bytes', async () => {
    const png = await readFile('tests/fixtures/synthetic/task3/pixel.png');
    expect(
      (
        await planRasterAsset(
          'Tutorials/example.ipynb#cell-1',
          png,
          'image/png',
        )
      ).width,
    ).toBe(1);
    for (const [bytes, mime] of [
      [png, 'image/jpeg'],
      [png.subarray(0, 24), 'image/png'],
      [Buffer.from('<svg/>'), 'image/png'],
      [new Uint8Array(26_214_401), 'image/png'],
    ] as const) {
      await expect(
        planRasterAsset('Tutorials/example.ipynb#cell-1', bytes, mime),
      ).rejects.toThrow('example.ipynb#cell-1');
    }
  });
});

describe('read-only validated planned asset bytes', () => {
  it('returns the exact sanitized planned bytes without touching the live output', async () => {
    const root = await archive();
    await writeFile(
      join(root, 'Tutorials/images/a.svg'),
      '<svg><script>bad()</script><path d="M0 0"/></svg>',
    );
    const [asset] = await planAssets(root, ['Tutorials/images/a.svg'], policy);
    const bytes = await readPlannedLocalAsset(root, asset!);
    expect(bytes.toString()).not.toContain('script');
    expect(asset!.url).toContain(
      createHash('sha256').update(bytes).digest('hex'),
    );
    await expect(readdir(join(root, 'site'))).rejects.toMatchObject({
      code: 'ENOENT',
    });
    await writeFile(join(root, 'Tutorials/images/a.svg'), '<svg/>');
    await expect(readPlannedLocalAsset(root, asset!)).rejects.toThrow(
      /changed|hash/i,
    );
    await expect(
      readPlannedLocalAsset(root, {
        ...asset!,
        url: '/content-assets/../../bad.svg',
      }),
    ).rejects.toThrow();
    await expect(
      readPlannedLocalAsset(root, { ...asset!, mode: 'external' }),
    ).rejects.toThrow();
  });
});
