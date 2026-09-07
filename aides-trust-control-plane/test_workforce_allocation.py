import unittest
from decimal import Decimal

from workforce_allocation import AllocationCandidate, recommend


def c(cid, *, authorised=True, risk=True, cost="1.00", latency=100, verified=10, success=8):
    return AllocationCandidate(
        candidate_id=cid,
        worker_id="scout",
        configuration_ref=f"config://{cid}",
        authority_eligible=authorised,
        risk_within_limit=risk,
        measured_cost_gbp=None if cost is None else Decimal(cost),
        median_latency_seconds=latency,
        verified_outcomes=verified,
        successful_verified_outcomes=success,
        evidence_ref=f"evidence://{cid}",
    )


class WorkforceAllocationTests(unittest.TestCase):
    def test_unauthorised_candidate_is_never_selected(self):
        result = recommend((c("cheap", authorised=False, cost="0.01", success=10), c("allowed", cost="2.00")), rationale_ref="decision://001")
        self.assertEqual(result.selected_candidate_id, "allowed")
        self.assertNotIn("cheap", result.eligible_candidate_ids)

    def test_risk_exceeding_candidate_is_never_selected(self):
        result = recommend((c("fast", risk=False, latency=1, success=10), c("safe", latency=200)), rationale_ref="decision://002")
        self.assertEqual(result.selected_candidate_id, "safe")

    def test_unknown_economics_do_not_become_zero_cost(self):
        result = recommend((c("unknown", cost=None), c("known", cost="4.00")), rationale_ref="decision://003")
        self.assertEqual(result.selected_candidate_id, "known")
        self.assertIn("unknown", result.insufficient_evidence_candidate_ids)

    def test_no_complete_evidence_returns_insufficient_evidence(self):
        result = recommend((c("unknown", cost=None),), rationale_ref="decision://004")
        self.assertIsNone(result.selected_candidate_id)
        self.assertEqual(result.status, "INSUFFICIENT_EVIDENCE")

    def test_verified_history_precedes_cheapest_price(self):
        stronger = c("stronger", cost="5.00", verified=20, success=18)
        cheaper = c("cheaper", cost="0.50", verified=20, success=12)
        result = recommend((cheaper, stronger), rationale_ref="decision://005")
        self.assertEqual(result.selected_candidate_id, "stronger")

    def test_cost_breaks_equivalent_history_tie(self):
        result = recommend((c("expensive", cost="5.00"), c("efficient", cost="1.00")), rationale_ref="decision://006")
        self.assertEqual(result.selected_candidate_id, "efficient")

    def test_no_authorised_candidate_returns_no_selection(self):
        result = recommend((c("blocked", authorised=False),), rationale_ref="decision://007")
        self.assertIsNone(result.selected_candidate_id)
        self.assertEqual(result.status, "NO_AUTHORISED_CANDIDATE")


if __name__ == "__main__":
    unittest.main()
