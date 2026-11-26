import { expect, test } from 'vitest';
import { validateTrace } from '../../../../src/content/leetcode/trace.js';

const frame = {
  stepId: 'check-0',
  codeLines: [1],
  explanation: 'Look for the complement of 2.',
  state: { kind: 'array', items: [2, 7] },
  highlights: [{ index: 0 }],
};

const trace = {
  version: 1,
  problemId: 'leetcode:1',
  approachId: 'hash-map',
  exampleId: 'pair',
  implementationSha256: 'a'.repeat(64),
  result: [0, 1],
  frames: [frame],
};

const nodes = [
  { id: 'root', value: 5 },
  { id: 'child', value: null },
];
const edges = [{ from: 'root', to: 'child' }];
const cell = { row: 0, column: 0 };

test.each([
  ['array', { items: [true] }, [{ index: 0 }]],
  ['stack', { items: ['('] }, [{ index: 0 }]],
  ['queue', { items: [null] }, [{ index: 0 }]],
  ['grid', { rows: [[1, 2]] }, [cell]],
  ['graph', { nodes, edges }, [{ nodeId: 'root' }, edges[0]]],
  ['tree', { nodes, edges }, [{ nodeId: 'child' }]],
  ['call-tree', { nodes, edges }, edges],
  ['table', { columns: ['id'], rows: [[5]] }, [cell]],
])(
  'round trips %s snapshots with typed references',
  (kind, payload, highlights) => {
    const input = {
      ...trace,
      frames: [{ ...frame, state: { kind, ...payload }, highlights }],
    };
    expect(validateTrace(input)).toEqual(input);
  },
);

test.each([
  ['negative index', { highlights: [{ index: -1 }] }],
  ['out-of-range index', { highlights: [{ index: 2 }] }],
  ['wrong highlight type', { highlights: [cell] }],
  ['unknown highlight field', { highlights: [{ index: 0, html: 'private' }] }],
  ['unknown renderer', { state: { kind: 'custom', items: [] } }],
  ['unknown state field', { state: { ...frame.state, extra: 'private' } }],
  ['nested display value', { state: { kind: 'array', items: [[2, 7]] } }],
  [
    'ragged grid',
    { state: { kind: 'grid', rows: [[1, 2], [3]] }, highlights: [] },
  ],
  ['absent row', { state: { kind: 'grid', rows: [] }, highlights: [cell] }],
  [
    'absent column',
    {
      state: { kind: 'grid', rows: [[1]] },
      highlights: [{ row: 0, column: 1 }],
    },
  ],
  [
    'ragged table',
    {
      state: { kind: 'table', columns: ['id'], rows: [[1, 2]] },
      highlights: [],
    },
  ],
  [
    'duplicate column',
    {
      state: { kind: 'table', columns: ['id', 'id'], rows: [] },
      highlights: [],
    },
  ],
  [
    'duplicate node',
    {
      state: { kind: 'tree', nodes: [nodes[0], nodes[0]], edges: [] },
      highlights: [],
    },
  ],
  [
    'absent edge endpoint',
    { state: { kind: 'graph', nodes: [nodes[0]], edges }, highlights: [] },
  ],
  [
    'absent edge origin',
    { state: { kind: 'graph', nodes: [nodes[1]], edges }, highlights: [] },
  ],
  [
    'absent node highlight',
    {
      state: { kind: 'graph', nodes, edges },
      highlights: [{ nodeId: 'missing' }],
    },
  ],
  [
    'absent edge highlight',
    {
      state: { kind: 'graph', nodes, edges },
      highlights: [{ from: 'child', to: 'root' }],
    },
  ],
  ['blank explanation', { explanation: ' \n ' }],
  ['absent explanation', { explanation: undefined }],
  ['duplicate code lines', { codeLines: [1, 1] }],
  ['no code lines', { codeLines: [] }],
  ['fractional code line', { codeLines: [1.5] }],
  ['zero code line', { codeLines: [0] }],
  ['unsafe code line', { codeLines: [2 ** 53] }],
  ['invalid step id', { stepId: 'check--0' }],
  ['unknown frame field', { debug: true }],
])('rejects %s', (_, change) => {
  expect(() =>
    validateTrace({ ...trace, frames: [{ ...frame, ...change }] }),
  ).toThrow();
});

test.each([
  { version: undefined },
  { version: 2 },
  { problemId: 1 },
  { problemId: 'leetcode:01' },
  { problemId: 'leetcode:2001' },
  { approachId: 'Hash Map' },
  { exampleId: 'pair/' },
  { implementationSha256: 'A'.repeat(64) },
  { result: undefined },
  { frames: [] },
  { frames: [frame, frame] },
  { debug: true },
])('rejects invalid identity or envelope %j', (change) => {
  expect(() => validateTrace({ ...trace, ...change })).toThrow();
});

test('accepts exactly 2000 frames and rejects 2001', () => {
  const frames = Array.from({ length: 2000 }, (_, index) => ({
    ...frame,
    stepId: `step-${index}`,
  }));
  expect(validateTrace({ ...trace, frames }).frames).toHaveLength(2000);
  expect(() => validateTrace({ ...trace, frames: [...frames, frame] })).toThrow(
    /2000 frames/,
  );
});

test('counts compact UTF-8 bytes inclusively, including multibyte values', () => {
  const head = { ...trace, result: '' };
  const remaining = 1_048_576 - Buffer.byteLength(JSON.stringify(head));
  const result =
    'é'.repeat(Math.floor(remaining / 2)) + 'x'.repeat(remaining % 2);
  expect(validateTrace({ ...head, result }).result).toBe(result);
  expect(() => validateTrace({ ...head, result: result + 'x' })).toThrow(
    /1 MiB/,
  );
});

test.each([
  NaN,
  Infinity,
  BigInt(1),
  new Date(0),
  { absent: undefined },
  new Array(1),
  { [Symbol('hidden')]: true },
])('rejects values that cannot round trip as JSON', (result) => {
  expect(() => validateTrace({ ...trace, result })).toThrow(/JSON/);
});

test('rejects cyclic result values and preserves deeply nested own JSON properties', () => {
  const cycle: unknown[] = [];
  cycle.push(cycle);
  expect(() => validateTrace({ ...trace, result: cycle })).toThrow(/JSON/);
  const depth = 20_000;
  const result: unknown = JSON.parse(
    '['.repeat(depth) +
      '{"__proto__":5,"constructor":true}' +
      ']'.repeat(depth),
  );
  expect(validateTrace({ ...trace, result }).result).toBe(result);
});

test('identifies the frame cap before traversing pathological input', () => {
  const frames = Array.from({ length: 200_000 }, () => null);
  expect(Buffer.byteLength(JSON.stringify(frames))).toBe(1_000_001);
  expect(() => validateTrace({ ...trace, frames })).toThrow(/2000 frames/);
  const unreadableFrames = Array.from({ length: 2001 }, () => null);
  Object.defineProperty(unreadableFrames, 0, {
    get() {
      throw new Error('Tried to read an over-limit frame');
    },
  });
  expect(() => validateTrace({ ...trace, frames: unreadableFrames })).toThrow(
    /2000 frames/,
  );
});

test('rejects duplicate directed renderer edges', () => {
  const state = { kind: 'graph', nodes, edges: [edges[0], edges[0]] };
  const input = { ...trace, frames: [{ ...frame, state, highlights: [] }] };
  expect(() => validateTrace(input)).toThrow(/duplicate edge/);
});

test('rejects own surprise properties even if Zod would ignore the name', () => {
  const input: unknown = JSON.parse(
    JSON.stringify(trace).replace(
      '"version":1',
      '"version":1,"__proto__":true',
    ),
  );
  expect(() => validateTrace(input)).toThrow(/trace structure/);
});

test('requires an own result property, even when the result is null', () => {
  const { result, ...withoutResult } = trace;
  expect(result).toEqual([0, 1]);
  expect(() => validateTrace(withoutResult)).toThrow(/trace structure/);
  expect(validateTrace({ ...withoutResult, result: null }).result).toBeNull();
});
