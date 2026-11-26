type Approval = {
  repository: string;
  ref: string;
  workflow: string;
};
type Candidate = Pick<Approval, 'repository' | 'ref'> & { sha: string };
type VerificationRun = Approval & {
  event: string;
  conclusion: string | null;
  headSha: string;
  verifiedSha?: string | undefined;
};

/** The caller supplies trusted workflow metadata and durable delivery state. */
export function getPortfolioNotification(
  candidate: Candidate,
  run: VerificationRun | undefined,
  approval: Approval | undefined,
  delivered: ReadonlySet<string>,
): { key: string; notesSha: string } | null {
  if (
    !approval?.repository ||
    !approval.workflow ||
    !/^refs\/heads\/.+$/.test(approval.ref) ||
    candidate.repository !== approval.repository ||
    candidate.ref !== approval.ref ||
    !/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/.test(candidate.sha)
  )
    return null;

  if (
    !run ||
    run.event !== 'push' ||
    run.conclusion !== 'success' ||
    run.repository !== approval.repository ||
    run.ref !== approval.ref ||
    run.workflow !== approval.workflow ||
    run.headSha !== candidate.sha ||
    run.verifiedSha !== candidate.sha
  )
    return null;

  const key = `${candidate.repository}@${candidate.sha}`;
  return delivered.has(key) ? null : { key, notesSha: candidate.sha };
}
