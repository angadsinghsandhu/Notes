# Verified Notes notifications to Portfolio

A successful `Notes site` run for a push to `angadsinghsandhu/Notes` master can
notify `angadsinghsandhu/angadsinghsandhu` through the
`portfolio-notes-verified` repository dispatch. The sender uses workflow ID
`379127533`, source repository ID `590347468`, and a required job named
`verify`.

The sender checks the GitHub API with its read-only Notes workflow token. It
matches the triggering run ID, attempt, and SHA to the successful workflow
run, requires exactly one completed successful `verify` job for that run,
attempt, and SHA, and checks that the SHA is still the protected master
head. A failed or ambiguous proof stops the notification. Portfolio verifies
the Notes evidence independently and deduplicates repeated deliveries for
the same Portfolio and Notes SHA pair.

## Enable the sender

1. In Notes, configure the `portfolio-notify` environment to allow only the
   `master` branch. Keep branch protection enabled on Notes master.
2. Store `NOTES_PORTFOLIO_DISPATCH_TOKEN` as a secret in that environment.
   Use a credential scoped to the Portfolio repository with the Contents
   write permission required by GitHub's repository dispatch endpoint.
3. After the workflow is on Notes master and the Portfolio receiver is
   ready, set the Notes repository Actions variable
   `NOTES_PORTFOLIO_NOTIFY_ENABLED` to `true`. Remove the variable or set it
   to `false` to disable future notifications.

The workflow uses its own trusted master revision and runs without installing
package dependencies. The proof step has the Notes read token. The final step
receives the Portfolio token and sends the verified Notes repository, full
branch ref, SHA, and numeric run ID. GitHub API failures are visible in the
workflow log with safe error messages.
