#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

policy_path = Path("policies/licenses/license-policy.json")
report_path = Path(
    sys.argv[1] if len(sys.argv) > 1
    else "evidence/test-results/licenses/license-scan.json"
)

try:
    policy = json.loads(policy_path.read_text())
    report = json.loads(report_path.read_text())
except (OSError, json.JSONDecodeError) as exc:
    print(f"ERROR: Cannot load policy or report: {exc}")
    sys.exit(2)

rules = policy.get("rules", {})
counts = Counter()
actions = Counter()
review_items = []

for result in report.get("Results", []):
    for item in result.get("Licenses", []):
        name = item.get("Name") or "UNKNOWN"
        category = (item.get("Category") or "unknown").lower()
        severity = (item.get("Severity") or "UNKNOWN").upper()
        action = rules.get(category, policy.get("default_action", "REVIEW_REQUIRED"))

        counts[category] += 1
        actions[action] += 1

        if action in {
            "BLOCK_UNLESS_APPROVED",
            "REVIEW_REQUIRED",
            "ALLOW_AFTER_VERIFICATION",
        }:
            review_items.append({
                "package": item.get("PkgName", "unknown"),
                "license": name,
                "category": category,
                "severity": severity,
                "action": action,
            })

print(f"Policy version: {policy.get('policy_version', 'unspecified')}")
print(f"Report: {report_path}")
print(f"Total license findings: {sum(counts.values())}")
print("\nCategories:")
for key, value in sorted(counts.items()):
    print(f"  {key}: {value}")

print("\nRequired actions:")
for key, value in sorted(actions.items()):
    print(f"  {key}: {value}")

print("\nSample findings requiring review or verification:")
for item in review_items[:15]:
    print(
        f"  [{item['action']}] {item['package']} | "
        f"{item['license']} | {item['category']} | {item['severity']}"
    )

print("\nAUDIT NOTE: This is a policy evaluation summary, not a legal determination.")
print("No release-blocking decision has been made; approved exceptions are not yet implemented.")
