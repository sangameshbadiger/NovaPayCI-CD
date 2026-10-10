# NovaPay Blue-Green Test Results

## 1. Purpose

This report records the results supported by the existing blue-green deployment evidence files. It does not replace Jenkins console logs or claim tests that are not evidenced.

## 2. Evidence Sources

- `evidence/blue-green-build-27.txt`
- `evidence/blue-green-rollback-test.txt`
- Jenkins Build #31 console log, which should be retained separately if available.

## 3. Recorded Results

| Check | Recorded observation | Assessment |
|---|---|---|
| Active upstream — Build 27 evidence | Nginx upstream points to `127.0.0.1:8082` | Recorded |
| Production HTTP response — Build 27 evidence | HTTP 200 | Passed for the recorded check |
| Application identity | NovaPay Digital Bank, version 1.2 | Recorded |
| Container state — Build 27 evidence | Blue and green containers shown as running | Recorded |
| Rollback evidence file | Green upstream on port 8082 and HTTP 200 | Passed for the recorded check |
| Full rollback execution details | The rollback evidence file ends with a truncated container listing | Incomplete in this file |
| Jenkins Build #31 forced rollback test | Previously recorded project notes report forced verification failure followed by successful rollback verification | Refer to the actual Jenkins console log for complete audit evidence |

## 4. Interpretation

The supplied records support that the application returned HTTP 200 while Nginx routed traffic to the green slot. They also provide evidence of both blue and green containers running in the Build 27 record.

These files alone do not prove every stage of the pipeline, all integration-test assertions, automated metric-based rollback, or recovery from every possible failure.

The rollback-test file is incomplete at the end. Its missing content should not be reconstructed or represented as original test output.

## 5. Recommended Additional Evidence

- Save the complete Jenkins Build #31 console log.
- Capture the Jenkins stage view and rollback verification output.
- Capture the live NovaPay page and the active Nginx upstream.
- Record test date, build number, source commit, outcome, and any limitations for each artifact.
