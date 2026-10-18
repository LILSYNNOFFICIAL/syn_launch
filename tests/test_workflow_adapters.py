import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from workflow_adapters import (
    run_device_configuration_audit,
    run_mobile_apk_inventory,
    run_assessment_report,
    run_web_api_review,
    run_workflow_adapter,
)


class WorkflowAdapterTests(unittest.TestCase):
    def test_device_audit_is_local_read_only_and_never_claims_validation(self):
        report = run_device_configuration_audit("local-device")
        self.assertEqual(report["workflow_id"], "device-configuration-audit")
        self.assertEqual(report["device_validation"], "not_run")
        self.assertFalse(report["execution"]["network_actions_executed"])
        self.assertFalse(report["execution"]["subprocesses_executed"])
        self.assertFalse(report["execution"]["catalog_tools_executed"])
        self.assertFalse(report["execution"]["packages_changed"])

    def test_device_audit_detects_optional_environment_markers_without_entering_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            prefix = Path(tmp) / "prefix"
            home.mkdir()
            rootfs = prefix / "var" / "lib" / "proot-distro" / "installed-rootfs"
            rootfs.mkdir(parents=True)
            (home / "kali-arm64").mkdir()
            with patch.dict(os.environ, {"HOME": str(home), "PREFIX": str(prefix), "SYN_LAUNCH_HOME": str(home / ".syn_launch")}):
                with patch("workflow_adapters.shutil.which", side_effect=lambda name: {
                    "proot": "/bin/proot", "proot-distro": "/bin/proot-distro", "nethunter": "/bin/nethunter"
                }.get(name)):
                    report = run_device_configuration_audit("local-device")
        optional = report["optional_linux_environments"]
        self.assertTrue(optional["proot_available"])
        self.assertTrue(optional["proot_distro_available"])
        self.assertTrue(optional["installed_proot_rootfs_directory_present"])
        self.assertTrue(optional["nethunter_launcher_available"])
        self.assertTrue(optional["nethunter_rootfs_marker_present"])
        self.assertIn("Presence indicators only", optional["interpretation"])
        self.assertFalse(report["execution"]["network_actions_executed"])

    def test_device_audit_rejects_remote_or_ambiguous_scope(self):
        for scope in ("localhost", "https://example.test", "", "local-device; other-host"):
            with self.subTest(scope=scope):
                with self.assertRaisesRegex(ValueError, "exactly 'local-device'"):
                    run_device_configuration_audit(scope)

    def test_mobile_apk_inventory_hashes_and_lists_without_extracting(self):
        with tempfile.TemporaryDirectory() as tmp:
            apk = Path(tmp) / "sample.apk"
            with zipfile.ZipFile(apk, "w") as archive:
                archive.writestr("AndroidManifest.xml", b"manifest-placeholder")
                archive.writestr("classes.dex", b"dex-placeholder")
                archive.writestr("lib/arm64-v8a/libsample.so", b"native-placeholder")
                archive.writestr("META-INF/CERT.RSA", b"signature-placeholder")
            report = run_mobile_apk_inventory(str(apk))
        self.assertEqual(report["workflow_id"], "mobile-app-review")
        self.assertEqual(len(report["sha256"]), 64)
        self.assertTrue(report["archive"]["android_manifest_present"])
        self.assertIn("classes.dex", report["archive"]["dex_files"])
        self.assertIn("arm64-v8a", report["archive"]["native_library_abis"])
        self.assertFalse(report["execution"]["apk_extracted"])
        self.assertFalse(report["execution"]["apk_executed"])
        self.assertEqual(report["verification"], "static_archive_inventory_only")

    def test_mobile_adapter_rejects_invalid_input_and_bad_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            wrong_extension = Path(tmp) / "sample.txt"
            wrong_extension.write_text("not apk", encoding="utf-8")
            bad_apk = Path(tmp) / "broken.apk"
            bad_apk.write_text("not a zip archive", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "local .apk"):
                run_mobile_apk_inventory(str(wrong_extension))
            with self.assertRaisesRegex(ValueError, "not a readable APK"):
                run_mobile_apk_inventory(str(bad_apk))
            with self.assertRaisesRegex(ValueError, "does not resolve"):
                run_mobile_apk_inventory(str(Path(tmp) / "missing.apk"))

    def test_mobile_adapter_rejects_oversized_apk_before_hashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            apk = Path(tmp) / "oversized.apk"
            apk.write_bytes(b"x" * 11)
            with patch("workflow_adapters.MAX_APK_BYTES", 10):
                with self.assertRaisesRegex(ValueError, "APK size must be"):
                    run_mobile_apk_inventory(str(apk))

    def test_mobile_adapter_rejects_excessive_archive_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            apk = Path(tmp) / "many-entries.apk"
            with zipfile.ZipFile(apk, "w") as archive:
                archive.writestr("one", b"1")
                archive.writestr("two", b"2")
                archive.writestr("three", b"3")
            with patch("workflow_adapters.MAX_APK_ENTRIES", 2):
                with self.assertRaisesRegex(ValueError, "more than 2 archive entries"):
                    run_mobile_apk_inventory(str(apk))

    def test_documented_example_evidence_bundle_is_valid(self):
        example = Path(__file__).resolve().parents[1] / "examples" / "assessment-evidence.example.json"
        report = run_assessment_report(str(example))
        self.assertEqual(report["finding_count"], 1)
        self.assertEqual(report["severity_counts"]["info"], 1)
        self.assertIn("PLACEHOLDER", report["findings"][0]["evidence"])

    def test_assessment_report_validates_and_summarizes_local_evidence(self):
        payload = {
            "findings": [
                {"title": "Missing header", "severity": "medium", "asset": "staging app",
                 "evidence": "Header absent in reviewed response", "remediation": "Set the header."},
                {"title": "Informational note", "severity": "info", "asset": "test APK",
                 "evidence": "Static inventory only", "remediation": "No action required."},
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence.json"
            evidence.write_text(json.dumps(payload), encoding="utf-8")
            report = run_assessment_report(str(evidence))
        self.assertEqual(report["workflow_id"], "assessment-report")
        self.assertEqual(report["finding_count"], 2)
        self.assertEqual(report["severity_counts"]["medium"], 1)
        self.assertEqual(report["severity_counts"]["info"], 1)
        self.assertFalse(report["execution"]["network_actions_executed"])
        self.assertFalse(report["execution"]["evidence_file_modified"])
        self.assertEqual(report["verification"], "input_schema_validated_only")

    def test_assessment_report_rejects_bad_schema_severity_and_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "bad.json"
            evidence.write_text(json.dumps({"findings": [
                {"title": "Bad", "severity": "urgent", "asset": "test",
                 "evidence": "sample", "remediation": "review"}
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "severity must be one of"):
                run_assessment_report(str(evidence))
            evidence.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "findings list"):
                run_assessment_report(str(evidence))
            with self.assertRaisesRegex(ValueError, "does not resolve"):
                run_assessment_report(str(Path(tmp) / "missing.json"))

    def test_assessment_report_rejects_oversized_evidence_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "large.json"
            evidence.write_text("{}", encoding="utf-8")
            with patch("workflow_adapters.MAX_EVIDENCE_JSON_BYTES", 1):
                with self.assertRaisesRegex(ValueError, "Evidence JSON must be"):
                    run_assessment_report(str(evidence))

    def test_web_api_adapter_sends_one_head_and_filters_headers(self):
        class Response:
            status = 200
            reason = "OK"
            def getheaders(self):
                return [
                    ("Strict-Transport-Security", "max-age=31536000"),
                    ("Content-Type", "application/json"),
                    ("Set-Cookie", "session=should-not-be-retained"),
                    ("Location", "https://other.example.test/"),
                ]

        created = []
        class Connection:
            def __init__(self, host, port, timeout, context):
                self.host, self.port, self.timeout = host, port, timeout
                self.context = context
                self.request_args = None
                self.closed = False
                created.append(self)
            def request(self, method, path, headers):
                self.request_args = (method, path, headers)
            def getresponse(self):
                return Response()
            def close(self):
                self.closed = True

        with patch("workflow_adapters.http.client.HTTPSConnection", side_effect=Connection):
            report = run_web_api_review("https://staging.example.test/api/v1")
        connection = created[0]
        self.assertEqual(report["request_status"], "response_received")
        self.assertEqual(report["response"]["status_code"], 200)
        self.assertEqual(connection.request_args[0:2], ("HEAD", "/api/v1"))
        self.assertEqual(connection.timeout, 5)
        self.assertTrue(connection.closed)
        self.assertIn("strict-transport-security", report["response"]["headers"])
        self.assertNotIn("set-cookie", report["response"]["headers"])
        self.assertNotIn("location", report["response"]["headers"])
        self.assertFalse(report["request"]["redirects_followed"])
        self.assertFalse(report["request"]["response_body_read"])
        self.assertEqual(report["execution"]["request_count"], 1)

    def test_web_api_adapter_rejects_unsafe_or_ambiguous_url_scope(self):
        invalid = (
            "http://staging.example.test/",
            "https://user:pass@staging.example.test/",
            "https://staging.example.test/?token=x",
            "https://staging.example.test:8443/",
            "https://*.example.test/",
            "https://staging.example.test/a/../admin",
        )
        for scope in invalid:
            with self.subTest(scope=scope):
                with self.assertRaises(ValueError):
                    run_web_api_review(scope)

    def test_web_api_adapter_reports_bounded_request_failure(self):
        class Connection:
            def __init__(self, *args, **kwargs):
                self.closed = False
            def request(self, *args, **kwargs):
                raise TimeoutError("details are not copied into report")
            def close(self):
                self.closed = True

        with patch("workflow_adapters.http.client.HTTPSConnection", Connection):
            report = run_web_api_review("https://staging.example.test/")
        self.assertEqual(report["request_status"], "request_failed")
        self.assertEqual(report["error_type"], "TimeoutError")
        self.assertNotIn("details", report)
        self.assertTrue(report["execution"]["network_actions_executed"])

    def test_unapproved_workflows_remain_plan_only(self):
        with self.assertRaisesRegex(ValueError, "No execution adapter is approved"):
            run_workflow_adapter("unknown-external-workflow", "https://staging.example.test")


if __name__ == "__main__":
    unittest.main()
