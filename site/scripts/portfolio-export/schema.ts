import { z } from 'zod';

const text = z.string();
const label = text.min(1);
const strings = z.array(text);
const slug = text.regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
const slugs = z.array(slug);
const digest = text.regex(/^[a-f0-9]{64}$/);
const sourceSha = text.regex(/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/);

function decodePath(value: string): string | undefined {
  try {
    return decodeURIComponent(value);
  } catch {
    return undefined;
  }
}

const alias = text
  .regex(/^\/(?:[a-zA-Z0-9_.%_-]+\/)*[a-zA-Z0-9_.%_-]*\/?$/)
  .refine(
    (value) =>
      !value.startsWith('//') &&
      value.split('/').every((part) => {
        const decoded = decodePath(part);
        return (
          decoded !== undefined &&
          decoded !== '.' &&
          decoded !== '..' &&
          !/[/\\%]/u.test(decoded) &&
          [...decoded].every(
            (char) => char.charCodeAt(0) >= 32 && char.charCodeAt(0) !== 127,
          )
        );
      }),
    'Aliases must be normalized URL paths with safe percent escapes',
  );
const route = text.regex(/^\/(?:[a-z0-9]+(?:-[a-z0-9]+)*\/)+$/);
const number = z.int().min(1).max(2000);
const problemId = text.regex(/^leetcode:(?:[1-9][0-9]{0,2}|1[0-9]{3}|2000)$/);
const uid = text.regex(/^doc-[a-f0-9]{64}$/);
const entryId = z.union([uid, digest]);
const publicAsset = text.regex(
  /^\/content-assets\/[a-f0-9]{64}\.(?:png|jpg|gif|webp|avif|svg|ico|pdf|ppt|pptx)$/,
);
const tracePath = text.regex(/^\/practice-traces\/[a-f0-9]{64}\.json$/);
const https = z.url().refine((value) => {
  const url = URL.parse(value);
  return url?.protocol === 'https:' && !url.username && !url.password;
});
const action = z.union([publicAsset, https]);
const bytes = z
  .int()
  .nonnegative()
  .max(25 * 1024 * 1024);
const heading = z.strictObject({
  id: text,
  text,
  depth: z.int().min(1).max(6),
});
const asset = z.strictObject({
  bytes,
  sha256: digest,
});
const pagesAsset = asset.extend({
  publicPath: publicAsset,
  exportPath: text.regex(
    /^assets\/[a-f0-9]{64}\.(?:png|jpg|gif|webp|avif|svg|ico|pdf|ppt|pptx)$/,
  ),
});
const workerAsset = asset.extend({
  publicPath: tracePath,
  exportPath: text.regex(
    /^worker-assets\/practice-traces\/[a-f0-9]{64}\.json$/,
  ),
});
const entry = z.strictObject({
  id: entryId,
  title: label,
  kind: z.enum(['markdown', 'notebook', 'code', 'pdf', 'slides']),
  route,
  aliases: z.array(alias),
  headings: z.array(heading),
  anchors: strings,
  description: text,
  tags: strings,
  section: z.enum([
    'books',
    'classes',
    'courses',
    'interview',
    'languages',
    'tutorials',
  ]),
  groupSegments: strings,
  searchIndexed: z.literal(true),
  role: z.literal('supplemental').optional(),
  order: z.number().optional(),
  updated: z.iso.date().optional(),
  bodyHtml: text.optional(),
  assetUrl: action.optional(),
  sourceUrl: action.optional(),
});
const described = { id: slug, title: label, summary: text };
const hierarchical = {
  parentId: slug.optional(),
  order: z.number().optional(),
};
const organization = z.strictObject({
  topics: z.array(z.strictObject({ ...described, ...hierarchical })),
  collections: z.array(
    z.strictObject({
      ...described,
      type: z.enum(['book', 'university-course', 'online-course', 'workshop']),
      provider: label.optional(),
      courseCode: label.optional(),
      edition: label.optional(),
      year: z.int().optional(),
      semester: label.optional(),
    }),
  ),
  groups: z.array(
    z.strictObject({
      ...described,
      ...hierarchical,
      collectionId: slug,
      type: z.enum(['chapter', 'module', 'project', 'assessment', 'reference']),
    }),
  ),
  paths: z.array(
    z.strictObject({
      ...described,
      steps: z.array(
        z.strictObject({
          ...described,
          entryUids: z.array(uid),
          topicIds: slugs,
        }),
      ),
    }),
  ),
  memberships: z.array(
    z.strictObject({
      entryId,
      uid: uid.optional(),
      topics: slugs,
      collectionId: slug.optional(),
      groupId: slug.optional(),
      purpose: z.enum(['note', 'exercise', 'reference', 'project-file']),
      status: z.enum(['unreviewed', 'outline', 'reviewed']),
      summary: text,
      relatedUids: z.array(uid),
    }),
  ),
});
const company = z.strictObject({
  companyId: slug,
  companyName: label,
  observedOn: z.iso.date(),
  reportingPeriod: label.optional(),
  sourceUrl: https.optional(),
});
const problem = z.strictObject({
  id: problemId,
  number,
  status: z.literal('verified'),
  title: label,
  slug,
  officialUrl: text.regex(
    /^https:\/\/leetcode\.com\/problems\/[a-z0-9]+(?:-[a-z0-9]+)*\/$/,
  ),
  domain: z.enum(['algorithm', 'sql', 'shell', 'concurrency']),
  difficulty: z.enum(['easy', 'medium', 'hard']),
  topics: slugs,
  officialQuestionObservedOn: z.iso.date(),
  companies: z.array(company),
});
const transcript = z.strictObject({
  exampleId: slug,
  steps: z.array(
    z.strictObject({
      stepId: slug,
      codeLines: z.array(z.int().positive()),
      explanation: label,
    }),
  ),
});
const lesson = z.strictObject({
  problemId,
  route: text.regex(/^\/practice\/leetcode\/[1-9][0-9]*\/$/),
  status: z.literal('verified'),
  bodyHtml: text,
  headings: z.array(heading),
  approaches: z.array(
    z.strictObject({
      id: slug,
      title: label,
      language: z.enum(['python', 'sql', 'shell']),
      implementationSha256: digest,
      entryPoint: text.regex(/^[a-zA-Z_][a-zA-Z_0-9]*$/).nullable(),
      codeHtml: text,
      trace: asset.extend({ url: tracePath, exampleIds: slugs }).nullable(),
      transcripts: z.array(transcript),
    }),
  ),
});
const node = { id: slug, childIds: slugs, prerequisiteIds: slugs };
const curriculum = z.strictObject({
  generation: digest.nullable(),
  problems: z.array(problem),
  lessons: z.array(lesson),
  paths: z.array(
    z.strictObject({
      id: slug,
      title: label,
      description: label,
      rootIds: slugs,
      nodes: z.array(
        z.discriminatedUnion('kind', [
          z.strictObject({ ...node, kind: z.literal('stage'), title: label }),
          z.strictObject({
            ...node,
            kind: z.literal('problem'),
            problemId,
            title: label.optional(),
          }),
        ]),
      ),
    }),
  ),
  pendingPathLabels: z.array(
    z.strictObject({ pathId: slug, nodeId: slug, problemId, title: label }),
  ),
  sourceVariants: z.array(
    z.strictObject({
      sourceId: entryId,
      sourceRoute: route,
      problemId,
      lessonRoute: lesson.shape.route,
    }),
  ),
  traceAssets: z.array(workerAsset),
});

const snapshot = z.strictObject({
  schemaVersion: z.literal(1),
  mode: z.enum(['production', 'preview']),
  sourceSha,
  entries: z.array(entry),
  organization,
  assets: z.array(pagesAsset),
  verifiedCurriculumIds: z.array(number),
  curriculum,
});

export type PortfolioSnapshotV1 = z.infer<typeof snapshot>;

function assertReferences(data: PortfolioSnapshotV1, context: z.RefinementCtx) {
  const issue = (message: string) =>
    context.addIssue({ code: 'custom', message });
  const index = <Item, Key>(
    items: Item[],
    key: (item: Item) => Key,
    field: string,
  ) => {
    const indexed = new Map(items.map((item) => [key(item), item]));
    if (indexed.size !== items.length) issue(`Duplicate ${field}`);
    return indexed;
  };
  const { entries, organization, curriculum, assets, verifiedCurriculumIds } =
    data;
  const entryIndex = index(entries, ({ id }) => id, 'entry ID');
  const pagesAssets = index(
    assets,
    ({ publicPath }) => publicPath,
    'Pages asset',
  );
  const workerAssets = index(
    curriculum.traceAssets,
    ({ publicPath }) => publicPath,
    'Worker asset',
  );
  const normalizeRoute = (value: string) =>
    (decodePath(value) ?? value).replace(/\/+$/, '').toLowerCase();
  index(
    entries.flatMap(({ route, aliases }) => [route, ...aliases]),
    normalizeRoute,
    'public route',
  );
  for (const { publicPath, exportPath, sha256 } of assets) {
    const filename = publicPath.slice('/content-assets/'.length);
    if (exportPath !== `assets/${filename}`)
      issue(`Pages asset export path differs from ${publicPath}`);
    if (filename.split('.')[0] !== sha256)
      issue(`Pages asset digest differs from ${publicPath}`);
  }
  for (const entry of entries) {
    const resource = entry.kind === 'pdf' || entry.kind === 'slides';
    if (
      resource
        ? !entry.assetUrl || entry.bodyHtml !== undefined
        : entry.bodyHtml === undefined
    )
      issue(`Incomplete prepared entry ${entry.route}`);
    for (const url of [entry.assetUrl, entry.sourceUrl]) {
      if (url?.startsWith('/') && !pagesAssets.has(url))
        issue(`Unregistered Pages asset ${url}`);
    }
  }

  const membership = index(
    organization.memberships,
    ({ entryId }) => entryId,
    'organization membership',
  );
  if (
    membership.size !== entries.length ||
    [...membership.keys()].some((id) => !entryIndex.has(id))
  )
    issue('Organization membership IDs differ from archive entry IDs');

  const documentUids = new Set<string>();
  for (const { entryId, uid } of organization.memberships) {
    if (uid === undefined) continue;
    if (uid !== entryId)
      issue(`Organization document UID differs from entry ID ${entryId}`);
    else documentUids.add(uid);
  }
  for (const { relatedUids } of organization.memberships)
    for (const uid of relatedUids)
      if (!documentUids.has(uid))
        issue(`Unregistered related document UID ${uid}`);
  for (const { steps } of organization.paths)
    for (const { entryUids } of steps)
      for (const uid of entryUids)
        if (!documentUids.has(uid))
          issue(`Unregistered path step document UID ${uid}`);

  const { problems, lessons, paths, pendingPathLabels, sourceVariants } =
    curriculum;
  const problemIndex = index(problems, ({ id }) => id, 'verified problem ID');
  const lessonIndex = index(
    lessons,
    ({ problemId }) => problemId,
    'verified lesson ID',
  );
  const verifiedNumbers = new Set(verifiedCurriculumIds);
  if (
    problems.length !== verifiedCurriculumIds.length ||
    verifiedNumbers.size !== problems.length ||
    lessons.length !== problems.length ||
    problems.some(
      ({ id, number }) =>
        id !== `leetcode:${number}` ||
        !verifiedNumbers.has(number) ||
        lessonIndex.get(id)?.route !== `/practice/leetcode/${number}/`,
    )
  )
    issue(
      'Verified curriculum numbers, problems and canonical lesson routes differ',
    );

  if (curriculum.generation === null && (problems.length || paths.length))
    issue('Curriculum projection is missing its verified generation');

  const linkedPackages = new Set<string>();
  for (const { approaches } of lessons) {
    for (const { trace } of approaches) {
      if (!trace) continue;
      linkedPackages.add(trace.url);
      const asset = workerAssets.get(trace.url);
      if (
        !asset ||
        asset.bytes !== trace.bytes ||
        asset.sha256 !== trace.sha256 ||
        trace.url !== `/practice-traces/${trace.sha256}.json` ||
        asset.exportPath !== `worker-assets${trace.url}`
      )
        issue(`Trace reference does not match package ${trace.url}`);
    }
  }
  if (linkedPackages.size !== workerAssets.size)
    issue('Unregistered Worker trace asset');
  for (const item of sourceVariants) {
    if (
      lessonIndex.get(item.problemId)?.route !== item.lessonRoute ||
      entryIndex.get(item.sourceId)?.route !== item.sourceRoute
    )
      issue(`Invalid curriculum source variant ${item.sourceRoute}`);
  }

  const labelKey = (pathId: string, nodeId: string) => `${pathId}/${nodeId}`;
  const labels = index(
    pendingPathLabels,
    ({ pathId, nodeId }) => labelKey(pathId, nodeId),
    'pending path label',
  );
  for (const { id, nodes } of paths) {
    for (const node of nodes) {
      if (node.kind !== 'problem') continue;
      const key = labelKey(id, node.id);
      if (problemIndex.has(node.problemId)) {
        if (!node.title || labels.has(key))
          issue(`Invalid verified path node ${key}`);
      } else {
        if (
          node.title !== undefined ||
          labels.get(key)?.problemId !== node.problemId
        )
          issue(`Invalid pending path node ${key}`);
        labels.delete(key);
      }
    }
  }
  if (labels.size) issue('Unregistered pending path label');
}

export const portfolioSnapshotV1 = snapshot.superRefine(assertReferences);
