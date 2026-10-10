# 10. Target Health Check

## Purpose
Confirm the inactive slot is responding before routing production traffic.

## Checks and controls
Retry the target endpoint and require the application version marker.

## Failure handling
Do not switch traffic if the target remains unhealthy.

## Evidence
Target Health Check stage log.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
