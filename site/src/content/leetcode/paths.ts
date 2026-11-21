import { learningPath } from './schema.js';
import type {
  LearningPathDefinition,
  LearningPathNode,
  ProblemId,
  ProblemRecord,
} from './types.js';

export type LearningPathIndex = ReadonlyMap<string, LearningPathDefinition>;

export interface PathProgress {
  required: number;
  available: number;
  verified: number;
  studied: number;
  complete: boolean;
  /** First ready problem in editorial order, or the first available unstudied problem. */
  nextReady: ProblemId | null;
}

interface PathNodeState {
  node: LearningPathNode;
  children: PathNodeState[];
  dependents: PathNodeState[];
  incoming: number;
}

function indexPath(path: LearningPathDefinition) {
  const nodes = new Map<string, PathNodeState>();
  for (const node of path.nodes) {
    if (nodes.has(node.id))
      throw new Error(`Path ${path.id}: duplicate node ${node.id}`);
    nodes.set(node.id, { node, children: [], dependents: [], incoming: 0 });
  }

  function resolveReferences(ids: readonly string[], label: string) {
    if (new Set(ids).size !== ids.length)
      throw new Error(`Path ${path.id}: duplicate ${label} reference`);
    return ids.map((id) => {
      const state = nodes.get(id);
      if (!state)
        throw new Error(`Path ${path.id}: missing ${label} node ${id}`);
      return state;
    });
  }

  const roots = resolveReferences(path.rootIds, 'root');
  for (const state of nodes.values()) {
    const { id, childIds, prerequisiteIds } = state.node;
    state.children = resolveReferences(childIds, `child of ${id}`);
    for (const child of state.children) {
      state.dependents.push(child);
      child.incoming++;
    }
    for (const prerequisite of resolveReferences(
      prerequisiteIds,
      `prerequisite of ${id}`,
    )) {
      prerequisite.dependents.push(state);
      state.incoming++;
    }
  }

  // Both edges point forward: parent to child and prerequisite to dependent.
  const dependencyOrder = [...nodes.values()].filter(
    ({ incoming }) => incoming === 0,
  );
  for (const { dependents } of dependencyOrder) {
    for (const dependent of dependents) {
      dependent.incoming--;
      if (dependent.incoming === 0) dependencyOrder.push(dependent);
    }
  }
  if (dependencyOrder.length !== nodes.size)
    throw new Error(`Path ${path.id}: cycle in hierarchy or prerequisites`);

  const editorialOrder = inEditorialOrder(roots);
  if (editorialOrder.size !== nodes.size)
    throw new Error(`Path ${path.id}: unreachable nodes in hierarchy`);

  return { roots, editorialOrder, dependencyOrder };
}

function inEditorialOrder(
  roots: PathNodeState[],
  eligible?: ReadonlySet<PathNodeState>,
): Set<LearningPathNode> {
  const ordered = new Set<LearningPathNode>();
  const remaining = roots.toReversed();
  for (let state = remaining.pop(); state; state = remaining.pop()) {
    if (eligible && !eligible.has(state)) continue;
    if (ordered.has(state.node)) continue;
    ordered.add(state.node);
    for (const child of state.children.toReversed()) remaining.push(child);
  }
  return ordered;
}

export function validateLearningPaths(
  paths: readonly LearningPathDefinition[],
  problems: readonly ProblemRecord[],
): LearningPathIndex {
  const problemIds = new Set(problems.map(({ id }) => id));
  const index = new Map<string, LearningPathDefinition>();
  for (const definition of paths) {
    const path = learningPath.parse(definition);
    if (index.has(path.id)) throw new Error(`Duplicate path ${path.id}`);
    const { editorialOrder } = indexPath(path);
    for (const node of editorialOrder) {
      if (node.kind === 'problem' && !problemIds.has(node.problemId))
        throw new Error(`Path ${path.id}: missing problem ${node.problemId}`);
    }
    index.set(path.id, path);
  }
  return index;
}

/**
 * Draft and planned targets remain pending. A stage used as a prerequisite
 * is satisfied when its explicit prerequisites are satisfied on an eligible
 * branch. For recommendations, a stage passes its prerequisites to its
 * descendants along that branch. Shared nodes can qualify through another branch.
 */
export function pathProgress(
  path: LearningPathDefinition,
  studied: ReadonlySet<ProblemId>,
  problems: ReadonlyMap<ProblemId, ProblemRecord>,
): PathProgress {
  const { roots, editorialOrder, dependencyOrder } = indexPath(path);
  const available = new Set<ProblemId>();
  const required = new Set<ProblemId>();
  const studiedTargets = new Set<ProblemId>();
  for (const node of editorialOrder) {
    if (node.kind === 'stage') continue;
    const { problemId } = node;
    required.add(problemId);
    if (problems.get(problemId)?.status !== 'verified') continue;
    available.add(problemId);
    if (studied.has(problemId)) studiedTargets.add(problemId);
  }

  const satisfied = new Set<string>();
  const eligible = new Set<PathNodeState>();
  const reachable = new Set(roots);
  for (const state of dependencyOrder) {
    const { node, children } = state;
    if (
      !reachable.has(state) ||
      !node.prerequisiteIds.every((id) => satisfied.has(id))
    ) {
      continue;
    }
    eligible.add(state);
    for (const child of children) reachable.add(child);
    if (node.kind === 'stage' || studiedTargets.has(node.problemId))
      satisfied.add(node.id);
  }

  function firstUnstudied(nodes: Iterable<LearningPathNode>): ProblemId | null {
    for (const node of nodes) {
      if (
        node.kind === 'problem' &&
        available.has(node.problemId) &&
        !studiedTargets.has(node.problemId)
      ) {
        return node.problemId;
      }
    }
    return null;
  }

  const nextReady = firstUnstudied(inEditorialOrder(roots, eligible));

  return {
    required: required.size,
    available: available.size,
    verified: available.size,
    studied: studiedTargets.size,
    complete: studiedTargets.size === required.size,
    nextReady: nextReady ?? firstUnstudied(editorialOrder),
  };
}
