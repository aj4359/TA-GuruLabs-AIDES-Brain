import unittest

from moat import EvidenceReference, OutcomeEvidence, OutcomeStatus
from outcome_ledger import OutcomeLedger


class OutcomeLedgerTests(unittest.TestCase):
    def setUp(self):
        self.ledger = OutcomeLedger()

    def test_records_evidence_backed_outcome(self):
        outcome = OutcomeEvidence(
            transaction_id="tx-100",
            intended_result="produce a reviewed internal recommendation",
            observed_result="recommendation created and review recorded",
            status=OutcomeStatus.ACHIEVED,
            evidence=(EvidenceReference("ev-1", "audit_event", "audit://tx-100/result", "2026-09-04T15:00:00Z"),),
            confidence=0.95,
        )
        entry = self.ledger.record(outcome, learning_ref="private-memory://lesson/100", recorded_at="2026-09-04T15:01:00Z")
        self.assertEqual(entry.evidence_count, 1)
        self.assertFalse(entry.causation_claimed)
        self.assertEqual(self.ledger.evidence_coverage()["with_evidence"], 1)

    def test_unknown_outcome_is_visible_not_fabricated(self):
        outcome = OutcomeEvidence(
            transaction_id="tx-101",
            intended_result="improve customer comprehension",
            observed_result=None,
            status=OutcomeStatus.UNKNOWN,
        )
        entry = self.ledger.record(outcome, learning_ref=None, recorded_at="2026-09-04T15:02:00Z")
        self.assertEqual(entry.status, OutcomeStatus.UNKNOWN)
        self.assertEqual(self.ledger.evidence_coverage()["without_evidence"], 1)

    def test_duplicate_transaction_outcome_is_rejected(self):
        outcome = OutcomeEvidence("tx-102", "test", None, OutcomeStatus.UNKNOWN)
        self.ledger.record(outcome, learning_ref=None, recorded_at="2026-09-04T15:03:00Z")
        with self.assertRaises(ValueError):
            self.ledger.record(outcome, learning_ref=None, recorded_at="2026-09-04T15:04:00Z")

    def test_status_counts_make_unknowns_visible(self):
        self.ledger.record(OutcomeEvidence("tx-103", "a", None, OutcomeStatus.UNKNOWN), learning_ref=None, recorded_at="2026-09-04T15:05:00Z")
        self.ledger.record(OutcomeEvidence("tx-104", "b", "observed", OutcomeStatus.PARTIAL), learning_ref=None, recorded_at="2026-09-04T15:06:00Z")
        counts = self.ledger.status_counts()
        self.assertEqual(counts["unknown"], 1)
        self.assertEqual(counts["partial"], 1)
        self.assertEqual(counts["achieved"], 0)


if __name__ == "__main__":
    unittest.main()
