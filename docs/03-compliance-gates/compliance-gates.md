# NovaPay Compliance Gate Matrix

## 1. Purpose

This document defines proposed and implemented controls for the NovaPay
demonstration. A control is not considered operational until its configuration,
execution result, and evidence have been reviewed.

## 2. Gate Matrix

| Gate | Tool | Proposed pass criteria | Current status |
|---|---|---|---|
| Static analysis (SAST) | SonarQube | 0 Critical, at most 2 High, coverage at least 80% | Planned; execution not verified |
| Dynamic analysis (DAST) | OWASP ZAP | 0 Critical/High findings within the configured scan scope | Planned; execution not verified |
| Container vulnerabilities | Trivy | Block HIGH and CRITICAL image findings | Implemented in Jenkins; Build #31 reported zero findings |
| SBOM and dependencies | Trivy SBOM/dependency tooling | Generate a CycloneDX or SPDX SBOM; block critical CVEs and CVSS >= 9.0 | Not verified |
| Licence compliance | FOSSA or ScanCode | No prohibited GPL/AGPL/SSPL dependency without approved review | Planned; execution not verified |
| Kubernetes policy | OPA or Kyverno | All required workload policies pass | Planned; execution not verified |
| Infrastructure policy | Checkov or equivalent | No privileged containers; resource limits defined | Planned; execution not verified |

## 3. Failure and Remediation

- SAST: fix the reported source-code defects and rerun analysis.
- DAST: reproduce findings, remediate application weaknesses, and rerun the scan.
- Container scan: update vulnerable packages or the base image and rebuild.
- SBOM/dependency checks: upgrade or remove affected dependencies and regenerate the SBOM.
- Licence checks: replace incompatible dependencies or obtain documented legal approval.
- Kubernetes policy: correct the workload manifest and rerun policy evaluation.
- Infrastructure policy: correct the Terraform configuration and rerun the scanner.

The pipeline must block release when an enforced gate fails. Remediation must
be linked to the relevant build, commit, scan result, and responsible owner.

## 4. Exceptions and Approvals

Proposed exception workflow:

1. The owner records the finding, affected component, risk, and remediation plan.
2. The request identifies a business justification and compensating controls.
3. An authorized reviewer independent of the requester approves or rejects it.
4. Approval records include approver, timestamp, scope, reason, and expiry.
5. Expired exceptions automatically cease to authorize release.
6. Exceptions are reviewed and closed when remediation is complete.

Suggested time limits must be approved by the organization before enforcement.
An exception must never silently bypass a gate.

## 5. Audit Record

Each gate execution should record:

- Repository, commit SHA, build ID, and image digest.
- Tool name and version, scan scope, and policy version.
- Timestamp and pass/fail result.
- Finding identifiers, severity, and remediation status.
- Exception ID, approver, approval time, and expiry if applicable.

Records should be access-controlled and retained under an approved retention
policy. An immutable audit store is a planned enhancement, not yet verified.

## 6. Regulatory Mapping

The following are design-level mappings and require compliance review before
they can be represented as formal regulatory compliance:

- RBI IT risk and change-management controls: access control, traceability,
  approvals, and evidence of testing.
- PCI DSS v4.0 Requirement 6: secure software development and vulnerability
  management.
- PCI DSS v4.0 Requirement 10: logging and audit trail protection.
- PCI DSS v4.0 Requirement 11: security testing, including penetration testing.
- Segregation of duties: independent approval for production changes and
  policy exceptions.

The exact applicable clauses, applicability, and evidence must be confirmed
by a qualified compliance reviewer. This demonstration does not establish
RBI or PCI DSS certification.

## 7. Current Verified Control

Jenkins Build #31 executed Trivy against the built container image and reported
zero detected vulnerabilities in its scan summary. The pipeline is configured
to fail when HIGH or CRITICAL findings are reported.

This result applies to that image and scan only; it is not proof that every
dependency, application layer, infrastructure component, or regulatory
requirement is compliant.
