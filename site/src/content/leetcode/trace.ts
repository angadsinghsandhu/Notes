import { z } from 'zod';
import type { ProblemId } from './types.js';

export const TRACE_BYTE_LIMIT = 1024 * 1024;
const frameLimit = 2000;
const encoder = new TextEncoder();

type JsonScalar = null | boolean | number | string;
type JsonValue = JsonScalar | JsonValue[] | { [key: string]: JsonValue };

const slug = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
const nonblank = z.string().refine((value) => value.trim().length > 0);
const scalar = z.union([z.null(), z.boolean(), z.number(), z.string()]);
const index = z.int().nonnegative();
const cell = z.strictObject({ row: index, column: index });
const node = z.strictObject({ id: slug, value: scalar });
const edge = z.strictObject({ from: slug, to: slug });
const rows = z.array(z.array(scalar));

const state = z.discriminatedUnion('kind', [
  z.strictObject({
    kind: z.literal(['array', 'stack', 'queue']),
    items: z.array(scalar),
  }),
  z.strictObject({ kind: z.literal('grid'), rows }),
  z.strictObject({
    kind: z.literal(['graph', 'tree', 'call-tree']),
    nodes: z.array(node),
    edges: z.array(edge),
  }),
  z.strictObject({
    kind: z.literal('table'),
    columns: z.array(nonblank).min(1),
    rows,
  }),
]);

const highlight = z.union([
  z.strictObject({ index }),
  cell,
  z.strictObject({ nodeId: slug }),
  edge,
]);

const frame = z.strictObject({
  stepId: slug,
  codeLines: z.array(z.int().positive()).min(1),
  explanation: nonblank,
  state,
  highlights: z.array(highlight),
});

const traceSchema = z.strictObject({
  version: z.literal(1),
  problemId: z.custom<ProblemId>(
    (value) =>
      typeof value === 'string' &&
      /^leetcode:[1-9][0-9]{0,3}$/.test(value) &&
      Number(value.slice('leetcode:'.length)) <= 2000,
  ),
  approachId: slug,
  exampleId: slug,
  implementationSha256: z.string().regex(/^[a-f0-9]{64}$/),
  result: z.custom<JsonValue>(),
  frames: z.array(frame).min(1),
});

export type AlgorithmTrace = z.infer<typeof traceSchema>;
export type TraceFrame = z.infer<typeof frame>;
export type TraceState = z.infer<typeof state>;
export type TraceHighlight = z.infer<typeof highlight>;

function failJson(): never {
  throw new Error(
    'Invalid public trace structure: values must be portable JSON',
  );
}

function scalarBytes(value: unknown): number {
  if (
    value === null ||
    typeof value === 'string' ||
    typeof value === 'boolean' ||
    (typeof value === 'number' && Number.isFinite(value))
  )
    return encoder.encode(JSON.stringify(value)).byteLength;
  return failJson();
}

function* jsonProperties(
  value: object,
): Generator<{ value: unknown; keyBytes: number }> {
  const array = Array.isArray(value);
  const prototype: unknown = Object.getPrototypeOf(value);
  if (
    array
      ? prototype !== Array.prototype
      : prototype !== null && prototype !== Object.prototype
  )
    failJson();

  const keys = Reflect.ownKeys(value);
  if (array && keys.length !== value.length + 1) failJson();
  let arrayIndex = 0;
  for (const key of keys) {
    if (array && key === 'length') continue;
    if (typeof key !== 'string' || (array && key !== String(arrayIndex++)))
      failJson();
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor?.enumerable || !('value' in descriptor)) failJson();
    yield {
      value: descriptor.value as unknown,
      keyBytes: array ? 0 : scalarBytes(key) + 1,
    };
  }
}

/** Count compact JSON bytes without recursively walking a deeply nested result. */
function assertJsonBytes(input: unknown): void {
  const containers = new Set<object>();
  const stack: {
    container: object;
    properties: ReturnType<typeof jsonProperties>;
    hasProperty: boolean;
  }[] = [];
  let bytes = 0;

  function visit(value: unknown) {
    if (value === null || typeof value !== 'object') {
      bytes += scalarBytes(value);
      return;
    }
    if (containers.has(value)) failJson();
    containers.add(value);
    bytes += 2;
    stack.push({
      container: value,
      properties: jsonProperties(value),
      hasProperty: false,
    });
  }

  visit(input);
  while (stack.length > 0) {
    if (bytes > TRACE_BYTE_LIMIT) break;
    const current = stack.at(-1)!;
    const next = current.properties.next();
    if (next.done) {
      containers.delete(current.container);
      stack.pop();
      continue;
    }
    bytes += next.value.keyBytes + Number(current.hasProperty);
    current.hasProperty = true;
    visit(next.value.value);
  }
  if (bytes > TRACE_BYTE_LIMIT)
    throw new Error('Trace exceeds the 1 MiB trace limit');
}

function checkHighlights({ stepId, state, highlights }: TraceFrame): void {
  if ('items' in state) {
    if (
      highlights.some(
        (reference) =>
          !('index' in reference) || reference.index >= state.items.length,
      )
    )
      throw new Error(`Step ${stepId} has an invalid item highlight`);
    return;
  }

  if ('rows' in state) {
    const columns = state.kind === 'table' ? state.columns : undefined;
    const width = columns?.length ?? state.rows[0]?.length ?? 0;
    if (
      (columns && new Set(columns).size !== width) ||
      state.rows.some((row) => row.length !== width)
    )
      throw new Error(
        `Step ${stepId} has invalid row widths or duplicate column names`,
      );
    if (
      highlights.some(
        (reference) =>
          !('row' in reference) ||
          reference.row >= state.rows.length ||
          reference.column >= width,
      )
    )
      throw new Error(`Step ${stepId} has an invalid cell highlight`);
    return;
  }

  const nodes = new Set(state.nodes.map(({ id }) => id));
  if (nodes.size !== state.nodes.length)
    throw new Error(`Step ${stepId} has duplicate node IDs`);
  const edges = new Set<string>();
  for (const { from, to } of state.edges) {
    if (!nodes.has(from) || !nodes.has(to))
      throw new Error(`Step ${stepId} has an edge with an unknown node`);
    const key = `${from}:${to}`;
    if (edges.has(key)) throw new Error(`Step ${stepId} has a duplicate edge`);
    edges.add(key);
  }
  for (const reference of highlights) {
    const resolves =
      'nodeId' in reference
        ? nodes.has(reference.nodeId)
        : 'from' in reference && edges.has(`${reference.from}:${reference.to}`);
    if (!resolves)
      throw new Error(`Step ${stepId} has an invalid node or edge highlight`);
  }
}

export function validateTrace(input: unknown): AlgorithmTrace {
  if (typeof input === 'object' && input !== null) {
    const frames: unknown = Object.getOwnPropertyDescriptor(
      input,
      'frames',
    )?.value;
    if (Array.isArray(frames) && frames.length > frameLimit)
      throw new Error('Trace exceeds 2000 frames');
  }
  assertJsonBytes(input);
  const candidate = traceSchema.safeParse(input);
  if (!candidate.success)
    throw new Error(
      `Invalid public trace structure: ${z.prettifyError(candidate.error)}`,
    );
  const ids = new Set<string>();
  for (const item of candidate.data.frames) {
    if (ids.has(item.stepId))
      throw new Error(`Duplicate step ID ${item.stepId}`);
    ids.add(item.stepId);
    if (new Set(item.codeLines).size !== item.codeLines.length)
      throw new Error(`Step ${item.stepId} has duplicate code lines`);
    checkHighlights(item);
  }
  return candidate.data;
}
