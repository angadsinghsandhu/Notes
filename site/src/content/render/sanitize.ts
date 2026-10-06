import { fromHtml } from 'hast-util-from-html';
import { sanitize, type Schema } from 'hast-util-sanitize';
import { toHtml } from 'hast-util-to-html';
import type { Nodes, Root } from 'hast';

const anchorTags = new Set([
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
]);
const schema: Schema = {
  tagNames: [
    'a',
    'p',
    'br',
    'hr',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'ul',
    'ol',
    'li',
    'blockquote',
    'pre',
    'code',
    'strong',
    'em',
    'del',
    's',
    'u',
    'ins',
    'mark',
    'details',
    'summary',
    'img',
    'table',
    'thead',
    'tbody',
    'tr',
    'th',
    'td',
    'div',
    'span',
    'figure',
    'figcaption',
    'sup',
    'sub',
    'input',
  ],
  attributes: {
    '*': ['id', 'title'],
    a: ['href'],
    img: ['src', 'alt', 'width', 'height'],
    ol: ['start'],
    th: ['align'],
    td: ['align'],
    details: ['open'],
    input: [['type', 'checkbox'], ['disabled', true], 'checked'],
  },
  protocols: { href: ['http', 'https', 'mailto'], src: ['http', 'https'] },
  strip: [
    'script',
    'style',
    'iframe',
    'object',
    'embed',
    'svg',
    'math',
    'template',
  ],
  clobber: [],
  required: {},
};

function safeUrl(url: string, image: boolean): boolean {
  if (
    url !== url.trim() ||
    url.startsWith('//') ||
    url.includes('\\') ||
    Array.from(url).some(
      (character) =>
        character.charCodeAt(0) < 32 || character.charCodeAt(0) === 127,
    )
  )
    return false;
  if (!/^[a-z][a-z0-9+.-]*:/i.test(url)) return true;
  try {
    const parsed = new URL(url);
    return (
      (image ? ['https:', 'http:'] : ['https:', 'http:', 'mailto:']).includes(
        parsed.protocol,
      ) &&
      !parsed.username &&
      !parsed.password
    );
  } catch {
    return false;
  }
}

/** Only author HTML passes this allowlist. Trusted renderer output is added later. */
export function sanitizeAuthorTree(tree: Root): Root {
  const clean = sanitize(tree, schema);
  if (clean.type !== 'root') throw new Error('Expected author HTML root');
  function walk(node: Nodes): void {
    if (node.type === 'element') {
      const properties = node.properties;
      const id = properties.id;
      if (
        typeof id !== 'string' ||
        !anchorTags.has(node.tagName) ||
        !/^[\p{L}\p{N}_.:-]+$/u.test(id)
      )
        delete properties.id;
      for (const key of ['href', 'src']) {
        const value = properties[key];
        if (typeof value === 'string' && !safeUrl(value, key === 'src'))
          delete properties[key];
      }
      for (const key of ['width', 'height']) {
        const value = properties[key];
        if (
          value !== undefined &&
          (!/^\d+$/.test(String(value)) ||
            Number(value) < 1 ||
            Number(value) > 40_000_000)
        )
          delete properties[key];
      }
      if (node.tagName === 'input') {
        properties.type = 'checkbox';
        properties.disabled = true;
      }
    }
    if ('children' in node) {
      node.children = node.children.filter(
        (child) =>
          child.type !== 'element' ||
          child.tagName !== 'input' ||
          child.properties.type === 'checkbox',
      );
      for (const child of node.children) walk(child);
    }
  }
  walk(clean);
  return clean;
}

export function sanitizeAuthorHtml(html: string): string {
  return toHtml(sanitizeAuthorTree(fromHtml(html, { fragment: true })));
}
