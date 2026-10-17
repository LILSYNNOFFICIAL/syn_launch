import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CatalogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((ROOT/"catalog.json").read_text(encoding="utf-8")); cls.tools=cls.data["tools"]
 def test_at_least_100_entries(self): self.assertGreaterEqual(len(self.tools),100)
 def test_unique_ids(self):
  ids=[t["id"] for t in self.tools]; self.assertEqual(len(ids),len(set(ids)))
 def test_required_fields_and_methods(self):
  allowed={"pkg","pip","go","manual","root"}
  for t in self.tools:
   for f in ("id","name","category","executable","install_kind","description","source","caveat"): self.assertTrue(t.get(f),f"{t.get('name')} missing {f}")
   self.assertIn(t["install_kind"],allowed)
   self.assertEqual(t["installable"],t["install_kind"] in {"pkg","pip","go"})
 def test_count_matches_metadata(self): self.assertEqual(self.data["tool_count"],len(self.tools))
 def test_categories_match(self): self.assertEqual(set(self.data["categories"]),{t["category"] for t in self.tools})
if __name__=="__main__": unittest.main()
