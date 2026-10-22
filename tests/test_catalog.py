import copy
import io
import importlib.util
import json
import os
import re
import subprocess
import tempfile
import sys
import unittest
from contextlib import redirect_stdout
from unittest import mock
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

    def test_local_markdown_links_resolve(self):
        """Catch broken relative links and images in README and wiki source pages."""
        markdown_files = [ROOT / "README.md", *ROOT.glob("wiki/**/*.md"), *ROOT.glob("docs/**/*.md")]
        link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
        checked = 0
        for markdown_file in markdown_files:
            if not markdown_file.is_file():
                continue
            content = markdown_file.read_text(encoding="utf-8")
            for raw_target in link_pattern.findall(content):
                target = raw_target.strip().split()[0].strip("<>")
                if not target or target.startswith(("https://", "http://", "mailto:", "#", "data:")):
                    continue
                relative_path = target.split("#", 1)[0].split("?", 1)[0]
                if not relative_path:
                    continue
                checked += 1
                resolved = (markdown_file.parent / relative_path).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"{markdown_file.relative_to(ROOT)} has broken local link/image: {raw_target}",
                )
        self.assertGreater(checked, 0, "Expected to check at least one local Markdown link")

    def test_source_backed_compatibility_metadata_is_explicit_and_not_verified(self):
        declared = [tool for tool in self.tools if tool.get("compatibility")]
        self.assertGreaterEqual(len(declared), 70)
        for tool in declared:
            metadata = tool["compatibility"]
            self.assertEqual(metadata["status"], "source_documented_not_device_verified", tool["name"])
            self.assertTrue(metadata["install_source"].startswith("https://"), tool["name"])
            self.assertTrue(metadata["evidence_scope"], tool["name"])
            self.assertIn("not_device_verified", metadata["status"])
            self.assertIs(type(metadata["root_required"]), bool)
            self.assertIsInstance(metadata["known_blockers"], list)

    def test_compatibility_coverage_and_unassessed_entries_are_explicit(self):
        declared = [tool for tool in self.tools if tool.get("compatibility")]
        unassessed = {tool["id"] for tool in self.tools if not tool.get("compatibility")}
        self.assertEqual(len(declared), 267)
        self.assertEqual(unassessed, {"burp-suite", "wappalyzer"})

    def test_roadmap_upstream_source_review_count_matches_list(self):
        roadmap = (ROOT / "PLATFORM_ROADMAP.md").read_text(encoding="utf-8")
        line = next(
            line for line in roadmap.splitlines()
            if "pinned upstream source snapshots" in line and "OSRFramework" in line
        )
        self.assertIn("Review eleven additional catalog entries", line)
        self.assertNotIn("Review nine additional catalog entries", line)
        expected_names = (
            "OSRFramework", "Nikto", "checksec", "PDFiD", "Kismet", "BlueZ tools",
            "Dalfox", "Nuclei templates", "Quark Engine", "Podman", "Rootkit Hunter",
        )
        for name in expected_names:
            self.assertIn(name, line)

    def test_optional_linux_environment_docs_match_detection_status(self):
        page = (ROOT / "wiki" / "Optional-Linux-Environments.md").read_text(encoding="utf-8")
        self.assertIn("already records PRoot and PRoot-Distro presence indicators", page)
        self.assertNotIn("may be detected as environment context in a future capability profile", page)
        self.assertIn("Physical-device confirmation is still required", page)

    def test_readme_compatibility_summary_matches_current_catalog_evidence(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        declared = [tool for tool in self.tools if tool.get("compatibility")]
        unassessed = {tool["id"] for tool in self.tools if not tool.get("compatibility")}
        self.assertIn(f"**{len(declared)} source-backed compatibility declarations**", readme)
        self.assertEqual(unassessed, {"burp-suite", "wappalyzer"})
        self.assertIn("Two catalog entries remain unassessed", readme)
        self.assertIn("DNSGen now has a pinned upstream source revision", readme)
        self.assertNotIn("**266 source-backed compatibility declarations**", readme)
        self.assertNotIn("Three catalog entries remain unassessed", readme)

    def test_compatibility_declarations_pin_reproducible_source_snapshots(self):
        declared = [tool for tool in self.tools if tool.get("compatibility")]
        self.assertGreaterEqual(len(declared), 266)
        for tool in declared:
            with self.subTest(tool=tool["id"]):
                metadata = tool["compatibility"]
                revision = metadata.get("source_revision")
                snapshot = metadata.get("source_snapshot_url")
                self.assertRegex(revision or "", r"^[0-9a-f]{40}$")
                self.assertTrue(snapshot.startswith("https://github.com/"))
                self.assertIn(revision, snapshot)
                self.assertTrue(metadata.get("evidence_scope"))
        for tool_id in ("pip-audit", "yamllint", "dirsearch", "sherlock", "bandit", "detect-secrets", "email-validator", "ssh-audit", "maigret", "h8mail", "theharvester"):
            tool = next(item for item in self.tools if item["id"] == tool_id)
            metadata = tool["compatibility"]
            self.assertTrue(metadata["evidence_kind"].startswith("upstream Python packaging metadata ("))
            self.assertTrue(metadata["declared_python_requirement"])

    def test_dnsgen_compatibility_evidence_is_pinned_and_cautious(self):
        tool = next(item for item in self.tools if item["id"] == "dnsgen")
        metadata = tool["compatibility"]
        self.assertEqual(metadata["source_revision"], "7c98e7ecda2f626d49c47be9c98b234a2e4db5b7")
        self.assertIn(metadata["source_revision"], metadata["source_snapshot_url"])
        self.assertIn("does not prove", metadata["evidence_scope"])
        self.assertIn("Android", metadata["platform"])
        self.assertFalse(metadata["root_required"])

    def test_php_catalog_carries_current_critical_security_advisory(self):
        php = next(tool for tool in self.tools if tool["id"] == "php")
        advisory = php.get("security_advisory", {})
        self.assertEqual(advisory.get("severity"), "critical")
        self.assertEqual(advisory.get("cves"), ["CVE-2026-109618", "CVE-2026-109619"])
        self.assertEqual(advisory.get("fixed_versions"), {
            "8.5": "8.5.12", "8.4": "8.4.27", "8.3": "8.3.36", "8.2": "8.2.35"
        })
        metadata = php["compatibility"]
        self.assertEqual(metadata["source_revision"], "c2bb85d3f26d52ba4a4a159d14214a8ace706235")
        self.assertIn(metadata["source_revision"], metadata["source_snapshot_url"])
        self.assertIn("critical", php["caveat"].lower())
        guide = (ROOT / "wiki" / "PHP-Security-Update-2026-10-21.md").read_text(encoding="utf-8")
        self.assertIn("pkg upgrade php", guide)
        self.assertIn("SYN_LAUNCH is implemented in Python", guide)

    def test_php_security_check_cli_outputs_json_and_exit_status(self):
        cases = [
            ({"resolved_version": "8.5.11-1", "version_evidence": "package_manager_metadata", "version_query_exit_code": 0}, 1, "update_required"),
            ({"resolved_version": "8.5.12-1", "version_evidence": "package_manager_metadata", "version_query_exit_code": 0}, 0, "fixed_release_or_newer"),
            ({"resolved_version": None, "version_evidence": "not_found", "version_query_exit_code": 1}, 0, "not_installed"),
        ]
        for version_result, expected_code, expected_status in cases:
            with self.subTest(version_result=version_result):
                output = io.StringIO()
                with mock.patch.object(APP, "collect_resolved_version", return_value=version_result), \
                     mock.patch("sys.argv", ["main.py", "--php-security-check"]), \
                     redirect_stdout(output):
                    exit_code = APP.main()
                self.assertEqual(exit_code, expected_code)
                report = json.loads(output.getvalue())
                self.assertEqual(report["status"], expected_status)
                self.assertFalse(report["checks"]["network_requests_made"])
                self.assertFalse(report["checks"]["package_changed"])

    def test_catalog_rejects_malformed_php_security_advisory_metadata(self):
        broken = copy.deepcopy(self.data)
        php = next(tool for tool in broken["tools"] if tool["id"] == "php")
        php["security_advisory"]["severity"] = "urgent"
        with self.assertRaisesRegex(ValueError, "security advisory severity"):
            APP.validate_catalog(broken)
        broken = copy.deepcopy(self.data)
        php = next(tool for tool in broken["tools"] if tool["id"] == "php")
        php["security_advisory"]["upstream_advisory"] = "http://example.test/advisory"
        with self.assertRaisesRegex(ValueError, "valid HTTPS URL"):
            APP.validate_catalog(broken)
        broken = copy.deepcopy(self.data)
        php = next(tool for tool in broken["tools"] if tool["id"] == "php")
        php["security_advisory"]["fixed_versions"]["8.5"] = "8.5.x"
        with self.assertRaisesRegex(ValueError, "fixed versions"):
            APP.validate_catalog(broken)

    def test_php_security_version_assessment_handles_fixed_and_vulnerable_versions(self):
        advisory = next(tool for tool in self.tools if tool["id"] == "php")["security_advisory"]
        assess = APP.assess_php_security_version
        cases = [
            ({"resolved_version": "8.5.12-1", "version_evidence": "package_manager_metadata"}, "fixed_release_or_newer"),
            ({"resolved_version": "8.5.13", "version_evidence": "package_manager_metadata"}, "fixed_release_or_newer"),
            ({"resolved_version": "8.4.26-2", "version_evidence": "package_manager_metadata"}, "update_required"),
            ({"resolved_version": "8.3.35", "version_evidence": "package_manager_metadata"}, "update_required"),
            ({"resolved_version": "8.2.35-0+termux", "version_evidence": "package_manager_metadata"}, "fixed_release_or_newer"),
            ({"resolved_version": "8.1.33", "version_evidence": "package_manager_metadata"}, "vendor_backport_or_upgrade_required"),
            ({"resolved_version": None, "version_evidence": "not_found"}, "not_installed"),
            ({"resolved_version": None, "version_evidence": "query_failed"}, "version_unavailable"),
            ({"resolved_version": "8.6.0RC3", "version_evidence": "package_manager_metadata"}, "version_unparseable"),
        ]
        for version_result, expected in cases:
            with self.subTest(version=version_result):
                report = assess(version_result, advisory)
                self.assertEqual(report["status"], expected)
                self.assertFalse(report["checks"]["network_requests_made"])
                self.assertFalse(report["checks"]["php_executable_run"])
                self.assertFalse(report["checks"]["package_changed"])

    def test_php_security_check_cli_uses_package_metadata_and_reports_exit_status(self):
        with mock.patch.object(APP, "collect_resolved_version", return_value={
            "resolved_version": "8.5.11-1",
            "version_evidence": "package_manager_metadata",
            "version_query_exit_code": 0,
        }):
            data = copy.deepcopy(self.data)
            report = APP.php_security_report(data)
        self.assertEqual(report["status"], "update_required")
        self.assertFalse(report["checks"]["network_requests_made"])
        self.assertEqual(report["source"], "local Termux package-manager metadata")

    def test_catalog_rejects_invalid_compatibility_evidence(self):
        broken = copy.deepcopy(self.data)
        tool = next(t for t in broken["tools"] if t.get("compatibility"))
        tool["compatibility"]["install_source"] = "http://example.invalid/package"
        with self.assertRaisesRegex(ValueError, "compatibility evidence must be a valid HTTPS URL"):
            APP.validate_catalog(broken)

    def test_catalog_rejects_incomplete_compatibility_metadata(self):
        broken = copy.deepcopy(self.data)
        tool = next(t for t in broken["tools"] if t.get("compatibility"))
        del tool["compatibility"]["root_required"]
        with self.assertRaisesRegex(ValueError, "incomplete compatibility metadata"):
            APP.validate_catalog(broken)

    def test_catalog_rejects_missing_compatibility_evidence_scope(self):
        broken = copy.deepcopy(self.data)
        tool = next(t for t in broken["tools"] if t.get("compatibility"))
        del tool["compatibility"]["evidence_scope"]
        with self.assertRaisesRegex(ValueError, "incomplete compatibility metadata"):
            APP.validate_catalog(broken)

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

    def test_bounded_probe_can_return_exit_code_without_breaking_legacy_callers(self):
        output, truncated, timed_out, exit_code = APP.bounded_probe(
            [sys.executable, "-c", "print('probe-ok')"], timeout=5, max_bytes=1024, include_returncode=True
        )
        self.assertEqual(output.strip(), "probe-ok")
        self.assertFalse(truncated)
        self.assertFalse(timed_out)
        self.assertEqual(exit_code, 0)

    def test_explicit_smoke_test_records_only_bounded_probe_evidence(self):
        import tempfile
        from unittest.mock import patch
        tool = {
            "id": "python-smoke-test", "name": "Python Smoke Test", "executable": "python",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/python",
            "caveat": "A version probe is not a feature test."
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), patch.object(APP.shutil, "which", return_value=sys.executable):
                record = APP.smoke_test_tool(tool)
                self.assertEqual(record["status"], "passed")
                self.assertEqual(record["probe"], "--version")
                self.assertEqual(record["exit_code"], 0)
                self.assertIn("not a functional test", record["scope"])
                saved = APP.load_smoke_evidence()
                self.assertEqual(saved["python-smoke-test"]["status"], "passed")
                report = APP.compatibility_report({"tools": [tool], "categories": ["Test"]})
                self.assertEqual(report["tools"][0]["smoke_test"], "passed")
                self.assertEqual(report["summary"]["smoke_tested_entries"], 1)
                self.assertEqual(report["tools"][0]["device_validation"], "not_run")

    def test_openssh_smoke_test_uses_supported_version_flag(self):
        import tempfile
        from unittest.mock import patch
        tool = {
            "id": "openssh-smoke-test", "name": "OpenSSH", "executable": "ssh",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/openssh",
            "caveat": "A version probe is not a feature test."
        }
        def probe(command, **kwargs):
            if command[-1] == "-V":
                return ("OpenSSH_test_version\n", False, False, 0)
            return ("", False, False, 1)
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), patch.object(APP.shutil, "which", return_value="/usr/bin/ssh"), patch.object(APP, "bounded_probe", side_effect=probe) as mocked:
                record = APP.smoke_test_tool(tool)
        self.assertEqual(record["status"], "passed")
        self.assertEqual(record["probe"], "-V")
        self.assertEqual(mocked.call_args_list[0].args[0][-1], "-V")

    def test_iproute2_smoke_test_uses_supported_version_flag(self):
        import tempfile
        from unittest.mock import patch
        tool = {
            "id": "iproute2-smoke-test", "name": "iproute2", "executable": "ip",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/iproute2",
            "caveat": "A version probe is not a feature test."
        }
        def probe(command, **kwargs):
            if command[-1] == "-V":
                return ("ip utility, iproute2-test-version\n", False, False, 0)
            return ("", False, False, 1)
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), patch.object(APP.shutil, "which", return_value="/usr/bin/ip"), patch.object(APP, "bounded_probe", side_effect=probe) as mocked:
                record = APP.smoke_test_tool(tool)
        self.assertEqual(record["status"], "passed")
        self.assertEqual(record["probe"], "-V")
        self.assertEqual(mocked.call_args_list[0].args[0][-1], "-V")

    def test_ssh_key_tools_accept_expected_usage_exit(self):
        import tempfile
        from unittest.mock import patch
        for executable, expected_flag in (("ssh-keygen", "--help"), ("ssh-keyscan", "-h")):
            with self.subTest(executable=executable):
                tool = {
                    "id": executable + "-smoke-test", "name": executable, "executable": executable,
                    "category": "Test", "install_kind": "manual", "package": None, "installable": False,
                    "description": "Test-only", "source": "https://example.org/openssh",
                    "caveat": "A usage probe is not a feature test."
                }
                def probe(command, **kwargs):
                    if command[-1] == expected_flag:
                        return ("usage: " + executable + " [options]\n", False, False, 1)
                    return ("", False, False, 1)
                with tempfile.TemporaryDirectory() as tmp:
                    with patch.object(APP, "STATE_DIR", Path(tmp)), patch.object(APP.shutil, "which", return_value="/usr/bin/" + executable), patch.object(APP, "bounded_probe", side_effect=probe) as mocked:
                        record = APP.smoke_test_tool(tool)
                self.assertEqual(record["status"], "passed")
                self.assertEqual(record["probe"], expected_flag)
                self.assertTrue(record["expected_usage_exit"])
                self.assertEqual(mocked.call_args_list[0].args[0][-1], expected_flag)

    def test_whois_smoke_test_accepts_usage_text_when_help_exits_nonzero(self):
        import tempfile
        from unittest.mock import patch
        tool = {
            "id": "whois-smoke-test", "name": "whois", "executable": "whois",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/whois",
            "caveat": "A usage probe is not a feature test."
        }
        def probe(command, **kwargs):
            if command[-1] == "--help":
                return ("Usage: whois [OPTION]... OBJECT...\n--help display this help and exit\n", False, False, 1)
            return ("", False, False, 1)
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), patch.object(APP.shutil, "which", return_value="/usr/bin/whois"), patch.object(APP, "bounded_probe", side_effect=probe) as mocked:
                record = APP.smoke_test_tool(tool)
        self.assertEqual(record["status"], "passed")
        self.assertEqual(record["probe"], "--help")
        self.assertTrue(record["expected_usage_exit"])
        self.assertEqual(mocked.call_args_list[0].args[0][-1], "--help")

    def test_non_usage_error_does_not_pass_expected_usage_probe(self):
        import tempfile
        from unittest.mock import patch
        tool = {
            "id": "ssh-keygen-error-test", "name": "ssh-keygen", "executable": "ssh-keygen",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/openssh",
            "caveat": "A bounded probe is not a feature test."
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), patch.object(APP.shutil, "which", return_value="/usr/bin/ssh-keygen"), patch.object(APP, "bounded_probe", return_value=("unsupported option\n", False, False, 1)):
                record = APP.smoke_test_tool(tool)
        self.assertEqual(record["status"], "output_observed_nonzero")
        self.assertFalse(record["attempts"][0]["expected_usage_exit"])

    def test_bounded_local_command_enforces_combined_output_cap(self):
        with self.assertRaisesRegex(RuntimeError, "combined stdout/stderr exceeded"):
            APP.run_bounded_local_command(
                [sys.executable, "-c", "import os; os.write(1, b'x' * 40000); os.write(2, b'y' * 30000)"],
                timeout_seconds=3, output_limit=65536,
            )

    def test_bounded_local_command_streams_large_stdin_without_deadlock(self):
        payload = b"x" * (1024 * 1024)
        output = APP.run_bounded_local_command(
            [sys.executable, "-c", "import sys; print(len(sys.stdin.buffer.read()))"],
            input_bytes=payload, timeout_seconds=3, output_limit=65536,
        )
        self.assertEqual(output.strip(), str(len(payload)).encode("ascii"))

    def test_bounded_local_command_kills_timed_out_process(self):
        import time
        started = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            APP.run_bounded_local_command(
                [sys.executable, "-c", "import time; time.sleep(5)"],
                timeout_seconds=0.2, output_limit=65536,
            )
        self.assertLess(time.monotonic() - started, 2.0)

    def test_functional_check_records_separate_local_only_evidence(self):
        from unittest.mock import patch
        tool = {
            "id": "python-functional-test", "name": "Python Functional Test", "executable": "python",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/python",
            "caveat": "A functional check is scoped evidence, not full compatibility certification."
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), patch.object(APP.shutil, "which", return_value=sys.executable):
                record = APP.functional_check_tool(tool)
                self.assertEqual(record["status"], "passed")
                self.assertEqual(record["check_id"], "python-json-and-sha256")
                self.assertFalse(record["network_actions_executed"])
                self.assertFalse(record["package_changes"])
                saved = APP.load_functional_evidence()
                self.assertEqual(saved["python-functional-test"]["status"], "passed")
                report = APP.compatibility_report({"tools": [tool], "categories": ["Test"]})
                self.assertEqual(report["tools"][0]["functional_check"], "passed")
                self.assertEqual(report["summary"]["functional_check_passed_entries"], 1)
                self.assertEqual(report["tools"][0]["device_validation"], "not_run")
                self.assertEqual(report["tools"][0]["smoke_test"], "not_run")

    def test_functional_check_local_only_adapters_for_available_tools(self):
        import shutil
        from unittest.mock import patch
        candidates = {
            "curl": "curl-local-file-roundtrip",
            "rg": "ripgrep-local-fixture-search",
            "fd": "fd-local-fixture-find",
            "file": "file-local-text-identification",
            "tree": "tree-local-directory-inventory",
            "vim": "vim-local-ex-mode-edit",
            "npm": "npm-offline-package-metadata",
            "make": "make-local-target",
            "ssh": "ssh-config-expansion-no-connect",
            "ps": "ps-current-process",
            "lsof": "lsof-current-process-open-file",
        }
        # npm can block for several seconds on hosted runner shims even with
        # offline mode; its adapter is exercised on the actual Termux device.
        if os.environ.get("CI"):
            candidates.pop("npm", None)
        available = {executable: shutil.which(executable) for executable in candidates}
        available = {executable: path for executable, path in available.items() if path}
        if not available:
            self.skipTest("No optional local-only adapter executable is installed")
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)):
                for executable, expected_check in candidates.items():
                    if executable not in available:
                        continue
                    with self.subTest(executable=executable):
                        tool = {
                            "id": "functional-" + executable, "name": executable,
                            "executable": executable, "category": "Test", "install_kind": "manual",
                            "package": None, "installable": False, "description": "Test-only",
                            "source": "https://example.org/test", "caveat": "Local-only test."
                        }
                        record = APP.functional_check_tool(tool)
                        self.assertEqual(record["status"], "passed", record)
                        self.assertEqual(record["check_id"], expected_check)
                        self.assertFalse(record["network_actions_executed"])
                        self.assertFalse(record["package_changes"])

    def test_local_search_and_inventory_adapters_are_bounded_and_fixture_only(self):
        import tempfile
        from unittest.mock import patch
        cases = {
            "rg": ("ripgrep-local-fixture-search", b"2:needle-one\n4:needle-two\n"),
            "fd": ("fd-local-fixture-find", None),
            "file": ("file-local-text-identification", b"ASCII text\n"),
            "tree": ("tree-local-directory-inventory", None),
        }
        for executable, (expected_check, canned_output) in cases.items():
            with self.subTest(executable=executable), tempfile.TemporaryDirectory() as tmp:
                calls = []
                def invoke(args, **kwargs):
                    calls.append(args)
                    if canned_output is not None:
                        return canned_output
                    root = Path(args[-1])
                    target = root / "nested" / "needle.txt"
                    return str(target).encode("utf-8") + b"\n"
                tool = {
                    "id": "functional-" + executable, "name": executable,
                    "executable": executable, "category": "Test", "install_kind": "manual",
                    "package": None, "installable": False, "description": "Test-only",
                    "source": "https://example.org/test", "caveat": "Local-only test."
                }
                with patch.object(APP, "STATE_DIR", Path(tmp)), \
                     patch.object(APP.shutil, "which", return_value="/mock/" + executable), \
                     patch.object(APP, "run_bounded_local_command", side_effect=invoke):
                    record = APP.functional_check_tool(tool)
                self.assertEqual(record["status"], "passed", record)
                self.assertEqual(record["check_id"], expected_check)
                self.assertTrue(calls)
                self.assertFalse(record["network_actions_executed"])
                self.assertFalse(record["package_changes"])

    def test_vim_functional_check_is_noninteractive_and_edits_only_temporary_fixture(self):
        import tempfile
        from unittest.mock import patch
        tool = {
            "id": "vim-functional-test", "name": "Vim", "executable": "vim",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/vim",
            "caveat": "A local fixture assertion is not full compatibility certification."
        }
        calls = []
        def invoke(args, **kwargs):
            calls.append((args, kwargs))
            fixture = Path(args[5])
            fixture.write_bytes(b"SYN_LAUNCH functional check\nedited line\n")
            return b""
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), \
                 patch.object(APP.shutil, "which", return_value="/mock/vim"), \
                 patch.object(APP, "run_bounded_local_command", side_effect=invoke):
                record = APP.functional_check_tool(tool)
        self.assertEqual(record["status"], "passed", record)
        self.assertEqual(record["check_id"], "vim-local-ex-mode-edit")
        self.assertEqual(calls[0][0][1:5], ["-Nu", "NONE", "-n", "-es"])
        self.assertEqual(calls[0][0][-2:], ["-c", "wq"])
        self.assertFalse(record["network_actions_executed"])
        self.assertFalse(record["package_changes"])

    def test_npm_functional_check_isolates_cache_config_and_logs(self):
        from unittest.mock import patch
        tool = {
            "id": "npm-isolation-test", "name": "npm isolation test", "executable": "npm",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/npm",
            "caveat": "Must not write to user npm configuration or cache."
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), \
                 patch.object(APP.shutil, "which", return_value="/mock/npm"), \
                 patch.object(APP, "run_bounded_local_command", return_value=b'"syn-launch-local-probe"\n') as invoke:
                record = APP.functional_check_tool(tool)
        self.assertEqual(record["status"], "passed", record)
        env = invoke.call_args.kwargs["env"]
        cache = Path(env["npm_config_cache"])
        self.assertTrue(cache.parent.name.startswith("syn-launch-functional-"))
        self.assertEqual(env["npm_config_logs"], "false")
        user_config = Path(env["npm_config_userconfig"])
        global_config = Path(env["npm_config_globalconfig"])
        self.assertNotEqual(user_config, global_config)
        self.assertEqual(user_config.parent, cache.parent)
        self.assertEqual(global_config.parent, cache.parent)
        allowed = {"npm_config_cache", "npm_config_logs", "npm_config_userconfig", "npm_config_globalconfig",
                   "npm_config_update_notifier", "npm_config_fund", "npm_config_audit", "npm_config_progress"}
        self.assertFalse(any(key.lower().startswith("npm_config_") and key.lower() not in allowed for key in env))

    def test_functional_check_does_not_execute_unsupported_tools(self):
        from unittest.mock import patch
        tool = {
            "id": "unsupported-functional-test", "name": "Unsupported Test", "executable": "unknown-tool",
            "category": "Test", "install_kind": "manual", "package": None, "installable": False,
            "description": "Test-only", "source": "https://example.org/unknown",
            "caveat": "No functional adapter."
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)), patch.object(APP.shutil, "which", return_value="/bin/true"):
                record = APP.functional_check_tool(tool)
                self.assertEqual(record["status"], "unsupported")
                self.assertIsNone(record["check_id"])
                self.assertIn("no command was run", record["detail"])

    def test_compatibility_report_marks_replaced_functional_evidence_stale(self):
        from unittest.mock import patch
        fake = {
            "id": "stale-functional-tool", "name": "Stale Functional Tool", "category": "Test",
            "executable": "stale-functional-tool", "install_kind": "manual", "package": None,
            "caveat": "Test-only entry."
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)):
                APP.save_private_json(APP.functional_evidence_path(), {
                    "stale-functional-tool": {
                        "tool_id": "stale-functional-tool", "status": "passed",
                        "path": "/old/path/stale-functional-tool", "check_id": "test-only",
                        "binary_identity": {"size_bytes": 1, "mtime_ns": 1}
                    }
                })
                with patch.object(APP.shutil, "which", return_value="/new/path/stale-functional-tool"), patch.object(
                    APP, "executable_identity", return_value={"size_bytes": 2, "mtime_ns": 2}
                ):
                    report = APP.compatibility_report({"tools": [fake], "categories": ["Test"]})
                self.assertEqual(report["tools"][0]["functional_check"], "stale_evidence")
                self.assertEqual(report["summary"]["functional_check_passed_entries"], 0)

    def test_compatibility_report_marks_replaced_binary_evidence_stale(self):
        import tempfile
        from unittest.mock import patch
        fake = {
            "id": "stale-tool", "name": "Stale Tool", "category": "Test",
            "executable": "stale-tool", "install_kind": "manual", "package": None,
            "caveat": "Test-only entry."
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(APP, "STATE_DIR", Path(tmp)):
                APP.save_private_json(APP.smoke_evidence_path(), {
                    "stale-tool": {
                        "tool_id": "stale-tool", "status": "passed",
                        "path": "/old/path/stale-tool",
                        "binary_identity": {"size_bytes": 1, "mtime_ns": 1}
                    }
                })
                with patch.object(APP.shutil, "which", return_value="/new/path/stale-tool"), patch.object(
                    APP, "executable_identity", return_value={"size_bytes": 2, "mtime_ns": 2}
                ):
                    report = APP.compatibility_report({"tools": [fake], "categories": ["Test"]})
                self.assertEqual(report["tools"][0]["smoke_test"], "stale_evidence")
                self.assertEqual(report["summary"]["smoke_tested_entries"], 0)

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
        self.assertEqual(report["report_schema"], 4)
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
        # The report intentionally includes saved smoke-test evidence. Give this
        # assertion an empty private state directory so it is deterministic on
        # developer devices that already have real smoke-test records.
        with tempfile.TemporaryDirectory(prefix="syn-launch-report-test-") as state_dir:
            env = os.environ.copy()
            env["SYN_LAUNCH_HOME"] = state_dir
            result = subprocess.run(
                [sys.executable, str(ROOT / "main.py"), "--compatibility-report"],
                capture_output=True, text=True, timeout=15, env=env
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["application"], "SYN_LAUNCH")
        self.assertEqual(report["summary"]["catalog_entries"], self.data["tool_count"])
        self.assertEqual(len(report["tools"]), self.data["tool_count"])
        self.assertEqual(report["report_schema"], 4)
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

    def test_version_reconciliation_marks_exact_go_version_match(self):
        tool = {"install_kind":"go", "package":"example.org/sample@v1.2.3"}
        result = APP.reconcile_requested_version(tool, {"resolved_version":"v1.2.3"})
        self.assertEqual(result["status"], "exact_match")
        self.assertEqual(result["comparison_basis"], "exact_string")

    def test_version_reconciliation_marks_explicit_mismatch(self):
        tool = {"install_kind":"go", "package":"example.org/sample@v1.2.3"}
        result = APP.reconcile_requested_version(tool, {"resolved_version":"v1.2.4"})
        self.assertEqual(result["status"], "mismatch")
        self.assertEqual(result["requested_version"], "v1.2.3")
        self.assertEqual(result["resolved_version"], "v1.2.4")

    def test_version_reconciliation_never_guesses_for_latest_or_unpinned(self):
        latest = {"install_kind":"go", "package":"example.org/sample@latest"}
        unpinned = {"install_kind":"cargo", "package":"sample-crate"}
        self.assertEqual(APP.reconcile_requested_version(latest, {"resolved_version":"v1.2.3"})["status"], "floating_request")
        self.assertEqual(APP.reconcile_requested_version(unpinned, {"resolved_version":"1.2.3"})["status"], "not_comparable_unpinned")
        self.assertEqual(APP.reconcile_requested_version(unpinned, {"resolved_version":None})["status"], "unresolved")

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
        tool = {"install_kind":"manual", "package":None}
        with patch.object(APP.subprocess, "run") as query:
            result = APP.collect_resolved_version(tool)
        query.assert_not_called()
        self.assertIsNone(result["resolved_version"])
        self.assertEqual(result["version_evidence"], "not_supported")

    def test_cargo_resolved_version_uses_crate_metadata_file(self):
        import json
        import tempfile
        from unittest.mock import patch
        tool = {"install_kind":"cargo", "package":"sample-crate"}
        with tempfile.TemporaryDirectory() as tmp:
            metadata = {"installs":{"sample-crate 1.2.3 (registry)": {
                "crate":"sample-crate", "version":"1.2.3"
            }}}
            Path(tmp, ".crates2.json").write_text(json.dumps(metadata), encoding="utf-8")
            with patch.dict(APP.os.environ, {"CARGO_HOME":tmp}):
                result = APP.collect_resolved_version(tool)
        self.assertEqual(result["resolved_version"], "1.2.3")
        self.assertEqual(result["version_evidence"], "package_manager_metadata")

    def test_cargo_ambiguous_versions_are_not_guessed(self):
        import json
        import tempfile
        from unittest.mock import patch
        tool = {"install_kind":"cargo", "package":"sample-crate"}
        with tempfile.TemporaryDirectory() as tmp:
            metadata = {"installs":{
                "sample-crate 1.2.3 (registry)": {"crate":"sample-crate","version":"1.2.3"},
                "sample-crate 2.0.0 (registry)": {"crate":"sample-crate","version":"2.0.0"},
            }}
            Path(tmp, ".crates2.json").write_text(json.dumps(metadata), encoding="utf-8")
            with patch.dict(APP.os.environ, {"CARGO_HOME":tmp}):
                result = APP.collect_resolved_version(tool)
        self.assertIsNone(result["resolved_version"])
        self.assertEqual(result["version_evidence"], "multiple_versions")

    def test_npm_resolved_version_reads_global_package_metadata(self):
        import json
        import tempfile
        from unittest.mock import patch, Mock
        tool = {"install_kind":"npm", "package":"sample-package"}
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = Path(tmp, "sample-package")
            package_dir.mkdir()
            Path(package_dir, "package.json").write_text(json.dumps({"version":"3.4.5"}), encoding="utf-8")
            with patch.object(APP.shutil, "which", return_value="/usr/bin/npm"), \
                 patch.object(APP, "bounded_probe", return_value=(tmp, False, False)):
                result = APP.collect_resolved_version(tool)
        self.assertEqual(result["resolved_version"], "3.4.5")
        self.assertEqual(result["version_evidence"], "package_manager_metadata")

    def test_npm_package_path_cannot_resolve_to_global_root(self):
        import json
        import tempfile
        from unittest.mock import patch, Mock
        tool = {"install_kind":"npm", "package":".."}
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "package.json").write_text(json.dumps({"version":"9.9.9"}), encoding="utf-8")
            with patch.object(APP.shutil, "which", return_value="/usr/bin/npm"), \
                 patch.object(APP, "bounded_probe", return_value=(tmp, False, False)):
                result = APP.collect_resolved_version(tool)
        self.assertIsNone(result["resolved_version"])
        self.assertEqual(result["version_evidence"], "invalid_package_path")

    def test_update_cancelled_does_not_run_package_manager_and_audits(self):
        import tempfile
        from unittest.mock import patch
        tool = {"id":"sample", "name":"Sample", "install_kind":"go", "package":"example.org/sample@v1.2.3", "executable":"sample"}
        original_state = APP.STATE_DIR
        with tempfile.TemporaryDirectory() as tmp:
            try:
                APP.STATE_DIR = Path(tmp)
                with patch.object(APP, "installed", return_value=True), \
                     patch.object(APP, "collect_resolved_version", return_value={"resolved_version":"v1.2.3","version_evidence":"package_manager_metadata"}), \
                     patch.object(APP, "run") as run:
                    result = APP.update_one(tool, confirmed=False)
                self.assertFalse(result)
                run.assert_not_called()
                event = json.loads((Path(tmp)/"lifecycle_audit.jsonl").read_text(encoding="utf-8").splitlines()[0])
                self.assertEqual(event["operation"], "update")
                self.assertEqual(event["status"], "cancelled_not_confirmed")
            finally:
                APP.STATE_DIR = original_state

    def test_update_uses_exact_go_module_spec_and_records_audit(self):
        import tempfile
        from unittest.mock import patch
        tool = {"id":"sample", "name":"Sample", "install_kind":"go", "package":"example.org/sample@v1.2.3", "executable":"sample"}
        original_state = APP.STATE_DIR
        with tempfile.TemporaryDirectory() as tmp:
            try:
                APP.STATE_DIR = Path(tmp)
                command_result = {"command":["go","install","example.org/sample@v1.2.3"],"exit_code":0,"timed_out":False,"launch_error":None}
                with patch.object(APP, "installed", side_effect=[True, True]), \
                     patch.object(APP, "collect_resolved_version", side_effect=[
                         {"resolved_version":"v1.2.3","version_evidence":"package_manager_metadata"},
                         {"resolved_version":"v1.2.3","version_evidence":"package_manager_metadata"},
                     ]), \
                     patch.object(APP.shutil, "which", return_value="/usr/bin/go"), \
                     patch.object(APP, "run", return_value=True) as run, \
                     patch.object(APP, "LAST_COMMAND_RESULT", command_result):
                    result = APP.update_one(tool, confirmed=True)
                self.assertTrue(result)
                run.assert_called_once_with(["go","install","example.org/sample@v1.2.3"], "Updating Go module example.org/sample@v1.2.3", 3600, {
                    "GOBIN":str(APP.BIN_DIR), "GOPROXY":"https://proxy.golang.org,direct",
                    "GOSUMDB":"sum.golang.org", "GONOSUMDB":"", "GOPRIVATE":"",
                    "GOINSECURE":"", "GOFLAGS":"", "GOTOOLCHAIN":"local"
                })
                event = json.loads((Path(tmp)/"lifecycle_audit.jsonl").read_text(encoding="utf-8").splitlines()[0])
                self.assertEqual(event["status"], "operation_succeeded")
                self.assertEqual(event["command"], ["go","install","example.org/sample@v1.2.3"])
                self.assertEqual(event["version_before"]["resolved_version"], "v1.2.3")
                self.assertEqual(event["version_after"]["resolved_version"], "v1.2.3")
            finally:
                APP.STATE_DIR = original_state

    def test_uninstall_cancelled_does_not_run_package_manager_and_audits(self):
        import tempfile
        from unittest.mock import patch
        tool = {"id":"sample", "name":"Sample", "install_kind":"pkg", "package":"sample-package", "executable":"sample"}
        original_state = APP.STATE_DIR
        with tempfile.TemporaryDirectory() as tmp:
            try:
                APP.STATE_DIR = Path(tmp)
                with patch.object(APP, "installed", return_value=True), \
                     patch.object(APP, "collect_resolved_version", side_effect=[
                         {"resolved_version":"1.2.3","version_evidence":"package_manager_metadata"},
                         {"resolved_version":"1.2.3","version_evidence":"package_manager_metadata"},
                     ]), \
                     patch.object(APP, "run") as run, \
                     patch.object(APP, "append_lifecycle_event", wraps=APP.append_lifecycle_event) as audit:
                    result = APP.uninstall_one(tool, confirmed=False)
                self.assertFalse(result)
                run.assert_not_called()
                audit.assert_called_once()
                event = audit.call_args.args[0]
                self.assertEqual(event["status"], "cancelled_not_confirmed")
                self.assertEqual(event["operation"], "uninstall")
            finally:
                APP.STATE_DIR = original_state

    def test_uninstall_uses_package_manager_and_records_exit_evidence(self):
        import tempfile
        from unittest.mock import patch
        tool = {"id":"sample", "name":"Sample", "install_kind":"cargo", "package":"sample-crate", "executable":"sample"}
        original_state = APP.STATE_DIR
        with tempfile.TemporaryDirectory() as tmp:
            try:
                APP.STATE_DIR = Path(tmp)
                command_result = {"command":["cargo","uninstall","sample-crate"],"exit_code":0,"timed_out":False,"launch_error":None}
                with patch.object(APP, "installed", side_effect=[True, False]), \
                     patch.object(APP, "collect_resolved_version", side_effect=[
                         {"resolved_version":"1.2.3","version_evidence":"package_manager_metadata"},
                         {"resolved_version":None,"version_evidence":"not_found"},
                     ]), \
                     patch.object(APP.shutil, "which", return_value="/usr/bin/cargo"), \
                     patch.object(APP, "run", return_value=True) as run, \
                     patch.object(APP, "LAST_COMMAND_RESULT", command_result):
                    result = APP.uninstall_one(tool, confirmed=True)
                self.assertTrue(result)
                run.assert_called_once_with(["cargo","uninstall","sample-crate"], "Removing Cargo-installed package sample-crate", 900)
                events = [json.loads(line) for line in (Path(tmp)/"lifecycle_audit.jsonl").read_text(encoding="utf-8").splitlines()]
                self.assertEqual(len(events), 1)
                self.assertEqual(events[0]["status"], "operation_succeeded")
                self.assertEqual(events[0]["exit_code"], 0)
                self.assertEqual(events[0]["version_before"]["resolved_version"], "1.2.3")
                self.assertIsNone(events[0]["version_after"]["resolved_version"])
            finally:
                APP.STATE_DIR = original_state

    def test_uninstall_refuses_unsupported_go_and_never_runs_command(self):
        import tempfile
        from unittest.mock import patch
        tool = {"id":"sample", "name":"Sample", "install_kind":"go", "package":"example.org/sample@v1.2.3", "executable":"sample"}
        original_state = APP.STATE_DIR
        with tempfile.TemporaryDirectory() as tmp:
            try:
                APP.STATE_DIR = Path(tmp)
                with patch.object(APP, "installed", return_value=True), \
                     patch.object(APP, "collect_resolved_version", return_value={"resolved_version":None,"version_evidence":"not_supported"}), \
                     patch.object(APP, "run") as run:
                    result = APP.uninstall_one(tool, confirmed=True)
                self.assertFalse(result)
                run.assert_not_called()
                event = json.loads((Path(tmp)/"lifecycle_audit.jsonl").read_text(encoding="utf-8").splitlines()[0])
                self.assertEqual(event["status"], "unsupported")
                self.assertIsNone(event["command"])
            finally:
                APP.STATE_DIR = original_state

    def test_version_metadata_is_collected_even_if_operation_failed(self):
        import tempfile
        import contextlib
        import io
        from unittest.mock import patch, Mock
        original_state = APP.STATE_DIR
        fake_tools = [{"id":"first", "name":"First", "install_kind":"pkg", "package":"sample-package", "executable":"first"}]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                APP.STATE_DIR = Path(tmp)
                with patch.object(APP, "installed", side_effect=[False, False]), \
                     patch.object(APP, "collect_resolved_version", return_value={
                         "resolved_version":"1.2.3", "version_evidence":"package_manager_metadata",
                         "version_query_exit_code":0
                     }) as query, \
                     patch.object(APP, "LAST_COMMAND_RESULT", {"command":None,"label":None,"exit_code":None,"timed_out":False,"launch_error":None}), \
                     contextlib.redirect_stdout(io.StringIO()):
                    APP.progress(fake_tools, lambda tool: False, "test")
                summary=json.loads((Path(tmp)/"last_install_summary.json").read_text(encoding="utf-8"))
                self.assertEqual(summary["results"][0]["resolved_version"], "1.2.3")
                query.assert_called_once_with(fake_tools[0])
        finally:
            APP.STATE_DIR = original_state

    def test_post_install_check_is_metadata_only_and_not_functional_verification(self):
        import tempfile
        import contextlib
        import io
        from unittest.mock import patch
        original_state = APP.STATE_DIR
        tool = {"id":"first", "name":"First", "install_kind":"pkg", "package":"sample-package", "executable":"first"}
        try:
            with tempfile.TemporaryDirectory() as tmp:
                APP.STATE_DIR = Path(tmp)
                with patch.object(APP, "installed", side_effect=[False, True]), \
                     patch.object(APP, "collect_resolved_version", return_value={
                         "resolved_version":"1.2.3", "version_evidence":"package_manager_metadata",
                         "version_query_exit_code":0
                     }), contextlib.redirect_stdout(io.StringIO()):
                    APP.progress([tool], lambda item: True, "test")
                entry=json.loads((Path(tmp)/"last_install_summary.json").read_text(encoding="utf-8"))["results"][0]
                self.assertEqual(entry["post_install_check"]["status"], "metadata_and_executable_present")
                self.assertEqual(entry["version_reconciliation"]["status"], "not_comparable_unpinned")
                self.assertEqual(entry["post_install_check"]["check_type"], "metadata_only")
                self.assertEqual(entry["verification"], "not_run")
        finally:
            APP.STATE_DIR = original_state

    def test_cargo_metadata_file_size_is_bounded(self):
        import tempfile
        from unittest.mock import patch
        tool = {"install_kind":"cargo", "package":"sample-crate"}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp, ".crates2.json")
            path.write_text(" " * (2 * 1024 * 1024 + 1), encoding="utf-8")
            with patch.dict(APP.os.environ, {"CARGO_HOME":tmp}):
                result=APP.collect_resolved_version(tool)
        self.assertEqual(result["version_evidence"], "metadata_too_large")

    def test_go_resolved_version_reads_build_metadata_without_running_tool(self):
        from unittest.mock import patch
        tool = {"install_kind":"go", "package":"example.org/sample/cmd/tool@v1.2.3", "executable":"sample-tool"}
        with patch.object(APP.shutil, "which", side_effect=["/usr/bin/go", "/home/user/.local/bin/sample-tool"]), \
             patch.object(APP, "bounded_probe", return_value=("/home/user/.local/bin/sample-tool: go1.23.0\n    mod example.org/sample/cmd/tool v1.2.3 h1:checksum\n", False, False)) as probe:
            result = APP.collect_resolved_version(tool)
        self.assertEqual(result["resolved_version"], "v1.2.3")
        self.assertEqual(result["version_evidence"], "package_manager_metadata")
        self.assertEqual(probe.call_args.args[0][1:3], ["version", "-m"])

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