# NovaPay Deployment Runbook

## 1. Purpose

This runbook provides operational steps for deploying NovaPay, verifying service health, and recovering from a failed release.

## 2. System Details

- **Platform:** Amazon Linux 2023 EC2
- **CI/CD:** Jenkins
- **Container registry:** Amazon ECR
- **Web server and traffic routing:** Nginx
- **Deployment strategy:** Blue-green
- **Blue slot:** Port 8081
- **Green slot:** Port 8082
- **Application endpoint:** `http://13.126.250.226/`

## 3. Pre-deployment Checklist

Before starting a deployment:

1. Confirm the intended source commit is available on the main branch.
2. Review the Jenkinsfile changes.
3. Confirm required CI checks and security scans are configured.
4. Verify Jenkins, Docker, ECR access, and the EC2 host are healthy.
5. Confirm the current production slot responds successfully.
6. Ensure the optional `TEST_ROLLBACK` parameter is **unchecked** for a routine deployment.
7. Record the current build and release identifiers.

## 4. Deploy a Release

1. Open the NovaPay Jenkins job, `NovaPay-CI`.
2. Select **Build with Parameters**, if available.
3. Leave `TEST_ROLLBACK` unchecked.
4. Start the build and monitor the console output.
5. Confirm the image build and configured security scan complete successfully.
6. Confirm the image is pushed to Amazon ECR.
7. Verify the inactive slot deployment and target health check.
8. Confirm integration tests pass.
9. Monitor the traffic-switch and live-verification stages.
10. Record the final build result and deployed version.

Do not manually switch production traffic to an unverified candidate.

## 5. Verify Production

Connect to the EC2 instance and run:

```bash
sudo nginx -t
sudo grep -m1 -oE '127\.0\.0\.1:(8081|8082)' /etc/nginx/conf.d/novapay.conf
curl -s -o /dev/null -w 'HTTP %{http_code}\n' http://127.0.0.1/
```

Expected results:

- Nginx configuration validation succeeds.
- The upstream points to the active blue or green slot.
- The application returns HTTP 200.

HTTP 200 alone does not prove that all business functions are working correctly.

## 6. Respond to a Failed Deployment

1. Open the failed Jenkins build and identify the failing stage.
2. Preserve the console log and build identifier.
3. Determine whether traffic switched to the candidate slot.
4. If live verification failed, inspect the rollback output.
5. Verify that Nginx routes to the previous working slot.
6. Confirm the live endpoint returns HTTP 200.
7. Check the deployed version marker where available.
8. Escalate if service health cannot be restored.
9. Document the failure, recovery actions, and follow-up tasks.

Use `docs/06-rollback-specification/rollback-specification.md` for the detailed rollback procedure.

## 7. Security Precautions

- Never paste passwords, access keys, tokens, or private keys into Jenkins logs or Git.
- Do not disable security scans merely to obtain a successful build.
- Keep production credentials restricted.
- Do not run the forced rollback test during routine deployments.
- Obtain authorization before performing disruptive production tests.

## 8. Evidence and Audit Trail

Record the Jenkins build number, source commit, image digest, scan results, deployment timestamp, active slot, health-check output, and rollback details when applicable.

## 9. Current Limitations

This runbook describes the current EC2/Jenkins blue-green workflow. It does not establish that multi-environment promotion, automated metric-based canary rollback, or database migration automation is implemented.
