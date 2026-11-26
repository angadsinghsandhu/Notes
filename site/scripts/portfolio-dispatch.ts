const notesRepository = 'angadsinghsandhu/Notes';
const notesRepositoryId = 590347468;
const notesWorkflowId = 379127533;
const branch = 'master';
const ref = 'refs/heads/master';
const eventType = 'portfolio-notes-verified';
const api = 'https://api.github.com/repos/';
const notesApi = api + notesRepository;

function record(value: unknown): Record<string, unknown> | undefined {
  if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
    return value as Record<string, unknown>;
  }
  return undefined;
}

function isId(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value > 0;
}

function isSha(value: unknown): value is string {
  return typeof value === 'string' && /^[a-f0-9]{40}(?![\s\S])/u.test(value);
}

function isNotes(value: unknown): boolean {
  const repository = record(value);
  return (
    repository?.id === notesRepositoryId &&
    repository.full_name === notesRepository
  );
}

function isSuccessful(check: Record<string, unknown>): boolean {
  return check.status === 'completed' && check.conclusion === 'success';
}

function notesRun(value: unknown) {
  const run = record(value);
  if (
    run?.workflow_id === notesWorkflowId &&
    isId(run.id) &&
    isId(run.run_attempt) &&
    isSha(run.head_sha) &&
    run.head_branch === branch &&
    run.event === 'push' &&
    isSuccessful(run) &&
    isNotes(run.repository) &&
    isNotes(run.head_repository)
  ) {
    return { id: run.id, attempt: run.run_attempt, sha: run.head_sha };
  }
  return undefined;
}

function payload(sha: string, runId: number) {
  return {
    event_type: eventType,
    client_payload: { repository: notesRepository, ref, sha, runId },
  };
}

function apiHeaders(token: string) {
  if (!token || /\s/u.test(token))
    throw new Error('Missing or invalid GitHub token');
  return {
    Accept: 'application/vnd.github+json',
    Authorization: 'Bearer ' + token,
  };
}

export async function provePortfolioDispatch(
  trigger: unknown,
  token: string,
  http = fetch,
) {
  const event = record(trigger);
  const run = notesRun(event?.workflow_run);
  if (!run || event?.action !== 'completed' || !isNotes(event.repository)) {
    throw new Error('Notes workflow trigger is ineligible');
  }

  const headers = apiHeaders(token);
  async function read(url: string, failure: string): Promise<unknown> {
    try {
      const response = await http(url, {
        method: 'GET',
        redirect: 'error',
        headers,
      });
      if (response.ok && !response.headers.has('link'))
        return (await response.json()) as unknown;
    } catch {
      // GitHub response bodies and transport errors stay out of workflow logs.
    }
    throw new Error(failure);
  }

  const runUrl = notesApi + '/actions/runs/' + run.id;
  const actual = notesRun(
    await read(runUrl, 'Notes workflow run proof failed'),
  );
  if (
    actual?.id !== run.id ||
    actual.attempt !== run.attempt ||
    actual.sha !== run.sha
  ) {
    throw new Error('Notes workflow run proof failed');
  }

  const jobFailure = 'Notes verify job proof failed';
  const jobsUrl = runUrl + '/attempts/' + run.attempt + '/jobs?per_page=100';
  const result = record(await read(jobsUrl, jobFailure));
  if (
    !Array.isArray(result?.jobs) ||
    result.total_count !== result.jobs.length ||
    result.jobs.length > 100
  ) {
    throw new Error(jobFailure);
  }
  const jobs = (result.jobs as unknown[]).map(record);
  if (
    jobs.some(
      (job) =>
        job?.run_id !== run.id ||
        job.run_attempt !== run.attempt ||
        typeof job.name !== 'string',
    )
  ) {
    throw new Error(jobFailure);
  }
  const required = jobs.filter((job) => job?.name === 'verify');
  const [job] = required;
  if (
    required.length !== 1 ||
    job?.head_sha !== run.sha ||
    !isSuccessful(job)
  ) {
    throw new Error(jobFailure);
  }

  const headFailure = 'Notes protected head proof failed';
  const head = record(
    await read(notesApi + '/branches/' + branch, headFailure),
  );
  if (
    head?.name !== branch ||
    head.protected !== true ||
    record(head.commit)?.sha !== run.sha
  ) {
    throw new Error(headFailure);
  }

  return payload(run.sha, run.id);
}

export async function sendPortfolioDispatch(
  output: string,
  token: string,
  http = fetch,
): Promise<void> {
  const headers = apiHeaders(token);
  const invalidPayload = 'Invalid Portfolio dispatch payload';
  let envelope: Record<string, unknown> | undefined;
  try {
    envelope = record(JSON.parse(output));
  } catch {
    throw new Error(invalidPayload);
  }
  const candidate = record(envelope?.client_payload);
  if (
    envelope?.event_type !== eventType ||
    candidate?.repository !== notesRepository ||
    candidate.ref !== ref ||
    !isSha(candidate.sha) ||
    !isId(candidate.runId)
  ) {
    throw new Error(invalidPayload);
  }
  let response: Response;
  try {
    response = await http(
      api + 'angadsinghsandhu/angadsinghsandhu/dispatches',
      {
        method: 'POST',
        redirect: 'error',
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify(payload(candidate.sha, candidate.runId)),
      },
    );
  } catch {
    throw new Error('Portfolio dispatch request failed');
  }
  if (response.status !== 204)
    throw new Error('Portfolio dispatch failed (HTTP ' + response.status + ')');
}
