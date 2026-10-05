import { readFile } from 'node:fs/promises';
import { describe, expect, it } from 'vitest';
import sharp from 'sharp';
import type {
  AssetRecord,
  RenderContext,
} from '../../../../src/content/types.js';
import { createRouteCatalog } from '../../../../src/content/links.js';
import { renderNotebook } from '../../../../src/content/render/notebook.js';

const codeCell = (
  outputs: unknown[] = [],
  source: unknown = 'globalThis.task4NotebookExecuted = true',
) => ({
  cell_type: 'code',
  source,
  metadata: {},
  execution_count: null,
  outputs,
});
const markdownCell = (source: unknown, attachments?: unknown) => ({
  cell_type: 'markdown',
  source,
  metadata: {},
  ...(attachments ? { attachments } : {}),
});
const notebook = (cells: unknown[]) => ({
  nbformat: 4,
  nbformat_minor: 5,
  metadata: { language_info: { name: 'python' } },
  cells,
});
const context = (sourcePath = 'Tutorials/note.ipynb'): RenderContext => ({
  sourcePath,
  catalog: createRouteCatalog([], []),
});
async function raster(mime: 'png' | 'jpeg' = 'png') {
  return sharp({
    create: { width: 2, height: 3, channels: 3, background: '#fff' },
  })
    .toFormat(mime)
    .toBuffer();
}

describe('validated notebook display', () => {
  it('preserve_gpu_and_pytorch_notebook_cells', async () => {
    const gpu = JSON.parse(
      await readFile('tests/fixtures/real/task4/gpu-excerpt.json', 'utf8'),
    ) as unknown;
    const ctx = context(
      'Tutorials/GPU/nv-gpu-workshop/1.0_CPU_GPU_Comparison.ipynb',
    );
    ctx.catalog.assets.set('Tutorials/GPU/nv-gpu-workshop/images/cpu-gpu.png', {
      sourcePath: 'Tutorials/GPU/nv-gpu-workshop/images/cpu-gpu.png',
      url: `/content-assets/${'b'.repeat(64)}.png`,
      bytes: 1,
      mode: 'local',
    });
    const gpuResult = await renderNotebook(gpu, ctx);
    expect(gpuResult.html.indexOf('CPU and GPU Comparison')).toBeLessThan(
      gpuResult.html.indexOf('Mythbusters explaination'),
    );
    expect(gpuResult.headings.map((h) => h.id)).toEqual([
      'cpu-and-gpu-comparison',
      'mythbusters-explaination',
    ]);
    expect(gpuResult.html).toContain('YouTubeVideo');
    expect(gpuResult.html).toContain('class="shiki');
    const pytorch = JSON.parse(
      await readFile('tests/fixtures/real/task4/pytorch-excerpt.json', 'utf8'),
    ) as unknown;
    const result = await renderNotebook(
      pytorch,
      context('Classes/tutorial.ipynb'),
    );
    expect(result.html.indexOf('Imports')).toBeLessThan(
      result.html.indexOf('import'),
    );
    expect(result.html.indexOf('import')).toBeLessThan(
      result.html.indexOf('Defining a torch tensor'),
    );
    expect(result.html).toContain('tensor([1, 2, 3])');
    expect(result.html).toContain('class="shiki');
    expect(result.html).not.toContain('outputId');
    expect('task4NotebookExecuted' in globalThis).toBe(false);
  });
  it('shares heading IDs across cells and escapes stored stream, error and raw cells', async () => {
    const result = await renderNotebook(
      notebook([
        markdownCell('# Repeat'),
        markdownCell('# Repeat'),
        codeCell([
          {
            output_type: 'stream',
            name: 'stdout',
            text: ['<script>evil()</script>'],
          },
          {
            output_type: 'error',
            ename: 'Error',
            evalue: '<img onerror="evil()">',
            traceback: ['<script>trace()</script>'],
          },
        ]),
        { cell_type: 'raw', metadata: {}, source: '<iframe>raw</iframe>' },
      ]),
      context(),
    );
    expect(result.headings.map((h) => h.id)).toEqual(['repeat', 'repeat-1']);
    expect(result.html).toContain('id="repeat-1"');
    expect(result.html).toContain('Error:');
    expect(result.html).not.toMatch(/<script|<img onerror|<iframe/);
    expect('task4NotebookExecuted' in globalThis).toBe(false);
  });
  it('uses PNG, then JPEG, then escaped plain text and placeholders for rich output', async () => {
    const png = await raster();
    const jpg = await raster('jpeg');
    const extracted: { asset: AssetRecord; bytes: Uint8Array }[] = [];
    const ctx = {
      ...context(),
      extractAsset: (asset: AssetRecord, bytes: Uint8Array) => {
        extracted.push({ asset, bytes });
      },
    };
    const result = await renderNotebook(
      notebook([
        codeCell([
          {
            output_type: 'display_data',
            metadata: {},
            data: {
              'image/png': png.toString('base64'),
              'image/jpeg': jpg.toString('base64'),
              'text/plain': 'unused',
              'text/html': '<script>evil()</script>',
            },
          },
          {
            output_type: 'execute_result',
            metadata: {},
            execution_count: 1,
            data: {
              'image/jpeg': [jpg.toString('base64')],
              'text/plain': 'unused',
            },
          },
          {
            output_type: 'display_data',
            metadata: {},
            data: {
              'text/plain': ['<b>plain</b>'],
              'text/html': '<script>evil()</script>',
            },
          },
          {
            output_type: 'display_data',
            metadata: {},
            data: {
              'text/html': '<script>evil()</script>',
              'image/svg+xml': '<svg onload="evil()"/>',
            },
          },
        ]),
      ]),
      ctx,
    );
    expect(extracted).toHaveLength(2);
    expect(Buffer.from(extracted[0]!.bytes)).toEqual(png);
    expect(Buffer.from(extracted[1]!.bytes)).toEqual(jpg);
    expect(ctx.catalog.assets.size).toBe(2);
    expect(result.html).toContain('width="2" height="3"');
    expect(result.html).toContain('Unsupported output (cell 0)');
    expect(result.html).not.toMatch(/<script|<svg|<b>plain|unused|data:image/);
  });
  it('extracts Markdown attachments before URL resolution and keeps cells isolated', async () => {
    const image = await raster();
    const assets: AssetRecord[] = [];
    const ctx = {
      ...context(),
      extractAsset: (asset: AssetRecord) => {
        assets.push(asset);
      },
    };
    const result = await renderNotebook(
      notebook([
        markdownCell('![first](attachment:plot.png)', {
          'plot.png': { 'image/png': image.toString('base64') },
        }),
        markdownCell('![second](attachment:plot.png)', {
          'plot.png': { 'image/png': image.toString('base64') },
        }),
      ]),
      ctx,
    );
    expect(assets).toHaveLength(2);
    expect(assets[0]!.sourcePath).not.toBe(assets[1]!.sourcePath);
    expect(result.html.match(/<img/g)).toHaveLength(2);
    expect(result.html).toContain('width="2" height="3"');
    expect(result.html).not.toContain('attachment:');
    await expect(
      renderNotebook(
        notebook([markdownCell('![missing](attachment:plot.png)')]),
        context(),
      ),
    ).rejects.toThrow(/Tutorials\/note.ipynb.*cell 0.*plot.png/);
  });
  it.each([
    ['nbformat', { ...notebook([]), nbformat: 3 }, /nbformat/],
    ['cells', { ...notebook([]), cells: {} }, /cells/],
    ['source', notebook([markdownCell([1])]), /cell 0.*source/],
    [
      'unknown',
      notebook([{ cell_type: 'mystery', source: '', metadata: {} }]),
      /cell 0.*cell_type/,
    ],
    [
      'outputs',
      notebook([codeCell('bad' as unknown as unknown[])]),
      /cell 0.*outputs/,
    ],
    [
      'output text',
      notebook([
        codeCell([{ output_type: 'stream', name: 'stdout', text: [1] }]),
      ]),
      /cell 0.*text/,
    ],
  ])(
    'rejects malformed %s with file and cell diagnostics',
    async (_, value, message) => {
      await expect(renderNotebook(value, context())).rejects.toThrow(message);
      await expect(renderNotebook(value, context())).rejects.toThrow(
        'Tutorials/note.ipynb',
      );
    },
  );
  it('fails explicitly when raster extraction is unavailable or invalid', async () => {
    const data = { 'image/png': (await raster()).toString('base64') };
    await expect(
      renderNotebook(
        notebook([
          codeCell([{ output_type: 'display_data', data, metadata: {} }]),
        ]),
        context(),
      ),
    ).rejects.toThrow(/cell 0.*extract/i);
    for (const base64 of [
      'not base64!',
      Buffer.from('<script>x()</script>').toString('base64'),
    ]) {
      await expect(
        renderNotebook(
          notebook([
            codeCell([
              {
                output_type: 'display_data',
                data: { 'image/png': base64 },
                metadata: {},
              },
            ]),
          ]),
          { ...context(), extractAsset: () => {} },
        ),
      ).rejects.toThrow(/cell 0.*(raster|base64)/i);
    }
  });
});
