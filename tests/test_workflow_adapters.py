import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from workflow_adapters import (
    run_device_configuration_audit,
    run_mobile_apk_inventory,
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

    def test_unapproved_workflows_remain_plan_only(self):
        with self.assertRaisesRegex(ValueError, "No execution adapter is approved"):
            run_workflow_adapter("web-api-review", "https://staging.example.test")


if __name__ == "__main__":
    unittest.main()
