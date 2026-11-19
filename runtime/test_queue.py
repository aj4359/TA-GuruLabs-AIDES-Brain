"""Run with: python -m unittest discover -s runtime -p 'test_*.py'."""
import tempfile
import unittest
from pathlib import Path
from queue import SimpleQueue
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue import SimpleQueue
import importlib.util

spec = importlib.util.spec_from_file_location("aides_queue", Path(__file__).with_name("queue.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class QueueTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.conn=module.db(Path(self.temp.name)/"q.sqlite3")
    def tearDown(self):
        self.conn.close()
        self.temp.cleanup()
    def task(self, approval="not_required"):
        return module.add(self.conn,"Review PAYE demo","quality_check","CONTINUITY_GUARD",
                          "PAYE Detective","Link to passing tests",approval)
    def test_evidence_required(self):
        t=self.task()
        module.change(self.conn,t,"running")
        with self.assertRaises(ValueError):module.change(self.conn,t,"done")
        module.change(self.conn,t,"done",evidence="tests/report.txt")
        self.assertEqual(module.list_tasks(self.conn)[0]["status"],"done")
    def test_approval_gate(self):
        t=self.task("required")
        with self.assertRaises(ValueError):module.change(self.conn,t,"running")
    def test_blocker_and_retry(self):
        t=self.task()
        with self.assertRaises(ValueError):module.change(self.conn,t,"blocked")
        module.change(self.conn,t,"blocked",blocker="Missing source asset")
        module.change(self.conn,t,"pending")
        self.assertEqual(module.list_tasks(self.conn)[0]["status"],"pending")
    def test_invalid_owner(self):
        with self.assertRaises(ValueError):
            module.add(self.conn,"x","quality_check","UNKNOWN","p","e")
if __name__=="__main__":
    unittest.main()
