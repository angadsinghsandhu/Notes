import { expect, it } from 'vitest';
import { getPortfolioNotification } from '../../scripts/portfolio-notification.js';

const source = {
  repository: 'example/notes',
  ref: 'refs/heads/approved-notes-fixture',
  sha: 'a'.repeat(40),
};
const approval = {
  repository: source.repository,
  ref: source.ref,
  workflow: '.github/workflows/notes-site.yml',
};
const run = {
  repository: source.repository,
  ref: source.ref,
  workflow: approval.workflow,
  event: 'push',
  conclusion: 'success',
  headSha: source.sha,
  verifiedSha: source.sha,
};

it('produces one effective notification for a successful approved edit and its repeated delivery', () => {
  const delivered = new Set<string>();
  const first = getPortfolioNotification(source, run, approval, delivered);
  expect(first).toEqual({
    key: `example/notes@${source.sha}`,
    notesSha: source.sha,
  });
  delivered.add(first!.key);
  expect(getPortfolioNotification(source, run, approval, delivered)).toBeNull();

  const nextSha = 'b'.repeat(40);
  expect(
    getPortfolioNotification(
      { ...source, sha: nextSha },
      { ...run, headSha: nextSha, verifiedSha: nextSha },
      approval,
      delivered,
    ),
  ).toEqual({ key: `example/notes@${nextSha}`, notesSha: nextSha });
});

it.each([
  ['a failed run', { conclusion: 'failure' }],
  ['an incomplete run', { conclusion: null }],
  ['a pull request event', { event: 'pull_request' }],
  ['a pull request target event', { event: 'pull_request_target' }],
  ['a non-push event', { event: 'workflow_dispatch' }],
  ['an unapproved run repository', { repository: 'example/fork' }],
  ['an unapproved run branch', { ref: 'refs/heads/unapproved' }],
  ['an unapproved workflow', { workflow: '.github/workflows/other.yml' }],
  ['a mismatched checkout', { headSha: 'b'.repeat(40) }],
  ['a mismatched verification output', { verifiedSha: 'b'.repeat(40) }],
  ['a missing verification output', { verifiedSha: undefined }],
])('produces no intent for %s', (_label, overrides) => {
  expect(
    getPortfolioNotification(
      source,
      { ...run, ...overrides },
      approval,
      new Set(),
    ),
  ).toBeNull();
});

it.each([
  ['a fork', { repository: 'example/fork' }],
  ['an unapproved branch', { ref: 'refs/heads/unapproved' }],
  ['a different revision', { sha: 'b'.repeat(40) }],
])('produces no intent for a candidate from %s', (_label, overrides) => {
  expect(
    getPortfolioNotification(
      { ...source, ...overrides },
      run,
      approval,
      new Set(),
    ),
  ).toBeNull();
});

it.each(['refs/pull/15/merge', 'refs/tags/v1', 'refs/heads/'])(
  'cannot treat %s as an approved branch',
  (ref) => {
    expect(
      getPortfolioNotification(
        { ...source, ref },
        { ...run, ref },
        { ...approval, ref },
        new Set(),
      ),
    ).toBeNull();
  },
);

it.each(['a'.repeat(39), 'A'.repeat(40), `${source.sha}\n`])(
  'rejects a non-canonical SHA even if every input matches it',
  (sha) => {
    expect(
      getPortfolioNotification(
        { ...source, sha },
        { ...run, headSha: sha, verifiedSha: sha },
        approval,
        new Set(),
      ),
    ).toBeNull();
  },
);

it('rejects missing approval and run evidence', () => {
  expect(
    getPortfolioNotification(source, run, undefined, new Set()),
  ).toBeNull();
  expect(
    getPortfolioNotification(source, undefined, approval, new Set()),
  ).toBeNull();
  expect(
    getPortfolioNotification(
      source,
      { ...run, workflow: '' },
      { ...approval, workflow: '' },
      new Set(),
    ),
  ).toBeNull();
});
