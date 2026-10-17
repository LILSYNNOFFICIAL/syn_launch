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
        with self.assertRaisesRegex(ValueError, "source must use HTTPS"):
            APP.validate_catalog(broken)

    def test_check_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "main.py"), "--check"], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Catalog:", result.stdout)


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
