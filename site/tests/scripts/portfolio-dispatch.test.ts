import { expect, it, vi } from 'vitest';
import {
  provePortfolioDispatch,
  sendPortfolioDispatch,
} from '../../scripts/portfolio-dispatch.js';

const notes = { id: 590347468, full_name: 'angadsinghsandhu/Notes' };
const sha = 'a'.repeat(40);
const run = {
  id: 203040,
  run_attempt: 2,
  workflow_id: 379127533,
  repository: notes,
  head_repository: notes,
  head_branch: 'master',
  head_sha: sha,
  event: 'push',
  status: 'completed',
  conclusion: 'success',
};
const job = {
  name: 'verify',
  run_id: run.id,
  run_attempt: run.run_attempt,
  head_sha: sha,
  status: 'completed',
  conclusion: 'success',
};
const head = { name: 'master', protected: true, commit: { sha } };
const event = { action: 'completed', repository: notes, workflow_run: run };
const payload = {
  event_type: 'portfolio-notes-verified',
  client_payload: {
    repository: notes.full_name,
    ref: 'refs/heads/master',
    sha,
    runId: run.id,
  },
};
const runUrl =
  'https://api.github.com/repos/angadsinghsandhu/Notes/actions/runs/203040';
const jobsUrl = runUrl + '/attempts/2/jobs?per_page=100';
const headUrl =
  'https://api.github.com/repos/angadsinghsandhu/Notes/branches/master';
const dispatchUrl =
  'https://api.github.com/repos/angadsinghsandhu/angadsinghsandhu/dispatches';

function proofApi({
  runResponse = Response.json(run),
  jobsResponse = Response.json({ total_count: 1, jobs: [job] }),
  headResponse = Response.json(head),
} = {}) {
  return vi.fn<typeof fetch>(async (url) => {
    const responses = new Map([
      [runUrl, runResponse],
      [jobsUrl, jobsResponse],
      [headUrl, headResponse],
    ]);
    const response = responses.get(String(url));
    if (!response) throw new Error('Unexpected fixture URL');
    return response;
  });
}

it('proves the exact dispatch envelope from a successful push and current protected master', async () => {
  const http = proofApi({
    jobsResponse: Response.json({
      total_count: 2,
      jobs: [job, { ...job, name: 'deploy', conclusion: 'skipped' }],
    }),
  });
  expect(await provePortfolioDispatch(event, 'repo-token', http)).toEqual(
    payload,
  );
  expect(
    http.mock.calls.map(([url, request]) => [
      url,
      request?.method,
      request?.redirect,
    ]),
  ).toEqual([
    [runUrl, 'GET', 'error'],
    [jobsUrl, 'GET', 'error'],
    [headUrl, 'GET', 'error'],
  ]);
  for (const [, request] of http.mock.calls) {
    expect(new Headers(request?.headers).get('Authorization')).toBe(
      'Bearer repo-token',
    );
  }
});

it.each([
  null,
  {},
  { ...event, action: 'requested' },
  { ...event, repository: {} },
  ...[
    { event: 'pull_request' },
    { event: 'workflow_dispatch' },
    { conclusion: 'failure' },
    { status: 'in_progress' },
    { head_repository: { ...notes, id: 15 } },
    { head_repository: { ...notes, full_name: 'fork/Notes' } },
    { repository: null },
    { head_branch: 'refs/heads/master' },
    { head_branch: 'preview' },
    { workflow_id: 5 },
    { id: '203040' },
    { id: 0 },
    { run_attempt: 0 },
    { run_attempt: 1.5 },
    { head_sha: sha + '\n' },
    { head_sha: sha.toUpperCase() },
  ].map((override) => ({ ...event, workflow_run: { ...run, ...override } })),
])(
  'denies an invalid trigger before reading the GitHub API (%#)',
  async (trigger) => {
    const http = proofApi();
    await expect(
      provePortfolioDispatch(trigger, 'repo-token', http),
    ).rejects.toThrow('trigger');
    expect(http).not.toHaveBeenCalled();
  },
);

it.each([
  null,
  { ...run, id: 1 },
  { ...run, run_attempt: 3 },
  { ...run, workflow_id: 42 },
  { ...run, conclusion: 'cancelled' },
  { ...run, head_sha: 'b'.repeat(40) },
])('denies missing or mismatched run evidence (%#)', async (actual) => {
  const http = proofApi({ runResponse: Response.json(actual) });
  await expect(
    provePortfolioDispatch(event, 'repo-token', http),
  ).rejects.toThrow('run');
  expect(http).toHaveBeenCalledTimes(1);
});

it.each([
  [0, []],
  [1, []],
  [1, null],
  [undefined, [job]],
  [101, Array(101).fill(job)],
  [2, [job, job]],
  [1, [{ ...job, name: 'verify (other)' }]],
  [1, [{ ...job, name: 'deploy' }]],
  [1, [{ ...job, conclusion: 'skipped' }]],
  [1, [{ ...job, status: 'queued' }]],
  [1, [{ ...job, head_sha: 'b'.repeat(40) }]],
  [1, [{ ...job, run_id: 12 }]],
  [1, [{ ...job, run_attempt: 1 }]],
  [2, [job, null]],
])(
  'denies ambiguous or failed job evidence (%#)',
  async (total_count, jobs) => {
    const http = proofApi({
      jobsResponse: Response.json({ total_count, jobs }),
    });
    await expect(
      provePortfolioDispatch(event, 'repo-token', http),
    ).rejects.toThrow('job');
    expect(http).toHaveBeenCalledTimes(2);
  },
);

it.each([
  null,
  { ...head, protected: false },
  { ...head, protected: undefined },
  { ...head, name: 'preview' },
  { ...head, commit: { sha: 'b'.repeat(40) } },
])('denies a stale or unprotected head (%#)', async (branch) => {
  const http = proofApi({ headResponse: Response.json(branch) });
  await expect(
    provePortfolioDispatch(event, 'repo-token', http),
  ).rejects.toThrow('head');
});

it('denies pagination, unavailable responses, corrupt JSON and transport errors', async () => {
  const paginated = Response.json(
    { total_count: 1, jobs: [job] },
    {
      headers: { link: '<https://api.github.com/next>; rel="next"' },
    },
  );
  const http = proofApi({ jobsResponse: paginated });
  await expect(
    provePortfolioDispatch(event, 'repo-token', http),
  ).rejects.toThrow('job');
  for (const runResponse of [
    new Response('private body', { status: 403 }),
    new Response('broken JSON'),
  ]) {
    await expect(
      provePortfolioDispatch(event, 'repo-token', proofApi({ runResponse })),
    ).rejects.toThrow('run');
  }
  await expect(
    provePortfolioDispatch(
      event,
      'repo-token',
      vi.fn().mockRejectedValue(new Error('private transport detail')),
    ),
  ).rejects.toThrow(/^Notes workflow run proof failed$/);
});

it('sends only the fixed repository dispatch with the supplied scoped token', async () => {
  const http = vi
    .fn<typeof fetch>()
    .mockResolvedValue(new Response(null, { status: 204 }));
  await sendPortfolioDispatch(JSON.stringify(payload), 'dispatch-token', http);
  expect(http).toHaveBeenCalledExactlyOnceWith(dispatchUrl, {
    method: 'POST',
    redirect: 'error',
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: 'Bearer dispatch-token',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
});

it.each([
  null,
  {},
  { ...payload, event_type: 'wrong-event' },
  { ...payload, client_payload: null },
  ...[
    { repository: 'fork/Notes' },
    { ref: 'refs/heads/preview' },
    { sha: 'invalid' },
    { runId: 0 },
  ].map((override) => ({
    ...payload,
    client_payload: { ...payload.client_payload, ...override },
  })),
])(
  'denies invalid handoff output without making a POST (%#)',
  async (value) => {
    const http = vi.fn<typeof fetch>();
    await expect(
      sendPortfolioDispatch(JSON.stringify(value), 'dispatch-token', http),
    ).rejects.toThrow('payload');
    expect(http).not.toHaveBeenCalled();
  },
);

it('fails closed on malformed output and absent or malformed credentials', async () => {
  const http = vi.fn<typeof fetch>();
  await expect(
    sendPortfolioDispatch('broken JSON', 'dispatch-token', http),
  ).rejects.toThrow('payload');
  for (const token of ['', 'invalid token']) {
    await expect(
      sendPortfolioDispatch(JSON.stringify(payload), token, http),
    ).rejects.toThrow('token');
    await expect(provePortfolioDispatch(event, token, http)).rejects.toThrow(
      'token',
    );
  }
  expect(http).not.toHaveBeenCalled();
});

it('fails visibly without displaying the response body or a transport error', async () => {
  const http = vi
    .fn<typeof fetch>()
    .mockResolvedValueOnce(
      new Response('sensitive response body', { status: 403 }),
    )
    .mockRejectedValueOnce(new Error('sensitive transport error'))
    .mockResolvedValueOnce(new Response('unexpected success', { status: 200 }));
  await expect(
    sendPortfolioDispatch(JSON.stringify(payload), 'dispatch-token', http),
  ).rejects.toThrow(/^Portfolio dispatch failed \(HTTP 403\)$/);
  await expect(
    sendPortfolioDispatch(JSON.stringify(payload), 'dispatch-token', http),
  ).rejects.toThrow(/^Portfolio dispatch request failed$/);
  await expect(
    sendPortfolioDispatch(JSON.stringify(payload), 'dispatch-token', http),
  ).rejects.toThrow(/^Portfolio dispatch failed \(HTTP 200\)$/);
});
