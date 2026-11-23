import {
  mkdir,
  mkdtemp,
  realpath,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import type { PublicationPolicy } from '../../../src/content/index.js';

const git = vi.hoisted(() => vi.fn());
vi.mock('node:child_process', async (original) => {
  const { promisify } = await import('node:util');
  return {
    ...(await original<typeof import('node:child_process')>()),
    execFile: Object.assign(vi.fn(), { [promisify.custom]: git }),
  };
});

import {
  requireDirectory,
  verifyCheckout,
  verifySourceDirectory,
} from '../../../scripts/portfolio-export/checkout.js';

const policy: PublicationPolicy = {
  roots: ['Books'],
  exclude: ['**/private/**'],
  overrides: {},
  repositoryPublic: false,
};
const revision = 'a'.repeat(40);
let root: string;
const command = new Map<string, string>();
beforeEach(async () => {
  root = await mkdtemp(join(await realpath(tmpdir()), 'notes-checkout-'));
  command.set('rev-parse --show-toplevel', `${root}\n`);
  command.set('rev-parse --verify HEAD', `${revision}\n`);
  git.mockImplementation(async (_executable: string, args: string[]) => ({
    stdout: command.get(args.slice(3).join(' ').split(' -- ')[0]!) ?? '',
  }));
});
afterEach(async () => {
  command.clear();
  git.mockReset();
  await rm(root, { recursive: true, force: true });
});

it('requires a matching full revision and rejects dirty or hidden tracked inputs', async () => {
  await expect(verifyCheckout(root, revision)).resolves.toBeUndefined();
  await expect(verifyCheckout(root, 'b'.repeat(40))).rejects.toThrow(
    /revision.*checkout/i,
  );
  command.set('rev-parse --show-toplevel', '/another-repository\n');
  await expect(verifyCheckout(root, revision)).rejects.toThrow(
    /revision.*checkout/i,
  );
  command.set('rev-parse --show-toplevel', `${root}\n`);
  command.set(
    'status --porcelain=v1 --untracked-files=no --ignore-submodules=none',
    ' M Books/page.md\n',
  );
  await expect(verifyCheckout(root, revision)).rejects.toThrow(
    'Dirty tracked checkout',
  );
  command.delete(
    'status --porcelain=v1 --untracked-files=no --ignore-submodules=none',
  );
  command.set('ls-files -v -z', 'S Books/page.md\0');
  await expect(verifyCheckout(root, revision)).rejects.toThrow('skip-worktree');
});

it('rejects untracked publishable sources, including ignored Notes inputs', async () => {
  const books = join(root, 'Books');
  await mkdir(books);
  await writeFile(join(books, 'new.md'), '# New');
  await writeFile(join(books, 'unsupported.bin'), 'sample');
  command.set(
    'ls-files --others -z',
    'Books/unsupported.bin\0Books/private/local.md\0',
  );
  await expect(verifyCheckout(root, revision, policy)).resolves.toBeUndefined();
  command.set('ls-files --others -z', 'Books/new.md\0');
  await expect(verifyCheckout(root, revision, policy)).rejects.toThrow(
    'Books/new.md',
  );
  command.set('ls-files --others -z', 'site/scripts/export-portfolio.js\0');
  await expect(verifyCheckout(root, revision, policy)).rejects.toThrow(
    'site/scripts/export-portfolio.js',
  );
});

it('rejects optional checked-out submodule content from a release input', async () => {
  const repo = join(root, 'Books/linked');
  command.set('ls-files --stage -z', `160000 ${revision} 0\tBooks/linked\0`);
  await expect(verifyCheckout(root, revision, policy)).resolves.toBeUndefined();
  await mkdir(repo, { recursive: true });
  await expect(verifyCheckout(root, revision, policy)).resolves.toBeUndefined();
  await writeFile(
    join(repo, 'extra.md'),
    '# Added only when the submodule is initialized',
  );
  await expect(verifyCheckout(root, revision, policy)).rejects.toThrow(
    'initialized submodule',
  );
});

it('accepts absent optional enrollment but rejects symbolic links in its path or files', async () => {
  const files = join(root, 'actual');
  await mkdir(join(files, 'child'), { recursive: true });
  await writeFile(join(files, 'child/ready.json'), '{}');
  await expect(
    verifySourceDirectory(join(root, 'optional')),
  ).resolves.toBeUndefined();
  await expect(verifySourceDirectory(files)).resolves.toBeUndefined();
  const alias = join(root, 'alias');
  await symlink(files, alias);
  await expect(requireDirectory(join(alias, 'child'))).rejects.toThrow(
    'Unsafe symbolic link',
  );
  await expect(verifySourceDirectory(alias)).rejects.toThrow(
    'Unsafe symbolic link',
  );
  await symlink(join(files, 'child/ready.json'), join(files, 'unsafe.json'));
  await expect(verifySourceDirectory(files)).rejects.toThrow(
    'Unsafe publication input',
  );
});
