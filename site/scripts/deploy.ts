export function getDeploymentDecision(input: {
  eventName: string;
  ref: string;
  gatesPassed: boolean;
  projectName?: string | undefined;
  accountId?: string | undefined;
  hasToken: boolean;
}): { deploy: boolean; reason: string } {
  if (input.eventName !== 'push' || input.ref !== 'refs/heads/master')
    return {
      deploy: false,
      reason: 'Publication disabled: trusted master push required.',
    };
  if (!input.gatesPassed)
    return {
      deploy: false,
      reason: 'Publication disabled: verification must pass.',
    };
  if (!input.projectName?.trim() || !input.accountId?.trim() || !input.hasToken)
    return {
      deploy: false,
      reason:
        'Publication disabled: CLOUDFLARE_PAGES_PROJECT, CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN are required.',
    };
  return {
    deploy: true,
    reason: 'Verified master artifact is ready for publication.',
  };
}
