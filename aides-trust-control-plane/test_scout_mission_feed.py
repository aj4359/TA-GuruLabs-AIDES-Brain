import unittest
from dataclasses import replace
from decimal import Decimal

from moat import OutcomeStatus
from scout_mission_feed import ScoutMissionStage, sanitised_scout_example


class ScoutMissionFeedTests(unittest.TestCase):
    def test_sanitised_fixture_is_valid(self):
        feed = sanitised_scout_example()
        feed.validate()
        payload = feed.public_payload()
        self.assertEqual(payload["worker"], "scout")
        self.assertEqual(payload["verifiedValueGbp"], None)
        self.assertEqual(payload["learningStatus"], "PROPOSED")

    def test_unknown_outcome_cannot_expose_verified_value(self):
        feed = replace(
            sanitised_scout_example(),
            outcome_status=OutcomeStatus.UNKNOWN,
            outcome_ref=None,
            verified_value_gbp=Decimal("50.00"),
        )
        with self.assertRaisesRegex(ValueError, "unknown outcome"):
            feed.validate()

    def test_unknown_outcome_cannot_expose_approved_learning(self):
        feed = replace(
            sanitised_scout_example(),
            outcome_status=OutcomeStatus.UNKNOWN,
            outcome_ref=None,
            verified_value_gbp=None,
            learning_status="APPROVED",
        )
        with self.assertRaisesRegex(ValueError, "approved learning"):
            feed.validate()

    def test_measured_cost_cannot_exceed_budget(self):
        feed = replace(sanitised_scout_example(), measured_cost_gbp=Decimal("20.01"))
        with self.assertRaisesRegex(ValueError, "exceeds mission budget"):
            feed.validate()

    def test_observed_outcome_requires_reference(self):
        feed = replace(sanitised_scout_example(), outcome_ref=None)
        with self.assertRaisesRegex(ValueError, "outcome evidence ref"):
            feed.validate()

    def test_stage_status_must_be_supported(self):
        feed = replace(
            sanitised_scout_example(),
            stages=(ScoutMissionStage("VERIFY", "MAGIC", "verification://001"),),
        )
        with self.assertRaisesRegex(ValueError, "unsupported stage status"):
            feed.validate()


if __name__ == "__main__":
    unittest.main()
