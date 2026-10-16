# NovaPay Digital Bank - Automated Compliance Gates Framework

This specification defines the six mandatory, hard-blocking automated compliance gates integrated into NovaPay Digital Bank's CI/CD infrastructure to satisfy regulatory standards and eliminate human error in change management tracking.

---

## 1. Automated Security and Compliance Architecture

| Gate Matrix | Applied Tool | Fail/Block Threshold | On-Failure Automated Remediation | Emergency Exception Lifecycle | Regulatory Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Static Analysis (SAST)** | Semgrep / SonarQube | • 0 Critical issues<br>• Max 2 High issues<br>• Line coverage >= 80% | • Break build stream<br>• Fail Git check status<br>• Auto-raise Jira ticket | • Requires written CISO sign-off<br>• Hard expiration: 24 Hours<br>• Blocked from auto-prod promotion | **PCI-DSS v4.0 Req 6.2** (Bespoke Software Code Quality)<br>**RBI IT Governance Sec 5.1** |
| **2. Dependency Analyzer** | Trivy | • 0 Critical vulnerabilities<br>• 0 Unapproved licenses (GPL/AGPL/SSPL) | • Block build execution<br>• Quarantine artifact package image layers | • Legal department review signature<br>• Strict 72-hour remediation buffer | **RBI IT Governance Sec 7.2** (Third-Party Risk Management)<br>**PCI-DSS v4.0 Req 6.3** |
| **3. Container Assessment** | Trivy Container Scan | • 0 Critical CVE tags<br>• Max 0 Root user execution pathways allowed | • Retain artifact inside internal registry registry<br>• Prevent deployment tag creation | • Tech Lead + CISO cryptographic bypass key authorization | **PCI-DSS v4.0 Req 6.3** (Vulnerability Assessment Lifecycle) |
| **4. Infrastructure as Code (IaC)** | Checkov / Terraform | • 0 Unencrypted S3 buckets<br>• 0 Privileged network access configurations | • Auto-reject open Pull Request branch merges | • Tech Lead short-term exception waiver code mapping | **RBI IT Governance Sec 5.4** (Data Transit Encryption Baseline) |
| **5. Policy-as-Code Engine** | OPA (Open Policy Agent) | • Failure of any strict cluster validation policies | • Reject runtime container admission control streams | • Dual-authorization override keys (Release Mgr + SRE Lead) | **RBI IT Governance Sec 4.3** (Segregation of Duties Core Check) |
| **6. Dynamic Testing (DAST)** | OWASP ZAP | • 0 Vulnerabilities mapped inside OWASP Top 10 | • Tear down temporary execution namespaces | • Risk acceptance template submittal to Technology Risk Committee | **PCI-DSS v4.0 Req 6.4 & 11.3** (Public Web App Boundary Rules) |

---

## 2. Standardized Audit Trail Schema

To satisfy **RBI IT Governance Section 6.1** requirements for continuous change management traceability, every execution gate outputs an immutable JSON signature containing the structural model below:

```json
{
  "\$schema": "https://json-schema.org",
  "title": "NovaPayComplianceAuditRecord",
  "type": "object",
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "pipeline_run_id": { "type": "string" },
    "git_sha": { "type": "string" },
    "executed_by": { "type": "string" },
    "gates_evaluated": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "gate_name": { "type": "string" },
          "status": { "type": "string", "enum": ["PASSED", "FAILED", "BYPASSED_WITH_EXCEPTION"] },
          "vulnerabilities_found": { "type": "integer" },
          "approver_signature_hash": { "type": ["string", "null"] }
        },
        "required": ["gate_name", "status", "vulnerabilities_found"]
      }
    }
  },
  "required": ["timestamp", "pipeline_run_id", "git_sha", "executed_by", "gates_evaluated"]
}
```
