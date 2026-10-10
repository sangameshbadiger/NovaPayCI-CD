# 7. Policy and Compliance Gates

## Purpose
Enforce deployment and regulatory controls before production release.

## Checks and controls
Planned: OPA or Kyverno policies, image provenance, approval separation, and auditable exceptions.

## Failure handling
Reject non-compliant deployments unless a formally approved, time-bound exception applies.

## Evidence
Policy test results and audit records required; this gate is not confirmed as implemented.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
