# NovaPay Digital Bank - Zero-Downtime Deployment Strategies

This document defines the production deployment methodology for NovaPay Digital Bank, transitioning the organization from high-risk manual SSH deployments to automated, zero-downtime Blue-Green switches and progressive Canary rollouts.

## 1. Nginx-Driven Blue-Green Architecture

NovaPay utilizes a high-availability Virtual Machine configuration where two identical deployment slots are maintained natively on the target fleet:
* **Blue Slot:** Application instance running on `http://127.0.0`
* **Green Slot:** Application instance running on `http://127.0.0`

### Atomic Traffic Switching Protocol
Traffic routing is handled at the reverse-proxy layer via Nginx. When a new release is authorized for deployment, the infrastructure executes the automated orchestrator script `/usr/local/bin/novapay-switch` which performs the following five operations:
1. **Health Verification:** Probes the inactive environment to confirm an `HTTP 200` baseline response.
2. **Configuration Backup:** Creates a time-stamped backup wrapper of `/etc/nginx/conf.d/novapay.conf`.
3. **Atomic Pointer Update:** Executes an in-place `sed` statement to rewrite the active upstream application port block.
4. **Syntax Pre-flight Check:** Validates configuration completeness via `/usr/sbin/nginx -t`.
5. **Graceful Service Reload:** Triggers `systemctl reload nginx` to apply the pointer transformation with zero dropped active TCP connection sockets.

---

## 2. Progressive Canary Rollout Matrix

To minimize blast radius for high-volume banking transactions, new features can optionally undergo a progressive rollout pattern monitored by Prometheus metrics across a rolling 7-day baseline comparison model:

| Phase | Traffic Allocation | Evaluation Window | Health Assessment Criteria | Automated Action Gate |
| :--- | :--- | :--- | :--- | :--- |
| **1. Canary** | 1% – 2% | 15 Minutes | HTTP 5xx rate < 0.1%<br>p99 latency < 200ms | Proceed to Early Adopter or execute Auto-Rollback |
| **2. Early Adopter** | 5% – 10% | 30 Minutes | 0 Critical security alerts fired<br>Error rate < 0.05% | Proceed to Expansion or execute Auto-Rollback |
| **3. Expansion** | 25% – 50% | 60 Minutes | System resource metrics baseline normal<br>All core SLO targets met | Proceed to Full Rollout |
| **4. Full Rollout** | 100% | 24 Hours | Complete transaction consistency validated | Mark deployment stable; terminate inactive code version |

---

## 3. Database State Handling & Session Management

* **Session Persistence:** Application session structures are entirely decoupled from the compute nodes and stored centrally inside a shared, 3-node **Redis 7 cluster**. This prevents active customers from being logged out during atomic port re-routing.
* **Connection Draining:** During a deployment swap, the old environment stops accepting incoming routing streams but allows active payment processing sessions up to **60 seconds** to gracefully complete operations before terminating the underlying runtime context.

## 4. Regulatory Compliance Alignment
* **RBI Master Direction Section 4.2:** Standardizes explicit validation rules and structured rollback blueprints to eliminate data corruption risks.
* **RBI Master Direction Section 6.3:** Enforces automated detection routines to guarantee prompt incident remediation.
