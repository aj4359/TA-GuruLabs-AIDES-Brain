import unittest

from intervention_metrics import (
    intervention_latency_seconds,
    intervention_slo_status,
    mean_time_to_intervention,
)


class InterventionMetricTests(unittest.TestCase):
    def test_latency_seconds(self):
        self.assertEqual(
            intervention_latency_seconds("2026-09-03T10:00:00Z", "2026-09-03T10:00:07Z"),
            7,
        )

    def test_mean_time_to_intervention(self):
        events = [
            {"detected_at": "2026-09-03T10:00:00Z", "enforced_at": "2026-09-03T10:00:04Z"},
            {"detected_at": "2026-09-03T11:00:00Z", "enforced_at": "2026-09-03T11:00:08Z"},
        ]
        self.assertEqual(mean_time_to_intervention(events), 6)

    def test_negative_latency_is_rejected(self):
        with self.assertRaises(ValueError):
            intervention_latency_seconds("2026-09-03T10:00:10Z", "2026-09-03T10:00:00Z")

    def test_slo_status_requires_evidence(self):
        self.assertEqual(intervention_slo_status(None, 10), "insufficient_evidence")
        self.assertEqual(intervention_slo_status(6, 10), "within_target")
        self.assertEqual(intervention_slo_status(12, 10), "outside_target")


if __name__ == "__main__":
    unittest.main()
