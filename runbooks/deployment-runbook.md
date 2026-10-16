# NovaPay Digital Bank - Production Deployment Runbook (SRE 3 AM Standard)

This document serves as the absolute operational deployment standard. Any deviation from this playbook automatically halts the release window stream.

---

## 1. Pre-Deployment Evidence Checklist
Before executing an environment change pointer update, the on-call engineer must verify the presence of the following cryptographic and analytical markers:
* [ ] **Artifact Signature Check:** Verify container image signature hash match: `cosign verify --key cosign.pub novapay-app:${BUILD_NUMBER}`
* [ ] **SAST Evidence Ledger:** Confirm Semgrep scan outputs `0 Critical` and line coverage `>= 80%`.
* [ ] **Trivy SBOM Attestation:** CycloneDX SBOM file archived inside `evidence/test-results/sbom/`.
* [ ] **Database Pre-Flight Check:** Verify that `V2.0_expand.sql` and `V2.1_migrate.sql` have finished executing inside Pre-Prod with zero table-locking events.

---

## 2. Step-by-Step Traffic Switching Procedure
1. **Target Identification:** Execute local health check to verify target environment readiness (e.g., if switching to green slot):
   ```bash
   curl -fsS http://127.0.0
   ```
2. **Execute Selector Tool:** Run the atomic proxy re-router framework using privileged permissions:
   ```bash
   sudo /usr/local/bin/novapay-switch green
   ```
3. **Parity Check:** Confirm that the active server profile has shifted fields smoothly:
   ```bash
   curl -s http://127.0.0 | grep -i "green"
   ```

---

## 3. Post-Deployment Verification Loop
* **Smoke Testing:** Execute the automated HTTP check package array: `pipeline/scripts/test-canary-routing.sh`.
* **Metric Stabilization:** Monitor the Grafana operational engineering interface for **15 minutes** to verify that p99 latency remains firmly under **200ms** and HTTP 5xx codes remain at **0%**.
