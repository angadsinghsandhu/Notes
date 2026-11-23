import { JSDOM } from 'jsdom';
import { beforeEach, expect, test } from 'vitest';
import { renderTraceFrame } from '../../../../src/client/leetcode/renderers.js';
import type { TraceFrame } from '../../../../src/content/index.js';

let container: HTMLElement;
beforeEach(() => {
  container = new JSDOM('<main></main>').window.document.querySelector('main')!;
});

function render(
  state: TraceFrame['state'],
  highlights: TraceFrame['highlights'] = [],
) {
  renderTraceFrame(container, {
    stepId: 'step',
    codeLines: [1],
    explanation: 'Observe state.',
    state,
    highlights,
  });
}

function text(selector: string) {
  return Array.from(
    container.querySelectorAll(selector),
    (element) => element.textContent,
  );
}

test('array pointers have visible zero-based indices, values and highlight text', () => {
  render(
    {
      kind: 'array',
      items: [
        null,
        false,
        true,
        '',
        0,
        '0',
        'null',
        '<img src=x onerror=alert(1)>',
      ],
    },
    [{ index: 0 }],
  );
  expect(text('.trace-item')).toEqual([
    'Index 0: null (highlighted)',
    'Index 1: false',
    'Index 2: true',
    'Index 3: ""',
    'Index 4: 0',
    'Index 5: "0"',
    'Index 6: "null"',
    'Index 7: "<img src=x onerror=alert(1)>"',
  ]);
  expect(text('.trace-highlight')).toEqual(['Index 0: null (highlighted)']);
  expect(container.querySelector('img')).toBeNull();
});

test.each([
  ['stack', ['Index 0: 3', 'Index 1 (top): 7']],
  ['queue', ['Index 0 (front): 3', 'Index 1 (back): 7']],
] as const)('%s identifies the ends of its logical order', (kind, labels) => {
  render({ kind, items: [3, 7] });
  expect(text('ul > li')).toEqual(labels);
  render({ kind, items: [] });
  expect(text('.trace-empty')).toEqual([`Empty ${kind}.`]);
});

test('a single queued item is both front and back', () => {
  render({ kind: 'queue', items: [4] });
  expect(text('li')).toEqual(['Index 0 (front and back): 4']);
});

test('replacing a snapshot and backtracking restore its exact state and highlights', () => {
  const earlier: TraceFrame['state'] = { kind: 'array', items: [3, 2] };
  render(earlier, [{ index: 1 }]);
  const original = container.innerHTML;
  render({ kind: 'array', items: [8] }, [{ index: 0 }]);
  expect(text('li')).toEqual(['Index 0: 8 (highlighted)']);
  expect(container.children).toHaveLength(1);
  render(earlier, [{ index: 1 }]);
  expect(container.innerHTML).toBe(original);
});

test('grid cells retain both original coordinates through native table headers', () => {
  render(
    {
      kind: 'grid',
      rows: [
        [1, 2],
        [3, 4],
      ],
    },
    [{ row: 1, column: 0 }],
  );
  expect(text('caption')).toEqual(['Grid']);
  expect(text('thead th[scope=col]')).toEqual(['Row', 'Column 0', 'Column 1']);
  expect(text('tbody th[scope=row]')).toEqual(['0', '1']);
  expect(text('td.trace-highlight')).toEqual(['3 (highlighted)']);
  render({ kind: 'grid', rows: [[], []] });
  expect(text('.trace-empty')).toEqual(['Empty grid (2 rows, 0 columns).']);
  render({ kind: 'grid', rows: [] });
  expect(text('.trace-empty')).toEqual(['Empty grid (0 rows, 0 columns).']);
});

test('SQL tables preserve semantic headers, cell values, highlights and empty results', () => {
  const columns = ['<script>header</script>', 'FirstName'];
  render(
    {
      kind: 'table',
      columns,
      rows: [
        [1, '<b>record</b>'],
        [2, null],
      ],
    },
    [{ row: 1, column: 1 }],
  );
  expect(text('thead th[scope=col]')).toEqual(['Row', ...columns]);
  expect(text('tbody td')).toEqual([
    '1',
    '"<b>record</b>"',
    '2',
    'null (highlighted)',
  ]);
  expect(container.querySelector('script, b')).toBeNull();
  render({ kind: 'table', columns, rows: [] });
  expect(text('thead th[scope=col]')).toEqual(['Row', ...columns]);
  expect(text('.trace-empty')).toEqual(['Empty table (0 rows).']);
});

test.each(['graph', 'tree', 'call-tree'] as const)(
  '%s shows node identifiers and the direction of each highlighted edge',
  (kind) => {
    render(
      {
        kind,
        nodes: [
          { id: 'a', value: '<em>x</em>' },
          { id: 'b', value: null },
        ],
        edges: [
          { from: 'a', to: 'b' },
          { from: 'b', to: 'a' },
          { from: 'a', to: 'a' },
        ],
      },
      [{ nodeId: 'b' }, { from: 'b', to: 'a' }],
    );
    expect(text('.trace-node')).toEqual([
      'Node 0 (a): "<em>x</em>"',
      'Node 1 (b): null (highlighted)',
    ]);
    expect(text('.trace-edge')).toEqual([
      'From node 0 to node 1',
      'From node 1 to node 0 (highlighted)',
      'From node 0 to node 0',
    ]);
    expect(container.querySelector('em')).toBeNull();
    render({ kind, nodes: [], edges: [] });
    expect(text('.trace-empty')).toEqual(['No nodes.', 'No directed edges.']);
  },
);

test('large lists keep highlighted coordinates and disclose item and text omissions', () => {
  const items = Array.from(
    { length: 1000 },
    (_, index): number | string => index,
  );
  items[999] = 'x'.repeat(150);
  render({ kind: 'array', items }, [{ index: 999 }]);
  expect(text('li')).toHaveLength(24);
  expect(text('.trace-highlight')).toEqual([
    `Index 999: "${'x'.repeat(120)}" (30 characters omitted) (highlighted)`,
  ]);
  expect(text('.trace-omitted')).toEqual(['976 items omitted.']);
});

test('oversized highlight sets retain the first distinct references up to the list limit', () => {
  const items = Array.from({ length: 50 }, (_, index) => index);
  const highlights = [
    { index: 49 },
    ...items.slice(25).map((index) => ({ index })),
  ];
  render({ kind: 'array', items }, highlights);
  expect(text('.trace-highlight')).toHaveLength(24);
  expect(text('.trace-highlight').at(-1)).toBe('Index 49: 49 (highlighted)');
  expect(text('li').at(0)).toBe('Index 25: 25 (highlighted)');
});

test('wide grids retain original highlighted coordinates and disclose omitted cells', () => {
  render(
    {
      kind: 'grid',
      rows: Array.from({ length: 100 }, (_, row) =>
        Array.from({ length: 100 }, (_, col) => row * 100 + col),
      ),
    },
    [{ row: 98, column: 97 }],
  );
  expect(text('tbody tr')).toHaveLength(12);
  expect(text('thead th')).toHaveLength(9);
  expect(text('tbody th').at(-1)).toBe('98');
  expect(text('thead th').at(-1)).toBe('Column 97');
  expect(text('td.trace-highlight')).toEqual(['9897 (highlighted)']);
  expect(text('.trace-omitted')).toEqual([
    '9,904 cells omitted (88 rows and 92 columns omitted).',
  ]);
});

test('wide empty tables disclose omitted column headers', () => {
  render({
    kind: 'table',
    columns: Array.from({ length: 12 }, (_, index) => `Column ${index}`),
    rows: [],
  });
  expect(text('thead th')).toHaveLength(9);
  expect(text('.trace-omitted')).toEqual([
    '0 cells omitted (0 rows and 4 columns omitted).',
  ]);
});

test('large graphs retain highlighted nodes and edges with their original node references', () => {
  const nodes = Array.from({ length: 75 }, (_, index) => ({
    id: `n-${index}`,
    value: index,
  }));
  const edges = nodes.slice(1).map(({ id }) => ({ from: 'n-0', to: id }));
  render({ kind: 'graph', nodes, edges }, [
    { nodeId: 'n-73' },
    { from: 'n-0', to: 'n-74' },
  ]);
  expect(text('.trace-node')).toHaveLength(24);
  expect(text('.trace-edge')).toHaveLength(12);
  expect(text('.trace-highlight')).toEqual([
    'Node 73 (n-73): 73 (highlighted)',
    'From node 0 to node 74 (highlighted)',
  ]);
  expect(text('.trace-node').at(-1)).toBe('Node 74 (n-74): 74');
  expect(text('.trace-omitted')).toEqual([
    '51 nodes omitted.',
    '62 edges omitted.',
  ]);
});

test('an over-limit column does not take a row away from a displayable highlight', () => {
  const rows = Array.from({ length: 40 }, (_, row) =>
    Array.from({ length: 12 }, (_, column) => row * 12 + column),
  );
  const highlights = [
    ...rows[0]!.slice(0, 8).map((_, column) => ({ row: 0, column })),
    ...rows.slice(1, 13).map((_, index) => ({ row: index + 1, column: 9 })),
    { row: 39, column: 0 },
  ];
  render({ kind: 'grid', rows }, highlights);
  expect(text('td.trace-highlight')).toContain('468 (highlighted)');
  expect(text('tbody th').at(-1)).toBe('39');
});

test('a highlighted edge identifies an endpoint outside the visible node list', () => {
  const nodes = Array.from({ length: 26 }, (_, index) => ({
    id: `n-${index}`,
    value: index,
  }));
  const edges = [{ from: 'n-0', to: 'n-25' }];
  render({ kind: 'graph', nodes, edges }, [
    ...nodes.slice(0, 24).map(({ id }) => ({ nodeId: id })),
    ...edges,
  ]);
  expect(text('.trace-edge')).toEqual([
    'From node 0 to node 25 (n-25) (highlighted)',
  ]);
});

test('the value preview keeps whole Unicode code points', () => {
  render({
    kind: 'array',
    items: ['🙂'.repeat(61), '🙂'.repeat(120), '🙂'.repeat(121)],
  });
  expect(text('.trace-value')).toEqual([
    `"${'🙂'.repeat(61)}"`,
    `"${'🙂'.repeat(120)}"`,
    `"${'🙂'.repeat(120)}" (1 character omitted)`,
  ]);
});

test('long SQL headers with a shared prefix remain distinguishable', () => {
  const prefix = 'field'.repeat(24);
  render({
    kind: 'table',
    columns: [prefix + '1', prefix + '2'],
    rows: [[1, 2]],
  });
  expect(text('thead th[scope=col]')).toEqual([
    'Row',
    `Column 0: ${prefix} (1 character omitted)`,
    `Column 1: ${prefix} (1 character omitted)`,
  ]);
});

test('wide SQL tables name the original coordinates of retained columns', () => {
  const columns = Array.from({ length: 20 }, (_, index) => `field-${index}`);
  const rows = [columns.map((_, index) => index)];
  render({ kind: 'table', columns, rows }, [{ row: 0, column: 19 }]);
  expect(text('thead th[scope=col]')).toEqual([
    'Row',
    ...columns.slice(0, 7).map((name, index) => `Column ${index}: ${name}`),
    'Column 19: field-19',
  ]);
  expect(text('td.trace-highlight')).toEqual(['19 (highlighted)']);
});
