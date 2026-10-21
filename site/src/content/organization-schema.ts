import { readFile, stat } from 'node:fs/promises';
import { join } from 'node:path';
import { z } from 'zod';
import { CONTENT_ROOTS } from './schema.js';
import type { OrganizationDefinition } from './organization-types.js';

const id = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
const uid = z.string().regex(/^doc-[a-f0-9]{64}$/);
const title = z.string().trim().min(1);
const ids = (schema: typeof id) =>
  z
    .array(schema)
    .refine(
      (values) => new Set(values).size === values.length,
      'References must be unique',
    );
const sourcePath = z.string().refine((value) => {
  const segments = value.split('/');
  return (
    segments.length > 1 &&
    CONTENT_ROOTS.some((root) => root === segments[0]) &&
    segments.every(
      (segment) => segment !== '' && segment !== '.' && segment !== '..',
    ) &&
    !value.includes('\\') &&
    value === value.normalize('NFC') &&
    Array.from(value).every((character) => {
      const code = character.charCodeAt(0);
      return code >= 32 && code !== 127;
    })
  );
}, 'Expected a normalized repository-relative sourcePath under a content root');
const descriptive = { id, title, summary: z.string() };
const topic = z
  .object({
    ...descriptive,
    parentId: id.optional(),
    order: z.number().optional(),
  })
  .strict();
const collection = z
  .object({
    ...descriptive,
    type: z.enum(['book', 'university-course', 'online-course', 'workshop']),
    provider: title.optional(),
    courseCode: title.optional(),
    edition: title.optional(),
    year: z.number().int().optional(),
    semester: title.optional(),
  })
  .strict();
const group = z
  .object({
    ...descriptive,
    collectionId: id,
    parentId: id.optional(),
    type: z.enum(['chapter', 'module', 'project', 'assessment', 'reference']),
    order: z.number().optional(),
  })
  .strict();
const entry = z
  .object({
    uid,
    sourcePath,
    topics: ids(id),
    collectionId: id.optional(),
    groupId: id.optional(),
    purpose: z.enum(['note', 'exercise', 'reference', 'project-file']),
    status: z.enum(['unreviewed', 'outline', 'draft', 'reviewed']),
    summary: z.string().optional(),
    relatedUids: ids(uid).optional(),
  })
  .strict();
const step = z
  .object({ ...descriptive, entryUids: ids(uid), topicIds: ids(id) })
  .strict();
const path = z.object({ ...descriptive, steps: z.array(step) }).strict();
const schema = z
  .object({
    taxonomy: z
      .object({ version: z.literal(1), topics: z.array(topic) })
      .strict(),
    collections: z
      .object({
        version: z.literal(1),
        collections: z.array(collection),
        groups: z.array(group),
      })
      .strict(),
    entries: z
      .object({ version: z.literal(1), entries: z.array(entry) })
      .strict(),
    paths: z.object({ version: z.literal(1), paths: z.array(path) }).strict(),
  })
  .strict();

function unique<T>(
  records: readonly T[],
  key: (record: T) => string,
  name: string,
): Map<string, T> {
  const indexed = new Map<string, T>();
  for (const record of records) {
    const value = key(record);
    if (indexed.has(value.toLowerCase()))
      throw new Error(
        `${name} ${value}: duplicate or case-colliding identifier`,
      );
    indexed.set(value.toLowerCase(), record);
  }
  return indexed;
}
function requireReference<T>(
  records: Map<string, T>,
  key: string,
  owner: string,
): void {
  if (!records.has(key)) throw new Error(`${owner}: unknown reference ${key}`);
}
function hierarchy<T extends { id: string; parentId?: string | undefined }>(
  records: readonly T[],
  key: (record: T) => string,
  parentKey: (record: T, parentId: string) => string,
  name: string,
  maxDepth = Infinity,
): void {
  const indexed = unique(records, key, name);
  for (const record of records) {
    const visited = new Set<string>();
    let current: T | undefined = record;
    while (current) {
      const currentKey = key(current);
      if (visited.has(currentKey))
        throw new Error(
          `${name} ${key(record)}: parent cycle at ${currentKey}`,
        );
      visited.add(currentKey);
      if (visited.size > maxDepth)
        throw new Error(`${name} ${key(record)}: depth exceeds ${maxDepth}`);
      if (!current.parentId) break;
      const parent = parentKey(current, current.parentId);
      requireReference(indexed, parent, `${name} ${key(record)}`);
      current = indexed.get(parent);
    }
  }
}
function schemaDiagnostic(value: unknown, issue: z.core.$ZodIssue): string {
  let current: unknown = value;
  let record = '';
  for (const segment of issue.path) {
    if (typeof current !== 'object' || current === null) break;
    current = Reflect.get(current, segment);
    if (typeof current === 'object' && current !== null) {
      const label: unknown =
        Reflect.get(current, 'sourcePath') ??
        Reflect.get(current, 'id') ??
        Reflect.get(current, 'uid');
      if (typeof label === 'string') record = ` (${label})`;
    }
  }
  return `${issue.path.join('.')}${record}: ${issue.message}`;
}

export function validateOrganization(value: unknown): OrganizationDefinition {
  const result = schema.safeParse(value);
  if (!result.success)
    throw new Error(
      `Invalid organization: ${result.error.issues.map((issue) => schemaDiagnostic(value, issue)).join('; ')}`,
    );
  const definition = result.data;
  const { topics } = definition.taxonomy;
  const { collections, groups } = definition.collections;
  const { entries } = definition.entries;
  const topicIndex = unique(topics, (record) => record.id, 'topic');
  const collectionIndex = unique(
    collections,
    (record) => record.id,
    'collection',
  );
  const groupKey = (record: { collectionId: string; id: string }) =>
    `${record.collectionId}/${record.id}`;
  const groupIndex = unique(groups, groupKey, 'group');
  const entryIndex = unique(entries, (record) => record.uid, 'entry');
  unique(entries, (record) => record.sourcePath, 'entry sourcePath');
  unique(definition.paths.paths, (record) => record.id, 'path');
  hierarchy(
    topics,
    (record) => record.id,
    (_record, parent) => parent,
    'topic',
    3,
  );
  hierarchy(
    groups,
    groupKey,
    (record, parent) => `${record.collectionId}/${parent}`,
    'group',
  );
  for (const record of groups)
    requireReference(
      collectionIndex,
      record.collectionId,
      `group ${groupKey(record)}`,
    );
  for (const record of entries) {
    const owner = `entry ${record.sourcePath} (${record.uid})`;
    for (const topicId of record.topics)
      requireReference(topicIndex, topicId, owner);
    if (record.collectionId)
      requireReference(collectionIndex, record.collectionId, owner);
    if (record.groupId) {
      if (!record.collectionId)
        throw new Error(`${owner}: groupId requires collectionId`);
      requireReference(
        groupIndex,
        `${record.collectionId}/${record.groupId}`,
        owner,
      );
    }
    for (const related of record.relatedUids ?? [])
      requireReference(entryIndex, related, owner);
  }
  for (const record of definition.paths.paths) {
    unique(record.steps, (item) => item.id, `path ${record.id} step`);
    for (const item of record.steps) {
      const owner = `path ${record.id} step ${item.id}`;
      if (!item.entryUids.length && !item.topicIds.length)
        throw new Error(`${owner}: requires an entry or populated topic`);
      for (const target of item.entryUids)
        requireReference(entryIndex, target, owner);
      for (const target of item.topicIds)
        requireReference(topicIndex, target, owner);
    }
  }
  return definition;
}

export async function readOrganization(
  directory: string,
): Promise<OrganizationDefinition> {
  try {
    await stat(directory);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error;
    return validateOrganization({
      taxonomy: { version: 1, topics: [] },
      collections: { version: 1, collections: [], groups: [] },
      entries: { version: 1, entries: [] },
      paths: { version: 1, paths: [] },
    });
  }
  const value: Record<string, unknown> = {};
  for (const name of ['taxonomy', 'collections', 'entries', 'paths']) {
    const filename = join(directory, `${name}.json`);
    try {
      value[name] = JSON.parse(await readFile(filename, 'utf8'));
    } catch (error) {
      throw new Error(
        `${filename}: cannot read organization sidecar: ${error instanceof Error ? error.message : String(error)}`,
        { cause: error },
      );
    }
  }
  try {
    return validateOrganization(value);
  } catch (error) {
    throw new Error(
      `${directory}: invalid organization sidecars: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error },
    );
  }
}
