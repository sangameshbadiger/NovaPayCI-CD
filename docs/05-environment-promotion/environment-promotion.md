# Environment Promotion Strategy

## 1. Purpose

This document defines the proposed process for promoting NovaPay releases through Development, Staging, Pre-production, and Production. Each environment must pass its required quality gates before the release advances.

**Current status:** The repository demonstrates a Jenkins-based deployment pipeline and blue-green deployment on EC2. The four-environment promotion workflow is a target design, not an already implemented capability.

## 2. Environment Overview

### Development

Purpose:
- Build and validate application changes.
- Run unit tests, code quality checks, and initial security scans.
- Detect defects early.

Promotion criteria:
- Build succeeds.
- Required tests pass.
- No unapproved critical security findings remain.

### Staging

Purpose:
- Validate integration between application components.
- Run integration and contract tests.
- Perform dependency, container, and dynamic security testing as configured.

Promotion criteria:
- Integration tests pass.
- Required security and compliance gates pass.
- Test results and build identifiers are recorded.

### Pre-production

Purpose:
- Validate the release in a production-like environment.
- Verify configuration, deployment scripts, capacity assumptions, and recovery procedures.
- Complete release review and obtain the required approval.

Promotion criteria:
- Health checks and release validation pass.
- Database compatibility and recovery plans are reviewed where applicable.
- Release approval is recorded.

### Production

Purpose:
- Release the approved artifact using a controlled deployment.
- Verify live application health and business-critical behavior.
- Roll back to the previous working slot if verification fails.

Promotion criteria:
- The exact approved artifact is deployed.
- Live verification passes.
- Deployment results and any rollback actions are recorded.

## 3. Promotion Flow

The target flow is:

Development → Staging → Pre-production → Production

A release must not skip required environments or quality gates without an approved exception. The same immutable artifact should be promoted between environments wherever the deployment design supports it, rather than rebuilding different artifacts for each environment.

## 4. Artifact and Configuration Management

- Record the source commit and build identifier for every release.
- Record the container image tag and immutable image digest.
- Separate environment-specific configuration from the application artifact.
- Store secrets in an approved secrets manager or protected CI/CD credentials.
- Restrict production credentials and deployment permissions.
- Keep deployment and approval logs for audit purposes.

## 5. Failure Handling

- Stop promotion when a required gate fails.
- Publish the failed gate and relevant diagnostic evidence.
- Correct the issue and rerun the required validation.
- Record any authorized exception with its owner, justification, expiry, and remediation plan.
- For production failures, use the documented rollback procedure and verify service recovery.

## 6. Security and Separation of Duties

- Use least-privilege access for each environment.
- Restrict production deployment permissions.
- Require independent approval for production releases where practical.
- Protect the main branch with review and status checks where repository settings support them.
- Audit privileged actions and exception approvals.

## 7. Evidence to Retain

For each promotion, record:

- Release identifier, source commit, and image digest.
- Environment and deployment timestamp.
- Test and security scan results.
- Approval identity and timestamp where required.
- Health-check and verification results.
- Exception details or rollback evidence, if applicable.

## 8. Current Limitations and Future Work

The current Jenkins pipeline demonstrates build, Trivy scanning, ECR publishing, inactive-slot deployment, health checks, integration tests, traffic switching, and rollback verification on EC2.

The repository does not yet demonstrate a complete automated four-environment promotion workflow. Future work includes provisioning isolated environments, implementing environment-specific credentials and approvals, promoting immutable image digests, and adding auditable promotion gates.

