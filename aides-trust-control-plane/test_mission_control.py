import unittest
from decimal import Decimal

from moat import OutcomeStatus
from mission_control import MissionControlRecord


def record(**changes):
    values = dict(
        mission_id="mission-001",
        commissioned_by="human://deployer",
        authorised_worker_id="scout",
        allocation_ref="allocation://001",
        graph_ref="graph://scout/001",
        budget_gbp=Decimal("20.00"),
        measured_cost_gbp=Decimal("2.00"),
        human_gate_required=True,
        human_gate_approved=True,
        executed=True,
        outcome_status=OutcomeStatus.ACHIEVED,
        outcome_ref="outcome://001",
        verified_value_gbp=None,
        learning_ref=None,
        learning_approved=False,
    )
    values.update(changes)
    return MissionControlRecord(**values)


class MissionControlTests(unittest.TestCase):
    def test_valid_end_to_end_record(self):
        item = record()
        item.validate()
        self.assertEqual(item.economic_status, "INSUFFICIENT_VERIFIED_VALUE")
        self.assertIn("worker:scout", item.proof_chain())

    def test_human_gate_cannot_be_bypassed(self):
        with self.assertRaisesRegex(ValueError, "human gate"):
            record(human_gate_approved=False).validate()

    def test_budget_overrun_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "exceeds authorised budget"):
            record(measured_cost_gbp=Decimal("21.00")).validate()

    def test_unknown_outcome_cannot_claim_value(self):
        with self.assertRaisesRegex(ValueError, "unknown outcome"):
            record(outcome_status=OutcomeStatus.UNKNOWN, verified_value_gbp=Decimal("100")).validate()

    def test_unexecuted_mission_cannot_claim_success(self):
        with self.assertRaisesRegex(ValueError, "unexecuted mission"):
            record(executed=False, human_gate_approved=False).validate()

    def test_verified_value_calculates_net_only_when_present(self):
        item = record(verified_value_gbp=Decimal("50.00"))
        item.validate()
        self.assertEqual(item.net_verified_value_gbp, Decimal("48.00"))
        self.assertEqual(item.economic_status, "POSITIVE_VERIFIED_ECONOMICS")

    def test_approved_learning_requires_reference(self):
        with self.assertRaisesRegex(ValueError, "provenance ref"):
            record(learning_approved=True).validate()

    def test_unknown_outcome_cannot_be_authoritative_learning(self):
        with self.assertRaisesRegex(ValueError, "unknown outcome"):
            record(outcome_status=OutcomeStatus.UNKNOWN, learning_ref="learning://001", learning_approved=True).validate()


if __name__ == "__main__":
    unittest.main()
