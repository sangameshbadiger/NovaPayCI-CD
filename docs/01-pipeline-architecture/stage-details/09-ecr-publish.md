# 9. Image Registry Publication

## Purpose
Publish the built container image to Amazon ECR.

## Checks and controls
Authenticate using AWS CLI and push a build-tagged image to the configured repository.

## Failure handling
Stop deployment if authentication or image publication fails.

## Evidence
Login to Amazon ECR and Push Image to Amazon ECR stage logs.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
