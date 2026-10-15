# NovaPay Observability & DORA Metrics Strategy

## 1. DORA Metrics Tracking
- **Deployment Frequency**: Automated tracking via Jenkins build logs.
- **Lead Time for Changes**: Calculated from GitHub commit timestamp to production deployment success.
- **Change Failure Rate**: Tracked via automated rollback execution counts.
- **MTTR**: Measured using Prometheus alerts duration from firing to resolution.

## 2. Dashboard Mockups
- **Engineering Dashboard**: Live container memory, CPU logs, and network connection status.
- **Regulatory Dashboard**: Clean compliance logs mapping SonarQube, Trivy, and OPA rules.
