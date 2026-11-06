import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("continuity_guard", pathlib.Path(__file__).parent / "guardian.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

class GuardianTests(unittest.TestCase):
    def test_integrity_and_canon(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            (root / "canon.txt").write_text("Mateo Cruz is the Sicario", encoding="utf-8")
            sha = hashlib.sha256((root / "canon.txt").read_bytes()).hexdigest()
            m = {"id": "test", "project": "Sicario", "canon": "canon.txt",
                 "protected_assets": [{"path": "canon.txt", "sha256": sha}],
                 "required_phrases": [{"path": "canon.txt", "phrases": ["Mateo Cruz"]}]}
            self.assertEqual(guard.validate(root, m), [])
            (root / "canon.txt").write_text("Someone else", encoding="utf-8")
            errors = [x["code"] for x in guard.validate(root, m)]
            self.assertIn("HASH_DRIFT", errors)
            self.assertIn("CANON_DRIFT", errors)

    def test_missing_and_path_escape(self):
        with tempfile.TemporaryDirectory() as d:
            m = {"id": "test", "project": "Sicario", "canon": "canon.txt",
                 "protected_assets": [{"path": "../secret.txt"}, {"path": "lost.mp4"}]}
            codes = [x["code"] for x in guard.validate(pathlib.Path(d), m)]
            self.assertIn("INVALID_PATH", codes)
            self.assertIn("MISSING_ASSET", codes)

if __name__ == "__main__":
    unittest.main()
