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

    def test_bounded_probe_caps_output(self):
        output, truncated = APP.bounded_probe(
            [sys.executable, "-c", "print('A' * 5000)"], timeout=5, max_bytes=1024
        )
        self.assertTrue(truncated)
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

if __name__ == "__main__":
    unittest.main()
