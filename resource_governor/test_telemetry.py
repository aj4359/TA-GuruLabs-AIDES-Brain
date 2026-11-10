import tempfile
import unittest
from pathlib import Path

from resource_governor.telemetry import Telemetry


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "usage.sqlite3"
        self.t = Telemetry(self.path)

    def test_real_usage_unknown_cost_is_not_zero(self):
        event = dict(event_id="req_1", workflow="Scout", provider="openai",
                     model="example-model", input_tokens=150,
                     output_tokens=20, source="provider_usage_response")
        self.assertTrue(self.t.record(**event))
        self.assertFalse(self.t.record(**event))
        summary = self.t.summary()[0]
        self.assertEqual(summary["runs"], 1)
        self.assertEqual(summary["input_tokens"], 150)
        self.assertIsNone(summary["reported_spend_usd"])
        self.assertEqual(summary["unknown_cost_events"], 1)

    def test_persists_between_instances(self):
        self.t.record(event_id="req_2", workflow="Scout", provider="anthropic",
                      model="example", source="provider_bill",
                      provider_cost_usd=0.02, success=False)
        another = Telemetry(self.path)
        self.assertEqual(another.summary()[0]["reported_spend_usd"], 0.02)
        self.assertEqual(another.summary()[0]["failures"], 1)

    def test_rejects_bad_values(self):
        common = dict(event_id="a", workflow="scout", provider="p",
                      model="m", source="response")
        with self.assertRaises(ValueError):
            self.t.record(**common, provider_cost_usd=float("nan"))
        with self.assertRaises(ValueError):
            self.t.record(**common, input_tokens=-2)
        with self.assertRaises(ValueError):
            self.t.record(**common, duration_ms=1.5)


if __name__ == "__main__":
    unittest.main()
