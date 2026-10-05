import { randomUUID } from 'node:crypto';
import { fromHtml } from 'hast-util-from-html';
import { toHtml } from 'hast-util-to-html';
import type { Nodes, Root as HtmlRoot, RootContent as HtmlContent } from 'hast';
import katex from 'katex';
import type { Root, RootContent } from 'mdast';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import { unified } from 'unified';
import type { RasterAsset } from '../assets.js';
import { collectHeadings, type HeadingSlugger } from '../headings.js';
import { resolveLink } from '../links.js';
import type { RenderContext, RenderResult } from '../types.js';
import { sanitizeAuthorTree } from './sanitize.js';
import { renderSource } from './source.js';

const parser = unified().use(remarkParse).use(remarkGfm);
function visit(
  node: Root | RootContent,
  callback: (node: RootContent) => void,
): void {
  if (node.type !== 'root') callback(node);
  if ('children' in node)
    for (const child of node.children) visit(child, callback);
}

/** Normalize legacy math only outside author HTML and code source ranges. */
function normalizeMath(markdown: string): string {
  const protectedRanges: [number, number][] = [];
  visit(parser.parse(markdown), (node) => {
    if (['code', 'inlineCode', 'html'].includes(node.type)) {
      const start = node.position?.start.offset;
      const end = node.position?.end.offset;
      if (start !== undefined && end !== undefined)
        protectedRanges.push([start, end]);
    }
  });
  function normalize(value: string): string {
    return (
      value
        .replace(/\\\[([\s\S]*?)\\\]/g, (_, math: string) => `$$${math}$$`)
        .replace(/\\\(([\s\S]*?)\\\)/g, (_, math: string) => `$${math}$`)
        // A bare amount followed by prose is currency; an enclosed numeric equation is math.
        .replace(
          /(?<![\\$])\$(\d+(?:[.,]\d+)?)(?!\d)(?=\s|[,.;]|$)/g,
          (match: string, amount: string, offset: number, input: string) => {
            const rest = input.slice(offset + match.length);
            const closing = /(?<!\\)\$/.exec(rest)?.index;
            const enclosed =
              closing !== undefined &&
              !/[\r\n]/.test(rest.slice(0, closing)) &&
              /^(?:$|\s|[.,;:!?)\]}])/.test(rest.slice(closing + 1));
            return enclosed ? match : `\\$${amount}`;
          },
        )
    );
  }
  let output = '';
  let cursor = 0;
  for (const [start, end] of protectedRanges.sort((a, b) => a[0] - b[0])) {
    if (start < cursor) continue;
    output +=
      normalize(markdown.slice(cursor, start)) + markdown.slice(start, end);
    cursor = end;
  }
  return output + normalize(markdown.slice(cursor));
}

/** The optional slugger is shared by notebook Markdown cells. */
export async function renderMarkdown(
  markdown: string,
  context: RenderContext,
  slugger?: HeadingSlugger,
  attachments?: ReadonlyMap<string, RasterAsset>,
): Promise<RenderResult> {
  const author = markdown
    .replace(/^\uFEFF/, '')
    .replace(/^---[ \t]*\r?\n[\s\S]*?\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/, '');
  const headings = collectHeadings(markdown, slugger);
  const processor = unified().use(remarkParse).use(remarkGfm).use(remarkMath);
  const normalized = normalizeMath(author);
  const tree = processor.parse(normalized);
  const slots = new Map<string, HtmlContent[]>();
  const headingIds = new Map<string, string>();
  let headingIndex = 0;
  const work: (() => Promise<void>)[] = [];
  function slot(
    node: RootContent,
    render: () => string | Promise<string>,
  ): void {
    const token = `RENDERER${randomUUID().replaceAll('-', '')}`;
    work.push(async () => {
      slots.set(token, fromHtml(await render(), { fragment: true }).children);
    });
    Object.assign(node, { type: 'text', value: token });
    delete node.data;
  }
  visit(tree, (node) => {
    if (node.type === 'heading') {
      const token = `HEADING${randomUUID().replaceAll('-', '')}`;
      headingIds.set(token, headings[headingIndex++]?.id ?? '');
      node.data = { ...node.data, hProperties: { id: token } };
    } else if (node.type === 'code') {
      const code = node.value;
      const language = node.lang ?? 'text';
      slot(node, async () => (await renderSource(code, language)).html);
    } else if (node.type === 'math' || node.type === 'inlineMath') {
      const math = node.value;
      const displayMode =
        node.type === 'math' ||
        normalized.slice(
          node.position?.start.offset,
          (node.position?.start.offset ?? 0) + 2,
        ) === '$$';
      slot(node, () =>
        katex.renderToString(math, {
          displayMode,
          trust: false,
          throwOnError: false,
          strict: 'ignore',
          maxExpand: 1000,
        }),
      );
    } else if (node.type === 'text') {
      // Narrow inline extension: highlight and wiki links are converted to safe AST nodes.
      const children: RootContent[] = [];
      let cursor = 0;
      for (const match of node.value.matchAll(
        /==([^=\r\n]+)==|\[\[([^\]\r\n[]+)\]\]/g,
      )) {
        children.push({
          type: 'text',
          value: node.value.slice(cursor, match.index),
        });
        if (match[1])
          children.push({
            type: 'emphasis',
            data: { hName: 'mark' },
            children: [{ type: 'text', value: match[1] }],
          });
        else
          children.push({
            type: 'link',
            url: match[0],
            children: [
              { type: 'text', value: match[2]?.split('|').at(-1) ?? '' },
            ],
          });
        cursor = match.index + match[0].length;
      }
      if (children.length) {
        children.push({ type: 'text', value: node.value.slice(cursor) });
        Object.assign(node, {
          type: 'emphasis',
          data: { hName: 'span' },
          children,
        });
      }
    }
  });
  const htmlProcessor = unified()
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw);
  const authorTree = (await htmlProcessor.run(tree)) as HtmlRoot;
  function attachmentLinks(node: Nodes): void {
    if (node.type === 'element') {
      const key =
        node.tagName === 'img'
          ? 'src'
          : node.tagName === 'a'
            ? 'href'
            : undefined;
      const href = key ? node.properties[key] : undefined;
      if (
        attachments &&
        key &&
        typeof href === 'string' &&
        href.startsWith('attachment:')
      ) {
        const name = decodeURIComponent(href.slice('attachment:'.length));
        const image = attachments.get(name);
        if (!image) throw new Error(`Missing notebook attachment ${name}`);
        node.properties[key] = image.asset.url;
        if (node.tagName === 'img')
          Object.assign(node.properties, {
            width: image.width,
            height: image.height,
          });
      }
    }
    if ('children' in node)
      for (const child of node.children) attachmentLinks(child);
  }
  attachmentLinks(authorTree);
  const clean = sanitizeAuthorTree(authorTree);
  function resolve(node: Nodes): void {
    if (node.type === 'element') {
      const id = node.properties.id;
      if (typeof id === 'string' && headingIds.has(id))
        node.properties.id = headingIds.get(id);
      const key =
        node.tagName === 'img'
          ? 'src'
          : node.tagName === 'a'
            ? 'href'
            : undefined;
      const href = key ? node.properties[key] : undefined;
      if (key && typeof href === 'string')
        node.properties[key] = resolveLink(
          href,
          context.sourcePath,
          context.catalog,
        );
    }
    if ('children' in node) for (const child of node.children) resolve(child);
  }
  resolve(clean);
  // Author HTML is now sanitized; only controlled transforms generate trusted HTML.
  await Promise.all(work.map((render) => render()));
  function insert(node: Nodes): void {
    if (!('children' in node)) return;
    const children: HtmlContent[] = [];
    for (const child of node.children) {
      if (child.type !== 'text') {
        insert(child);
        children.push(child);
        continue;
      }
      // Raw HTML parsing may merge a generated slot with neighboring author text.
      const pattern = /RENDERER[a-f0-9]{32}/g;
      let cursor = 0;
      for (const match of child.value.matchAll(pattern)) {
        const replacement = slots.get(match[0]);
        if (!replacement) continue;
        children.push(
          { type: 'text', value: child.value.slice(cursor, match.index) },
          ...replacement,
        );
        cursor = match.index + match[0].length;
      }
      children.push({ type: 'text', value: child.value.slice(cursor) });
    }
    node.children = children;
  }
  insert(clean);
  return { html: toHtml(clean), headings };
}
