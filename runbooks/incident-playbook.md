# NovaPay Incident Response Playbook

## 1. Purpose

This playbook defines how operators respond to NovaPay deployment failures and application outages. The priorities are restoring service, preserving evidence, and preventing recurrence.

## 2. Incident Severity

- **SEV-1 — Critical:** Production unavailable or a suspected major security incident.
- **SEV-2 — High:** Major functionality degraded or repeated production errors.
- **SEV-3 — Moderate:** Limited impact with a workable alternative.

These are proposed classifications and should be aligned with the organization's incident policy.

## 3. Initial Response

1. Record the incident start time and observed symptoms.
2. Identify the affected endpoint, release, and Jenkins build.
3. Check the Jenkins console log for failed stages.
4. Check application and Nginx health.
5. Identify the active blue-green slot.
6. Assign an incident owner and notify the appropriate stakeholders.
7. Preserve logs and avoid unrelated production changes.

## 4. Diagnostic Commands

Check Nginx configuration:

```bash
sudo nginx -t
```

Inspect the active upstream:

```bash
sudo grep -m1 -oE '127\.0\.0\.1:(8081|8082)' /etc/nginx/conf.d/novapay.conf
```

Check the live endpoint:

```bash
curl -s -o /dev/null -w 'HTTP %{http_code}\n' http://127.0.0.1/
```

Inspect recent Nginx errors:

```bash
sudo tail -n 100 /var/log/nginx/error.log
```

Use only logs and services that exist on the host. Do not publish credentials or sensitive logs in incident reports.

## 5. Failed Deployment

1. Open the failed Jenkins build.
2. Identify whether the failure occurred during scanning, image publishing, target health checks, integration tests, or live verification.
3. Do not promote an image that failed a required security gate.
4. If traffic has not switched, keep the existing production slot active.
5. If traffic switched and live verification failed, inspect the automated rollback result.
6. Verify the active upstream and live HTTP status.
7. Escalate if the previous slot is unhealthy or traffic restoration fails.

Refer to `docs/06-rollback-specification/rollback-specification.md` for the detailed recovery procedure.

## 6. Production Outage

1. Confirm the outage from the application endpoint.
2. Check Nginx configuration and error logs.
3. Determine whether the active slot is healthy.
4. If a recent release caused the outage, follow the approved rollback procedure.
5. Verify service restoration with health checks and application-level checks where available.
6. Record the recovery time and notify stakeholders.
7. If rollback does not restore service, escalate to the responsible infrastructure or application owner.

Do not make destructive changes or restart unrelated services without understanding the impact.

## 7. Security Incident

For suspected credential exposure, unauthorized access, or malicious activity:

- Notify the designated security contact immediately.
- Preserve relevant logs and timestamps.
- Restrict affected access using the approved security process.
- Rotate exposed credentials through the authorized procedure.
- Do not delete evidence or include secrets in Git commits.
- Follow organizational incident-response and reporting requirements.

## 8. Communications

Maintain an incident record containing:

- Incident identifier, severity, owner, and start time.
- Customer or service impact.
- Affected build, commit, and application version.
- Diagnostic findings and actions taken.
- Rollback and recovery results.
- Resolution time and stakeholder updates.
- Follow-up actions, owners, and target dates.

## 9. Recovery Verification

Before declaring the incident resolved:

- Confirm the expected slot is active.
- Confirm the live endpoint responds successfully.
- Verify the expected application version where possible.
- Run relevant integration or business-level checks.
- Confirm monitoring shows recovery where monitoring is available.
- Document any remaining risks.

## 10. Post-Incident Review

For significant incidents, conduct a blameless review that records:

- A factual timeline.
- Root cause or the current best-supported explanation.
- Detection and recovery gaps.
- What worked and what did not.
- Concrete corrective actions with owners and deadlines.
- Tests that will help prevent recurrence.

## 11. Current Limitations

This playbook documents an operational procedure. Automated paging, centralized log aggregation, service-level objectives, and a formal incident-management integration are not demonstrated by the current repository evidence.
