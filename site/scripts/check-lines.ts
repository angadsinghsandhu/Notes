import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const limit = 500;
const git = (cwd: string, args: string[]) =>
  execFileSync('git', ['--no-optional-locks', ...args], {
    cwd,
    encoding: 'utf8',
    maxBuffer: 16 * 1024 * 1024,
  });

function isTestModule(path: string, source: string): boolean {
  const javascript =
    /\.(?:test|spec)\.[cm]?[jt]sx?$/u.test(path) &&
    /^[\t ]*import\b[^;]*?\bfrom\s+["'](?:node:test|@playwright\/test|vitest)["']/mu.test(
      source,
    ) &&
    /\b(?:test|it|describe)(?:\.[a-z]+)?\s*\(/u.test(source);
  const python =
    /^site\/tests\/(?:[^/]+\/)*test_[^/]+\.py$/u.test(path) &&
    /^(?:import unittest\b|from unittest import\b)/mu.test(source) &&
    /^[\t ]+def test_\w+\(/mu.test(source);
  return javascript || python;
}

function decodeText(bytes: Buffer): string | undefined {
  if (bytes[0] === 0xff && bytes[1] === 0xfe)
    return bytes.toString('utf16le', 2);
  if (bytes[0] === 0xfe && bytes[1] === 0xff)
    return new TextDecoder('utf-16be').decode(bytes);
  return bytes.includes(0) ? undefined : new TextDecoder().decode(bytes);
}

function gitBlob(bytes: Buffer): string {
  return createHash('sha1')
    .update(`blob ${bytes.length}\0`)
    .update(bytes)
    .digest('hex');
}

export function oversizedFile(
  path: string,
  bytes: Buffer,
  baseline: ReadonlyMap<string, string>,
): number | undefined {
  const source = decodeText(bytes);
  if (!source || isTestModule(path, source)) return;
  const separators = source.match(/\r\n|[\r\n]/gu);
  const count = (separators?.length ?? 0) + Number(!/[\r\n]$/u.test(source));
  if (count <= limit) return;
  const recorded = baseline.get(path);
  if (recorded && gitBlob(bytes) === recorded) return;
  return count;
}

export function lineCapFailures(root: string): string[] {
  const inventory = readFileSync(
    join(root, 'site/content/portfolio-export/baseline-oversized.tsv'),
    'utf8',
  );
  const baseline = new Map<string, string>();
  for (const line of inventory.trimEnd().split('\n').slice(1)) {
    const [, hash, path] = line.split('\t');
    if (!path || !hash || !/^[a-f0-9]{40}$/.test(hash) || baseline.has(path))
      throw new Error(`Invalid 500-line baseline entry: ${line}`);
    baseline.set(path, hash);
  }
  const files = git(root, [
    'ls-files',
    '--cached',
    '--others',
    '--exclude-standard',
    '-z',
  ]);
  const failures: string[] = [];
  for (const path of new Set(files.split('\0').filter(Boolean))) {
    const file = join(root, path);
    if (!existsSync(file) || !lstatSync(file).isFile()) continue;
    const bytes = readFileSync(file);
    const count = oversizedFile(path, bytes, baseline);
    if (count !== undefined) failures.push(`${path}: ${count} lines`);
    else if (baseline.has(path) && baseline.get(path) === gitBlob(bytes))
      baseline.delete(path);
  }
  for (const path of baseline.keys())
    failures.push(`${path}: remove the obsolete baseline exemption`);
  return failures.sort();
}

export function runLineCap(cwd = process.cwd()): number {
  const root = git(cwd, ['rev-parse', '--show-toplevel']).trimEnd();
  const failures = lineCapFailures(root);
  if (failures.length) {
    console.error(`Files over ${limit} lines:\n${failures.join('\n')}`);
    return 1;
  }
  console.log(
    `All non-test text files meet the ${limit}-line cap or match the Notes baseline.`,
  );
  return 0;
}

if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
)
  process.exitCode = runLineCap();
