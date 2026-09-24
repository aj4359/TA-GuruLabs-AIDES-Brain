import unittest
from ta_verified import VerificationRecord, assert_verified

def record(**overrides):
    d=dict(claim="outcome",acceptance_criteria="deterministic pass",scenario="fixture-1",evidence_refs=["artifact://proof"],failure_correction_history=[],result="PASS",version="0.1",timestamp="2026-09-24T00:00:00Z",limitations=[],release_decision="VERIFIED_LIMITED_RELEASE")
    d.update(overrides)
    return VerificationRecord(**d)

class TaVerifiedTests(unittest.TestCase):
    def test_verified_record_passes(self):
        assert_verified(record())
    def test_no_evidence_fails(self):
        with self.assertRaises(ValueError):
            assert_verified(record(evidence_refs=[]))
    def test_failed_result_fails(self):
        with self.assertRaises(ValueError):
            assert_verified(record(result="FAIL"))

if __name__ == "__main__":
    unittest.main()
