# NovaPay Digital Bank - Incident Response & Disaster Recovery Playbook

This playbook establishes the operational protocol for classifying, managing, and resolving production-grade application anomalies.

---

## 1. Incident Severity Classification Matrix

| Incident Tier | Definition and Structural Bounds | Target Response SLA | Executive Escalation Vector |
| :--- | :--- | :--- | :--- |
| **SEV-1** | Complete core transaction system outage; data corruption risk; customer-facing failure. | **< 5 Minutes** | CTO + CISO + VP Engineering |
| **SEV-2** | Major component degradation (e.g., UPI transfers failing for >10% of active sessions). | **< 15 Minutes** | SRE Lead + VP Engineering |
| **SEV-3** | Minor feature failure with a functional, documented workaround available on disk. | **< 1 Hour** | SRE On-Call Team |
| **SEV-4** | Micro cosmetic issues; zero performance latency or transaction impacts. | Next Business Day | Assigned Engineering Pod |

---

## 2. Case Study Simulation: The Friday 5:07 PM Crisis Timeline
* **Scenario Context:** A developer bypasses staging to push a "critical hotfix." 8 minutes into the canary test, multiple priority metrics breach system thresholds simultaneously.

```mermaid
timeline
    title Incident Response Execution Timeline (Friday 5:07 PM IST)
    T+00m (5:07 PM) : Developer pushes unverified hotfix directly to Canary fleet.
    T+08m (5:15 PM) : Prometheus alerts breach: HTTP 500 error rate at 12%, DB pool exhausted, UPI gateway timeouts at 35%.
    T+09m (5:16 PM) : Incident classified as SEV-1. PagerDuty auto-escalates to CTO and CISO.
    T+10m (5:17 PM) : Automated Category A Rollback Trigger fires. Nginx proxy pointer instantly reverts traffic to Blue slot.
    T+11m (5:18 PM) : Internal engineering bridge activated. Status page updated with notice.
    T+15m (5:22 PM) : Post-deployment verification script runs. HTTP 5xx codes return to 0% on stable Blue baseline.
    T+30m (5:37 PM) : System confirmed stable. Root cause identified: manual database update script locked pool allocations.
```

### Post-Mortem Remediation Action Items
1. **Hard Pipeline Gate:** Revoke manual server access credentials for non-production workflows to block future bypass vectors (**RBI Sec 4.3 parity**).
2. **Connection Optimization:** Readjust `pgBouncer` pooling capacities to prevent saturation spikes from cascading into downstream connection blockages.
