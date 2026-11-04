"""Harness verification regression tests: run with python -m unittest discover -s harness."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from harness.runner import load_contract, run, resolve_inside


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "project"
        self.root.mkdir()
        self.state = self.base / "state"
        self.contract_file = self.base / "task.json"

    def contract(self, checks):
        self.contract_file.write_text(json.dumps({
            "task_id": "demo_001", "goal": "Verify demo output",
            "root": str(self.root), "checks": checks
        }), encoding="utf-8")

    def test_valid_artifact_receipt(self):
        (self.root / "output.json").write_text('{"ok":true}', encoding="utf-8")
        self.contract([{"type": "json_valid", "path": "output.json"}])
        receipt = run(self.contract_file, self.state)
        self.assertEqual(receipt["status"], "verified_complete")
        self.assertEqual(receipt["attempts"], 1)
        self.assertTrue(receipt["evidence"][0]["passed"])
        self.assertEqual(len((self.state / "receipts.jsonl").read_text().splitlines()), 1)

    def test_missing_artifact_fails_closed(self):
        self.contract([{"type": "file_exists", "path": "missing.html"}])
        receipt = run(self.contract_file, self.state)
        self.assertEqual(receipt["status"], "needs_repair")
        self.assertTrue(receipt["human_review_required"])

    def test_invalid_json_fails(self):
        (self.root / "bad.json").write_text("{broken", encoding="utf-8")
        self.contract([{"type": "json_valid", "path": "bad.json"}])
        self.assertEqual(run(self.contract_file, self.state)["status"], "needs_repair")

    def test_no_checks_rejected(self):
        self.contract([])
        with self.assertRaises(ValueError):
            load_contract(self.contract_file)

    def test_unknown_check_rejected(self):
        self.contract([{"type": "shell", "path": "anything"}])
        with self.assertRaises(ValueError):
            load_contract(self.contract_file)

    def test_path_escape_blocked(self):
        with self.assertRaises(ValueError):
            resolve_inside(self.root, "../secrets.txt")
        with self.assertRaises(ValueError):
            resolve_inside(self.root, "/etc/passwd")

    def test_symlink_escape_blocked(self):
        external = self.base / "outside.json"
        external.write_text('{"secret": 1}', encoding="utf-8")
        (self.root / "link.json").symlink_to(external)
        self.contract([{"type": "json_valid", "path": "link.json"}])
        self.assertEqual(run(self.contract_file, self.state)["status"], "needs_repair")


if __name__ == "__main__":
    unittest.main()
