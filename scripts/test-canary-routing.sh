#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:18088/}"
REQUESTS="${2:-100}"

for i in $(seq 1 "$REQUESTS"); do
  curl -fsS -o /dev/null "$URL"
done

echo "Canary routing test completed."
echo "Requests sent: $REQUESTS"
echo "Check the Nginx access log for backend distribution."
