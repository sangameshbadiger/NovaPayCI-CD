#!/usr/bin/env python3
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
POLICY_PATH = BASE / "policies/licenses/license-policy.json"
APPROVAL_PATH = BASE / "policies/licenses/approved-exceptions.json"
DEFAULT_REPORT = BASE / "evidence/test-results/licenses/license-scan.json"
NOTICE_TRACKING_PATH = BASE / "policies/licenses/notice-tracking.json"
ALIAS_PATH = BASE / "policies/licenses/license-aliases.json"

def load_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path}: {exc}") from exc


def valid_approval(item, approvals, today):
    """Require exact package/version/license match and valid approval metadata."""
    version = item.get("version")
    if not version:
        return False

    for approval in approvals:
        if not isinstance(approval, dict):
            continue

        if (
            approval.get("package") != item.get("package")
            or approval.get("version") != version
            or approval.get("license") != item.get("license")
        ):
            continue

        approver = approval.get("approver")
        reason = approval.get("reason")
        expiry = approval.get("expiry")

        if not all(isinstance(x, str) and x.strip()
                   for x in (approver, reason, expiry)):
            continue

        try:
            expiry_date = date.fromisoformat(expiry)
        except ValueError:
            continue

        if expiry_date >= today:
            return True

    return False
def valid_notice_tracking(finding, entries):
    """Require a matching verified notice record with an existing evidence file."""
    matches = [
        entry for entry in entries
        if isinstance(entry, dict)
        and entry.get("package") == finding.get("package")
        and entry.get("version") == finding.get("version")
        and entry.get("license") == finding.get("license")
    ]

    if len(matches) != 1:
        return False

    entry = matches[0]
    if entry.get("status") != "VERIFIED":
        return False

    evidence = entry.get("evidence")
    if not isinstance(evidence, str) or not evidence.strip():
        return False

    evidence_path = Path(evidence)
    if not evidence_path.is_absolute():
        evidence_path = BASE / evidence_path

    try:
        evidence_path.resolve().relative_to(BASE.resolve())
    except ValueError:
        return False

    return evidence_path.is_file()

def main():
    args = [arg for arg in sys.argv[1:] if arg != "--enforce"]
    report_path = Path(args[0]).resolve() if args else DEFAULT_REPORT

    try:
        policy = load_json(POLICY_PATH)
        report = load_json(report_path)
        register = load_json(APPROVAL_PATH)
        tracking = load_json(NOTICE_TRACKING_PATH)
        alias_config = load_json(ALIAS_PATH)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2

    if not isinstance(register, dict) or not isinstance(
        register.get("exceptions"), list
    ):
        print("ERROR: Invalid approval register schema.")
        return 2

    approvals = register["exceptions"]
    if (
        not isinstance(tracking, dict)
        or not isinstance(tracking.get("entries"), list)
    ):
        print("ERROR: Invalid notice tracking schema.")
        return 2

    notice_entries = tracking["entries"]
    if (
        not isinstance(alias_config, dict)
        or not isinstance(alias_config.get("aliases"), dict)
        or not isinstance(alias_config.get("requires_manual_review"), list)
    ):
        print("ERROR: Invalid license alias configuration.")
        return 2

    aliases = alias_config["aliases"]
    manual_review = set(alias_config["requires_manual_review"])
    rules = policy.get("rules", {})
    today = date.today()
    categories = Counter()
    actions = Counter()
    unresolved = []

    for result in report.get("Results", []):
        for item in result.get("Licenses", []):
            package = item.get("PkgName") or "unknown"
            raw_license_name = item.get("Name") or "UNKNOWN"
            license_name = aliases.get(raw_license_name, raw_license_name)
            category = (item.get("Category") or "unknown").lower()
            severity = (item.get("Severity") or "UNKNOWN").upper()
            action = rules.get(
                category, policy.get("default_action", "REVIEW_REQUIRED")
            )

            # An alias only normalizes a label; it never grants approval.
            # Identifiers requiring manual review cannot be auto-approved.
            if raw_license_name in manual_review:
                action = "REVIEW_REQUIRED"

            categories[category] += 1

            # Trivy may place OS package metadata and license findings
            # in separate Results entries. Match across all Results.
            versions = {
                pkg.get("Version")
                for package_result in report.get("Results", [])
                for pkg in package_result.get("Packages", [])
                if pkg.get("Name") == package
                and license_name in (pkg.get("Licenses") or [])
                and pkg.get("Version")
            }
            version = next(iter(versions)) if len(versions) == 1 else None
            finding = {
                "package": package,
                "version": version,
                "license": license_name,
                "category": category,
                "severity": severity,
                "action": action,
            }

            if action in {"BLOCK_UNLESS_APPROVED", "REVIEW_REQUIRED"}:
                if not valid_approval(finding, approvals, today):
                    unresolved.append(finding)
                    actions[action] += 1
                else:
                    actions["APPROVED_EXCEPTION"] += 1

            elif action == "ALLOW_AFTER_VERIFICATION":
                # Do not silently treat unverified packages as approved.
                unresolved.append(finding)
                actions["ALLOW_AFTER_VERIFICATION"] += 1
            elif action == "NOTICE_TRACKING_REQUIRED":
                artifact = report.get("ArtifactName")
                tracking_artifact = tracking.get("report")

                if not artifact or tracking_artifact != artifact:
                    unresolved.append(finding)
                    actions[action] += 1
                elif not valid_notice_tracking(finding, notice_entries):
                    unresolved.append(finding)
                    actions[action] += 1
                else:
                    actions[action] += 1
            else:
                actions[action] += 1


    print(f"Policy version: {policy.get('policy_version', 'unspecified')}")
    print(f"Report: {report_path}")
    print(f"Total license findings: {sum(categories.values())}")
    print("\nCategories:")
    for key, value in sorted(categories.items()):
        print(f"  {key}: {value}")

    print("\nRequired actions:")
    for key, value in sorted(actions.items()):
        print(f"  {key}: {value}")

    print("\nSample unresolved findings:")
    for item in unresolved[:20]:
        print(
            f"  [{item['action']}] {item['package']} "
            f"version={item['version'] or 'MISSING'} | "
            f"{item['license']} | {item['category']} | {item['severity']}"
        )

    print(
        "\nAUDIT NOTE: This is a policy evaluation summary, not a legal determination."
    )

    if "--enforce" in sys.argv[1:]:
        if unresolved:
            print(
                f"POLICY GATE FAILED: {len(unresolved)} finding(s) "
                "remain unresolved or unverified."
            )
            return 1
        print("POLICY GATE PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
