# OWASP ZAP Security Scan Summary

## Latest Scan — Jenkins Build #71

- **Target:** Deployed NovaPay application
- **Scan type:** OWASP ZAP DAST scan
- **Build status:** SUCCESS
- **FAIL alerts:** 0
- **PASS alerts:** 66
- **Warning categories:** 1
- **Warning instances:** 3

## Remaining Finding

### Non-Storable Content — Informational (Medium)

- **Alert ID:** 10049
- **Instances:** 3
- **Affected paths:** `/`, `/robots.txt`, `/sitemap.xml`
- **Description:** Responses are marked as non-storable by caching components.

**Risk assessment:** The application intentionally uses `Cache-Control: no-store`. This can be appropriate for sensitive banking-related responses. Confirm the caching policy against the actual data sensitivity and application requirements before changing it.

**Disposition:** Retain the header pending review. The ZAP warning remains unresolved as a scanner finding; it is not recorded as fixed.

## Verification

The latest report files are located in:
- `evidence/test-results/zap/zap-report.json`
- `evidence/test-results/zap/zap-report.html`

The JSON report parses successfully, and the HTML report contains the remaining finding.

## Limitations

A successful DAST scan does not prove the application is free of vulnerabilities or replace a full penetration test. Findings require review, risk-based disposition, and retesting after remediation.
fixed.

## Verification

The latest report files are located in:
- `evidence/test-results/zap/zap-report.json`
- `evidence/test-results/zap/zap-report.html`

The JSON report parses successfully, and the HTML report contains the remaining finding.

## Limitations

A successful DAST scan does not prove the application is free of vulnerabilities or replace a full penetration test. Findings require review, risk-based disposition, and retesting after remediation.
