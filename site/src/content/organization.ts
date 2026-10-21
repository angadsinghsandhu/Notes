import type { ContentEntry } from './types.js';
import type {
  Membership,
  OrganizationDefinition,
  OrganizationSnapshot,
  Purpose,
} from './organization-types.js';

function fallbackPurpose(entry: ContentEntry): Purpose {
  if (entry.kind === 'code') return 'project-file';
  return !entry.role && (entry.kind === 'markdown' || entry.kind === 'notebook')
    ? 'note'
    : 'reference';
}

export function resolveOrganization(
  entries: readonly ContentEntry[],
  definition: OrganizationDefinition,
): OrganizationSnapshot {
  const sources = new Map(entries.map((entry) => [entry.sourcePath, entry]));
  const records = new Map(
    definition.entries.entries.map((record) => [record.sourcePath, record]),
  );
  for (const record of definition.entries.entries) {
    if (!sources.has(record.sourcePath))
      throw new Error(
        `entry ${record.sourcePath} (${record.uid}): registered source is missing or excluded; pass discovered drafts before publication filtering`,
      );
  }
  const memberships: Membership[] = [];
  const publicUids = new Set<string>();
  const populatedTopics = new Set<string>();
  const topicIndex = new Map(
    definition.taxonomy.topics.map((topic) => [topic.id, topic]),
  );
  for (const entry of entries) {
    const record = records.get(entry.sourcePath);
    if (entry.draft || record?.status === 'draft') continue;
    const membership: Membership = {
      entryId: entry.id,
      ...(record
        ? {
            uid: record.uid,
            ...(record.collectionId
              ? { collectionId: record.collectionId }
              : {}),
            ...(record.groupId ? { groupId: record.groupId } : {}),
          }
        : {}),
      topics: [...(record?.topics ?? [])],
      purpose: record?.purpose ?? fallbackPurpose(entry),
      status: record?.status ?? 'unreviewed',
      summary: record?.summary ?? entry.description,
      relatedUids: [...(record?.relatedUids ?? [])],
    };
    memberships.push(membership);
    if (membership.uid) publicUids.add(membership.uid);
    if (
      !entry.role &&
      membership.purpose !== 'project-file' &&
      membership.status !== 'outline'
    ) {
      for (const assigned of membership.topics) {
        let topic = topicIndex.get(assigned);
        while (topic) {
          populatedTopics.add(topic.id);
          topic = topic.parentId ? topicIndex.get(topic.parentId) : undefined;
        }
      }
    }
  }
  function requirePublic(uid: string, owner: string): void {
    if (!publicUids.has(uid))
      throw new Error(`${owner}: target ${uid} is missing, excluded, or draft`);
  }
  for (const record of definition.entries.entries) {
    if (!publicUids.has(record.uid)) continue;
    for (const related of record.relatedUids ?? []) {
      requirePublic(related, `entry ${record.sourcePath}`);
    }
  }
  for (const path of definition.paths.paths) {
    for (const step of path.steps) {
      const owner = `path ${path.id} step ${step.id}`;
      for (const uid of step.entryUids) requirePublic(uid, owner);
      if (
        !step.entryUids.length &&
        !step.topicIds.some((topic) => populatedTopics.has(topic))
      )
        throw new Error(
          `${owner}: requires an entry or populated public learning topic`,
        );
    }
  }
  return structuredClone({
    topics: definition.taxonomy.topics,
    collections: definition.collections.collections,
    groups: definition.collections.groups,
    paths: definition.paths.paths,
    memberships,
  });
}
