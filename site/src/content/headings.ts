import GithubSlugger from 'github-slugger';
import { fromHtml } from 'hast-util-from-html';
import type { Element, Nodes } from 'hast';
import remarkGfm from 'remark-gfm';
import remarkParse from 'remark-parse';
import remarkMath from 'remark-math';
import { unified } from 'unified';
import type { Root, RootContent } from 'mdast';
import type { Heading } from './types.js';

export type HeadingSlugger = Pick<GithubSlugger, 'slug'>;
export type MarkdownLink = { href: string; image: boolean; wiki: boolean };
const authorParser = unified().use(remarkParse).use(remarkGfm);
const parser = unified().use(remarkParse).use(remarkGfm).use(remarkMath);

export function createHeadingSlugger(): HeadingSlugger {
  return new GithubSlugger();
}

/** Normalize legacy math only outside author HTML and code source ranges. */
function normalizeMath(markdown: string): string {
  const protectedRanges: [number, number][] = [];
  visit(authorParser.parse(markdown), (node) => {
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

/** Shared math-aware AST convention for collection and controlled rendering. */
export function parseMarkdown(markdown: string): Root {
  const normalized = normalizeMath(
    markdown
      .replace(/^\uFEFF/, '')
      .replace(
        /^---[ \t]*\r?\n[\s\S]*?\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/,
        '',
      ),
  );
  const tree = parser.parse(normalized);
  visit(tree, (node) => {
    if (
      node.type === 'inlineMath' &&
      normalized.slice(
        node.position?.start.offset,
        (node.position?.start.offset ?? 0) + 2,
      ) === '$$'
    ) {
      node.data = {
        ...node.data,
        hProperties: {
          ...node.data?.hProperties,
          className: ['language-math', 'math-display'],
        },
      };
    }
  });
  return tree;
}

function visit(
  node: Root | RootContent,
  callback: (node: RootContent) => void,
): void {
  if (node.type !== 'root') callback(node);
  if ('children' in node)
    for (const child of node.children) visit(child, callback);
}

function text(node: RootContent): string {
  if (
    node.type === 'text' ||
    node.type === 'inlineCode' ||
    node.type === 'inlineMath' ||
    node.type === 'math'
  )
    return node.value;
  if (node.type === 'image' || node.type === 'imageReference')
    return node.alt ?? '';
  return 'children' in node ? node.children.map(text).join('') : '';
}

export function collectHeadings(
  markdown: string,
  slugger: HeadingSlugger = createHeadingSlugger(),
): Heading[] {
  const headings: Heading[] = [];
  visit(parseMarkdown(markdown), (node) => {
    if (node.type === 'heading') {
      const value = text(node);
      headings.push({
        id: slugger.slug(value),
        text: value,
        depth: node.depth,
      });
    }
  });
  return headings;
}

function visitHtml(html: string, callback: (element: Element) => void): void {
  function walk(node: Nodes): void {
    if (node.type === 'element') callback(node);
    if ('children' in node) for (const child of node.children) walk(child);
  }
  walk(fromHtml(html, { fragment: true }));
}

export function collectExplicitAnchors(markdown: string): string[] {
  const anchors: string[] = [];
  visit(parseMarkdown(markdown), (node) => {
    if (node.type !== 'html') return;
    visitHtml(node.value, (element) => {
      if (
        ![
          'a',
          'summary',
          'details',
          'div',
          'span',
          'h1',
          'h2',
          'h3',
          'h4',
          'h5',
          'h6',
        ].includes(element.tagName)
      )
        return;
      const id = element.properties.id;
      if (typeof id === 'string' && /^[\p{L}\p{N}_.:-]+$/u.test(id))
        anchors.push(id);
    });
  });
  return [...new Set(anchors)];
}

export function collectMarkdownLinks(markdown: string): MarkdownLink[] {
  const tree = parseMarkdown(markdown);
  const definitions = new Map<string, string>();
  visit(tree, (node) => {
    if (node.type === 'definition') {
      const identifier = node.identifier.toLowerCase();
      if (!definitions.has(identifier)) definitions.set(identifier, node.url);
    }
  });
  const links: MarkdownLink[] = [];
  visit(tree, (node) => {
    if (node.type === 'link' || node.type === 'image') {
      links.push({ href: node.url, image: node.type === 'image', wiki: false });
    } else if (
      node.type === 'linkReference' ||
      node.type === 'imageReference'
    ) {
      const href = definitions.get(node.identifier.toLowerCase());
      if (href !== undefined)
        links.push({
          href,
          image: node.type === 'imageReference',
          wiki: false,
        });
    } else if (node.type === 'html') {
      visitHtml(node.value, (element) => {
        const href =
          element.tagName === 'img'
            ? element.properties.src
            : element.tagName === 'a'
              ? element.properties.href
              : undefined;
        if (typeof href === 'string')
          links.push({ href, image: element.tagName === 'img', wiki: false });
      });
    } else if (node.type === 'text') {
      for (const match of node.value.matchAll(/\[\[[^\]\r\n[]+\]\]/g)) {
        links.push({ href: match[0], image: false, wiki: true });
      }
    }
  });
  return links;
}
