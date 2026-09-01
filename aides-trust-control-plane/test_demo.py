import unittest

from demo import evaluate, load_json, run


class TrustControlPlaneTests(unittest.TestCase):
    def test_consequential_action_requires_human_approval(self):
        policy = load_json("policy.json")
        self.assertEqual(
            evaluate(policy, "scout", "contact_external_party"),
            "require_human_approval",
        )

    def test_human_denial_blocks_execution(self):
        events = run(approve=False)
        types = [event["event_type"] for event in events]
        self.assertIn("approval.denied", types)
        self.assertIn("execution.denied", types)
        self.assertNotIn("execution.started", types)

    def test_revocation_kills_before_execution(self):
        events = run(approve=True, kill_before_execution=True)
        types = [event["event_type"] for event in events]
        self.assertIn("authority.revoked", types)
        self.assertIn("execution.killed", types)
        self.assertNotIn("execution.started", types)

    def test_approved_path_records_outcome(self):
        events = run(approve=True)
        types = [event["event_type"] for event in events]
        self.assertIn("approval.granted", types)
        self.assertIn("execution.simulated", types)
        self.assertIn("outcome.recorded", types)


if __name__ == "__main__":
    unittest.main()
