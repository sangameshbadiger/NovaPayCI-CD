# 4. Dependency and Container Scanning

## Purpose
Identify known vulnerabilities in container images and dependencies.

## Checks and controls
Implemented: Trivy image scan blocks HIGH and CRITICAL findings. SBOM and licence checks require separate verification.

## Failure handling
Fail the pipeline when the configured severity gate is breached.

## Evidence
Trivy report from Jenkins; Build #31 reported zero detected vulnerabilities.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
