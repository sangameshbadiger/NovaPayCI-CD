# NovaPay Digital Bank — CI/CD Pipeline Architecture

## 1. Purpose

This project demonstrates automated container build, security scanning,
deployment, verification, and rollback using Jenkins, Docker, Amazon ECR,
EC2, and Nginx.

## 2. Implemented Pipeline Stages

1. Checkout source code.
2. Build a versioned Docker image.
3. Scan the image with Trivy for HIGH and CRITICAL vulnerabilities.
4. Authenticate to Amazon ECR.
5. Push the image to Amazon ECR.
6. Identify the active and inactive deployment slots.
7. Deploy the image to the inactive slot.
8. Run the target health check.
9. Run HTTP integration tests.
10. Switch Nginx traffic to the target slot.
11. Verify the live application and attempt rollback on failure.

## 3. Architecture Components

- Source control: GitHub.
- Pipeline orchestration: Jenkins, job NovaPay-CI.
- Containerization: Docker.
- Image scanning: Trivy.
- Registry: Amazon ECR, region ap-south-1.
- Runtime: Docker on an EC2 host.
- Routing: Nginx.
- Blue-green slots: ports 8081 and 8082.
- Demo application: Nginx-based NovaPay web page.

## 4. Deployment Workflow

Jenkins checks out the repository, builds and scans the image, pushes it to
ECR, and deploys it to the inactive slot. The pipeline checks target health
and runs integration tests before switching Nginx traffic. It then verifies
the live endpoint. If live verification fails, the rollback handler attempts
to restore the previously active slot and verifies recovery.

## 5. Verified Rollback Evidence

Jenkins Build #31 deliberately forced live verification to fail after traffic
switched to blue on port 8081. The rollback handler switched traffic back to
green on port 8082. The log reported "Rollback verification passed".
A subsequent manual check confirmed port 8082 was active and HTTP returned
status 200.

Build #31 finished with FAILURE intentionally because the test simulated an
unsuccessful release. The rollback itself succeeded.

## 6. Current Security Checks

The pipeline runs Trivy image scanning and blocks the build when HIGH or
CRITICAL findings are reported. Target health checks, integration tests, and
live verification are also implemented.

Do not consider SAST, DAST, licence enforcement, SBOM generation, or Kubernetes
policy enforcement implemented until configuration and execution evidence
are available.

## 7. Limitations and Planned Work

- The current demonstration uses Docker on EC2, not a complete banking
  production platform.
- Automated canary analysis and metric-based promotion are not yet verified.
- Database expand-contract migration automation is not yet verified.
- Comprehensive compliance gates and DORA dashboards require further work.
- A successful demonstration does not establish regulatory compliance or
  five-nines availability.

## 8. Evidence References

- evidence/blue-green-build-27.txt
- evidence/blue-green-rollback-test.txt
- docs/canary-test-report.md

Additional test results and screenshots should be recorded as capabilities
are implemented and verified.
