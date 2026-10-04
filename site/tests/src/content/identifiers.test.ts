import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import {
  assertUniqueRoutes,
  createEntry,
  compareSourcePaths,
} from '../../../src/content/identifiers.js';
import type { Metadata, SourceEntry } from '../../../src/content/types.js';
const metadata: Metadata = {
  title: 'Title',
  description: '',
  tags: [],
  aliases: [],
  draft: false,
};
function source(
  sourcePath: string,
  kind: SourceEntry['kind'] = 'markdown',
): SourceEntry {
  return {
    sourcePath,
    absolutePath: `/archive/${sourcePath}`,
    section: sourcePath.startsWith('Languages') ? 'languages' : 'tutorials',
    kind,
    bytes: 0,
  };
}
describe('canonical identifiers', () => {
  it.each(['README.md', 'ReadMe.md', 'readme.MD'])(
    'makes %s the directory landing note',
    (filename) => {
      expect(
        createEntry(
          source(`Tutorials/AI/Andrej Karpathy/Let's build GPT/${filename}`),
          metadata,
        ).route,
      ).toBe('/notes/tutorials/ai/andrej-karpathy/lets-build-gpt/');
    },
  );
  it('has stable source-derived IDs and NFC normalization', () => {
    const path = "Tutorials/AI/Let's build GPT/notes/README.md";
    expect(createEntry(source(path), metadata)).toMatchObject({
      id: createHash('sha256').update(path).digest('hex'),
      groupSegments: ['AI', "Let's build GPT", 'notes'],
      headings: [],
    });
    expect(createEntry(source('Tutorials/Cafe\u0301.md'), metadata).id).toBe(
      createEntry(source('Tutorials/Café.md'), metadata).id,
    );
  });
  it('uses exact original-segment SHA fallback for synthetic Unicode', () => {
    const hash = createHash('sha256')
      .update('日本語')
      .digest('hex')
      .slice(0, 8);
    expect(
      createEntry(source('Languages/Japanese/日本語.md'), metadata).route,
    ).toBe(`/notes/languages/japanese/item-${hash}/`);
  });
  it('distinguishes same-stem resources and honors explicit slugs', () => {
    const entries = ['html', 'js', 'css'].map((ext) =>
      createEntry(source(`Tutorials/project/index.${ext}`, 'code'), metadata),
    );
    expect(entries.map((entry) => entry.route)).toEqual([
      '/resources/tutorials/project/index-html/',
      '/resources/tutorials/project/index-js/',
      '/resources/tutorials/project/index-css/',
    ]);
    expect(
      createEntry(source('Tutorials/project/index.js', 'code'), {
        ...metadata,
        slug: 'curated/demo',
      }).route,
    ).toBe('/resources/tutorials/curated/demo/');
    expect(() => assertUniqueRoutes(entries)).not.toThrow();
  });
  it.each([
    ['Tutorials/Foo.md', 'Tutorials/foo.md'],
    ['Tutorials/a b.md', 'Tutorials/a-b.md'],
  ])('fails remaining route collisions with both paths', (a, b) => {
    const check = () =>
      assertUniqueRoutes([
        createEntry(source(a), metadata),
        createEntry(source(b), metadata),
      ]);
    expect(check).toThrow(a);
    expect(check).toThrow(b);
  });
  it('detects alias-route and alias-alias collisions including case variants', () => {
    const a = createEntry(source('Tutorials/a.md'), {
      ...metadata,
      aliases: ['/notes/tutorials/B/'],
    });
    const b = createEntry(source('Tutorials/b.md'), metadata);
    expect(() => assertUniqueRoutes([a, b])).toThrow('Tutorials/a.md');
    expect(() =>
      assertUniqueRoutes([a, { ...b, aliases: ['/notes/tutorials/B/'] }]),
    ).toThrow('Tutorials/b.md');
  });
  it('sorts numeric source inputs naturally with deterministic case tie breaks', () => {
    expect(
      ['Tutorials/10.md', 'Tutorials/2.md', 'Tutorials/1.md'].sort(
        compareSourcePaths,
      ),
    ).toEqual(['Tutorials/1.md', 'Tutorials/2.md', 'Tutorials/10.md']);
    expect(compareSourcePaths('Tutorials/A.md', 'Tutorials/a.md')).not.toBe(0);
  });
});
