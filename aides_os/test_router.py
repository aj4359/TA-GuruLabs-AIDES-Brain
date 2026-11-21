import unittest
from router import plan, route

class RouterTests(unittest.TestCase):
    def test_read_only_assigned(self):
        r = route({"id":"1","type":"inspect","actions":["read"]})
        self.assertEqual(r["owner"], "Scout")
        self.assertEqual(r["status"], "ASSIGNED")

    def test_risky_action_needs_approval(self):
        for action in ("deploy", "spend", "merge", "delete", "secrets", "external_message", "live_trade"):
            with self.subTest(action=action):
                self.assertEqual(route({"id":"x","type":"prototype","actions":[action]})["status"],
                                 "APPROVAL_REQUIRED")

    def test_unknown_task_blocked(self):
        self.assertEqual(route({"id":"x","type":"anything"})["status"], "BLOCKED")

    def test_release_needs_approval(self):
        self.assertEqual(route({"id":"x","type":"release"})["status"], "APPROVAL_REQUIRED")

    def test_duplicate_ids_blocked(self):
        report = plan([{"id":"a","type":"inspect"},{"id":"a","type":"test"}])
        self.assertEqual(report["summary"]["BLOCKED"],1)

if __name__ == "__main__":
    unittest.main()
