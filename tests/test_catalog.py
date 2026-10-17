import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("syn_launch_main", ROOT / "main.py")
APP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(APP)

class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        cls.tools = cls.data["tools"]

    def test_catalog_is_large_and_metadata_count_matches(self):
        self.assertGreaterEqual(len(self.tools), 200)
        self.assertEqual(self.data["tool_count"], len(self.tools))

    def test_unique_ids_and_required_fields(self):
        ids = [t["id"] for t in self.tools]
        self.assertEqual(len(ids), len(set(ids)))
        for t in self.tools:
            for field in ("id", "name", "category", "executable", "install_kind", "description", "source", "caveat"):
                self.assertTrue(t.get(field), f"{t.get('name')} missing {field}")

    def test_categories_match(self):
        self.assertEqual(set(self.data["categories"]), {t["category"] for t in self.tools})

    def test_install_methods_and_flags(self):
        allowed = {"pkg", "pip", "go", "cargo", "npm", "manual", "root"}
        for t in self.tools:
            self.assertIn(t["install_kind"], allowed, t["name"])
            self.assertEqual(t["installable"], t["install_kind"] in {"pkg", "pip", "go", "cargo", "npm"}, t["name"])

    def test_sources_are_https(self):
        for t in self.tools:
            self.assertTrue(t["source"].startswith("https://"), t["name"])

    def test_catalog_rejects_duplicate_ids(self):
        broken = copy.deepcopy(self.data)
        broken["tools"].append(copy.deepcopy(broken["tools"][0]))
        broken["tool_count"] += 1
        with self.assertRaisesRegex(ValueError, "duplicate id"):
            APP.validate_catalog(broken)

    def test_catalog_rejects_shell_metacharacters_in_package(self):
        broken = copy.deepcopy(self.data)
        tool = next(t for t in broken["tools"] if t["install_kind"] == "pkg")
        tool["package"] = "nmap;touch /tmp/should-not-run"
        with self.assertRaisesRegex(ValueError, "unsafe package/module syntax"):
            APP.validate_catalog(broken)

    def test_catalog_rejects_unsafe_package_syntax(self):
        broken = copy.deepcopy(self.data)
        tool = next(t for t in broken["tools"] if t["install_kind"] == "pkg")
        tool["package"] = "nmap;touch /tmp/should-not-run"
        with self.assertRaisesRegex(ValueError, "unsafe package/module syntax"):
            APP.validate_catalog(broken)

    def test_catalog_rejects_duplicate_display_names(self):
        broken = copy.deepcopy(self.data)
        duplicate = copy.deepcopy(broken["tools"][0])
        duplicate["id"] = "different-id"
        broken["tools"].append(duplicate)
        broken["tool_count"] += 1
        with self.assertRaisesRegex(ValueError, "duplicate display name"):
            APP.validate_catalog(broken)

    def test_catalog_rejects_non_https_source(self):
        broken = copy.deepcopy(self.data)
        broken["tools"][0]["source"] = "http://example.com/tool"
        with self.assertRaisesRegex(ValueError, "valid HTTPS URL"):
            APP.validate_catalog(broken)

    def test_catalog_rejects_https_url_with_credentials(self):
        broken = copy.deepcopy(self.data)
        broken["tools"][0]["source"] = "https://trusted.example@evil.example/path"
        with self.assertRaisesRegex(ValueError, "valid HTTPS URL"):
            APP.validate_catalog(broken)

    def test_catalog_rejects_invalid_executable_name(self):
        broken = copy.deepcopy(self.data)
        broken["tools"][0]["executable"] = "python;touch"
        with self.assertRaisesRegex(ValueError, "invalid executable name"):
            APP.validate_catalog(broken)

    def test_catalog_requires_boolean_installable_flag(self):
        broken = copy.deepcopy(self.data)
        broken["tools"][0]["installable"] = "true"
        with self.assertRaisesRegex(ValueError, "installable flag mismatch"):
            APP.validate_catalog(broken)

    def test_show_tool_does_not_execute_local_binary(self):
        import contextlib
        import io
        original_installed = APP.installed
        original_docs = APP.show_local_docs
        called = []
        try:
            APP.installed = lambda tool: True
            APP.show_local_docs = lambda tool: called.append(tool["id"])
            with contextlib.redirect_stdout(io.StringIO()):
                APP.show_tool(self.tools[0])
            self.assertEqual(called, [])
        finally:
            APP.installed = original_installed
            APP.show_local_docs = original_docs

    def test_bootstrap_pins_remote_and_disables_hooks(self):
        script = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn('ORIGIN" != "https://github.com/LILSYNNOFFICIAL/syn_launch.git"', script)
        self.assertIn('BRANCH" != "main"', script)
        self.assertIn('git -C "$BASE" -c core.hooksPath=/dev/null fetch --no-tags origin main', script)
        self.assertIn('git -c core.hooksPath=/dev/null clone --branch main --single-branch', script)
        self.assertIn('git -C "$BASE" diff --quiet', script)

    def test_bootstrap_uses_isolated_official_pypi(self):
        script = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn('--isolated --disable-pip-version-check --index-url https://pypi.org/simple', script)
        self.assertIn('unset PYTHONPATH PYTHONHOME PYTHONSTARTUP', script)

    def test_package_manager_environment_overrides_are_removed(self):
        from unittest.mock import patch
        with patch.dict("os.environ", {
            "PIP_INDEX_URL": "https://attacker.invalid/simple",
            "PIP_TRUSTED_HOST": "attacker.invalid",
            "GOPROXY": "https://attacker.invalid",
            "npm_config_registry": "https://attacker.invalid",
            "PYTHONPATH": "/tmp/untrusted",
        }):
            child = APP.build_child_env()
        for key in ("PIP_INDEX_URL", "PIP_TRUSTED_HOST", "GOPROXY", "npm_config_registry", "PYTHONPATH"):
            self.assertNotIn(key, child)

    def test_bounded_probe_caps_output(self):
        output, truncated, timed_out = APP.bounded_probe(
            [sys.executable, "-c", "print('A' * 5000)"], timeout=5, max_bytes=1024
        )
        self.assertTrue(truncated)
        self.assertFalse(timed_out)
        self.assertLessEqual(len(output.encode("utf-8")), 1024)
        self.assertEqual(output, "A" * 1024)

    def test_check_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "main.py"), "--check"], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Catalog:", result.stdout)



    def test_custom_tools_are_merged_and_private_json_round_trips(self):
        import tempfile
        original = APP.CUSTOM_PATH
        try:
            with tempfile.TemporaryDirectory() as tmp:
                APP.CUSTOM_PATH = Path(tmp) / "custom_tools.json"
                tool = {
                    "id": "my-lab-tool", "name": "My Lab Tool", "category": "Custom Tools",
                    "executable": "my-lab-tool", "install_kind": "manual", "package": None,
                    "installable": False, "description": "Local lab utility for my own systems.",
                    "example": "my-lab-tool --help", "source": "https://example.org/project",
                    "caveat": "User-managed entry; verify the upstream source before installing."
                }
                APP.save_private_json(APP.CUSTOM_PATH, [tool])
                self.assertEqual(json.loads(APP.CUSTOM_PATH.read_text(encoding="utf-8")), [tool])
                merged = APP.load_catalog()
                self.assertIn("my-lab-tool", {t["id"] for t in merged["tools"]})
                self.assertIn("Custom Tools", merged["categories"])
        finally:
            APP.CUSTOM_PATH = original



    def test_favorites_persist_and_toggle(self):
        import contextlib
        import io
        import tempfile
        original = APP.FAVORITES_PATH
        try:
            with tempfile.TemporaryDirectory() as tmp:
                APP.FAVORITES_PATH = Path(tmp) / "favorites.json"
                tool = self.tools[0]
                with contextlib.redirect_stdout(io.StringIO()):
                    APP.toggle_favorite(tool)
                self.assertIn(tool["id"], APP.get_favorites())
                with contextlib.redirect_stdout(io.StringIO()):
                    APP.toggle_favorite(tool)
                self.assertNotIn(tool["id"], APP.get_favorites())
        finally:
            APP.FAVORITES_PATH = original

    def test_malformed_custom_catalog_fails_closed(self):
        import tempfile
        original = APP.CUSTOM_PATH
        try:
            with tempfile.TemporaryDirectory() as tmp:
                APP.CUSTOM_PATH = Path(tmp) / "custom_tools.json"
                APP.save_private_json(APP.CUSTOM_PATH, [None])
                with self.assertRaisesRegex(ValueError, "list of tool objects"):
                    APP.load_catalog()
        finally:
            APP.CUSTOM_PATH = original

    def test_subprocess_timeout_terminates_process(self):
        import time
        started = time.monotonic()
        ok = APP.run([sys.executable, "-c", "import time; time.sleep(5)"], "timeout regression test", timeout=0.2)
        self.assertFalse(ok)
        self.assertLess(time.monotonic() - started, 3.0)

    def test_subprocess_arguments_are_not_shell_interpreted(self):
        import contextlib
        import io
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "should-not-exist"
            argument = f"literal;touch {marker}"
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                ok = APP.run([sys.executable, "-c", "import sys; print(sys.argv[1])", argument], "argument safety regression")
            self.assertTrue(ok)
            self.assertIn(argument, output.getvalue())
            self.assertFalse(marker.exists())


    def test_architecture_normalization(self):
        cases = {
            "aarch64": "arm64", "arm64-v8a": "arm64",
            "armv7l": "armv7", "x86_64": "x86_64",
            "amd64": "x86_64", "i686": "x86",
        }
        for machine, expected in cases.items():
            with self.subTest(machine=machine):
                self.assertEqual(APP.normalized_architecture(machine), expected)

    def test_environment_profile_is_structured_and_cautious(self):
        profile = APP.environment_profile({"tools": self.tools, "categories": self.data["categories"]})
        self.assertEqual(profile["application"], "SYN_LAUNCH")
        self.assertEqual(profile["profile_schema"], 1)
        self.assertEqual(profile["catalog_entries"], len(self.tools))
        self.assertIn("not proof", profile["compatibility_note"])
        self.assertIn("runtimes", profile)
        self.assertIn("install_method_counts", profile)

    def test_compatibility_report_never_claims_path_matches_are_verified(self):
        from unittest.mock import patch
        fake = {
            "id": "fake-tool", "name": "Fake Tool", "category": "Test",
            "executable": "fake-tool", "install_kind": "manual", "package": None,
            "caveat": "Test-only entry."
        }
        with patch.object(APP.shutil, "which", side_effect=lambda command: "/test/fake-tool" if command == "fake-tool" else None):
            report = APP.compatibility_report({"tools": [fake], "categories": ["Test"]})
        self.assertEqual(report["report_schema"], 2)
        self.assertEqual(report["summary"]["catalog_entries"], 1)
        self.assertEqual(report["summary"]["catalog_installable_entries"], 0)
        self.assertEqual(report["summary"]["path_match_entries"], 1)
        self.assertEqual(report["summary"]["not_detected_entries"], 0)
        self.assertEqual(report["summary"]["verified_tools"], 0)
        self.assertFalse(report["summary"]["tools_executed_by_report"])
        self.assertEqual(report["tools"][0]["status"], "path_match_unverified")
        self.assertEqual(report["tools"][0]["compatibility_assessment"], "not_assessed")
        self.assertEqual(report["tools"][0]["smoke_test"], "not_run")
        self.assertEqual(report["tools"][0]["device_validation"], "not_run")
        self.assertEqual(report["tools"][0]["verification"], "not_run")

    def test_compatibility_report_cli_outputs_json_for_entire_catalog(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "main.py"), "--compatibility-report"],
            capture_output=True, text=True, timeout=15
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["application"], "SYN_LAUNCH")
        self.assertEqual(report["summary"]["catalog_entries"], self.data["tool_count"])
        self.assertEqual(len(report["tools"]), self.data["tool_count"])
        self.assertEqual(report["report_schema"], 2)
        self.assertEqual(report["summary"]["verified_tools"], 0)
        self.assertFalse(report["summary"]["tools_executed_by_report"])
        self.assertTrue(all(item["verification"] == "not_run" for item in report["tools"]))
        self.assertTrue(all(item["smoke_test"] == "not_run" for item in report["tools"]))
        self.assertTrue(all(item["device_validation"] == "not_run" for item in report["tools"]))

    def test_install_summary_separates_path_detection_from_verification(self):
        import tempfile
        import contextlib
        import io
        from unittest.mock import patch
        original_state = APP.STATE_DIR
        fake_tools = [
            {"id":"first", "name":"First", "install_kind":"pkg", "package":"first", "executable":"first"},
            {"id":"second", "name":"Second", "install_kind":"pkg", "package":"second", "executable":"second"},
        ]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                APP.STATE_DIR = Path(tmp)
                with patch.object(APP, "installed", side_effect=[False, True, False, False]), contextlib.redirect_stdout(io.StringIO()):
                    APP.progress(fake_tools, lambda tool: tool["id"] == "first", "test")
                summary = json.loads((Path(tmp) / "last_install_summary.json").read_text(encoding="utf-8"))
                self.assertEqual(summary["summary_schema"], 2)
                self.assertEqual(summary["operation_success_count"], 1)
                self.assertEqual(summary["path_match_after_attempt_count"], 1)
                self.assertEqual(summary["results"][0]["result_state"], "path_match_unverified_after_attempt")
                self.assertEqual(summary["results"][0]["verification"], "not_run")
                self.assertEqual(summary["results"][1]["result_state"], "operation_failed_or_unavailable")
                self.assertEqual(summary["verified_tools"], 0)
        finally:
            APP.STATE_DIR = original_state

    def test_install_preflight_warns_about_low_storage_and_missing_runtimes(self):
        items = [
            {"id": "one", "name": "One", "install_kind": "go", "package": "example.org/one@v1"},
            {"id": "two", "name": "Two", "install_kind": "npm", "package": "two"},
            {"id": "three", "name": "Three", "install_kind": "go", "package": "example.org/one@v1"},
        ]
        report = APP.build_install_preflight(items, "third_party_builds", 1, {"python"})
        self.assertEqual(report["preflight_schema"], 1)
        self.assertEqual(report["tool_count"], 3)
        self.assertEqual(report["distinct_package_count"], 2)
        self.assertEqual(report["missing_commands"], [
            {"command": "go", "affected_tool_count": 2},
            {"command": "npm", "affected_tool_count": 1},
        ])
        self.assertEqual(report["verification"], "not_run")
        self.assertFalse(report["installers_executed"])
        self.assertTrue(any("below" in warning for warning in report["warnings"]))
        self.assertTrue(any("missing" in warning for warning in report["warnings"]))

    def test_install_preflight_blocks_package_batch_without_pkg(self):
        items = [{"id": "pkg-tool", "name": "Pkg Tool", "install_kind": "pkg", "package": "pkg-tool"}]
        report = APP.build_install_preflight(items, "termux_packages", 4 * 1024**3, set())
        self.assertFalse(report["proceed"])
        self.assertEqual(report["missing_commands"], [{"command": "pkg", "affected_tool_count": 1}])

    def test_install_preflight_handles_unknown_storage_without_claiming_verification(self):
        report = APP.build_install_preflight([], "runtime_prerequisites", None, {"pkg"})
        self.assertEqual(report["free_bytes"], None)
        self.assertTrue(any("could not be measured" in warning for warning in report["warnings"]))
        self.assertEqual(report["verification"], "not_run")
        self.assertFalse(report["installers_executed"])

    def test_run_captures_structured_exit_code_without_changing_boolean_return(self):
        import tempfile
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            old_log_dir = APP.LOG_DIR
            try:
                APP.LOG_DIR = Path(tmp)
                with contextlib.redirect_stdout(io.StringIO()):
                    result = APP.run([sys.executable, "-c", "raise SystemExit(7)"], "nonzero test", timeout=5)
                self.assertFalse(result)
                self.assertEqual(APP.LAST_COMMAND_RESULT["exit_code"], 7)
                self.assertFalse(APP.LAST_COMMAND_RESULT["timed_out"])
                self.assertIsNone(APP.LAST_COMMAND_RESULT["launch_error"])
                self.assertEqual(APP.LAST_COMMAND_RESULT["label"], "nonzero test")
            finally:
                APP.LOG_DIR = old_log_dir

    def test_run_captures_success_exit_code(self):
        import tempfile
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            old_log_dir = APP.LOG_DIR
            try:
                APP.LOG_DIR = Path(tmp)
                with contextlib.redirect_stdout(io.StringIO()):
                    result = APP.run([sys.executable, "-c", "print('ok')"], "success test", timeout=5)
                self.assertTrue(result)
                self.assertEqual(APP.LAST_COMMAND_RESULT["exit_code"], 0)
                self.assertGreater(APP.LAST_COMMAND_RESULT["output_bytes"], 0)
            finally:
                APP.LOG_DIR = old_log_dir

    def test_install_summary_carries_subprocess_evidence(self):
        import tempfile
        import contextlib
        import io
        original_state = APP.STATE_DIR
        fake_tools = [{"id":"first", "name":"First", "install_kind":"pkg", "package":"first", "executable":"first"}]
        command_evidence = {
            "command": ["pkg", "install", "-y", "first"], "label": "Installing First",
            "exit_code": 23, "timed_out": False, "launch_error": None,
            "output_bytes": 40, "output_truncated": False,
            "started_at": "2026-10-17 12:00:00", "finished_at": "2026-10-17 12:00:01",
        }
        def fake_worker(tool):
            APP.LAST_COMMAND_RESULT.update(command_evidence)
            return False
        try:
            with tempfile.TemporaryDirectory() as tmp:
                APP.STATE_DIR = Path(tmp)
                old_installed = APP.installed
                try:
                    APP.installed = lambda tool: False
                    with contextlib.redirect_stdout(io.StringIO()):
                        APP.progress(fake_tools, fake_worker, "test")
                finally:
                    APP.installed = old_installed
                summary = json.loads((Path(tmp) / "last_install_summary.json").read_text(encoding="utf-8"))
                entry = summary["results"][0]
                self.assertEqual(entry["installer_exit_code"], 23)
                self.assertEqual(entry["installer_command"], ["pkg", "install", "-y", "first"])
                self.assertEqual(entry["installer_label"], "Installing First")
                self.assertEqual(entry["installer_output_bytes"], 40)
                self.assertEqual(entry["verification"], "not_run")
        finally:
            APP.STATE_DIR = original_state

    def test_requested_package_evidence_does_not_claim_resolution(self):
        pkg = APP.requested_package_evidence({"install_kind":"pkg","package":"sample-package"})
        self.assertEqual(pkg["requested_package"], "sample-package")
        self.assertIsNone(pkg["requested_version"])
        self.assertEqual(pkg["version_specification"], "unpinned")
        self.assertIsNone(pkg["resolved_version"])
        self.assertEqual(pkg["version_evidence"], "not_collected")

        go = APP.requested_package_evidence({"install_kind":"go","package":"example.org/sample/cmd/tool@v1.2.3"})
        self.assertEqual(go["requested_package"], "example.org/sample/cmd/tool")
        self.assertEqual(go["requested_version"], "v1.2.3")
        self.assertEqual(go["version_specification"], "requested_version")
        self.assertIsNone(go["resolved_version"])

    def test_requested_latest_go_version_is_marked_floating(self):
        go = APP.requested_package_evidence({"install_kind":"go","package":"example.org/sample@latest"})
        self.assertEqual(go["requested_version"], "latest")
        self.assertEqual(go["version_specification"], "floating_latest")
        self.assertEqual(go["version_evidence"], "not_collected")

    def test_pkg_resolved_version_comes_from_dpkg_metadata(self):
        from unittest.mock import patch, Mock
        tool = {"install_kind":"pkg", "package":"sample-package"}
        with patch.object(APP.shutil, "which", return_value="/usr/bin/dpkg-query"), \
             patch.object(APP.subprocess, "run", return_value=Mock(returncode=0, stdout="1.2.3-4", stderr="")) as query:
            result = APP.collect_resolved_version(tool)
        self.assertEqual(result["resolved_version"], "1.2.3-4")
        self.assertEqual(result["version_evidence"], "package_manager_metadata")
        self.assertEqual(result["version_query_exit_code"], 0)
        self.assertEqual(query.call_args.args[0][-1], "sample-package")
        self.assertEqual(query.call_args.kwargs["timeout"], 5)

    def test_pip_resolved_version_reads_only_version_metadata(self):
        from unittest.mock import patch, Mock
        tool = {"install_kind":"pip", "package":"sample-package"}
        with patch.object(APP.Path, "is_file", return_value=True), \
             patch.object(APP.subprocess, "run", return_value=Mock(
                 returncode=0, stdout="4.5.6\n", stderr=""
             )) as query:
            result = APP.collect_resolved_version(tool)
        self.assertEqual(result["resolved_version"], "4.5.6")
        self.assertEqual(result["version_evidence"], "package_manager_metadata")
        command = query.call_args.args[0]
        self.assertEqual(command[-1], "sample-package")
        self.assertIn("importlib.metadata.version", command[2])

    def test_version_query_failure_never_invents_a_version(self):
        from unittest.mock import patch
        tool = {"install_kind":"pkg", "package":"sample-package"}
        with patch.object(APP.shutil, "which", return_value="/usr/bin/dpkg-query"), \
             patch.object(APP.subprocess, "run", side_effect=FileNotFoundError):
            result = APP.collect_resolved_version(tool)
        self.assertIsNone(result["resolved_version"])
        self.assertEqual(result["version_evidence"], "query_failed")

    def test_unsupported_package_manager_does_not_run_a_probe(self):
        from unittest.mock import patch
        tool = {"install_kind":"go", "package":"example.org/sample@v1.2.3"}
        with patch.object(APP.subprocess, "run") as query:
            result = APP.collect_resolved_version(tool)
        query.assert_not_called()
        self.assertIsNone(result["resolved_version"])
        self.assertEqual(result["version_evidence"], "not_supported")

    def test_profile_cli_outputs_valid_json(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "main.py"), "--profile"],
            capture_output=True, text=True, timeout=15
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        profile = json.loads(result.stdout)
        self.assertEqual(profile["application"], "SYN_LAUNCH")
        self.assertEqual(profile["catalog_entries"], self.data["tool_count"])

    def test_doctor_cli_reports_architecture_and_runtimes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "main.py"), "--doctor"],
            capture_output=True, text=True, timeout=15
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Architecture:", result.stdout)
        self.assertIn("proot:", result.stdout)

if __name__ == "__main__":
    unittest.main()
