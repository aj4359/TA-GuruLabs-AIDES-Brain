import unittest
from decimal import Decimal

from cost_telemetry import MeasuredCostEvent
from scout_mission_economics import build_scout_mission_economics


def cost(amount: str, ref: str, *, mission: str = "scout-001") -> MeasuredCostEvent:
    return MeasuredCostEvent(
        mission_id=mission,
        worker_id="scout",
        category="model",
        provider="provider-neutral",
        amount_gbp=Decimal(amount),
        evidence_ref=ref,
        measured_at="2026-09-06T20:00:00Z",
    )


class ScoutMissionEconomicsTests(unittest.TestCase):
    def test_unverified_outcome_never_creates_roi(self):
        result = build_scout_mission_economics(
            mission_id="scout-001", worker_id="scout", elapsed_seconds=198,
            cost_events=[cost("0.84", "billing://001")],
            outcome_ref="outcome://scout-001", outcome_verified=False,
        )
        self.assertEqual(result.measured_cost_gbp, Decimal("0.84"))
        self.assertIsNone(result.verified_value_gbp)
        self.assertIsNone(result.net_verified_value_gbp)
        self.assertEqual(result.economic_status, "OUTCOME_UNVERIFIED")

    def test_verified_outcome_without_verified_value_stays_unknown(self):
        result = build_scout_mission_economics(
            mission_id="scout-001", worker_id="scout", elapsed_seconds=101,
            cost_events=[cost("3.62", "billing://002")],
            outcome_ref="outcome://scout-001", outcome_verified=True,
        )
        self.assertEqual(result.economic_status, "VALUE_UNVERIFIED")
        self.assertIsNone(result.net_verified_value_gbp)

    def test_verified_value_produces_net_economics(self):
        result = build_scout_mission_economics(
            mission_id="scout-001", worker_id="scout", elapsed_seconds=101,
            cost_events=[cost("3.62", "billing://003")],
            outcome_ref="outcome://scout-001", outcome_verified=True,
            verified_value_gbp=Decimal("50.00"),
        )
        self.assertEqual(result.net_verified_value_gbp, Decimal("46.38"))
        self.assertEqual(result.economic_status, "POSITIVE_VERIFIED_ECONOMICS")

    def test_unverified_outcome_rejects_verified_value(self):
        with self.assertRaises(ValueError):
            build_scout_mission_economics(
                mission_id="scout-001", worker_id="scout", elapsed_seconds=10,
                cost_events=[], outcome_ref="outcome://scout-001",
                outcome_verified=False, verified_value_gbp=Decimal("100"),
            )

    def test_cross_mission_cost_is_rejected(self):
        with self.assertRaises(ValueError):
            build_scout_mission_economics(
                mission_id="scout-001", worker_id="scout", elapsed_seconds=10,
                cost_events=[cost("1.00", "billing://004", mission="other")],
                outcome_ref="outcome://scout-001", outcome_verified=False,
            )


if __name__ == "__main__":
    unittest.main()
