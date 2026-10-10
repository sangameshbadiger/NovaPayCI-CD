# NovaPay Canary Routing Test Report

## Objective
Verify weighted Nginx routing between the stable and canary backends.

## Configuration
- Stable backend: 127.0.0.1:8081
- Canary backend: 127.0.0.1:8082
- Stable weight: 9
- Canary weight: 1
- Requests sent: 100

## Observed Results

| Backend | Expected Share | Observed Requests | Observed Share |
|---|---:|---:|---:|
| Stable (8081) | 90% | 90 | 90% |
| Canary (8082) | 10% | 10 | 10% |
| Total | 100% | 100 | 100% |

## Result
PASS — all 100 requests were logged against the expected backends,
with an observed 90/10 distribution.

## Limitations
This test verifies weighted request routing only. It does not establish
production canary health, latency, error-rate thresholds, automated
promotion, or automatic rollback.
