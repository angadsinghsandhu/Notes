import type { TestInfo } from '@playwright/test';
import type { ChildProcess } from 'node:child_process';
import { createServer } from 'node:net';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';

// Provisional full-archive bounds; Linux child timings must validate these.
export const fullArchiveReadinessTimeout = 180_000;
export const fullArchivePublicationTimeout = 180_000;
export const developmentSearchTimeout = 240_000;

export function developmentDiagnostics(child: ChildProcess, info: TestInfo) {
  const events: string[] = [];
  const record = (message: string) =>
    events.push(`${new Date().toISOString()} ${message}`);
  record(`npm dev startup PID ${child.pid}`);
  for (const [stream, label] of [
    [child.stdout, 'stdout'],
    [child.stderr, 'stderr'],
  ] as const)
    stream?.on('data', (bytes: Buffer) =>
      record(`${label}: ${bytes.toString()}`),
    );
  child.once('error', (error) => record(`startup error: ${error.message}`));
  child.once('exit', (code, signal) =>
    record(`exit code=${code} signal=${signal}`),
  );
  const exited = new Promise<void>((done) => child.once('close', () => done()));
  return {
    record,
    contains: (message: string) =>
      events.some((event) => event.includes(message)),
    exited,
    fail(error: unknown): never {
      record('test failed');
      if (error instanceof Error)
        error.message += `\nLast npm dev diagnostics:\n${events.join('\n').slice(-8000)}`;
      throw error;
    },
    async save(name: string, assertions = '') {
      try {
        const path = info.outputPath(name);
        await mkdir(dirname(path), { recursive: true });
        await writeFile(path, `${assertions}\n${events.join('\n')}\n`);
        await info.attach('npm-dev-diagnostics', {
          path,
          contentType: 'text/plain',
        });
      } catch (error) {
        console.error('Could not retain npm dev diagnostics', error);
      }
    },
  };
}

export async function freePort(): Promise<number> {
  const socket = createServer();
  await new Promise<void>((done) => socket.listen(0, '127.0.0.1', done));
  const address = socket.address();
  if (!address || typeof address === 'string') throw new Error('No port');
  await new Promise<void>((done, reject) =>
    socket.close((e) => (e ? reject(e) : done())),
  );
  return address.port;
}
