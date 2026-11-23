import type {
  AlgorithmTrace,
  TracePackageReference,
} from '../../content/index.js';

const maxPackageBytes = 25 * 1024 * 1024;

async function readPackageBytes(
  body: ReadableStream<Uint8Array>,
  expectedBytes: number,
  signal: AbortSignal,
): Promise<Uint8Array<ArrayBuffer>> {
  const bytes = new Uint8Array(expectedBytes);
  const reader = body.getReader();
  let offset = 0;
  try {
    while (true) {
      signal.throwIfAborted();
      const chunk = await reader.read();
      signal.throwIfAborted();
      if (chunk.done) break;
      if (chunk.value.byteLength > bytes.byteLength - offset)
        throw new Error('Trace package byte count exceeds the reference');
      bytes.set(chunk.value, offset);
      offset += chunk.value.byteLength;
    }
  } finally {
    void reader.cancel().catch(() => undefined);
    reader.releaseLock();
  }
  if (offset !== bytes.byteLength)
    throw new Error('Trace package byte count does not match the reference');
  return bytes;
}

export async function loadTracePackage(
  reference: TracePackageReference,
  signal: AbortSignal,
): Promise<AlgorithmTrace[]> {
  const { url, sha256, bytes, exampleIds } = reference;
  signal.throwIfAborted();
  if (
    sha256.length !== 64 ||
    !/^[0-9a-f]{64}$/.test(sha256) ||
    url !== `/practice-traces/${sha256}.json`
  )
    throw new Error('Invalid trace package route');
  if (!Number.isSafeInteger(bytes) || bytes <= 0 || bytes > maxPackageBytes)
    throw new Error('Invalid trace package byte count');

  const response = await fetch(url, {
    credentials: 'omit',
    mode: 'same-origin',
    redirect: 'error',
    signal,
  });
  if (response.status !== 200 || response.redirected) {
    void response.body?.cancel().catch(() => undefined);
    throw new Error('Unexpected trace package response');
  }
  if (!response.body) throw new Error('Missing trace package response body');

  const contents = await readPackageBytes(response.body, bytes, signal);
  signal.throwIfAborted();
  const digest = await crypto.subtle.digest('SHA-256', contents);
  signal.throwIfAborted();
  const actualHash = Array.from(new Uint8Array(digest), (byte) =>
    byte.toString(16).padStart(2, '0'),
  ).join('');
  if (actualHash !== sha256) throw new Error('Trace package SHA-256 mismatch');

  const decoded = new TextDecoder('utf-8', {
    fatal: true,
    ignoreBOM: true,
  }).decode(contents);
  // The digest binds these traces to the frames validated during publication.
  const value = JSON.parse(decoded) as {
    version: unknown;
    traces: AlgorithmTrace[];
  } | null;
  if (
    value?.version !== 1 ||
    Object.keys(value).length !== 2 ||
    !Array.isArray(value.traces) ||
    value.traces.length === 0 ||
    value.traces.length !== exampleIds.length ||
    value.traces.some(
      (trace, index) =>
        typeof trace?.exampleId !== 'string' ||
        trace.exampleId !== exampleIds[index],
    )
  )
    throw new Error('Unexpected trace package envelope or example order');
  return value.traces;
}
