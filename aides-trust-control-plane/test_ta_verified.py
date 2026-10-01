import unittest
from ta_verified import VerificationRecord, assert_verified

def record(**overrides):
    d=dict(
        claim="outcome", acceptance_criteria="deterministic pass", scenario="fixture-1",
        evidence_refs=["artifact://proof"], failure_correction_history=[], result="PASS",
        version="0.2", timestamp="2026-10-01T00:00:00Z", limitations=[],
        release_decision="VERIFIED_LIMITED_RELEASE", identity="AIDE:SCOUT",
        authority={"policy":"scout-v1","scope":"analysis"},
        action="produce verified outcome", cost={"currency":"GBP","amount":0.01},
        outcome={"status":"completed"}, value={"type":"verified_result","score":1},
        intervention_state="ALLOW")
    d.update(overrides)
    return VerificationRecord(**d)

class TaVerifiedTests(unittest.TestCase):
    def test_verified_record_passes(self): assert_verified(record())
    def test_no_evidence_fails(self):
        with self.assertRaises(ValueError): assert_verified(record(evidence_refs=[]))
    def test_failed_result_fails(self):
        with self.assertRaises(ValueError): assert_verified(record(result="FAIL"))
    def test_missing_authority_fails(self):
        with self.assertRaises(ValueError): assert_verified(record(authority={}))
    def test_missing_cost_fails(self):
        with self.assertRaises(ValueError): assert_verified(record(cost={}))
    def test_missing_value_fails(self):
        with self.assertRaises(ValueError): assert_verified(record(value={}))
    def test_unresolved_human_review_fails(self):
        with self.assertRaises(ValueError): assert_verified(record(intervention_state="HUMAN_REVIEW"))
    def test_stop_fails(self):
        with self.assertRaises(ValueError): assert_verified(record(intervention_state="STOP"))

if __name__ == "__main__": unittest.main()
