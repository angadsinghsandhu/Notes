import { afterEach, expect, test, vi } from 'vitest';
import { loadTracePackage } from '../../../../src/client/leetcode/trace.js';
import type {
  AlgorithmTrace,
  TracePackageReference,
} from '../../../../src/content/index.js';

const first: AlgorithmTrace = {
  version: 1,
  problemId: 'leetcode:1',
  approachId: 'hash-map',
  exampleId: 'duplicate',
  implementationSha256: 'a'.repeat(64),
  result: [0, 1],
  frames: [
    {
      stepId: 'lookup',
      codeLines: [1],
      explanation: 'Check for a match → return indices.',
      state: { kind: 'array', items: [3, 3] },
      highlights: [],
    },
  ],
};
const traces = [first, { ...first, exampleId: 'distinct' }];
const envelope = { version: 1, traces };
const encode = (value: unknown) =>
  new TextEncoder().encode(JSON.stringify(value));
const payload = encode(envelope);

async function reference(body = payload): Promise<TracePackageReference> {
  const digest = await crypto.subtle.digest('SHA-256', body);
  const sha256 = Buffer.from(digest).toString('hex');
  return {
    sha256,
    url: `/practice-traces/${sha256}.json`,
    bytes: body.byteLength,
    exampleIds: traces.map(({ exampleId }) => exampleId),
  };
}

function mockFetch(response: Response) {
  const fetch = vi.fn().mockResolvedValue(response);
  vi.stubGlobal('fetch', fetch);
  return fetch;
}

const signal = new AbortController().signal;

afterEach(() => vi.unstubAllGlobals());

test('loads the exact decoded bytes in order with one credential-free request', async () => {
  const expected = await reference();
  const body = new ReadableStream({
    start(controller) {
      for (let offset = 0; offset < payload.length; offset += 3)
        controller.enqueue(payload.subarray(offset, offset + 3));
      controller.close();
    },
  });
  const fetch = mockFetch(
    new Response(body, {
      headers: { 'Content-Encoding': 'gzip', 'Content-Length': '128' },
    }),
  );
  await expect(loadTracePackage(expected, signal)).resolves.toEqual(traces);
  expect(fetch).toHaveBeenCalledExactlyOnceWith(expected.url, {
    credentials: 'omit',
    mode: 'same-origin',
    redirect: 'error',
    signal,
  });
});

test.each([
  (url: string) => `https://other.test${url}`,
  (url: string) => `/.${url}`,
  (url: string) => `${url}?cache=false`,
  (url: string) => `${url}\n`,
  () => `/practice-traces/${'b'.repeat(64)}.json`,
])('rejects noncanonical routes before fetching', async (changeRoute) => {
  const expected = await reference();
  expected.url = changeRoute(expected.url);
  const fetch = mockFetch(new Response(payload));
  await expect(loadTracePackage(expected, signal)).rejects.toThrow(/route/i);
  expect(fetch).not.toHaveBeenCalled();
});

test.each(['A'.repeat(64), 'a'.repeat(63), `${'a'.repeat(64)}\n`])(
  'rejects noncanonical digests before fetching',
  async (sha256) => {
    const expected = await reference();
    const fetch = mockFetch(new Response(payload));
    await expect(
      loadTracePackage(
        { ...expected, sha256, url: `/practice-traces/${sha256}.json` },
        signal,
      ),
    ).rejects.toThrow(/route/i);
    expect(fetch).not.toHaveBeenCalled();
  },
);

test.each([0, -1, 1.5, Number.NaN, 25 * 1024 * 1024 + 1])(
  'rejects invalid declared byte count %s before fetching',
  async (bytes) => {
    const expected = await reference();
    const fetch = mockFetch(new Response(payload));
    await expect(
      loadTracePackage({ ...expected, bytes }, signal),
    ).rejects.toThrow(/byte count/i);
    expect(fetch).not.toHaveBeenCalled();
  },
);

test.each([206, 404, 500])('rejects HTTP %s', async (status) => {
  mockFetch(new Response(payload, { status }));
  await expect(loadTracePackage(await reference(), signal)).rejects.toThrow(
    /response/i,
  );
});

test('rejects a redirected response with otherwise valid bytes', async () => {
  const response = new Response(payload);
  Object.defineProperty(response, 'redirected', { value: true });
  mockFetch(response);
  await expect(loadTracePackage(await reference(), signal)).rejects.toThrow(
    /response/i,
  );
});

test('preserves an HTTP error when canceling its unread body fails', async () => {
  const cancel = vi.fn().mockRejectedValue(new Error('cannot cancel'));
  const body = new ReadableStream({ cancel }, { highWaterMark: 0 });
  mockFetch(new Response(body, { status: 404 }));
  await expect(loadTracePackage(await reference(), signal)).rejects.toThrow(
    /response/i,
  );
  expect(cancel).toHaveBeenCalledOnce();
});

test('rejects a successful response with no body', async () => {
  mockFetch(new Response());
  await expect(loadTracePackage(await reference(), signal)).rejects.toThrow(
    /body/i,
  );
});

test('rejects a short response', async () => {
  mockFetch(new Response(payload.subarray(0, -1)));
  await expect(loadTracePackage(await reference(), signal)).rejects.toThrow(
    /byte count/i,
  );
});

test('cancels an oversized stream as soon as a chunk crosses the declared limit', async () => {
  const pull = vi.fn((controller: ReadableStreamDefaultController) =>
    controller.enqueue(payload),
  );
  const cancel = vi.fn();
  const body = new ReadableStream({ pull, cancel }, { highWaterMark: 0 });
  mockFetch(new Response(body));
  const expected = await reference();
  await expect(loadTracePackage(expected, signal)).rejects.toThrow(
    /byte count/i,
  );
  expect(pull).toHaveBeenCalledTimes(2);
  expect(cancel).toHaveBeenCalledOnce();
  expect(body.locked).toBe(false);
});

test('checks integrity before trying to parse invalid JSON of the right length', async () => {
  mockFetch(new Response(new Uint8Array(payload.length)));
  await expect(loadTracePackage(await reference(), signal)).rejects.toThrow(
    /SHA-256/i,
  );
});

test('rejects invalid UTF-8 even when the hash and byte count match', async () => {
  const invalid = payload.slice();
  invalid[invalid.indexOf(0xe2)] = 0xff;
  mockFetch(new Response(invalid));
  await expect(
    loadTracePackage(await reference(invalid), signal),
  ).rejects.toBeInstanceOf(TypeError);
});

test('rejects malformed JSON even when the hash and byte count match', async () => {
  const invalid = payload.subarray(0, -1);
  mockFetch(new Response(invalid));
  await expect(
    loadTracePackage(await reference(invalid), signal),
  ).rejects.toBeInstanceOf(SyntaxError);
});

test.each([
  null,
  { ...envelope, version: 2 },
  { ...envelope, extra: true },
  { ...envelope, traces: null },
  { ...envelope, traces: [] },
  { ...envelope, traces: [first] },
  { ...envelope, traces: [...traces].reverse() },
  { ...envelope, traces: [null, traces[1]] },
  { ...envelope, traces: [42, traces[1]] },
  { ...envelope, traces: [{ ...first, exampleId: 1 }, traces[1]] },
])('rejects a mismatched envelope or ordered example IDs', async (value) => {
  const invalid = encode(value);
  mockFetch(new Response(invalid));
  await expect(
    loadTracePackage(await reference(invalid), signal),
  ).rejects.toThrow(/package/i);
});

test('does not fetch if the signal is already aborted', async () => {
  const controller = new AbortController();
  controller.abort();
  const fetch = mockFetch(new Response(payload));
  await expect(
    loadTracePackage(await reference(), controller.signal),
  ).rejects.toHaveProperty('name', 'AbortError');
  expect(fetch).not.toHaveBeenCalled();
});

test('rejects data delivered after an in-flight request is aborted', async () => {
  const controller = new AbortController();
  const cancel = vi.fn();
  const body = new ReadableStream(
    {
      pull(stream) {
        controller.abort();
        stream.enqueue(payload);
      },
      cancel,
    },
    { highWaterMark: 0 },
  );
  mockFetch(new Response(body));
  await expect(
    loadTracePackage(await reference(), controller.signal),
  ).rejects.toHaveProperty('name', 'AbortError');
  expect(cancel).toHaveBeenCalledOnce();
});

test('propagates stream read failures and unlocks the stream', async () => {
  const error = new Error('connection closed');
  const body = new ReadableStream({
    start(controller) {
      controller.error(error);
    },
  });
  mockFetch(new Response(body));
  await expect(loadTracePackage(await reference(), signal)).rejects.toBe(error);
  expect(body.locked).toBe(false);
});
