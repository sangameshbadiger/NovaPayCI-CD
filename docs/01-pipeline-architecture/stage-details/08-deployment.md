# 8. Deployment and Verification

## Purpose
Deploy to the inactive blue-green slot and validate the candidate.

## Checks and controls
Implemented: inactive-slot selection, Docker deployment, health check, integration checks, Nginx traffic switch, and live verification.

## Failure handling
On live verification failure, attempt to restore the previous slot and verify recovery.

## Evidence
Jenkins Build #27 and Build #31 logs; rollback verification passed in Build #31.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
