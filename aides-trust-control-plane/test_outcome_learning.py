import unittest

from moat import OutcomeStatus
from outcome_learning import LearningCandidate, LearningStatus, OutcomeLearningLedger


def candidate(learning_id="learn-001", *, outcome=OutcomeStatus.ACHIEVED, supersedes=None, correction=None):
    return LearningCandidate(
        learning_id=learning_id,
        transaction_id="tx-001",
        outcome_status=outcome,
        lesson_ref="lesson://sanitised/001",
        evidence_refs=("evidence://outcome/001",),
        supersedes_learning_id=supersedes,
        correction_ref=correction,
    )


class OutcomeLearningTests(unittest.TestCase):
    def test_proposed_learning_is_not_authoritative(self):
        ledger = OutcomeLearningLedger()
        item = ledger.propose(candidate())
        self.assertEqual(item.status, LearningStatus.PROPOSED)
        self.assertFalse(item.authoritative)
        self.assertEqual(ledger.authoritative(), ())

    def test_human_approval_promotes_learning(self):
        ledger = OutcomeLearningLedger()
        ledger.propose(candidate())
        approved = ledger.approve("learn-001", approved_by="deployer:anthony", decision_ref="decision://001")
        self.assertTrue(approved.authoritative)
        self.assertEqual(len(ledger.authoritative()), 1)

    def test_unknown_outcome_cannot_propose_learning(self):
        ledger = OutcomeLearningLedger()
        with self.assertRaisesRegex(ValueError, "unknown outcome"):
            ledger.propose(candidate(outcome=OutcomeStatus.UNKNOWN))

    def test_rejected_learning_never_becomes_authoritative(self):
        ledger = OutcomeLearningLedger()
        ledger.propose(candidate())
        rejected = ledger.reject("learn-001", decision_ref="decision://reject/001")
        self.assertEqual(rejected.status, LearningStatus.REJECTED)
        self.assertEqual(ledger.authoritative(), ())

    def test_correction_supersedes_without_erasing_history(self):
        ledger = OutcomeLearningLedger()
        ledger.propose(candidate())
        ledger.approve("learn-001", approved_by="deployer:anthony", decision_ref="decision://001")
        replacement = candidate("learn-002", supersedes="learn-001", correction="correction://001")
        proposed_replacement = ledger.supersede("learn-001", replacement)
        self.assertEqual(proposed_replacement.status, LearningStatus.PROPOSED)
        self.assertEqual(ledger.authoritative(), ())
        self.assertGreaterEqual(len(ledger.history()), 4)

    def test_revocation_preserves_provenance_and_removes_authority(self):
        ledger = OutcomeLearningLedger()
        ledger.propose(candidate())
        ledger.approve("learn-001", approved_by="deployer:anthony", decision_ref="decision://001")
        revoked = ledger.revoke("learn-001", correction_ref="correction://bad-assumption")
        self.assertEqual(revoked.status, LearningStatus.REVOKED)
        self.assertEqual(revoked.correction_ref, "correction://bad-assumption")
        self.assertEqual(ledger.authoritative(), ())


if __name__ == "__main__":
    unittest.main()
