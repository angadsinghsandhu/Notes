import {
  readFile,
  mkdtemp,
  mkdir,
  writeFile,
  open,
  rm,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { planAssets } from '../../../../src/content/assets.js';
import { describe, expect, it } from 'vitest';
import { fromHtml } from 'hast-util-from-html';
import type { Nodes } from 'hast';
import { collectHeadings } from '../../../../src/content/headings.js';
import { createRouteCatalog } from '../../../../src/content/links.js';
import { createEntry } from '../../../../src/content/identifiers.js';
import { renderMarkdown } from '../../../../src/content/render/markdown.js';

function context(markdown: string) {
  const sourcePath = 'Interview/note.md';
  const entry = createEntry(
    {
      sourcePath,
      absolutePath: '/unused',
      section: 'interview',
      kind: 'markdown',
      bytes: 1,
    },
    { title: 'Note', description: '', tags: [], draft: false, aliases: [] },
  );
  entry.headings = collectHeadings(markdown);
  return {
    sourcePath,
    catalog: createRouteCatalog(
      [entry],
      [
        {
          sourcePath: 'Interview/pic.png',
          bytes: 1,
          mode: 'local',
          url: `/content-assets/${'a'.repeat(64)}.png`,
        },
      ],
    ),
  };
}
function text(node: Nodes): string {
  return node.type === 'text'
    ? node.value
    : 'children' in node
      ? node.children.map(text).join('')
      : '';
}

describe('safe shared Markdown rendering', () => {
  it('render_transformer_note_with_math_and_code', async () => {
    for (const file of [
      'transformers.md',
      'masters-theorem.md',
      'nlp-week2-excerpt.md',
    ]) {
      const markdown = await readFile(
        `tests/fixtures/real/task4/${file}`,
        'utf8',
      );
      const result = await renderMarkdown(markdown, context(markdown));
      expect(result.headings).toEqual(collectHeadings(markdown));
      for (const heading of result.headings)
        expect(result.html).toContain(`id="${heading.id}"`);
      if (file === 'transformers.md') {
        expect(result.html).toContain('class="shiki');
        expect(result.html).toContain('<table>');
      } else expect(result.html).toContain('class="katex');
    }
  });
  it('keeps the actual heading ID after Markdown-looking display math', async () => {
    const markdown = '$$\nx\n---\n$$\n\n# Actual heading';
    const result = await renderMarkdown(markdown, context(markdown));
    expect(result.headings).toEqual([
      { id: 'actual-heading', text: 'Actual heading', depth: 1 },
    ]);
    expect(result.html).toContain(
      '<h1 id="actual-heading">Actual heading</h1>',
    );
    expect(result.html).toContain('class="katex-display"');
    expect(result.html).not.toContain('id="x"');
  });
  it('preserves display semantics and numeric inline math without confusing currency', async () => {
    const markdown = String.raw`\[ x^2 \] and $$y^2$$ and $5 + 3$ and $5 n$. Cost $5 and $10. Also $20 for $x$.`;
    const result = await renderMarkdown(markdown, context(markdown));
    expect((result.html.match(/class="katex-display"/g) ?? []).length).toBe(2);
    expect((result.html.match(/class="katex"/g) ?? []).length).toBe(5);
    expect(text(fromHtml(result.html, { fragment: true }))).toContain(
      'Cost $5 and $10. Also $20 for',
    );
  });
  it('retains collected IDs for punctuation-only and combining-character headings', async () => {
    const markdown = '# ???\n\n# cafe\u0301';
    const result = await renderMarkdown(markdown, context(markdown));
    expect(result.headings.map((heading) => heading.id)).toEqual([
      '',
      'cafe\u0301',
    ]);
    expect(result.html).toContain('<h1 id="">');
    expect(result.html).toContain('<h1 id="cafe\u0301">');
  });
  it('keeps synthetic Japanese Unicode and safe disclosure anchors', async () => {
    const markdown = await readFile(
      'tests/fixtures/synthetic/task4/unicode.md',
      'utf8',
    );
    const result = await renderMarkdown(markdown, context(markdown));
    expect(text(fromHtml(result.html, { fragment: true }))).toContain('日本語');
    const details =
      '<details open><summary id="help">Help</summary><u>under</u></details>\n\n==highlight==';
    const rendered = await renderMarkdown(details, context(details));
    expect(rendered.html).toContain('id="help"');
    expect(rendered.html).toContain('<u>under</u>');
    expect(rendered.html).toContain('<mark>highlight</mark>');
  });
  it('resolves author and Markdown URLs after sanitizing active markup', async () => {
    const markdown =
      '# Note\n\n[heading](#note) ![pic](pic.png)\n\n<a href="#note" onclick="evil()">jump</a><script>evil()</script><svg onload="evil()"></svg><iframe></iframe><img src="javascript:evil()">';
    const result = await renderMarkdown(markdown, context(markdown));
    expect(result.html).toContain('href="/notes/interview/note/#note"');
    expect(result.html).toContain(`/content-assets/${'a'.repeat(64)}.png`);
    expect(result.html).not.toMatch(
      /onclick|<script|<svg|iframe|javascript:|evil\(\)/,
    );
    await expect(
      renderMarkdown('[missing](absent.md)', context('')),
    ).rejects.toThrow(/Interview\/note.md.*absent.md/);
  });
  it('adds trusted math and highlighting after removing author renderer lookalikes', async () => {
    const markdown =
      '<span class="katex" style="color:red">fake</span>\n\n$\\href{javascript:evil()}{x}$\n\n```js\n<script>evil()</script>\n```';
    const result = await renderMarkdown(markdown, context(markdown));
    expect(result.html).toContain('<span>fake</span>');
    expect(result.html).toContain('class="katex');
    expect(result.html).toContain('class="shiki');
    expect(result.html).not.toMatch(/href="javascript:|<script>/);
  });
  it('preserves code delimiters and currency while rendering legacy and dollar equations', async () => {
    const markdown =
      'Cost $5 and $10. Escaped \\$20. `\\(x\\)` and `$x$`.\n\n\\(a^2\\) and \\[ b^2 \\] and $c^2$.\n\n```text\n\\[raw\\] $raw$ ==raw==\n```';
    const result = await renderMarkdown(markdown, context(markdown));
    const displayed = text(fromHtml(result.html, { fragment: true }));
    expect(displayed).toContain('Cost $5 and $10. Escaped $20.');
    expect(displayed).toContain('\\(x\\)');
    expect(displayed).toContain('\\[raw\\] $raw$ ==raw==');
    expect((result.html.match(/class="katex"/g) ?? []).length).toBe(3);
  });
});

it('resolves labeled wiki text through the shared catalog and rejects missing attachment maps', async () => {
  const markdown = '[[Note|Readable label]]';
  expect((await renderMarkdown(markdown, context(markdown))).html).toContain(
    'Readable label</a>',
  );
  await expect(
    renderMarkdown(
      '![plot](attachment:missing.png)',
      context(''),
      undefined,
      new Map(),
    ),
  ).rejects.toThrow('Missing notebook attachment');
});

it('rejects missing, ambiguous and draft wiki targets through the actual renderer', async () => {
  const ctx = context('');
  await expect(renderMarkdown('[[Missing|Label]]', ctx)).rejects.toThrow(
    /Missing|Unresolved/,
  );
  const existing = [...ctx.catalog.sources.values()][0]!;
  for (const [draft, title] of [
    [true, 'Private'],
    [false, 'Note'],
  ] as const) {
    const entry = {
      ...existing,
      id: `other-${title}`,
      sourcePath: `Interview/${title}.md`,
      route: `/notes/interview/other-${title.toLowerCase()}/`,
      draft,
      title,
    };
    const catalog = createRouteCatalog([existing, entry], []);
    await expect(
      renderMarkdown(`[[${title}|Readable label]]`, { ...ctx, catalog }),
    ).rejects.toThrow(draft ? /unresolved|unpublished|Missing/i : /ambiguous/i);
  }
});

it('renders real planned local geometry and oversized image source actions without nested anchors', async () => {
  const root = await mkdtemp(join(tmpdir(), 'notes-image-render-'));
  const markdown =
    '![Local](pic.jpg) <img src="pic.jpg" width="12"> <img src="pic.jpg" height="8"> <img src="pic.jpg" width="9" height="7"> ![Remote](https://example.test/remote.png) ![Large diagram](large.png?download=1#preview) [![Linked diagram](large.png?download=2#linked)![Second linked diagram](large.png?download=3#second)](https://example.test/context) ![](large.png)';
  try {
    await mkdir(join(root, 'Interview'));
    await writeFile(
      join(root, 'Interview/pic.jpg'),
      await readFile('tests/fixtures/real/task3/Ubuntu-Reference.jpg'),
    );
    const file = await open(join(root, 'Interview/large.png'), 'w');
    await file.truncate(26_214_401);
    await file.close();
    const policy = {
      roots: [
        'Books',
        'Classes',
        'Courses',
        'Interview',
        'Languages',
        'Tutorials',
      ],
      exclude: [],
      overrides: {},
      repositoryPublic: true,
      repositoryUrl: 'https://github.com/owner/repo',
      revision: 'b'.repeat(40),
    };
    const assets = await planAssets(
      root,
      ['Interview/pic.jpg', 'Interview/large.png'],
      policy,
    );
    const ctx = context(markdown);
    ctx.catalog = createRouteCatalog(
      [...ctx.catalog.sources.values()],
      assets,
      policy,
    );
    const result = await renderMarkdown(markdown, ctx);
    const tree = fromHtml(result.html, { fragment: true });
    const images: Nodes[] = [];
    const links: Nodes[] = [];
    function walk(node: Nodes, inAnchor = false): void {
      if (node.type === 'element') {
        if (node.tagName === 'a') {
          expect(inAnchor).toBe(false);
          links.push(node);
        }
        if (node.tagName === 'img') images.push(node);
        inAnchor ||= node.tagName === 'a';
      }
      if ('children' in node)
        for (const child of node.children) walk(child, inAnchor);
    }
    walk(tree);
    expect(images).toHaveLength(5);
    const properties = images.map((node) =>
      node.type === 'element' ? node.properties : {},
    );
    expect(properties.slice(0, 4)).toMatchObject([
      { width: 1700, height: 2200 },
      { width: 12, height: 16 },
      { width: 6, height: 8 },
      { width: 9, height: 7 },
    ]);
    for (const image of properties)
      expect(image).toMatchObject({ loading: 'lazy', decoding: 'async' });
    expect(properties[4]).not.toHaveProperty('width');
    const source = `https://github.com/owner/repo/blob/${'b'.repeat(40)}/Interview/large.png`;
    expect(
      links.filter((node) => text(node).includes('View image source')),
    ).toMatchObject([
      { properties: { href: `${source}?download=1#preview` } },
      { properties: { href: `${source}?download=2#linked` } },
      { properties: { href: `${source}?download=3#second` } },
      { properties: { href: source } },
    ]);
    expect(result.html).toContain('Large diagram');
    expect(result.html).toContain('Linked diagram');
    expect(result.html).toContain('Second linked diagram');
    expect(result.html).toContain('View image source: Image');
    expect(result.html).toContain('href="https://example.test/context"');
    expect(result.html).not.toContain(`<img src="${source}`);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

it('never creates zero or overflowing image geometry from an author presentation size', async () => {
  const markdown =
    '<img src="pic.png" width="40000000"><img src="pic.png" height="1">';
  const ctx = context(markdown);
  ctx.catalog.assets.get('Interview/pic.png')!.dimensions = {
    width: 1,
    height: 40_000_000,
  };
  const result = await renderMarkdown(markdown, ctx);
  expect(result.html).not.toMatch(/(?:width|height)="(?:0|1600000000000000)"/);
  expect(result.html).toContain('width="40000000"');
  expect(result.html).toContain('height="1"');
});
