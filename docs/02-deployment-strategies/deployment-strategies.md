# NovaPay Deployment Strategies

## 1. Objectives

The deployment design aims to reduce release risk, validate a candidate before
production traffic changes, and provide a recovery path when verification fails.

## 2. Blue-Green Deployment

### Architecture

- Blue slot: application container exposed on host port 8081.
- Green slot: application container exposed on host port 8082.
- Nginx routes production traffic to one active slot.
- Jenkins deploys the candidate to the inactive slot.

### Workflow

1. Identify the currently active slot.
2. Build, scan, and publish the versioned container image.
3. Deploy the candidate to the inactive slot.
4. Run target health checks and integration tests.
5. Switch Nginx traffic to the candidate.
6. Verify the live production endpoint.
7. If verification fails, attempt to restore the previous slot.
8. Verify recovery and mark the release as failed.

### Verified Result

Jenkins Build #31 intentionally forced live verification to fail after traffic
switched to blue on port 8081. The rollback handler switched traffic back to
green on port 8082 and reported "Rollback verification passed". A subsequent
manual check confirmed that port 8082 was active and the production endpoint
returned HTTP 200.

Build #31 ended in FAILURE intentionally because it simulated an unsuccessful
release. This is evidence of rollback behavior, not a successful release.

## 3. Canary Routing

The repository contains `pipeline/nginx/novapay-canary.conf` and
`scripts/test-canary-routing.sh`. The existing canary test report documents
weighted routing behavior.

The configured example sends approximately 90% of requests to the stable
upstream and 10% to the canary upstream. This is a routing demonstration.

### Important Limitations

Weighted routing alone does not prove that the canary is safe. Automated
analysis of latency, error rate, saturation, or business metrics has not been
established by the routing test alone.

Automated promotion and rollback based on observed canary metrics remain
planned work until implemented and tested.

## 4. Safety Controls

- Do not route traffic to a target until health and integration checks pass.
- Validate Nginx configuration before reloading it.
- Verify the live endpoint after switching.
- Record the previous slot so rollback can restore it.
- Record deployment, verification, and rollback results against the build ID.
- Keep the optional TEST_ROLLBACK parameter disabled for routine deployments.

## 5. Operational Risks

A traffic switch can briefly expose the candidate before live verification
finishes. The forced rollback test therefore requires an approved test window
or a separate test environment. A healthy HTTP response is useful evidence
but does not replace business-level synthetic transactions or full monitoring.

## 6. Evidence

- `evidence/blue-green-build-27.txt`
- `evidence/blue-green-rollback-test.txt`
- `docs/canary-test-report.md`
- Jenkins Build #31 console log

## 7. Future Improvements

- Add automated canary metric analysis and explicit promotion thresholds.
- Trigger canary rollback on defined error-rate or latency thresholds.
- Capture deployment duration and rollback frequency.
- Add authenticated synthetic transactions and business-level checks.
