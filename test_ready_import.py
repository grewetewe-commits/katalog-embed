import json
from pathlib import Path
import tempfile
import unittest
from ready_import import import_ready

class ReadyImportTest(unittest.TestCase):
    def test_actual_bank_preserves_body_and_layering(self):
        data = json.loads(Path("bank/ready_outfits.json").read_text(encoding="utf-8"))
        st = {"outfit": {}, "meta": {}}
        self.assertEqual(import_ready(st), len(data["seeds"]))
        for original in data["seeds"]:
            s = st["outfit"][original["H"]]
            for field in ("BP", "SC", "AM", "BC", "Origin"):
                self.assertEqual(s[field], original[field])
            self.assertTrue(s["K"].startswith("ready:"))
        self.assertEqual(import_ready(st), 0)

    def test_bad_ids_and_scales_do_not_enter_training(self):
        data = json.loads(Path("bank/ready_outfits.json").read_text(encoding="utf-8"))
        seed = data["seeds"][0]
        seed["SC"][0] = True
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "bank.json"
            p.write_text(json.dumps({"schema": 1, "seeds": [seed], "meta": {}}))
            st = {"outfit": {}, "meta": {}}
            self.assertEqual(import_ready(st, p), 0)
            self.assertEqual(st["outfit"], {})

if __name__ == "__main__":
    unittest.main()
