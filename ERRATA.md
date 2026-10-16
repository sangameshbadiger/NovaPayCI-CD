# NovaPay Digital Bank - Project Errata Report

The following three deliberate technical/regulatory errors hidden inside the project documentation have been successfully identified and tracked below:

## 1. Part A: Database Core Specification Overlap
* **Location:** Part A - Section A3 (Zero-Downtime Deployment Strategies)
* **Discrepancy:** The text recommends deploying PostgreSQL 16 microservices but instructs using `gh-ost` or `pt-online-schema-change` for zero-downtime database migrations. 
* **Correction:** `gh-ost` and `pt-online-schema-change` are toolchains exclusively architecture-engineered for MySQL/MariaDB engines. For NovaPay's native PostgreSQL 16 framework, `pgroll` or native transactional migration workflows must be utilised instead to avoid data locking issues.

## 2. Part C: Cloudflare Outage Timeline Misrepresentation
* **Location:** Part C - Case Study 3 (Cloudflare Global Outage)
* **Discrepancy:** The text initially claims that the catastrophic regex configuration drop caused an outage lasting 21 minutes.
* **Correction:** The original outage duration spanned exactly 27 minutes before the core mitigation layers were fully restored.

## 3. Part D: Mandatory Directory Layout Discrepancy
* **Location:** Part D - Section D2 (Mandatory Repository Structure)
* **Discrepancy:** The required directory layout lists policy structures inside `pipeline/policies/` and automation shell code files inside `pipeline/scripts/`. However, the downstream daily breakdown steps and the pre-existing baseline template directories initialized these assets directly in the root directory paths (`/policies` and `/scripts`).
* **Correction:** The root folder structures have been systematically migrated into `pipeline/policies/` and `pipeline/scripts/` to ensure absolute compliance with the primary directory layout structural schema checked during verification.
