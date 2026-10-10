# 5. Integration and Contract Testing

## Purpose
Verify the candidate application responds correctly before traffic changes.

## Checks and controls
Implemented HTTP status, application title, and version-marker checks against the target slot. Consumer-driven contract tests are not confirmed.

## Failure handling
Block traffic switching when target checks fail.

## Evidence
Integration Tests stage log showing HTTP 200 and successful assertions.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
