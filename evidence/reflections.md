# NovaPay CI/CD Project — Reflections

## 1. What were the most challenging parts of building the CI/CD pipeline?

One of the most challenging parts of building the NovaPay CI/CD pipeline was coordinating the different tools and stages into a reliable deployment process. Jenkins, Docker, Amazon ECR, EC2, Nginx, and Trivy each serve a different purpose. A problem in one stage can prevent the entire release from completing, so understanding the dependencies between stages was essential.

Container image creation and publication required attention to build configuration, registry authentication, image tags, and permissions. The pipeline also needed to ensure that a candidate image was healthy before production traffic was redirected to it. This made the order of the stages important: building and scanning the image, publishing it, deploying it to an inactive slot, checking its health, running integration tests, switching traffic, and verifying the live application.

Another challenge was diagnosing failures without confusing an expected test failure with an ordinary deployment failure. The rollback exercise deliberately forced live verification to fail. The Jenkins build consequently ended in FAILURE, even though the rollback successfully restored the previous working slot. Understanding this distinction was important when interpreting pipeline results.

I learned that successful automation requires more than connecting commands together. Each stage needs clear inputs, success criteria, failure behavior, and evidence. Logging and verification make it possible to understand what happened during a deployment.

If I continued this project, I would improve error reporting, add stronger business-level checks, and test more failure scenarios. I would also make stage results and release metadata easier to correlate. These improvements would make the pipeline easier to maintain and would help an operator investigate failures more quickly.

## 2. How did blue-green deployment improve the release process, and what are its limitations?

Blue-green deployment separates the application into two deployment slots. In NovaPay, the blue slot uses host port 8081 and the green slot uses host port 8082. The active slot serves production traffic while a candidate release is deployed and checked in the inactive slot.

This approach reduces the need to replace the running application in place. The candidate can be deployed and tested before Nginx redirects traffic to it. If the candidate fails live verification after the switch, the pipeline can restore traffic to the previous working slot. This gives the deployment process a defined recovery path.

The rollback test provided practical evidence of this behavior. Jenkins Build #31 deliberately failed live verification after switching traffic. The rollback handler restored the previous green slot, and rollback verification passed. A subsequent manual check confirmed that Nginx routed to port 8082 and the live endpoint returned HTTP 200.

However, blue-green deployment does not eliminate every deployment risk. Both slots must have sufficient resources, and configuration must be correct. A successful HTTP response does not guarantee that important business operations work correctly. The approach also does not automatically reverse database schema or data changes. Database compatibility therefore needs separate planning.

Another limitation is that the tested rollback scenario covers only one deliberately injected failure. It does not prove that every infrastructure, networking, application, or data failure will recover automatically.

My main lesson is that deployment strategy and verification must work together. I would extend the project with authenticated synthetic transactions, additional failure tests, stronger monitoring, and explicit checks for application-version consistency. I would also test recovery procedures in a controlled environment before relying on them for critical releases.

## 3. How should security and compliance controls be integrated into CI/CD?

Security and compliance should be integrated into the delivery process rather than treated as a final manual review. In NovaPay, Trivy is configured to fail the container scanning stage for HIGH and CRITICAL findings. The recorded Build #31 evidence reported zero vulnerabilities in that scan. This demonstrates a container-scanning control, but it does not prove that every security requirement has been implemented.

A more complete pipeline would include static application security testing, dependency and licence checks, software bill of materials generation, dynamic application security testing, and infrastructure-as-code scanning. Each tool should have a defined purpose, configured thresholds, and an understood response when a check fails. Results should be retained with the build identifier and source commit.

Policy gates should prevent promotion when mandatory requirements are not met. For example, a critical security finding could block release until it is corrected or an authorized exception is granted. Exceptions should have a documented owner, justification, expiry date, compensating controls, and remediation plan. Expired exceptions should not silently remain valid.

Credentials also require careful handling. Registry and deployment credentials should be stored in protected Jenkins credentials or an approved secrets manager. Least-privilege permissions should limit what the pipeline can change. Secrets must not be committed to the repository or printed in logs.

I learned that a security tool being mentioned in documentation is not equivalent to an operational control. A control should be considered implemented only when its configuration, execution, result, and failure behavior can be demonstrated. For future development, I would add the missing scanners incrementally, validate their output using controlled test cases, and preserve evidence of both passing and blocked releases.

## 4. How would you measure the effectiveness and reliability of the pipeline?

Pipeline reliability should be measured with a combination of delivery, security, deployment, and application-health metrics. Four important delivery metrics are deployment frequency, lead time for changes, change failure rate, and mean time to recovery.

Deployment frequency measures how often production deployments occur. Lead time measures the time between a relevant code change and its production deployment. Change failure rate measures the proportion of production changes that cause a failure requiring remediation, rollback, or a hotfix. Mean time to recovery measures the time needed to restore service after an incident. These metrics are meaningful only when their definitions and reporting windows are consistent.

NovaPay already provides some useful evidence through Jenkins build history, pipeline stage results, deployment logs, and rollback records. These sources can support initial manual calculations. However, the project does not yet demonstrate a fully automated DORA dashboard or complete incident correlation.

Additional pipeline metrics should include total pipeline duration, individual stage duration, scan findings by severity, integration-test failures, health-check failures, and rollback duration. Application monitoring should track availability, latency, HTTP error rates, resource utilization, and meaningful synthetic transactions.

I would use Grafana to present these metrics once reliable data collection is available. Every dashboard panel should identify its source, time window, and calculation method. Deliberately injected failures, such as the NovaPay rollback test, should be classified separately so they do not distort normal production change-failure reporting.

The key lesson is that collecting numbers is not enough. Metrics need accurate event data and agreed definitions. I would first automate collection of deployment timestamps, commit identifiers, outcomes, and incident recovery times, then validate the calculations against known build and rollback records before using the dashboard for decisions.

## 5. What would you improve if you continued the NovaPay project?

My next priority would be to close the gap between the current working deployment workflow and the assessment's broader target architecture. NovaPay already demonstrates container builds, Trivy scanning, ECR publication, deployment to an inactive slot, health checks, integration checks, blue-green traffic switching, and a tested rollback path. Several advanced controls remain documented strategies rather than verified automated capabilities.

First, I would add missing security checks in a controlled sequence. Static analysis, dependency scanning, software bill of materials generation, licence validation, dynamic testing, and infrastructure scanning should each have explicit policies and test evidence. I would then add policy-as-code checks and an auditable exception workflow.

Second, I would build isolated Development, Staging, Pre-production, and Production environments. Releases should promote the same immutable image digest wherever possible, with environment-specific configuration and approval requirements. This would reduce the risk of different artifacts being tested and released.

Third, I would extend deployment verification. Canary routing should be combined with reliable telemetry and explicit error-rate and latency thresholds. Automated rollback should be triggered only when validated conditions are met. I would also test database expand-contract migrations, because application rollback alone cannot guarantee data recovery.

Finally, I would improve observability, evidence, and operational readiness. I would automate DORA metric collection, create dashboards, test runbooks, and retain reproducible test results and screenshots. I would validate configuration files and documentation links and ensure repository protection settings meet the assessment requirements.

This project taught me to distinguish a working demonstration from a complete production-grade platform. My goal would be to improve the implementation and prove each new control with reproducible evidence rather than claiming completion based only on documentation.
