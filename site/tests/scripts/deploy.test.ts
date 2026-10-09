import { readFile, mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { parse } from 'yaml';
import { expect, it } from 'vitest';
import { getDeploymentDecision } from '../../scripts/deploy.js';

const trusted = {
  eventName: 'push',
  ref: 'refs/heads/master',
  gatesPassed: true,
  projectName: 'notes-library',
  accountId: 'account-id',
  hasToken: true,
};

it('allows a configured trusted master push after successful verification', () => {
  expect(getDeploymentDecision(trusted)).toEqual({
    deploy: true,
    reason: 'Verified master artifact is ready for publication.',
  });
});

it.each([
  { eventName: 'pull_request' },
  { eventName: 'pull_request_target' },
  { ref: 'refs/heads/feature' },
  { ref: 'refs/tags/master' },
  { gatesPassed: false },
  { projectName: undefined },
  { projectName: '' },
  { projectName: '  ' },
  { accountId: undefined },
  { accountId: '' },
  { accountId: '  ' },
  { hasToken: false },
])('disables publication for %j with value-free diagnostics', (change) => {
  const decision = getDeploymentDecision({ ...trusted, ...change });
  expect(decision.deploy).toBe(false);
  expect(decision.reason).toMatch(/Publication disabled:/);
  expect(decision.reason).not.toContain(trusted.accountId);
  expect(decision.reason).not.toContain(trusted.projectName);
});

type Step = {
  id?: string;
  uses?: string;
  run?: string;
  env?: Record<string, string>;
  with?: Record<string, string | number | boolean>;
};
type Job = {
  if?: string;
  needs?: string | string[];
  steps: Step[];
  outputs?: Record<string, string>;
  env?: Record<string, string>;
  defaults?: { run: { 'working-directory': string } };
};
async function workflow() {
  return parse(
    await readFile('../.github/workflows/notes-site.yml', 'utf8'),
  ) as {
    on: Record<string, unknown>;
    jobs: Record<'verify' | 'readiness' | 'deploy', Job>;
  };
}
it('separates PR verification from trusted configured artifact-only publication', async () => {
  const { on, jobs } = await workflow();
  expect(Object.keys(on).sort()).toEqual(['pull_request', 'push']);
  expect(jobs.verify.defaults?.run['working-directory']).toBe('site');
  expect(JSON.stringify(jobs.verify)).not.toContain('CLOUDFLARE_API_TOKEN');
  for (const job of [jobs.readiness, jobs.deploy]) {
    expect(job.if).toContain("github.event_name == 'push'");
    expect(job.if).toContain("github.ref == 'refs/heads/master'");
    expect(job.if).toContain("needs.verify.result == 'success'");
  }
  expect(jobs.deploy.if).toContain(
    "needs.readiness.outputs.configured == 'true'",
  );
  const verifyRuns = jobs.verify.steps.map((step) => step.run).join('\n');
  expect(verifyRuns).toContain('npm ci');
  expect(verifyRuns).toContain('npx playwright install --with-deps chromium');
  expect(verifyRuns).not.toContain('--only-shell');
  expect(verifyRuns).toContain('npm run verify');
  expect(jobs.verify.env?.['SOURCE_REVISION']).toBe('${{ github.sha }}');
  expect(jobs.verify.env?.['SITE_URL']).toBe('${{ vars.SITE_URL }}');
  const upload = jobs.verify.steps.find((step) => step.id === 'artifact')!;
  expect(upload.with?.['path']).toBe('site/dist');
  expect(upload.with?.['if-no-files-found']).toBe('error');
  expect(jobs.verify.outputs?.['artifact-id']).toBe(
    '${{ steps.artifact.outputs.artifact-id }}',
  );
  expect(jobs.verify.outputs?.['artifact-digest']).toBe(
    '${{ steps.artifact.outputs.artifact-digest }}',
  );
  const download = jobs.deploy.steps.find((step) =>
    step.uses?.startsWith('actions/download-artifact@'),
  )!;
  expect(download.with?.['artifact-ids']).toBe(
    '${{ needs.verify.outputs.artifact-id }}',
  );
  expect(download.with?.['digest-mismatch']).toBe('error');
  expect(
    jobs.deploy.steps.some((step) =>
      step.uses?.startsWith('actions/checkout@'),
    ),
  ).toBe(false);
  const deployRuns = jobs.deploy.steps.map((step) => step.run).join('\n');
  expect(deployRuns).not.toMatch(/npm (?:ci|run)|astro build/);
  expect(deployRuns).toContain('wrangler@4.147.0 pages deploy ./dist');
  expect(deployRuns).toContain(
    '--branch master --commit-hash "$SOURCE_REVISION"',
  );
  expect(deployRuns).toContain('artifact.digest !== `sha256:${expected}`');
  for (const job of Object.values(jobs))
    for (const step of job.steps)
      if (step.uses) expect(step.uses).toMatch(/@[a-f0-9]{40}$/);
});

it('installs pinned isolated parity dependencies only before the verification job gate', async () => {
  const { jobs } = await workflow();
  const steps = jobs.verify.steps;
  const setup = steps.findIndex((step) =>
    step.uses?.startsWith('actions/setup-python@'),
  );
  const install = steps.findIndex((step) =>
    step.run?.includes('requirements-polars.txt'),
  );
  const verify = steps.findIndex((step) => step.run === 'npm run verify');
  expect(setup).toBeGreaterThanOrEqual(0);
  expect(install).toBeGreaterThan(setup);
  expect(verify).toBeGreaterThan(install);
  expect(steps[setup]?.uses).toBe(
    'actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97',
  );
  expect(steps[setup]?.with?.['python-version']).toBe('3.12.14');
  expect(steps[install]?.run).toContain(
    'python -m venv ../.superpowers/polars-venv',
  );
  expect(steps[install]?.run).toContain(
    '../.superpowers/polars-venv/bin/python -m pip install -r tests/requirements-polars.txt',
  );
  expect(steps[install]?.run).toContain(
    'echo "$GITHUB_WORKSPACE/.superpowers/polars-venv/bin" >> "$GITHUB_PATH"',
  );
  const requirements = (await readFile('tests/requirements-polars.txt', 'utf8'))
    .split('\n')
    .filter((line) => line && !line.startsWith('#'));
  expect(requirements.map((line) => line.split('==')[0]).sort()).toEqual([
    'fastexcel',
    'nbformat',
    'numpy',
    'openpyxl',
    'pandas',
    'polars',
    'scipy',
  ]);
  for (const line of requirements)
    expect(line).toMatch(/^[a-z]+==\d+\.\d+\.\d+$/);
  for (const job of [jobs.readiness, jobs.deploy])
    expect(JSON.stringify(job)).not.toMatch(
      /setup-python|requirements-polars|polars-venv/,
    );
});

it('actual workflow readiness rejects incomplete/invalid settings without exposing values', async () => {
  const { jobs } = await workflow();
  const script = jobs.readiness.steps.find(
    (step) => step.id === 'decision',
  )!.run!;
  const directory = await mkdtemp(join(tmpdir(), 'notes-readiness-'));
  const configured = {
    ...process.env,
    GITHUB_EVENT_NAME: 'push',
    GITHUB_REF: 'refs/heads/master',
    GATES_PASSED: 'true',
    CLOUDFLARE_PAGES_PROJECT: 'private-project-value',
    CLOUDFLARE_ACCOUNT_ID: 'private-account-value',
    CLOUDFLARE_API_TOKEN: 'never-print-this-token-value',
    SITE_URL: 'https://notes.example.test',
    GITHUB_OUTPUT: join(directory, 'output'),
    GITHUB_STEP_SUMMARY: join(directory, 'summary'),
  };
  try {
    for (const [change, expected] of [
      [{}, true],
      [{ SITE_URL: '' }, false],
      [{ SITE_URL: 'http://notes.example.test' }, false],
      [{ SITE_URL: 'https://user:pass@notes.example.test' }, false],
      [{ SITE_URL: 'https://notes.example.test?query' }, false],
      [{ SITE_URL: 'https://notes.example.test#fragment' }, false],
      [{ SITE_URL: 'invalid' }, false],
      [{ CLOUDFLARE_API_TOKEN: '' }, false],
      [{ CLOUDFLARE_PAGES_PROJECT: '' }, false],
      [{ CLOUDFLARE_ACCOUNT_ID: '' }, false],
      [{ GATES_PASSED: 'false' }, false],
      [{ GITHUB_EVENT_NAME: 'pull_request' }, false],
      [{ GITHUB_REF: 'refs/heads/feature' }, false],
    ] as const) {
      const { stdout, stderr } = await promisify(execFile)(
        'bash',
        ['-e', '-c', script],
        { env: { ...configured, ...change } },
      );
      const output = await readFile(configured.GITHUB_OUTPUT, 'utf8');
      expect(output.trim().split('\n').at(-1)).toBe(`configured=${expected}`);
      const summary = await readFile(configured.GITHUB_STEP_SUMMARY, 'utf8');
      const diagnostics = `${stdout}${stderr}${output}${summary}`;
      for (const value of [
        configured.CLOUDFLARE_API_TOKEN,
        configured.CLOUDFLARE_ACCOUNT_ID,
        configured.CLOUDFLARE_PAGES_PROJECT,
      ])
        expect(diagnostics).not.toContain(value);
    }
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

it('actual artifact verifier accepts only matching metadata and fails closed without leaking credentials', async () => {
  const { jobs } = await workflow();
  const run = jobs.deploy.steps.find((step) =>
    step.run?.includes('Verified artifact identity/digest'),
  )!.run!;
  const script = /<<'NODE'\n([\s\S]*?)\nNODE/.exec(run)![1]!;
  const digest = 'a'.repeat(64);
  const matching = {
    id: 42,
    digest: `sha256:${digest}`,
    workflow_run: { id: 77 },
  };
  const cases = [
    { env: {}, metadata: matching, status: 200, success: true },
    {
      env: { ARTIFACT_ID: '' },
      metadata: matching,
      status: 200,
      success: false,
    },
    {
      env: { ARTIFACT_ID: 'bad-id' },
      metadata: matching,
      status: 200,
      success: false,
    },
    {
      env: { EXPECTED_DIGEST: '' },
      metadata: matching,
      status: 200,
      success: false,
    },
    {
      env: { EXPECTED_DIGEST: 'bad-digest' },
      metadata: matching,
      status: 200,
      success: false,
    },
    { env: {}, metadata: matching, status: 503, success: false },
    { env: {}, metadata: { ...matching, id: 43 }, status: 200, success: false },
    {
      env: {},
      metadata: { ...matching, digest: `sha256:${'b'.repeat(64)}` },
      status: 200,
      success: false,
    },
    {
      env: {},
      metadata: { ...matching, workflow_run: { id: 78 } },
      status: 200,
      success: false,
    },
  ];
  for (const example of cases) {
    // Transport-only GET stub; the unmodified workflow verifier executes below.
    const stub = `globalThis.fetch = async (url, options) => {
      if (url !== 'https://api.example.test/repos/owner/notes/actions/artifacts/42' || (options.method && options.method !== 'GET'))
        throw new Error('Unexpected metadata GET');
      if (options.headers.Authorization !== 'Bearer ' + process.env.GH_TOKEN)
        throw new Error('Unexpected metadata authorization');
      return new Response(${JSON.stringify(JSON.stringify(example.metadata))}, { status: ${example.status} });
    };`;
    const env = {
      ...process.env,
      ARTIFACT_ID: '42',
      EXPECTED_DIGEST: digest,
      GITHUB_API_URL: 'https://api.example.test',
      GITHUB_REPOSITORY: 'owner/notes',
      GITHUB_RUN_ID: '77',
      GH_TOKEN: 'synthetic-token-never-print',
      ...example.env,
    };
    let code = 0;
    let diagnostics: string;
    try {
      const result = await promisify(execFile)(
        process.execPath,
        ['--input-type=module', '-e', `${stub}\n${script}`],
        { env },
      );
      diagnostics = `${result.stdout}${result.stderr}`;
    } catch (error) {
      const failure = error as { code: number; stdout: string; stderr: string };
      code = failure.code;
      diagnostics = `${failure.stdout}${failure.stderr}`;
    }
    expect(code, JSON.stringify(example)).toBe(example.success ? 0 : 1);
    expect(diagnostics).not.toContain(env.GH_TOKEN);
    if (!example.success)
      expect(diagnostics).toMatch(
        /Verified artifact .*unavailable|Verified artifact .*mismatch/,
      );
  }
});
