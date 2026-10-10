# 3. Static Analysis and SAST

## Purpose
Detect source-code security defects before release.

## Checks and controls
Planned gate: zero critical findings and no more than two high findings, subject to tool configuration.

## Failure handling
Block release when configured thresholds are exceeded; provide remediation guidance.

## Evidence
SAST execution report is required. This gate is not confirmed as implemented.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
