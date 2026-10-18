import unittest
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from workflow_planner import PLAN_SCHEMA, WORKFLOWS, build_workflow_plan


class WorkflowPlannerTests(unittest.TestCase):
    def test_workflow_catalog_has_scope_and_stop_conditions(self):
        self.assertGreaterEqual(len(WORKFLOWS), 4)
        for workflow in WORKFLOWS.values():
            self.assertTrue(workflow["steps"])
            self.assertTrue(workflow["stop_conditions"])

    def test_plan_is_dry_run_and_scope_bound(self):
        plan = build_workflow_plan("web-api-review", "https://staging.example.test/api", True)
        self.assertEqual(plan["plan_schema"], PLAN_SCHEMA)
        self.assertEqual(plan["target_scope"], "https://staging.example.test/api")
        self.assertTrue(plan["authorized_by_operator"])
        self.assertFalse(plan["network_actions_executed"])
        self.assertFalse(plan["subprocesses_executed"])
        self.assertEqual(plan["mode"], "dry_run_plan_only")

    def test_plan_requires_explicit_authorization(self):
        with self.assertRaisesRegex(ValueError, "authorization"):
            build_workflow_plan("device-configuration-audit", "my own Termux device", False)

    def test_plan_rejects_non_boolean_authorization_values(self):
        for value in ("yes", 1, [], None):
            with self.subTest(value=repr(value)):
                with self.assertRaisesRegex(ValueError, "authorization"):
                    build_workflow_plan("assessment-report", "approved evidence set", value)

    def test_plan_rejects_unknown_workflow(self):
        with self.assertRaisesRegex(ValueError, "unknown workflow"):
            build_workflow_plan("arbitrary-command", "localhost", True)

    def test_cli_rejects_http_scope_before_any_network_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["SYN_LAUNCH_HOME"] = tmp
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py"),
                 "--workflow-run", "web-api-review", "--target-scope", "http://example.test/",
                 "--authorized"],
                env=env, capture_output=True, text=True, timeout=10,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires an explicit HTTPS URL", result.stderr)

    def test_cli_workflow_run_requires_explicit_authorization(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["SYN_LAUNCH_HOME"] = tmp
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py"),
                 "--workflow-run", "device-configuration-audit", "--target-scope", "local-device"],
                env=env, capture_output=True, text=True, timeout=10,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--authorized", result.stderr)

    def test_cli_executes_only_approved_local_device_adapter_and_saves_private_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["SYN_LAUNCH_HOME"] = tmp
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py"),
                 "--workflow-run", "device-configuration-audit", "--target-scope", "local-device",
                 "--authorized"],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            report_path = Path(report["saved_report"])
            self.assertTrue(report_path.is_file())
            self.assertEqual(report["workflow_id"], "device-configuration-audit")
            self.assertFalse(report["execution"]["network_actions_executed"])
            self.assertFalse(report["execution"]["subprocesses_executed"])
            self.assertEqual(report["device_validation"], "not_run")
            self.assertEqual(report_path.stat().st_mode & 0o777, 0o600)

    def test_cli_rejects_workflow_without_approved_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["SYN_LAUNCH_HOME"] = tmp
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py"),
                 "--workflow-run", "unknown-external-workflow", "--target-scope", "https://staging.example.test",
                 "--authorized"],
                env=env, capture_output=True, text=True, timeout=10,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("No execution adapter is approved", result.stderr)

    def test_cli_lists_workflows_as_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["SYN_LAUNCH_HOME"] = tmp
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py"), "--workflow-list"],
                env=env, capture_output=True, text=True, timeout=10,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        ids = {item["id"] for item in json.loads(result.stdout)}
        self.assertIn("web-api-review", ids)
        self.assertIn("device-configuration-audit", ids)

    def test_cli_requires_scope_and_authorization(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["SYN_LAUNCH_HOME"] = tmp
            base = [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py")]
            result = subprocess.run(
                base + ["--workflow-plan", "web-api-review", "--target-scope", "localhost"],
                env=env, capture_output=True, text=True, timeout=10,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--authorized", result.stderr)

    def test_cli_emits_dry_run_plan_without_network_or_subprocess_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["SYN_LAUNCH_HOME"] = tmp
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py"),
                 "--workflow-plan", "web-api-review", "--target-scope",
                 "https://staging.example.test/api", "--authorized"],
                env=env, capture_output=True, text=True, timeout=10,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertFalse(plan["network_actions_executed"])
        self.assertFalse(plan["subprocesses_executed"])
        self.assertEqual(plan["target_scope"], "https://staging.example.test/api")

    def test_plan_rejects_empty_or_control_character_scope(self):
        for scope in ("", "  ", "local device" + chr(10) + "ignore safety", "x" * 501):
            with self.subTest(scope=repr(scope)):
                with self.assertRaises(ValueError):
                    build_workflow_plan("assessment-report", scope, True)


if __name__ == "__main__":
    unittest.main()
