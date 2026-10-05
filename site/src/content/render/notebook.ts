import { createHash } from 'node:crypto';
import { toHtml } from 'hast-util-to-html';
import { z } from 'zod';
import {
  MAX_LOCAL_ASSET_BYTES,
  planRasterAsset,
  type RasterAsset,
} from '../assets.js';
import { createHeadingSlugger, collectMarkdownLinks } from '../headings.js';
import type { RenderContext, RenderResult } from '../types.js';
import { renderMarkdown } from './markdown.js';
import { renderSource } from './source.js';

const multiline = z
  .union([z.string(), z.array(z.string())])
  .transform((value) => (typeof value === 'string' ? value : value.join('')));
const dictionary = z.record(z.string(), z.unknown());
const rich = { data: dictionary, metadata: dictionary };
const outputSchema = z.discriminatedUnion('output_type', [
  z.object({
    output_type: z.literal('stream'),
    name: z.enum(['stdout', 'stderr']),
    text: multiline,
  }),
  z.object({
    output_type: z.literal('error'),
    ename: z.string(),
    evalue: z.string(),
    traceback: z.array(z.string()),
  }),
  z.object({ output_type: z.literal('display_data'), ...rich }),
  z.object({
    output_type: z.literal('execute_result'),
    ...rich,
    execution_count: z.number().int().nonnegative(),
  }),
]);
const cellFields = { source: multiline, metadata: dictionary };
const cellSchema = z.discriminatedUnion('cell_type', [
  z.object({
    cell_type: z.literal('markdown'),
    ...cellFields,
    attachments: z.record(z.string(), dictionary).optional(),
  }),
  z.object({ cell_type: z.literal('raw'), ...cellFields }),
  z.object({
    cell_type: z.literal('code'),
    ...cellFields,
    execution_count: z.number().int().nonnegative().nullable(),
    outputs: z.array(outputSchema),
  }),
]);
const notebookSchema = z.object({
  nbformat: z.literal(4),
  nbformat_minor: z.number().int().nonnegative(),
  metadata: dictionary,
  cells: z.array(z.unknown()),
});

function validation<T>(schema: z.ZodType<T>, value: unknown, label: string): T {
  const parsed = schema.safeParse(value);
  if (!parsed.success)
    throw new Error(
      `${label}: invalid notebook: ${parsed.error.issues.map((issue) => `${issue.path.join('.')}: ${issue.message}`).join('; ')}`,
    );
  return parsed.data;
}
function plain(value: string): string {
  return toHtml({
    type: 'element',
    tagName: 'pre',
    properties: {},
    children: [
      {
        type: 'element',
        tagName: 'code',
        properties: {},
        children: [{ type: 'text', value }],
      },
    ],
  });
}
function rasterMime(
  data: Record<string, unknown>,
): 'image/png' | 'image/jpeg' | undefined {
  return Object.hasOwn(data, 'image/png')
    ? 'image/png'
    : Object.hasOwn(data, 'image/jpeg')
      ? 'image/jpeg'
      : undefined;
}
async function extract(
  data: Record<string, unknown>,
  sourcePath: string,
  context: RenderContext,
): Promise<RasterAsset> {
  const mime = rasterMime(data);
  if (!mime) throw new Error('Attachment has no supported PNG/JPEG raster');
  if (!context.extractAsset)
    throw new Error('Raster extraction requires RenderContext.extractAsset');
  const original = validation(multiline, data[mime], sourcePath);
  // Bound allocation before decoding; nbformat permits line-wrapped base64.
  if (original.length > Math.ceil(MAX_LOCAL_ASSET_BYTES / 3) * 4 + 1_000_000)
    throw new Error('Raster base64 exceeds bounded image size');
  const base64 = original.replace(/[\r\n]/g, '');
  if (
    !base64 ||
    !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(
      base64,
    )
  )
    throw new Error('Invalid raster base64');
  const bytes = Buffer.from(base64, 'base64');
  const image = await planRasterAsset(sourcePath, bytes, mime);
  await context.extractAsset(image.asset, bytes);
  context.catalog.assets.set(sourcePath, image.asset);
  return image;
}
function imageHtml(image: RasterAsset): string {
  return toHtml({
    type: 'element',
    tagName: 'img',
    properties: {
      src: image.asset.url,
      alt: 'Stored notebook output',
      width: image.width,
      height: image.height,
    },
    children: [],
  });
}

/** Parse unknown nbformat-4 data and display stored cells only. Never execute. */
export async function renderNotebook(
  json: unknown,
  context: RenderContext,
): Promise<RenderResult> {
  const parsed = validation(notebookSchema, json, context.sourcePath);
  const cells = parsed.cells.map((cell, index) =>
    validation(cellSchema, cell, `${context.sourcePath}: cell ${index}`),
  );
  const info = parsed.metadata.language_info;
  const language =
    typeof info === 'object' &&
    info !== null &&
    'name' in info &&
    typeof info.name === 'string'
      ? info.name
      : 'text';
  const slugger = createHeadingSlugger();
  const result: RenderResult = { html: '', headings: [] };
  for (const [cellIndex, cell] of cells.entries()) {
    const label = `${context.sourcePath}: cell ${cellIndex}`;
    try {
      let html = '';
      if (cell.cell_type === 'markdown') {
        const attachments = new Map<string, RasterAsset>();
        const references = new Set(
          collectMarkdownLinks(cell.source)
            .filter((link) => link.href.startsWith('attachment:'))
            .map((link) =>
              decodeURIComponent(link.href.slice('attachment:'.length)),
            ),
        );
        for (const name of references) {
          if (!cell.attachments || !Object.hasOwn(cell.attachments, name))
            throw new Error(`Missing notebook attachment ${name}`);
          const data = cell.attachments[name]!;
          const mime = rasterMime(data);
          const key = createHash('sha256').update(name).digest('hex');
          const sourcePath = `${context.sourcePath}.assets/cell-${cellIndex}/attachment-${key}.${mime === 'image/jpeg' ? 'jpg' : 'png'}`;
          const image = await extract(data, sourcePath, context);
          attachments.set(name, image);
        }
        const rendered = await renderMarkdown(
          cell.source,
          context,
          slugger,
          attachments,
        );
        html = rendered.html;
        result.headings.push(...rendered.headings);
      } else if (cell.cell_type === 'raw') {
        html = plain(cell.source);
      } else {
        html = (await renderSource(cell.source, language)).html;
        for (const [outputIndex, output] of cell.outputs.entries()) {
          if (output.output_type === 'stream') html += plain(output.text);
          else if (output.output_type === 'error')
            html += plain(
              `${output.ename}: ${output.evalue}\n${output.traceback.join('\n')}`,
            );
          else if (rasterMime(output.data)) {
            const mime = rasterMime(output.data);
            const image = await extract(
              output.data,
              `${context.sourcePath}.assets/cell-${cellIndex}/output-${outputIndex}.${mime === 'image/jpeg' ? 'jpg' : 'png'}`,
              context,
            );
            html += imageHtml(image);
          } else if (Object.hasOwn(output.data, 'text/plain')) {
            html += plain(
              validation(multiline, output.data['text/plain'], label),
            );
          } else {
            html += `<p class="notebook-unsupported-output">Unsupported output (cell ${cellIndex})</p>`;
          }
        }
      }
      result.html += `<section class="notebook-cell" data-cell-index="${cellIndex}">${html}</section>\n`;
    } catch (error) {
      throw new Error(
        `${label}: ${error instanceof Error ? error.message : String(error)}`,
        { cause: error },
      );
    }
  }
  return result;
}
