import { execFile } from 'node:child_process';
import { lstat, realpath, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { promisify } from 'node:util';
import {
  discoverEntries,
  publicationExclusion,
  type PublicationPolicy,
} from '../../src/content/index.js';

const exec = promisify(execFile);
const git = async (cwd: string, args: string[]) => {
  const { stdout } = await exec(
    'git',
    ['--no-optional-locks', '-c', 'core.fsmonitor=false', ...args],
    {
      cwd,
      maxBuffer: 16 * 1024 * 1024,
      env: Object.fromEntries(
        Object.entries(process.env).filter(
          ([name]) => !name.startsWith('GIT_'),
        ),
      ),
    },
  );
  return stdout;
};

export const isMissing = (error: unknown) =>
  error instanceof Error && 'code' in error && error.code === 'ENOENT';

export async function requireDirectory(path: string): Promise<void> {
  if (!(await lstat(path)).isDirectory() || (await realpath(path)) !== path)
    throw new Error(`Unsafe symbolic link or non-directory: ${path}`);
}

export async function verifySourceDirectory(path: string): Promise<void> {
  const info = await lstat(path).catch((error: unknown) => {
    if (!isMissing(error)) throw error;
  });
  if (info === undefined) return;
  await requireDirectory(path);
  for (const entry of await readdir(path, { withFileTypes: true })) {
    const target = join(path, entry.name);
    if (entry.isDirectory()) await verifySourceDirectory(target);
    else if (!entry.isFile())
      throw new Error(`Unsafe publication input: ${target}`);
  }
}

export async function verifyCheckout(
  root: string,
  revision: string,
  policy?: PublicationPolicy,
): Promise<void> {
  const top = (await git(root, ['rev-parse', '--show-toplevel'])).trimEnd();
  const head = (await git(root, ['rev-parse', '--verify', 'HEAD'])).trimEnd();
  if (top !== root || head !== revision)
    throw new Error(
      `Source revision ${revision} does not match checkout ${head} at ${top}`,
    );
  const status = await git(root, [
    'status',
    '--porcelain=v1',
    '--untracked-files=no',
    '--ignore-submodules=none',
  ]);
  if (status) throw new Error(`Dirty tracked checkout:\n${status.trimEnd()}`);
  const flags = await git(root, ['ls-files', '-v', '-z']);
  if (flags.split('\0').some((value) => /^[a-zS] /.test(value)))
    throw new Error(
      'Checkout includes skip-worktree or assume-unchanged tracked files',
    );

  if (!policy) return;
  const trackedSourceRoots = [
    ...policy.roots,
    'site/content',
    'site/src',
    'site/scripts',
  ];
  const candidates = (
    await git(root, ['ls-files', '--others', '-z', '--', ...trackedSourceRoots])
  )
    .split('\0')
    .filter(Boolean);
  const archivePaths = candidates.filter(
    (path) =>
      !path.startsWith('site/') &&
      !publicationExclusion(path.normalize('NFC'), policy),
  );
  const illegal = candidates.filter((path) => path.startsWith('site/'));
  if (archivePaths.length) {
    const { ledger } = await discoverEntries(root, policy);
    const unpublished = new Set(
      ledger
        .filter(
          ({ disposition }) =>
            disposition === 'excluded' || disposition === 'unsupported',
        )
        .map(({ sourcePath }) => sourcePath),
    );
    illegal.push(
      ...archivePaths.filter((path) => !unpublished.has(path.normalize('NFC'))),
    );
  }
  if (illegal.length)
    throw new Error(`Untracked publication inputs:\n${illegal.join('\n')}`);

  const tracked = await git(root, [
    'ls-files',
    '--stage',
    '-z',
    '--',
    ...trackedSourceRoots,
  ]);
  for (const entry of tracked.split('\0')) {
    const path = /^160000 [a-f0-9]+ 0\t([\s\S]+)$/.exec(entry)?.[1];
    if (!path || publicationExclusion(path.normalize('NFC'), policy)) continue;
    const contents = await readdir(join(root, path)).catch((error: unknown) => {
      if (!isMissing(error)) throw error;
      return [];
    });
    if (contents.length)
      throw new Error(
        `Publication input contains an initialized submodule: ${path}`,
      );
  }
}
