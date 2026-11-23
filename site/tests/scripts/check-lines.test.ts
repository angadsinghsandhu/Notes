import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { expect, it, vi } from 'vitest';
import {
  lineCapFailures,
  oversizedFile,
  runLineCap,
} from '../../scripts/check-lines.js';

const testModule = 'import { it } from "vitest";\nit("works", () => {});\n';
const blob = (bytes: Buffer) =>
  createHash('sha1')
    .update(`blob ${bytes.length}\0`)
    .update(bytes)
    .digest('hex');

it('checks physical lines and content regardless of the tests directory', () => {
  const noExceptions = new Map();
  expect(
    oversizedFile('lf.txt', Buffer.from('x\n'.repeat(500)), noExceptions),
  ).toBeUndefined();
  expect(
    oversizedFile(
      'crlf.txt',
      Buffer.from('x\r\n'.repeat(499) + 'x'),
      noExceptions,
    ),
  ).toBeUndefined();
  expect(
    oversizedFile(
      'crlf.txt',
      Buffer.from('x\r\n'.repeat(500) + 'x'),
      noExceptions,
    ),
  ).toBe(501);
  expect(
    oversizedFile(
      'site/tests/fixture.test.ts',
      Buffer.from('x\n'.repeat(501)),
      noExceptions,
    ),
  ).toBe(501);
  expect(
    oversizedFile(
      'site/tests/fixture.json',
      Buffer.from('x\n'.repeat(501)),
      noExceptions,
    ),
  ).toBe(501);
  expect(
    oversizedFile(
      'site/tests/integration.test.ts',
      Buffer.from(testModule + '\n'.repeat(501)),
      noExceptions,
    ),
  ).toBeUndefined();
  expect(
    oversizedFile('cr.txt', Buffer.from('x\r'.repeat(501)), noExceptions),
  ).toBe(501);
  expect(
    oversizedFile('empty.txt', Buffer.alloc(0), noExceptions),
  ).toBeUndefined();
  expect(
    oversizedFile(
      'site/tests/test_example.py',
      Buffer.from(
        'import unittest\nclass Check(unittest.TestCase):\n  def test_value(self): pass\n' +
          '\n'.repeat(501),
      ),
      noExceptions,
    ),
  ).toBeUndefined();
  expect(
    oversizedFile(
      'site/tests/test_fixture.py',
      Buffer.from('x\n'.repeat(501)),
      noExceptions,
    ),
  ).toBe(501);
  expect(
    oversizedFile(
      'binary.dat',
      Buffer.from('\0' + '\n'.repeat(501)),
      noExceptions,
    ),
  ).toBeUndefined();
  const littleEndian = Buffer.from('\uFEFF' + 'x\r\n'.repeat(501), 'utf16le');
  expect(oversizedFile('le.txt', littleEndian, noExceptions)).toBe(501);
  expect(
    oversizedFile('be.txt', Buffer.from(littleEndian).swap16(), noExceptions),
  ).toBe(501);
});

it('grandfathers only the exact path and unchanged Git blob bytes', () => {
  const baseline = Buffer.from('x\n'.repeat(501));
  const file = 'Courses/large notes.txt';
  const inventory = new Map([[file, blob(baseline)]]);
  expect(oversizedFile(file, baseline, inventory)).toBeUndefined();
  expect(oversizedFile(file, Buffer.from('y\n'.repeat(501)), inventory)).toBe(
    501,
  );
  expect(oversizedFile('Courses/moved notes.txt', baseline, inventory)).toBe(
    501,
  );
});

it('runs the wired cap against the actual baseline with the pinned exceptions', () => {
  const log = vi.spyOn(console, 'log').mockImplementation(() => {});
  try {
    expect(runLineCap()).toBe(0);
    expect(log.mock.lastCall?.[0]).toContain('500-line cap');
  } finally {
    log.mockRestore();
  }
}, 30_000);

it('rejects an invalid baseline exception before scanning', async () => {
  const root = await mkdtemp(join(tmpdir(), 'notes-lines-'));
  try {
    const content = join(root, 'site/content/portfolio-export');
    await mkdir(content, { recursive: true });
    await writeFile(
      join(content, 'baseline-oversized.tsv'),
      'lines\tblob\tpath\n901\tbad\tfile.txt\n',
    );
    expect(() => lineCapFailures(root)).toThrow(
      'Invalid 500-line baseline entry',
    );
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

const gitFiles = vi.hoisted(() => ({ value: undefined as string | undefined }));
vi.mock('node:child_process', async (original) => {
  const child = await original<typeof import('node:child_process')>();
  return {
    ...child,
    execFileSync: (...args: Parameters<typeof child.execFileSync>) =>
      gitFiles.value ?? child.execFileSync(...args),
  };
});

it('requires the inventory to shrink when an exact baseline file goes away', async () => {
  const root = await mkdtemp(join(tmpdir(), 'notes-lines-ratchet-'));
  const original = Buffer.from('x\n'.repeat(501));
  const path = 'old.txt';
  try {
    const content = join(root, 'site/content/portfolio-export');
    await mkdir(content, { recursive: true });
    await writeFile(
      join(content, 'baseline-oversized.tsv'),
      `lines\tblob\tpath\n501\t${blob(original)}\t${path}\n`,
    );
    await writeFile(join(root, path), original);
    gitFiles.value = `${path}\0`;
    expect(lineCapFailures(root)).toEqual([]);
    await writeFile(join(root, path), 'x\n');
    expect(lineCapFailures(root)).toEqual([
      `${path}: remove the obsolete baseline exemption`,
    ]);
    gitFiles.value = '';
    expect(lineCapFailures(root)).toEqual([
      `${path}: remove the obsolete baseline exemption`,
    ]);
  } finally {
    gitFiles.value = undefined;
    await rm(root, { recursive: true, force: true });
  }
});
