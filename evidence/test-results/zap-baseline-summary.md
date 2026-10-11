# OWASP ZAP Baseline Scan

- Target: http://127.0.0.1:8082/
- Scan type: Passive baseline scan
- FAIL alerts: 0
- Warning types: 8
- PASS alerts: 59

## Warnings observed
- Missing anti-clickjacking header
- Missing X-Content-Type-Options header
- Server version information exposed
- Missing Content Security Policy
- Cacheable content
- Missing Permissions Policy
- Missing or invalid Cross-Origin-Embedder-Policy

## Limitations
This baseline scan is not a full penetration test.
Warnings require review and risk-based remediation.
