# NovaPay Observability and DORA Metrics

## 1. Purpose

This document defines how NovaPay should measure deployment performance, application health, and recovery effectiveness.

**Current status:** Jenkins build logs and deployment evidence are available. A centralized observability platform and automated DORA dashboard are proposed future improvements.

## 2. DORA Metrics

### 2.1 Deployment Frequency

**Definition:** How often successful production deployments occur during a defined period.

**Measurement:** Count successful production deployment events per day, week, or month.

**Data source:** Jenkins build history and deployment records.

**Improvement:** Automate collection of successful production deployment events and distinguish normal releases from test-only rollback runs.

### 2.2 Lead Time for Changes

**Definition:** Time from a code change being committed until that change reaches production.

**Measurement:** Production deployment timestamp minus the relevant source commit timestamp.

**Data source:** Git commit metadata and Jenkins deployment timestamps.

**Improvement:** Associate each production deployment with its source commit and record timestamps consistently.

### 2.3 Change Failure Rate

**Definition:** Percentage of production deployments that result in a failure requiring remediation, rollback, or a hotfix.

**Measurement:**

Change failure rate = (Failed production changes / Total production changes) × 100

**Data source:** Deployment records, incidents, rollbacks, and hotfix records.

**Important:** A deliberately injected rollback test must be identified separately so it does not distort normal production change-failure reporting.

### 2.4 Mean Time to Recovery (MTTR)

**Definition:** Average time taken to restore service following a production failure.

**Measurement:** Total recovery time across qualifying incidents divided by the number of those incidents.

**Data source:** Incident start and recovery timestamps, supported by deployment and rollback logs.

**Improvement:** Record incident timestamps consistently and automate incident-to-deployment correlation.

## 3. Pipeline Metrics

Track the following metrics alongside DORA metrics:

- Pipeline success and failure rates.
- Duration of each pipeline stage.
- Total build and deployment duration.
- Security scan findings by severity.
- Integration-test pass and failure counts.
- Health-check failure counts.
- Rollback count and rollback duration.
- Time spent waiting for approvals.
- Failed deployments by release and environment.

## 4. Application Health Signals

Recommended signals include:

- HTTP availability and response status.
- Request latency, including p95 and p99.
- HTTP 5xx error rate.
- CPU and memory utilization.
- Container restart count.
- Nginx upstream health.
- Synthetic transaction results for critical application workflows.

HTTP 200 alone is not sufficient to prove complete business functionality.

## 5. Dashboard Design

A proposed Grafana dashboard should include:

1. Deployment frequency over time.
2. Lead-time distribution.
3. Change failure rate.
4. MTTR trend.
5. Jenkins pipeline duration and success rate.
6. Security scan findings.
7. Rollback events and outcomes.
8. Application availability, latency, and error rate.

Every panel should identify its data source, measurement window, and calculation method.

## 6. Alerting and Response

Suggested alert conditions should be configured only after establishing baseline measurements and ownership.

Examples include:

- Sustained HTTP 5xx errors.
- Failed production health checks.
- High p95 latency.
- Repeated pipeline failures.
- Rollback failure.
- Critical security findings blocking release promotion.

Alerts should identify severity, affected service, runbook link, and escalation owner. Thresholds must be validated against observed behavior rather than treated as already configured.

## 7. Evidence and Data Quality

For every release, retain the source commit, Jenkins build number, image digest, deployment timestamps, environment, test results, verification outcome, and rollback information.

Exclude duplicate events and classify deliberate failure-injection tests separately. Use consistent definitions and reporting windows to avoid misleading comparisons.

## 8. Current Limitations and Future Work

The repository contains Jenkins pipeline evidence and a tested blue-green rollback scenario. It does not yet demonstrate an automatically populated DORA dashboard, centralized application telemetry, or fully automated incident correlation.

Future work includes deploying an approved metrics stack, exporting Jenkins and application metrics, adding Grafana dashboards, configuring alert rules, and validating metric calculations against real deployment and incident records.
