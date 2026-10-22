import json
import subprocess
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class PhoneAndroidToolsetTests(unittest.TestCase):
    def test_toolset_has_exactly_75_unique_catalog_backed_tools(self):
        payload=json.loads((ROOT/"toolsets"/"phone-android-top75.json").read_text(encoding="utf-8"))
        catalog=json.loads((ROOT/"catalog.json").read_text(encoding="utf-8")); ids=[i for g in payload["groups"] for i in g["tool_ids"]]
        self.assertEqual(payload["tool_count"],75); self.assertEqual(len(ids),75); self.assertEqual(len(set(ids)),75)
        self.assertTrue(set(ids).issubset({t["id"] for t in catalog["tools"]})); self.assertEqual(payload["tool_count"],len(ids))
    def test_toolset_cli_emits_json_and_correct_summary(self):
        proc=subprocess.run([sys.executable,str(ROOT/"main.py"),"--toolset","phone-android-top75"],capture_output=True,text=True,timeout=20)
        self.assertEqual(proc.returncode,0,proc.stderr); payload=json.loads(proc.stdout)
        self.assertEqual(payload["tool_count"],75); self.assertEqual(payload["summary"]["catalog_entries_reused"],75)
        self.assertEqual(sum(len(g["tools"]) for g in payload["groups"]),75); self.assertIn("No tools were installed or executed",payload["note"])
    def test_unknown_toolset_fails_cleanly(self):
        proc=subprocess.run([sys.executable,str(ROOT/"main.py"),"--toolset","missing-toolset"],capture_output=True,text=True,timeout=20)
        self.assertEqual(proc.returncode,2); self.assertIn("unknown toolset",proc.stderr)
if __name__=="__main__": unittest.main()