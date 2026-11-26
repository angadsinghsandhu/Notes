import { createHash } from 'node:crypto';
import { readFile, stat } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import {
  createEntry,
  discoverEntries,
  readMetadata,
  readOrganization,
  readPolicy,
  resolveOrganization,
} from '../../../src/content/index.js';
import type {
  ContentEntry,
  OrganizationDefinition,
  OrganizationMigrationPlan,
} from '../../../src/content/index.js';

const root = resolve(process.cwd(), '..');
const bookRoot = 'Books/Programming PyTorch for Deep Learning - Ian Pointer/';
const reactRoot = 'Courses/Udemy/React/';
const appliedRoot = 'Interview/Applied Science/';
const bookId = 'programming-pytorch-deep-learning';
const reactId = 'react-complete-guide';
let definition: OrganizationDefinition;
let entries: ContentEntry[];
let registeredSources: Set<string>;
const unregisteredSources = [
  'Tutorials/new-unregistered-note.md',
  `${bookRoot}Chapter 1 - Getting Started with Pytorch/new-unregistered-note.md`,
  `${reactRoot}src/01 Getting Started/edited-first-app/new-unregistered-note.md`,
];
const digest = (text: string) =>
  createHash('sha256').update(text).digest('hex');
const uid = (source: string) => `doc-${digest(source)}`;

beforeAll(async () => {
  definition = await readOrganization(join(root, 'site/content/organization'));
  registeredSources = new Set(
    definition.entries.entries.map((entry) => entry.sourcePath),
  );
  const policy = await readPolicy(join(root, 'site/content/publication.json'));
  const discovery = await discoverEntries(root, policy);
  entries = (
    await Promise.all(
      discovery.sources.map(async (source) =>
        createEntry(source, await readMetadata(source, policy)),
      ),
    )
  ).filter((entry) => !entry.draft);
  const template = discovery.sources.find(
    (source) =>
      source.sourcePath ===
      `${bookRoot}Chapter 1 - Getting Started with Pytorch/ReadMe.md`,
  )!;
  const metadata = await readMetadata(template, policy);
  // Exercise the real membership assertions with future notes inside existing groups.
  entries.push(
    ...unregisteredSources.map((sourcePath) =>
      createEntry(
        {
          ...template,
          sourcePath,
          absolutePath: join(root, sourcePath),
          section: sourcePath.startsWith(bookRoot)
            ? 'books'
            : sourcePath.startsWith(reactRoot)
              ? 'courses'
              : 'tutorials',
        },
        { ...metadata, title: 'New unregistered note' },
      ),
    ),
  );
}, 30_000);

function record(source: string) {
  const found = definition.entries.entries.find(
    (entry) => entry.sourcePath === source,
  );
  expect(found, source).toBeDefined();
  return found!;
}

const appliedOrder = [
  'roadmap.md',
  'breadth/1-basics.md',
  'breadth/2-data-fitting.md',
  'breadth/3.1-linear-models.md',
  'breadth/3.2-tree-models.md',
  'breadth/3.3-svm.md',
  'breadth/4.1-clustering.md',
  'breadth/4.2-dim-reduc.md',
  'breadth/5-prob-models.md',
  'breadth/6.1-nn-basics.md',
  'breadth/6.2-cnn.md',
  'breadth/6.3-cv.md',
  'breadth/6.4-nlp.md',
  'breadth/6.5-seq-models.md',
  'breadth/6.6.1-attn.md',
  'breadth/6.6.2-transformers.md',
  'breadth/7-rl.md',
  'breadth/8-train-optim.md',
  'breadth/9-splits.md',
  'breadth/10-eval.md',
  'breadth/11-practical.md',
  'breadth/12-stats.md',
];
const chapterDirectories = [
  'Chapter 0 - Preface',
  'Chapter 1 - Getting Started with Pytorch',
  'Chapter 2 - Image Clasification with Pytorch',
  'Chapter 3 - Convolutional Neural Networks',
  'Chapter 4 - Transfer Learning and Other Tricks',
  'Chapter 5 - Text Classification',
  'Chapter 6 - A Journey into Sound',
];

// These fixed inventories were independently matched to current source paths and IDs.
const reviewedPilotSets = [
  [
    appliedRoot,
    22,
    'ee7bc4c9ab576e69260804b604d5b751d7d5705df259a9c6d270c4ca398996cd',
  ],
  [
    bookRoot,
    13,
    '471c678adf05a5737aaf8fe85f9906c5a266af70faf7209050a373875990e759',
  ],
  [
    reactRoot,
    5071,
    '8cc3a04cbbf5cac99529160f736520607efd27ae5b1c1218302f0cfe24dde29e',
  ],
] as const;

describe('reviewed organization pilot data', () => {
  it('preserves initial reviewed enrollment while permitting new unregistered public sources', async () => {
    const records = definition.entries.entries;
    const audit = JSON.parse(
      await readFile(
        join(root, 'site/content/organization-migration-report.json'),
        'utf8',
      ),
    ) as Pick<OrganizationMigrationPlan, 'inventory'>;
    const initialPublicSources = audit.inventory
      .filter((entry) => entry.entryId && entry.disposition !== 'excluded')
      .map((entry) => entry.sourcePath)
      .sort();
    expect(initialPublicSources).toHaveLength(6279);
    expect(records.map((entry) => entry.sourcePath).sort()).toEqual(
      initialPublicSources,
    );
    const currentSources = new Set(entries.map((entry) => entry.sourcePath));
    expect(
      initialPublicSources.every((source) => currentSources.has(source)),
    ).toBe(true);
    expect(new Set(records.map((entry) => entry.uid)).size).toBe(6279);
    const registered = new Set(records.map((entry) => entry.sourcePath));
    for (const entry of entries.filter((entry) =>
      registered.has(entry.sourcePath),
    )) {
      const enrolled = record(entry.sourcePath);
      expect(enrolled.uid).toBe(`doc-${entry.id}`);
      expect(enrolled.purpose).toBe(
        entry.kind === 'code'
          ? 'project-file'
          : !entry.role && ['markdown', 'notebook'].includes(entry.kind)
            ? 'note'
            : 'reference',
      );
      expect(enrolled.status).toBe(
        chapterDirectories
          .slice(4)
          .some(
            (chapter) => entry.sourcePath === `${bookRoot}${chapter}/ReadMe.md`,
          )
          ? 'outline'
          : 'unreviewed',
      );
    }
    expect(records.filter((entry) => entry.status === 'outline')).toHaveLength(
      3,
    );
    const remainder = records.filter(
      (entry) =>
        !reviewedPilotSets.some(([prefix]) =>
          entry.sourcePath.startsWith(prefix),
        ),
    );
    expect(remainder).toHaveLength(1173);
    for (const entry of remainder) {
      expect(entry.topics).toEqual([]);
      expect(entry.collectionId).toBeUndefined();
    }
  });

  it.each(unregisteredSources)(
    'publishes unenrolled Markdown note %s with fallback classification',
    (source) => {
      const additional = entries.find((entry) => entry.sourcePath === source)!;
      const snapshot = resolveOrganization(entries, definition);
      expect(
        definition.entries.entries.find((entry) => entry.sourcePath === source),
      ).toBeUndefined();
      expect(
        snapshot.memberships.find((member) => member.entryId === additional.id),
      ).toEqual({
        entryId: additional.id,
        topics: [],
        purpose: 'note',
        status: 'unreviewed',
        summary: '',
        relatedUids: [],
      });
    },
  );

  it.each(reviewedPilotSets)(
    'preserves the exact reviewed source/UID set for %s',
    (prefix, count, expectedHash) => {
      const records = definition.entries.entries.filter((entry) =>
        entry.sourcePath.startsWith(prefix),
      );
      expect(records).toHaveLength(count);
      const inventory = records
        .map((entry) => [entry.sourcePath, entry.uid])
        .sort(([left], [right]) =>
          left! < right! ? -1 : left! > right! ? 1 : 0,
        );
      expect(digest(JSON.stringify(inventory))).toBe(expectedHash);
    },
  );

  it('links all applied-science notes once in the explicit study order to canonical readers', () => {
    expect(definition.paths.paths).toHaveLength(1);
    const path = definition.paths.paths[0]!;
    expect(path.id).toBe('applied-scientist-interview-preparation');
    expect(path.steps.map((step) => step.entryUids)).toEqual(
      appliedOrder.map((source) => [uid(`${appliedRoot}${source}`)]),
    );
    const snapshot = resolveOrganization(entries, definition);
    expect(snapshot.paths[0]!.steps).toEqual(path.steps);
    for (const source of appliedOrder) {
      expect(record(`${appliedRoot}${source}`).topics.length).toBeGreaterThan(
        0,
      );
      const entry = entries.find(
        (entry) => entry.sourcePath === `${appliedRoot}${source}`,
      )!;
      expect(entry.route.startsWith('/notes/interview/applied-science/')).toBe(
        true,
      );
      expect(
        snapshot.memberships.find((member) => member.entryId === entry.id)?.uid,
      ).toBe(uid(entry.sourcePath));
    }
    expect(
      entries.find(
        (entry) => entry.sourcePath === `${appliedRoot}breadth/6.2-cnn.md`,
      )?.route,
    ).toBe('/notes/interview/applied-science/breadth/6-2-cnn/');
  });

  it('keeps ordered book chapters and the matching notebooks, code and whole-book PDF adjacent', () => {
    expect(
      definition.collections.collections.map((collection) => collection.id),
    ).toEqual([bookId, reactId]);
    const groups = definition.collections.groups.filter(
      (group) => group.collectionId === bookId,
    );
    expect(groups.map((group) => [group.id, group.type, group.order])).toEqual(
      chapterDirectories.map((_, chapter) => [
        `chapter-${chapter}`,
        'chapter',
        chapter,
      ]),
    );
    for (const [chapter, directory] of chapterDirectories.entries()) {
      const expected = entries.filter(
        (entry) =>
          entry.sourcePath.startsWith(`${bookRoot}${directory}/`) &&
          registeredSources.has(entry.sourcePath),
      );
      const actual = definition.entries.entries.filter(
        (entry) =>
          entry.collectionId === bookId &&
          entry.groupId === `chapter-${chapter}`,
      );
      expect(actual.map((entry) => entry.sourcePath).sort()).toEqual(
        expected.map((entry) => entry.sourcePath).sort(),
      );
    }
    for (const [chapter, name] of [
      [1, 'basic_pytorch.ipynb'],
      [2, 'ch2.ipynb'],
      [2, 'download.py'],
      [3, 'ch3.ipynb'],
    ] as const) {
      const source = `${bookRoot}${chapterDirectories[chapter]}/${name}`;
      expect(record(source).relatedUids).toEqual([
        uid(`${bookRoot}${chapterDirectories[chapter]}/ReadMe.md`),
      ]);
      expect(record(source).groupId).toBe(`chapter-${chapter}`);
    }
    const pdf = record(
      `${bookRoot}Programming PyTorch for Deep Learning - Ian Pointer.pdf`,
    );
    expect(pdf.collectionId).toBe(bookId);
    expect(pdf.groupId).toBeUndefined();
    expect(pdf.topics).toEqual([]);
    expect(record(`${bookRoot}ReadMe.md`).topics).toEqual([
      'frameworks-gpu-computing',
    ]);
  });

  it('keeps all 34 React modules and 363 real source snapshots separate without losing direct resources', async () => {
    const groups = definition.collections.groups.filter(
      (group) => group.collectionId === reactId,
    );
    expect(groups).toHaveLength(398);
    const modules = groups.filter((group) => group.type === 'module');
    const projects = groups.filter((group) => group.type === 'project');
    expect(modules).toHaveLength(34);
    expect(projects).toHaveLength(363);
    const roots = projects.map((project) => {
      const module = modules.find((module) => module.id === project.parentId);
      expect(module).toBeDefined();
      return `${reactRoot}src/${module!.title}/${project.title}`;
    });
    expect(digest([...roots].sort().join('\n'))).toBe(
      'c39fea821afdf426aaa95ec42c792afc1f69d00ba08822532d6b219942034596',
    );
    const assigned = new Set<string>();
    for (const [index, project] of projects.entries()) {
      const sourceRoot = roots[index]!;
      expect((await stat(join(root, sourceRoot))).isDirectory()).toBe(true);
      const expected = entries.filter(
        (entry) =>
          entry.sourcePath.startsWith(`${sourceRoot}/`) &&
          registeredSources.has(entry.sourcePath),
      );
      expect(expected.length).toBeGreaterThan(0);
      const actual = definition.entries.entries.filter(
        (entry) =>
          entry.collectionId === reactId && entry.groupId === project.id,
      );
      expect(actual.map((entry) => entry.sourcePath).sort()).toEqual(
        expected.map((entry) => entry.sourcePath).sort(),
      );
      actual.forEach((entry) => assigned.add(entry.sourcePath));
    }
    expect(assigned.size).toBe(4998);
    const directModule = definition.entries.entries.filter(
      (entry) =>
        entry.collectionId === reactId &&
        modules.some((module) => module.id === entry.groupId),
    );
    expect(directModule).toHaveLength(68);
    expect(
      definition.entries.entries.filter(
        (entry) =>
          entry.collectionId === reactId &&
          entry.groupId === 'course-references',
      ),
    ).toHaveLength(4);
    expect(
      definition.entries.entries
        .filter((entry) => entry.collectionId === reactId && !entry.groupId)
        .map((entry) => entry.sourcePath),
    ).toEqual([`${reactRoot}README.md`]);
    for (const name of [
      '17b Form Actions',
      '25 NextJS App Router Introduction',
      '25 NextJS Introduction',
      '25b RSC, Suspense, Server Actions',
      '27 Patterns',
      '27 Replacing Redux with Hooks',
    ])
      expect(modules.find((module) => module.title === name)).toBeDefined();
    const groupFor = (source: string) =>
      record(`${reactRoot}src/${source}`).groupId;
    expect(groupFor('28 Testing/01-starting-project/src/App.js')).not.toBe(
      groupFor('28 Testing/01-starting-project-vite/src/App.jsx'),
    );
    expect(
      groupFor(
        '01 Getting Started/react-vs-vanilla-js-example/just-js/index.html',
      ),
    ).not.toBe(
      groupFor(
        '01 Getting Started/react-vs-vanilla-js-example/react/src/App.js',
      ),
    );
    expect(groupFor('30 React Summary/21-finished/backend/app.js')).toBe(
      groupFor('30 React Summary/21-finished/react-app/src/main.jsx'),
    );
    expect(groupFor('02 JS Refresher/code/finished/index.html')).toBe(
      'project-02-js-refresher-code-finished',
    );
  }, 30_000);

  it('keeps all React code in file scope and preserves the 37 supplemental roles', () => {
    const react = entries.filter((entry) =>
      entry.sourcePath.startsWith(reactRoot),
    );
    expect(react.filter((entry) => entry.kind === 'code')).toHaveLength(5027);
    for (const entry of react.filter((entry) => entry.kind === 'code')) {
      expect(record(entry.sourcePath).purpose).toBe('project-file');
      expect(record(entry.sourcePath).topics).toEqual([]);
      expect(record(entry.sourcePath).groupId).toBeDefined();
    }
    expect(react.filter((entry) => entry.role === 'supplemental')).toHaveLength(
      37,
    );
    for (const entry of react.filter((entry) => entry.role === 'supplemental'))
      expect(record(entry.sourcePath).purpose).toBe('reference');
    expect(
      record(`${reactRoot}notes/Section 2 - JavaScript Refresher.md`).topics,
    ).toEqual(['javascript-typescript']);
    expect(
      record(
        `${reactRoot}notes/09 Practice Project - Project Management/tailwind-css-classes-used.md`,
      ).topics,
    ).toEqual(['css-tailwind']);
  });

  it('uses approved topic labels and evidenced CNN overlap without inventing book transformer teaching', async () => {
    const allowed = [
      'Mathematics & Statistics',
      'Probability',
      'Statistics & Experimentation',
      'Machine Learning',
      'Foundations & Data Preparation',
      'Supervised Learning',
      'Unsupervised Learning',
      'Probabilistic Models',
      'Training & Regularization',
      'Evaluation & Validation',
      'Deep Learning',
      'Neural Networks',
      'Computer Vision',
      'Natural Language Processing',
      'Attention, Transformers & Language Models',
      'Audio & Speech',
      'Reinforcement Learning',
      'Frameworks & GPU Computing',
      'Web Development',
      'JavaScript & TypeScript',
      'React',
      'CSS & Tailwind',
    ];
    expect(definition.taxonomy.topics.map((topic) => topic.title)).toEqual(
      allowed,
    );
    const topicIds = new Set(
      definition.taxonomy.topics.map((topic) => topic.id),
    );
    for (const entry of definition.entries.entries)
      for (const topic of entry.topics) expect(topicIds.has(topic)).toBe(true);
    for (const source of [
      `${appliedRoot}breadth/6.2-cnn.md`,
      `${bookRoot}${chapterDirectories[3]}/ReadMe.md`,
      `${bookRoot}${chapterDirectories[3]}/ch3.ipynb`,
    ])
      expect(record(source).topics).toEqual(
        expect.arrayContaining(['computer-vision', 'neural-networks']),
      );
    expect(
      definition.entries.entries.filter(
        (entry) =>
          entry.sourcePath.startsWith(bookRoot) &&
          entry.topics.includes('attention-transformers-language-models'),
      ),
    ).toEqual([]);
    expect(
      record(`${appliedRoot}breadth/6.6.2-transformers.md`).topics,
    ).toEqual(['attention-transformers-language-models']);
    for (const chapter of chapterDirectories.slice(4)) {
      const text = await readFile(
        join(root, bookRoot, chapter, 'ReadMe.md'),
        'utf8',
      );
      expect(
        text
          .replace(/^---\n[\s\S]*?\n---\n/, '')
          .split('\n')
          .every((line) => !line.trim() || /^#{1,6} /.test(line)),
      ).toBe(true);
    }
  });
});
