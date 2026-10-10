# 2. Build and Container Image

## Purpose
Build a versioned Docker image for the application.

## Checks and controls
Require a successful Docker build and use a traceable image tag.

## Failure handling
Fail the pipeline if the image cannot be built.

## Evidence
Build Docker Image stage and image tag in Jenkins logs.

## Current status
This stage is documented for the NovaPay demonstration. Claims of successful
execution must be supported by the corresponding Jenkins console log or test
artifact. Planned controls must not be represented as implemented.
