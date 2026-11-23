import type {
  TraceFrame,
  TraceHighlight,
  TraceState,
} from '../../content/index.js';

const itemLimit = 24;
const edgeLimit = 12;
const rowLimit = 12;
const columnLimit = 8;
const textLimit = 120;
const count = new Intl.NumberFormat('en-US');

type ItemState = Extract<TraceState, { items: unknown }>;
type MatrixState = Extract<TraceState, { rows: unknown }>;
type NetworkState = Extract<TraceState, { nodes: unknown }>;
type Scalar = ItemState['items'][number];

function append<K extends keyof HTMLElementTagNameMap>(
  parent: HTMLElement,
  tag: K,
  className = '',
  label = '',
): HTMLElementTagNameMap[K] {
  const child = parent.ownerDocument.createElement(tag);
  child.className = className;
  child.textContent = label;
  parent.append(child);
  return child;
}

function boundedText(value: string, quoted = false): string {
  const display = (text: string) => (quoted ? JSON.stringify(text) : text);
  if (value.length <= textLimit) return display(value);
  let length = 0;
  let preview = '';
  for (const character of value) {
    if (length++ < textLimit) preview += character;
  }
  if (length <= textLimit) return display(value);
  const omitted = length - textLimit;
  return `${display(preview)} (${count.format(omitted)} ${omitted === 1 ? 'character' : 'characters'} omitted)`;
}

function scalarLabel(value: Scalar): string {
  return typeof value === 'string' ? boundedText(value, true) : String(value);
}

function mark(element: HTMLElement, highlighted: boolean): void {
  if (!highlighted) return;
  element.classList.add('trace-highlight');
  append(element, 'span', 'trace-highlight-label', ' (highlighted)');
}

function showOmitted(
  parent: HTMLElement,
  quantity: number,
  noun: string,
): void {
  if (quantity > 0)
    append(
      parent,
      'p',
      'trace-omitted',
      `${count.format(quantity)} ${noun} omitted.`,
    );
}

/** Keep prioritized positions in frame order, fill from the start, and render in original order. */
function visiblePositions(
  total: number,
  limit: number,
  priority: Iterable<number>,
): number[] {
  const positions = new Set<number>();
  for (const position of priority) {
    positions.add(position);
    if (positions.size === limit) break;
  }
  for (let index = 0; index < total && positions.size < limit; index++)
    positions.add(index);
  return [...positions].sort((left, right) => left - right);
}

function itemPosition({ kind, items }: ItemState, index: number): string {
  const last = index === items.length - 1;
  if (kind === 'stack' && last) return ' (top)';
  if (kind !== 'queue') return '';
  if (index === 0) return last ? ' (front and back)' : ' (front)';
  return last ? ' (back)' : '';
}

function* itemPriorities(
  state: ItemState,
  active: Set<number>,
): Iterable<number> {
  yield* active;
  if (state.kind !== 'array') yield state.items.length - 1;
  if (state.kind === 'queue') yield 0;
}

function renderItems(
  parent: HTMLElement,
  state: ItemState,
  highlights: TraceHighlight[],
): void {
  if (!state.items.length) {
    append(parent, 'p', 'trace-empty', `Empty ${state.kind}.`);
    return;
  }

  const active = new Set<number>();
  for (const highlight of highlights)
    if ('index' in highlight) active.add(highlight.index);
  const positions = visiblePositions(
    state.items.length,
    itemLimit,
    itemPriorities(state, active),
  );
  const list = append(parent, 'ul', 'trace-items');
  list.setAttribute(
    'aria-label',
    { array: 'Array', stack: 'Stack', queue: 'Queue' }[state.kind],
  );
  for (const index of positions) {
    const item = append(list, 'li', 'trace-item');
    append(
      item,
      'span',
      'trace-coordinate',
      `Index ${index}${itemPosition(state, index)}: `,
    );
    append(item, 'span', 'trace-value', scalarLabel(state.items[index]!));
    mark(item, active.has(index));
  }
  showOmitted(parent, state.items.length - positions.length, 'items');
}

function renderMatrix(
  parent: HTMLElement,
  state: MatrixState,
  highlights: TraceHighlight[],
): void {
  const height = state.rows.length;
  const grid = state.kind === 'grid';
  const width = grid ? (state.rows[0]?.length ?? 0) : state.columns.length;
  if (grid && !width) {
    append(
      parent,
      'p',
      'trace-empty',
      `Empty grid (${count.format(height)} rows, 0 columns).`,
    );
    return;
  }

  const activeRows = new Set<number>();
  const activeColumns = new Set<number>();
  const active = new Set<string>();
  for (const highlight of highlights) {
    if (!('row' in highlight)) continue;
    const { row, column } = highlight;
    if (
      (activeRows.size === rowLimit && !activeRows.has(row)) ||
      (activeColumns.size === columnLimit && !activeColumns.has(column))
    )
      continue;
    activeRows.add(row);
    activeColumns.add(column);
    active.add(`${row}:${column}`);
  }

  const rows = visiblePositions(height, rowLimit, activeRows);
  const columns = visiblePositions(width, columnLimit, activeColumns);
  const omittedColumns = width - columns.length;
  const wrapper = append(parent, 'div', 'trace-table-wrap');
  const table = append(wrapper, 'table', 'trace-table');
  append(table, 'caption', '', grid ? 'Grid' : 'Table');
  const header = append(append(table, 'thead'), 'tr');
  append(header, 'th', '', 'Row').scope = 'col';
  for (const column of columns) {
    const label = grid ? `Column ${column}` : state.columns[column]!;
    const preview = boundedText(label);
    const showIndex = !grid && (omittedColumns > 0 || preview !== label);
    append(
      header,
      'th',
      '',
      showIndex ? `Column ${column}: ${preview}` : preview,
    ).scope = 'col';
  }

  const body = append(table, 'tbody');
  for (const row of rows) {
    const line = append(body, 'tr');
    append(line, 'th', 'trace-coordinate', String(row)).scope = 'row';
    for (const column of columns) {
      const cell = append(
        line,
        'td',
        'trace-value',
        scalarLabel(state.rows[row]![column]!),
      );
      mark(cell, active.has(`${row}:${column}`));
    }
  }
  if (!height) append(parent, 'p', 'trace-empty', 'Empty table (0 rows).');
  const omittedRows = height - rows.length;
  if (omittedRows || omittedColumns) {
    const cells = count.format(height * width - rows.length * columns.length);
    append(
      parent,
      'p',
      'trace-omitted',
      `${cells} cells omitted (${count.format(omittedRows)} rows and ${count.format(omittedColumns)} columns omitted).`,
    );
  }
}

function edgeKey({ from, to }: NetworkState['edges'][number]): string {
  return `${from}:${to}`;
}

function renderNetwork(
  parent: HTMLElement,
  state: NetworkState,
  highlights: TraceHighlight[],
): void {
  const activeNodes = new Set<string>();
  const activeEdges = new Set<string>();
  for (const highlight of highlights) {
    if ('nodeId' in highlight) activeNodes.add(highlight.nodeId);
    if ('from' in highlight) activeEdges.add(edgeKey(highlight));
  }

  const nodeIndex = new Map(state.nodes.map(({ id }, index) => [id, index]));
  const highlightedEdges = new Map<string, number>();
  for (const [index, edge] of state.edges.entries()) {
    const key = edgeKey(edge);
    if (activeEdges.has(key)) highlightedEdges.set(key, index);
  }

  const edgePositions = visiblePositions(
    state.edges.length,
    edgeLimit,
    Array.from(activeEdges, (key) => highlightedEdges.get(key)!),
  );
  const nodePriorities = Array.from(activeNodes, (id) => nodeIndex.get(id)!);
  for (const index of edgePositions) {
    const { from, to } = state.edges[index]!;
    nodePriorities.push(nodeIndex.get(from)!, nodeIndex.get(to)!);
  }
  const nodePositions = visiblePositions(
    state.nodes.length,
    itemLimit,
    nodePriorities,
  );

  if (nodePositions.length) {
    const kindNames = {
      graph: 'Graph',
      tree: 'Tree',
      'call-tree': 'Call tree',
    };
    const list = append(parent, 'ul', 'trace-nodes');
    list.setAttribute('aria-label', `${kindNames[state.kind]} nodes`);
    for (const index of nodePositions) {
      const { id, value } = state.nodes[index]!;
      const node = append(list, 'li', 'trace-node');
      append(
        node,
        'span',
        'trace-coordinate',
        `Node ${index} (${boundedText(id)}): `,
      );
      append(node, 'span', 'trace-value', scalarLabel(value));
      mark(node, activeNodes.has(id));
    }
    showOmitted(parent, state.nodes.length - nodePositions.length, 'nodes');
  } else append(parent, 'p', 'trace-empty', 'No nodes.');

  if (edgePositions.length) {
    const list = append(parent, 'ul', 'trace-edges');
    list.setAttribute('aria-label', 'Directed edges');
    const visibleNodes = new Set(nodePositions);
    const label = (id: string) => {
      const index = nodeIndex.get(id)!;
      return visibleNodes.has(index)
        ? String(index)
        : `${index} (${boundedText(id)})`;
    };
    for (const index of edgePositions) {
      const edge = state.edges[index]!;
      const item = append(
        list,
        'li',
        'trace-edge',
        `From node ${label(edge.from)} to node ${label(edge.to)}`,
      );
      mark(item, activeEdges.has(edgeKey(edge)));
    }
    showOmitted(parent, state.edges.length - edgePositions.length, 'edges');
  } else append(parent, 'p', 'trace-empty', 'No directed edges.');
}

/** Render the state of one validated frame without retaining references to older snapshots. */
export function renderTraceFrame(
  container: HTMLElement,
  { state, highlights }: TraceFrame,
): void {
  const snapshot = container.ownerDocument.createElement('div');
  snapshot.className = 'trace-frame';
  snapshot.dataset.kind = state.kind;
  if ('items' in state) renderItems(snapshot, state, highlights);
  else if ('rows' in state) renderMatrix(snapshot, state, highlights);
  else renderNetwork(snapshot, state, highlights);
  container.replaceChildren(snapshot);
}
