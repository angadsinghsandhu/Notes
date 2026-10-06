import { readFile } from 'node:fs/promises';
import { toHast } from 'mdast-util-to-hast';
import { toHtml } from 'hast-util-to-html';
import remarkParse from 'remark-parse';
import { unified } from 'unified';
import { describe, expect, it } from 'vitest';
import {
  collectHeadings,
  collectExplicitAnchors,
  collectMarkdownLinks,
  createHeadingSlugger,
} from '../../../src/content/headings.js';

describe('Markdown heading and authored link collection', () => {
  it('shares duplicate slug order across notebook cells and extracts inline text', () => {
    const slugger = createHeadingSlugger();
    expect(
      collectHeadings(
        '# Hello *world*!\n\n## Hello world!\n\n```md\n# Hidden\n```',
        slugger,
      ),
    ).toEqual([
      { id: 'hello-world', text: 'Hello world!', depth: 1 },
      { id: 'hello-world-1', text: 'Hello world!', depth: 2 },
    ]);
    expect(
      collectHeadings('Hello world!\n===\n\n# `code` & 日本語', slugger),
    ).toEqual([
      { id: 'hello-world-2', text: 'Hello world!', depth: 1 },
      { id: 'code--日本語', text: 'code & 日本語', depth: 1 },
    ]);
  });
  it('does not collect Markdown-looking display math as headings across notebook cells', () => {
    const slugger = createHeadingSlugger();
    const markdown = '$$\nx\n---\n$$\n\n# Actual heading';
    expect(collectHeadings(markdown, slugger)).toEqual([
      { id: 'actual-heading', text: 'Actual heading', depth: 1 },
    ]);
    expect(collectHeadings('# Actual heading', slugger)).toEqual([
      { id: 'actual-heading-1', text: 'Actual heading', depth: 1 },
    ]);
    expect(collectHeadings(String.raw`# Equation \(x^2\)`)).toEqual([
      { id: 'equation-x2', text: 'Equation x^2', depth: 1 },
    ]);
    expect(
      collectMarkdownLinks(
        '$$\n![not an attachment](attachment:hidden.png)\n$$',
      ),
    ).toEqual([]);
  });
  it('recognizes real summary anchors separately from headings', async () => {
    const guide = await readFile(
      'tests/fixtures/real/task3/course-update-guide-udemy.md',
      'utf8',
    );
    expect(collectExplicitAnchors(guide)).toContain('faq-how-to-get-update');
    expect(collectHeadings(guide).map((heading) => heading.id)).toContain(
      'youre-currently-taking-the-course',
    );
    expect(collectHeadings(guide).map((heading) => heading.id)).not.toContain(
      'faq-how-to-get-update',
    );
    expect(
      collectExplicitAnchors(
        '<!-- <a id="comment"></a> -->\n<script id="script"></script>\n<summary id="safe-id">Yes</summary>\n<a id="bad id">Bad</a>',
      ),
    ).toEqual(['safe-id']);
  });
  it('collects actual AST links and wiki text, not fenced or inline arrays', () => {
    expect(
      collectMarkdownLinks(
        '[[Unique|Label]]\n\n`[[Array]]`\n\n```py\n[[1],[2]]\n```\n\n[[1],[2]]\n\n[page][ref]\n\n![pic](image.png)\n\n[ref]: note.md',
      ),
    ).toEqual([
      { href: '[[Unique|Label]]', image: false, wiki: true },
      { href: 'note.md', image: false, wiki: false },
      { href: 'image.png', image: true, wiki: false },
    ]);
  });
  it('parses real HTML attributes without fabricating anchors from quoted text', () => {
    expect(
      collectExplicitAnchors(
        `<summary title='id="fake"' id=real>Real</summary>\n<a id=foo.bar>Text</a>`,
      ),
    ).toEqual(['real', 'foo.bar']);
    expect(
      collectMarkdownLinks(
        '<img src="image.png" alt="pic"><a href="note.md">Note</a>',
      ),
    ).toEqual([
      { href: 'image.png', image: true, wiki: false },
      { href: 'note.md', image: false, wiki: false },
    ]);
  });
  it('ignores YAML frontmatter headings', () => {
    expect(collectHeadings('---\ntitle: Title\n---\n# Real')).toEqual([
      { id: 'real', text: 'Real', depth: 1 },
    ]);
  });
});

it('keeps the first normalized reference definition, matching CommonMark rendering', () => {
  const markdown =
    '[page][ ref  KEY ]\n\n![image][REF key]\n\n[REF key]: first.md\n\n[ref KEY]: second.md';
  const html = toHtml(toHast(unified().use(remarkParse).parse(markdown)));
  const links = collectMarkdownLinks(markdown);
  expect(links).toEqual([
    { href: 'first.md', image: false, wiki: false },
    { href: 'first.md', image: true, wiki: false },
  ]);
  expect(html).toContain(`href="${links[0]!.href}"`);
  expect(html).toContain(`src="${links[1]!.href}"`);
  expect(html).not.toContain('second.md');
});
