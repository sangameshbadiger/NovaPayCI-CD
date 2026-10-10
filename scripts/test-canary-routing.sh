#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:18088/}"
REQUESTS="${2:-100}"
LOG="/tmp/novapay-canary-access.log"

if ! [[ "$REQUESTS" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: REQUESTS must be a positive integer."
  exit 1
fi

if [[ ! -f "$LOG" ]]; then
  echo "ERROR: Canary access log not found: $LOG"
  echo "Start the temporary Nginx canary proxy with access logging first."
  exit 1
fi

: > "$LOG"

for i in $(seq 1 "$REQUESTS"); do
  curl -fsS -o /dev/null "$URL"
done

STABLE=$(grep -c '^127\.0\.0\.1:8081$' "$LOG" || true)
CANARY=$(grep -c '^127\.0\.0\.1:8082$' "$LOG" || true)
TOTAL=$((STABLE + CANARY))

echo "Requests requested: $REQUESTS"
echo "Stable backend (8081): $STABLE"
echo "Canary backend (8082): $CANARY"
echo "Logged upstream requests: $TOTAL"

if [[ "$TOTAL" -ne "$REQUESTS" ]]; then
  echo "FAIL: Some requests were not logged to the expected backends."
  exit 1
fi

echo "PASS: All requests reached an expected backend."
