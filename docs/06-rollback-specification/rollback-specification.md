# Rollback Specification

## 1. Purpose

This document defines how NovaPay restores the previous working application version when a deployment fails verification.

## 2. Deployment Model

NovaPay uses a blue-green deployment approach on EC2:

- **Blue slot:** Application on host port 8081.
- **Green slot:** Application on host port 8082.
- **Traffic routing:** Nginx selects the active slot.
- **Rollback mechanism:** Restore Nginx routing to the previously working slot, validate the configuration, and reload Nginx.

## 3. Rollback Triggers

Initiate rollback when any of the following occurs:

- The newly deployed slot fails its health check.
- Integration tests fail before traffic switching.
- Live verification fails after switching traffic.
- The application returns persistent unexpected HTTP errors.
- The deployed version marker does not match the expected release.
- Critical functional checks fail after deployment.

Automated metric-based triggers for latency and error rate remain future work unless separately implemented and verified.

## 4. Rollback Procedure

1. Identify the candidate slot and the previously active slot.
2. Capture the build identifier, deployment logs, and failure details.
3. Confirm the previous slot is running and responds successfully.
4. Restore Nginx routing to the previous slot using the approved switch script.
5. Validate the Nginx configuration with `nginx -t`.
6. Reload Nginx only after configuration validation succeeds.
7. Check the live endpoint and expected application version.
8. Record the rollback outcome and notify the responsible operator.

Example verification commands:

```bash
sudo grep -m1 -oE '127\.0\.0\.1:(8081|8082)' /etc/nginx/conf.d/novapay.conf
curl -s -o /dev/null -w 'HTTP %{http_code}\n' http://127.0.0.1/
```

Expected result: the active upstream points to the restored slot and the live endpoint returns HTTP 200.

## 5. Failure Handling

If the previous slot is unhealthy or traffic restoration fails:

- Do not claim rollback success.
- Preserve logs and diagnostic information.
- Escalate to the responsible operator.
- Follow the incident playbook to restore service.
- Use a known-good release or an approved recovery procedure.
- Verify application health before closing the incident.

Application rollback does not automatically reverse database changes. Database recovery must follow the separate database migration strategy.

## 6. Verification and Audit Evidence

Record:

- Jenkins build number and source commit.
- Previous and candidate slots.
- Deployment and rollback timestamps.
- Failed verification or trigger.
- Nginx configuration validation results.
- HTTP status and application version after rollback.
- Operator actions, approvals, and incident reference where applicable.

## 7. Tested Evidence

Jenkins Build #31 was deliberately run with `TEST_ROLLBACK=true` to test the rollback path.

The recorded outcome was:

- Candidate deployment and pre-switch checks succeeded.
- Forced live verification failed as expected.
- Traffic was restored to the previous green slot on port 8082.
- Rollback verification passed.
- The Jenkins build ended in FAILURE intentionally because the test injected a deployment verification failure.

A subsequent manual check confirmed that Nginx routed to `127.0.0.1:8082` and the live endpoint returned HTTP 200.

This evidence verifies the tested rollback scenario only. It does not establish that every failure mode or metric-based rollback trigger has been tested.

## 8. Future Improvements

- Add configurable error-rate and latency thresholds.
- Add automated deployment-duration and rollback-frequency metrics.
- Test rollback under additional failure scenarios.
- Integrate alerting and incident tracking.
- Schedule periodic recovery exercises.
