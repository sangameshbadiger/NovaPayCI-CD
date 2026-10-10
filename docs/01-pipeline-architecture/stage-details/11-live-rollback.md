# 11. Live Verification and Rollback

## Purpose
Validate the production endpoint after switching traffic.

## Checks and controls
Check HTTP availability and the application version marker; the optional TEST_ROLLBACK mode deliberately forces verification failure.

## Failure handling
Attempt to switch back to the previous slot and verify recovery; report the release as failed when the test or deployment fails.

## Evidence
Build #31 log: forced verification failure, switch to green port 8082, and 'Rollback verification passed'.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
