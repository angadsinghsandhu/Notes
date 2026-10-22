import {
  compareSourcePaths,
  isLearningEntry,
  resolveOrganization,
} from '../content/index.js';
import type {
  ContentEntry,
  Topic,
  Collection,
  Group,
  LearningPath,
  Membership,
  OrganizationSnapshot,
} from '../content/index.js';

/** The internal ledger/assets never become page props. Select public fields explicitly. */
export function publicEntry(entry: ContentEntry): ContentEntry {
  const {
    id,
    title,
    role,
    description,
    tags,
    draft,
    slug,
    order,
    updated,
    aliases,
    sourcePath,
    section,
    kind,
    bytes,
    groupSegments,
    route,
    headings,
    anchors,
    bodyFile,
    assetUrl,
    sourceUrl,
  } = entry;
  if (
    sourcePath.startsWith('/') ||
    sourcePath.includes('\\') ||
    bodyFile?.startsWith('/') ||
    bodyFile?.split('/').includes('..')
  )
    throw new Error('Catalog entries must contain repository-relative paths');
  return {
    id,
    title,
    description,
    tags: [...tags],
    draft,
    aliases: [...aliases],
    sourcePath,
    section,
    kind,
    bytes,
    groupSegments: [...groupSegments],
    route,
    headings: headings.map((heading) => ({ ...heading })),
    ...(role ? { role } : {}),
    ...(slug !== undefined ? { slug } : {}),
    ...(order !== undefined ? { order } : {}),
    ...(updated !== undefined ? { updated } : {}),
    ...(anchors ? { anchors: [...anchors] } : {}),
    ...(bodyFile ? { bodyFile } : {}),
    ...(assetUrl ? { assetUrl } : {}),
    ...(sourceUrl ? { sourceUrl } : {}),
  };
}

type NodeBase = {
  id: string;
  title: string;
  summary: string;
  route: string;
  entryCount: number;
};
export type LibraryLink = Pick<NodeBase, 'id' | 'title' | 'route'>;
export type ResolvedPathStep = {
  id: string;
  title: string;
  summary: string;
  entries: LibraryLink[];
  topics: LibraryLink[];
};
export type LibraryNode = NodeBase &
  (
    | { type: 'topic'; record: Topic }
    | { type: 'collection'; record: Collection }
    | { type: 'group'; record: Group }
    | { type: 'path'; record: LearningPath; steps: ResolvedPathStep[] }
  );
export type OrganizationIndex = {
  listNodes(type: LibraryNode['type'], parentKey?: string): LibraryNode[];
  getNode(type: LibraryNode['type'], key: string): LibraryNode | undefined;
  getMembership(entryId: string): Membership;
  getEntryByUid(uid: string): ContentEntry | undefined;
  listNodeEntries(
    type: 'topic' | 'collection' | 'group',
    key: string,
    options?: { descendants?: boolean; scope?: 'learning' | 'files' },
  ): ContentEntry[];
};

const emptyDefinition = {
  taxonomy: { version: 1 as const, topics: [] },
  collections: { version: 1 as const, collections: [], groups: [] },
  entries: { version: 1 as const, entries: [] },
  paths: { version: 1 as const, paths: [] },
};
type EntryNodeType = 'topic' | 'collection' | 'group';
type Bucket = { direct: Set<string>; descendants: Set<string> };

export function buildOrganizationIndex(
  entries: readonly ContentEntry[],
  snapshot?: OrganizationSnapshot,
): OrganizationIndex {
  const fallback = resolveOrganization(entries, emptyDefinition);
  const organization = snapshot ?? fallback;
  const memberships = new Map(fallback.memberships.map((m) => [m.entryId, m]));
  for (const m of organization.memberships) {
    const {
      entryId,
      uid,
      topics,
      collectionId,
      groupId,
      purpose,
      status,
      summary,
      relatedUids,
    } = m;
    memberships.set(entryId, {
      entryId,
      ...(uid ? { uid } : {}),
      topics: [...topics],
      ...(collectionId ? { collectionId } : {}),
      ...(groupId ? { groupId } : {}),
      purpose,
      status,
      summary,
      relatedUids: [...relatedUids],
    });
  }
  const publicEntries = new Map(
    entries
      .filter((e) => !e.draft && memberships.get(e.id)!.status !== 'draft')
      .map((e) => [e.id, publicEntry(e)]),
  );
  const uids = new Map<string, ContentEntry>();
  const topics = new Map(organization.topics.map((t) => [t.id, t]));
  const groups = new Map(
    organization.groups.map((g) => [`${g.collectionId}/${g.id}`, g]),
  );
  const buckets = new Map<string, Bucket>();
  const bucket = (type: EntryNodeType, key: string) => {
    const name = `${type}:${key}`;
    let value = buckets.get(name);
    if (!value) {
      value = { direct: new Set(), descendants: new Set() };
      buckets.set(name, value);
    }
    return value;
  };
  for (const entry of publicEntries.values()) {
    const m = memberships.get(entry.id)!;
    if (m.uid) uids.set(m.uid, entry);
    for (const assigned of m.topics) {
      bucket('topic', assigned).direct.add(entry.id);
      let topic = topics.get(assigned);
      while (topic) {
        bucket('topic', topic.id).descendants.add(entry.id);
        topic = topic.parentId ? topics.get(topic.parentId) : undefined;
      }
    }
    if (m.collectionId) {
      const collection = bucket('collection', m.collectionId);
      collection.descendants.add(entry.id);
      if (!m.groupId) collection.direct.add(entry.id);
      else {
        const key = `${m.collectionId}/${m.groupId}`;
        bucket('group', key).direct.add(entry.id);
        let group = groups.get(key);
        while (group) {
          bucket('group', `${group.collectionId}/${group.id}`).descendants.add(
            entry.id,
          );
          group = group.parentId
            ? groups.get(`${group.collectionId}/${group.parentId}`)
            : undefined;
        }
      }
    }
  }
  const selectedIds = (
    type: EntryNodeType,
    key: string,
    descendants: boolean,
    scope: 'learning' | 'files',
  ) =>
    [
      ...(buckets.get(`${type}:${key}`)?.[
        descendants ? 'descendants' : 'direct'
      ] ?? []),
    ].filter(
      (id) =>
        scope === 'files' ||
        isLearningEntry(publicEntries.get(id)!, memberships.get(id)!),
    );
  const nodes = new Map<string, LibraryNode>();
  const children = new Map<string, LibraryNode[]>();
  function add(node: LibraryNode, parent = ''): void {
    nodes.set(
      `${node.type}:${node.type === 'group' ? `${node.record.collectionId}/${node.id}` : node.id}`,
      node,
    );
    const key = `${node.type}:${parent}`;
    const list = children.get(key) ?? [];
    list.push(node);
    children.set(key, list);
    if (node.type === 'group' && !node.record.parentId) {
      const roots = children.get('group:') ?? [];
      roots.push(node);
      children.set('group:', roots);
    }
  }
  const base = (
    type: EntryNodeType,
    id: string,
    title: string,
    summary: string,
    key = id,
  ) => ({
    id,
    title,
    summary,
    route:
      type === 'group'
        ? `/library/collections/${key.split('/')[0]}/groups/${id}/`
        : `/library/${type === 'topic' ? 'topics' : 'collections'}/${id}/`,
    entryCount: selectedIds(type, key, true, 'learning').length,
  });
  for (const t of organization.topics) {
    if (!selectedIds('topic', t.id, true, 'files').length) continue;
    const { id, title, summary, parentId, order } = t;
    add(
      {
        ...base('topic', id, title, summary),
        type: 'topic',
        record: {
          id,
          title,
          summary,
          ...(parentId ? { parentId } : {}),
          ...(order !== undefined ? { order } : {}),
        },
      },
      parentId,
    );
  }
  for (const c of organization.collections) {
    if (!selectedIds('collection', c.id, true, 'files').length) continue;
    const {
      id,
      title,
      summary,
      type,
      provider,
      courseCode,
      edition,
      year,
      semester,
    } = c;
    add({
      ...base('collection', id, title, summary),
      type: 'collection',
      record: {
        id,
        title,
        summary,
        type,
        ...(provider !== undefined ? { provider } : {}),
        ...(courseCode !== undefined ? { courseCode } : {}),
        ...(edition !== undefined ? { edition } : {}),
        ...(year !== undefined ? { year } : {}),
        ...(semester !== undefined ? { semester } : {}),
      },
    });
  }
  for (const g of organization.groups) {
    const key = `${g.collectionId}/${g.id}`;
    if (!selectedIds('group', key, true, 'files').length) continue;
    const { id, title, summary, type, collectionId, parentId, order } = g;
    add(
      {
        ...base('group', id, title, summary, key),
        type: 'group',
        record: {
          id,
          title,
          summary,
          type,
          collectionId,
          ...(parentId ? { parentId } : {}),
          ...(order !== undefined ? { order } : {}),
        },
      },
      parentId ? `${collectionId}/${parentId}` : collectionId,
    );
  }
  const link = ({ id, title, route }: LibraryLink): LibraryLink => ({
    id,
    title,
    route,
  });
  for (const p of organization.paths) {
    const entryIds = new Set<string>();
    const steps: ResolvedPathStep[] = [];
    for (const s of p.steps) {
      const stepEntries = s.entryUids
        .map((uid) => uids.get(uid))
        .filter(
          (e): e is ContentEntry =>
            !!e && isLearningEntry(e, memberships.get(e.id)!),
        );
      const stepTopics = s.topicIds
        .map((id) => nodes.get(`topic:${id}`))
        .filter((n): n is LibraryNode => !!n && n.entryCount > 0);
      if (!stepEntries.length && !stepTopics.length) continue;
      for (const e of stepEntries) entryIds.add(e.id);
      for (const t of stepTopics)
        for (const id of selectedIds('topic', t.id, true, 'learning'))
          entryIds.add(id);
      steps.push({
        id: s.id,
        title: s.title,
        summary: s.summary,
        entries: stepEntries.map(link),
        topics: stepTopics.map(link),
      });
    }
    if (!steps.length) continue;
    add({
      id: p.id,
      title: p.title,
      summary: p.summary,
      type: 'path',
      route: `/library/paths/${p.id}/`,
      entryCount: entryIds.size,
      record: {
        id: p.id,
        title: p.title,
        summary: p.summary,
        steps: p.steps.map((s) => ({
          id: s.id,
          title: s.title,
          summary: s.summary,
          entryUids: [...s.entryUids],
          topicIds: [...s.topicIds],
        })),
      },
      steps,
    });
  }
  for (const list of children.values())
    list.sort(
      (a, b) =>
        ('order' in a.record ? (a.record.order ?? Infinity) : Infinity) -
          ('order' in b.record ? (b.record.order ?? Infinity) : Infinity) ||
        compareSourcePaths(a.title, b.title) ||
        compareSourcePaths(a.id, b.id),
    );
  return {
    listNodes: (type, parentKey) =>
      structuredClone(children.get(`${type}:${parentKey ?? ''}`) ?? []),
    getNode: (type, key) => {
      const node = nodes.get(`${type}:${key}`);
      return node ? structuredClone(node) : undefined;
    },
    getMembership: (id) => {
      if (!publicEntries.has(id))
        throw new Error(`Unknown public entry: ${id}`);
      return structuredClone(memberships.get(id)!);
    },
    getEntryByUid: (uid) => {
      const entry = uids.get(uid);
      return entry ? publicEntry(entry) : undefined;
    },
    listNodeEntries: (type, key, options = {}) =>
      selectedIds(
        type,
        key,
        options.descendants ?? false,
        options.scope ?? 'learning',
      ).map((id) => publicEntry(publicEntries.get(id)!)),
  };
}
