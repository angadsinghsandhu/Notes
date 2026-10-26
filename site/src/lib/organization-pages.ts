import { isLearningEntry } from '../content/index.js';
import type {
  ContentEntry,
  EditorialStatus,
  Purpose,
} from '../content/index.js';
import type {
  Catalog,
  LibraryLink,
  LibraryNode,
  OrganizationIndex,
} from './catalog.js';

export type OrganizationTreeNode = {
  id: string;
  title: string;
  route?: string;
  children: OrganizationTreeNode[];
};
export type OrganizationDocument = LibraryLink & {
  sourcePath: string;
  summary: string;
  kind: ContentEntry['kind'];
  status: EditorialStatus;
  purpose: Purpose;
};
export type ReaderOrganization = {
  learning: boolean;
  topicIds: string[];
  topics: LibraryLink[];
  collection?: LibraryLink;
  group?: LibraryLink;
  tree: OrganizationTreeNode[];
  status: EditorialStatus;
  purpose: Purpose;
  summary: string;
};
const link = ({ id, title, route }: LibraryLink): LibraryLink => ({
  id,
  title,
  route,
});

export function organizationTree(
  index: OrganizationIndex,
  type: 'topic' | 'group',
  parent?: string,
  activeGroup?: string,
): OrganizationTreeNode[] {
  const active = new Set<string>();
  let node =
    activeGroup && parent
      ? index.getNode('group', parent + '/' + activeGroup)
      : undefined;
  while (node?.type === 'group') {
    active.add(node.id);
    node = node.record.parentId
      ? index.getNode(
          'group',
          node.record.collectionId + '/' + node.record.parentId,
        )
      : undefined;
  }
  const children = (key?: string): OrganizationTreeNode[] =>
    index.listNodes(type, key).map((n) => ({
      ...link(n),
      children:
        activeGroup && !active.has(n.id)
          ? []
          : children(
              n.type === 'group' ? n.record.collectionId + '/' + n.id : n.id,
            ),
    }));
  return children(parent);
}

export function readerOrganization(
  catalog: Catalog,
  entry: ContentEntry,
): ReaderOrganization {
  const index = catalog.organization;
  const membership = index.getMembership(entry.id);
  const collection = membership.collectionId
    ? index.getNode('collection', membership.collectionId)
    : undefined;
  const group =
    membership.collectionId && membership.groupId
      ? index.getNode(
          'group',
          membership.collectionId + '/' + membership.groupId,
        )
      : undefined;
  const topicIds = new Set<string>();
  for (const id of membership.topics) {
    let node = index.getNode('topic', id);
    while (node?.type === 'topic' && !topicIds.has(node.id)) {
      topicIds.add(node.id);
      node = node.record.parentId
        ? index.getNode('topic', node.record.parentId)
        : undefined;
    }
  }
  return {
    learning: isLearningEntry(entry, membership),
    topicIds: [...topicIds],
    topics: membership.topics.flatMap((id) => {
      const node = index.getNode('topic', id);
      return node ? [link(node)] : [];
    }),
    ...(collection ? { collection: link(collection) } : {}),
    ...(group ? { group: link(group) } : {}),
    tree: collection
      ? organizationTree(index, 'group', collection.id, group?.id ?? '__root__')
      : [],
    status: membership.status,
    purpose: membership.purpose,
    summary: membership.summary,
  };
}

export function organizationDocuments(
  index: OrganizationIndex,
  type: 'topic' | 'collection' | 'group',
  key: string,
  descendants = false,
) {
  const result: Record<
    'notes' | 'exercises' | 'resources',
    OrganizationDocument[]
  > = { notes: [], exercises: [], resources: [] };
  for (const e of index.listNodeEntries(type, key, {
    descendants,
    scope: 'files',
  })) {
    const m = index.getMembership(e.id);
    const learning =
      e.role !== 'supplemental' &&
      m.status !== 'outline' &&
      m.purpose !== 'project-file';
    const bucket =
      learning && m.purpose === 'note'
        ? 'notes'
        : learning && m.purpose === 'exercise'
          ? 'exercises'
          : 'resources';
    result[bucket].push({
      ...link(e),
      sourcePath: e.sourcePath,
      summary: m.summary,
      kind: e.kind,
      status: m.status,
      purpose: m.purpose,
    });
  }
  return result;
}

export function organizationCards(
  index: OrganizationIndex,
  nodes: LibraryNode[],
) {
  const projects = (key: string): number =>
    index
      .listNodes('group', key)
      .reduce(
        (sum, n) =>
          sum +
          (n.type === 'group' && n.record.type === 'project' ? 1 : 0) +
          projects(
            n.type === 'group' ? n.record.collectionId + '/' + n.id : n.id,
          ),
        0,
      );
  return nodes.map((n) => {
    if (n.type === 'path')
      return {
        ...link(n),
        summary: n.summary,
        learningCount: n.entryCount,
        resourceCount: 0,
        projectCount: 0,
      };
    const key = n.type === 'group' ? n.record.collectionId + '/' + n.id : n.id;
    const count = index.listNodeEntries(n.type, key, {
      descendants: true,
      scope: 'files',
    }).length;
    return {
      ...link(n),
      summary: n.summary,
      learningCount: n.entryCount,
      resourceCount: count - n.entryCount,
      projectCount: n.type === 'topic' ? 0 : projects(key),
    };
  });
}

export function projectFileTree(
  documents: OrganizationDocument[],
): OrganizationTreeNode[] {
  if (!documents.length) return [];
  const paths = documents.map((d) => d.sourcePath.split('/'));
  let prefix = 0;
  while (
    paths.every((p) => p.length > prefix + 1 && p[prefix] === paths[0]![prefix])
  )
    prefix++;
  const roots: OrganizationTreeNode[] = [];
  for (const [i, document] of documents.entries()) {
    let children = roots;
    const parts = paths[i]!.slice(prefix);
    parts.forEach((title, part) => {
      const last = part === parts.length - 1;
      let node = children.find((n) => n.title === title);
      if (!node) {
        node = {
          id: document.id + ':' + part,
          title,
          ...(last ? { route: document.route } : {}),
          children: [],
        };
        children.push(node);
      }
      children = node.children;
    });
  }
  const sort = (nodes: OrganizationTreeNode[]): void => {
    nodes.sort((a, b) =>
      a.title.localeCompare(b.title, 'en', { numeric: true }),
    );
    nodes.forEach((n) => sort(n.children));
  };
  sort(roots);
  return roots;
}
