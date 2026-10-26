import type { ContentEntry } from './types.js';
import type { OrganizationSnapshot } from './organization-types.js';
import { isLearningEntry } from './organization.js';

/** Emission differs from ownership: empty configured IDs still reserve routes. */
export function organizationPageRoutes(
  entries: readonly ContentEntry[],
  snapshot?: OrganizationSnapshot,
): string[] {
  const routes = [
    '/library/topics/',
    '/library/collections/',
    '/library/paths/',
  ];
  if (!snapshot) return routes;
  const entriesById = new Map(
    entries.filter((e) => !e.draft).map((e) => [e.id, e]),
  );
  const topics = new Map(snapshot.topics.map((t) => [t.id, t]));
  const groups = new Map(
    snapshot.groups.map((g) => [g.collectionId + '/' + g.id, g]),
  );
  const populatedTopics = new Set<string>();
  const learningTopics = new Set<string>();
  const collections = new Set<string>();
  const populatedGroups = new Set<string>();
  const learningUids = new Set<string>();
  for (const m of snapshot.memberships) {
    const entry = entriesById.get(m.entryId);
    if (!entry || m.status === 'draft') continue;
    const learning = isLearningEntry(entry, m);
    if (learning && m.uid) learningUids.add(m.uid);
    for (const assigned of m.topics) {
      let topic = topics.get(assigned);
      while (topic) {
        populatedTopics.add(topic.id);
        if (learning) learningTopics.add(topic.id);
        topic = topic.parentId ? topics.get(topic.parentId) : undefined;
      }
    }
    if (m.collectionId) {
      collections.add(m.collectionId);
      let group = m.groupId
        ? groups.get(m.collectionId + '/' + m.groupId)
        : undefined;
      while (group) {
        populatedGroups.add(group.collectionId + '/' + group.id);
        group = group.parentId
          ? groups.get(group.collectionId + '/' + group.parentId)
          : undefined;
      }
    }
  }
  for (const t of snapshot.topics)
    if (populatedTopics.has(t.id)) routes.push('/library/topics/' + t.id + '/');
  for (const c of snapshot.collections)
    if (collections.has(c.id))
      routes.push('/library/collections/' + c.id + '/');
  for (const g of snapshot.groups)
    if (populatedGroups.has(g.collectionId + '/' + g.id))
      routes.push(
        '/library/collections/' + g.collectionId + '/groups/' + g.id + '/',
      );
  for (const p of snapshot.paths)
    if (
      p.steps.some(
        (s) =>
          s.entryUids.some((uid) => learningUids.has(uid)) ||
          s.topicIds.some((id) => learningTopics.has(id)),
      )
    )
      routes.push('/library/paths/' + p.id + '/');
  return routes;
}
