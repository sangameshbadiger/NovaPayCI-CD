import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHECKER = ROOT / "policies/licenses/check_license_policy.py"


class LicensePolicyTests(unittest.TestCase):
    def run_checker(self, report, exceptions=None):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            report_path = temp / "report.json"
            report_path.write_text(json.dumps(report))

            # Checker reads the repository approval register, so preserve it.
            approval_path = ROOT / "policies/licenses/approved-exceptions.json"
            original = approval_path.read_text()
            try:
                approval_path.write_text(json.dumps({
                    "schema_version": "1.0",
                    "exceptions": exceptions or [],
                }))
                return subprocess.run(
                    [sys.executable, str(CHECKER), str(report_path), "--enforce"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
            finally:
                approval_path.write_text(original)

    def report(self, category="restricted", version="1.2.3"):
        return {
            "ArtifactName": "test-image",
            "Results": [
                {
                    "Target": "test-image",
                    "Packages": [{
                        "Name": "test-package",
                        "Version": version,
                        "Licenses": ["GPL-2.0-only"],
                    }],
                },
                {
                    "Target": "OS Packages",
                    "Licenses": [{
                        "PkgName": "test-package",
                        "Name": "GPL-2.0-only",
                        "Category": category,
                        "Severity": "HIGH",
                    }],
                },
            ]
        }

    def approval(self, **overrides):
        item = {
            "package": "test-package",
            "version": "1.2.3",
            "license": "GPL-2.0-only",
            "approver": "reviewer@example.com",
            "reason": "Documented legal review reference LEG-123",
            "expiry": (date.today() + timedelta(days=30)).isoformat(),
        }
        item.update(overrides)
        return item

    def test_restricted_without_approval_fails(self):
        result = self.run_checker(self.report())
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("POLICY GATE FAILED", result.stdout)

    def test_valid_approval_is_accepted(self):
        result = self.run_checker(
            self.report(), [self.approval()]
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("POLICY GATE PASSED", result.stdout)

    def test_expired_approval_fails(self):
        expired = (date.today() - timedelta(days=1)).isoformat()
        result = self.run_checker(
            self.report(), [self.approval(expiry=expired)]
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_missing_reason_fails(self):
        result = self.run_checker(
            self.report(), [self.approval(reason="")]
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_version_mismatch_fails(self):
        result = self.run_checker(
            self.report(), [self.approval(version="9.9.9")]
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_unknown_finding_fails_without_approval(self):
        result = self.run_checker(self.report(category="unknown"))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)


    def test_pending_notice_tracking_fails(self):
        result = self.run_checker(self.report(category="notice"))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("NOTICE_TRACKING_REQUIRED", result.stdout)
        self.assertIn("POLICY GATE FAILED", result.stdout)


    def test_manual_review_license_is_not_auto_approved(self):
        result = self.run_checker(self.report(category="unknown"))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("REVIEW_REQUIRED", result.stdout)
        self.assertIn("POLICY GATE FAILED", result.stdout)

    def test_ambiguous_license_names_require_manual_review(self):
        aliases_path = ROOT / "policies/licenses/license-aliases.json"
        config = json.loads(aliases_path.read_text())
        manual = set(config["requires_manual_review"])
        self.assertTrue(
            {"custom", "GD", "IJG", "Beerware"} <= manual
        )

if __name__ == "__main__":
    unittest.main()
