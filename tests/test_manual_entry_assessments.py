"""Regression guards for reference-only catalog entries and release caveats."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ManualEntryAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        cls.tools = {tool["id"]: tool for tool in cls.catalog["tools"]}
        cls.guide = (ROOT / "wiki" / "Using-web-app-testing.md").read_text(encoding="utf-8")
        cls.compatibility = (ROOT / "wiki" / "Compatibility-and-Verification.md").read_text(encoding="utf-8")
        cls.release = (ROOT / "wiki" / "Release-Readiness.md").read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_burp_suite_stays_manual_and_not_installable(self):
        tool = self.tools["burp-suite"]
        self.assertEqual(tool["install_kind"], "manual")
        self.assertIs(tool["installable"], False)
        self.assertIn("not listed as a supported operating system", self.guide)
        self.assertIn("portswigger.net/burp/documentation/desktop/getting-started/system-requirements", self.guide)

    def test_wappalyzer_stays_manual_and_not_installable(self):
        tool = self.tools["wappalyzer"]
        self.assertEqual(tool["install_kind"], "manual")
        self.assertIs(tool["installable"], False)
        self.assertIn("public npm `wappalyzer` package is deprecated", self.guide)
        self.assertIn("HTTP Archive repository", self.guide)
        self.assertIn("npmjs.com/package/wappalyzer", self.guide)

    def test_unassessed_entries_and_external_staging_gate_are_documented(self):
        self.assertIn("Two entries are intentionally reference-only", self.compatibility)
        self.assertIn("blocked / not run", self.compatibility)
        self.assertIn("Release-Readiness.md", self.readme)
        self.assertIn("External HTTPS staging adapter", self.release)
        self.assertIn("No authorized staging endpoint was supplied", self.release)


if __name__ == "__main__":
    unittest.main()
