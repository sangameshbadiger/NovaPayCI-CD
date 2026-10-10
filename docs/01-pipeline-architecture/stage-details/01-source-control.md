# 1. Source Control and Trigger

## Purpose
Retrieve the intended NovaPay source revision from GitHub.

## Checks and controls
Verify the checked-out commit and branch; review changes before release.

## Failure handling
Stop the pipeline if checkout fails or the intended revision cannot be retrieved.

## Evidence
Jenkins checkout log and Git commit history.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
