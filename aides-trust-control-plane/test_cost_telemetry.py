import unittest
from decimal import Decimal

from cost_telemetry import CostTelemetryLedger, MeasuredCostEvent


class CostTelemetryTests(unittest.TestCase):
    def event(self, **overrides):
        data = {
            "mission_id": "mission-1",
            "worker_id": "scout",
            "category": "model",
            "provider": "provider-x",
            "amount_gbp": Decimal("1.25"),
            "evidence_ref": "billing://provider-x/usage/abc",
            "measured_at": "2026-09-05T13:20:00Z",
            "usage_ref": "usage://abc",
        }
        data.update(overrides)
        return MeasuredCostEvent(**data)

    def test_measured_cost_converts_to_spend_record(self):
        event = self.event()
        spend = event.to_spend_record()
        self.assertEqual(spend.amount_gbp, Decimal("1.25"))
        self.assertEqual(spend.evidence_ref, "billing://provider-x/usage/abc")

    def test_missing_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            self.event(evidence_ref="").validate()

    def test_negative_cost_is_rejected(self):
        with self.assertRaises(ValueError):
            self.event(amount_gbp=Decimal("-0.01")).validate()

    def test_duplicate_cost_evidence_is_rejected(self):
        ledger = CostTelemetryLedger()
        ledger.record(self.event())
        with self.assertRaises(ValueError):
            ledger.record(self.event())

    def test_total_is_based_only_on_recorded_measured_costs(self):
        ledger = CostTelemetryLedger()
        ledger.record(self.event())
        ledger.record(self.event(
            category="search",
            amount_gbp=Decimal("0.75"),
            evidence_ref="billing://provider-y/usage/def",
            provider="provider-y",
        ))
        self.assertEqual(ledger.total_gbp("mission-1"), Decimal("2.00"))


if __name__ == "__main__":
    unittest.main()
