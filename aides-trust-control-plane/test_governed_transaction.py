import unittest

from governed_transaction import GovernedTransactionProof, scout_internal_recommendation_proof
from moat import AuthorityLineage, EvidenceReference, LearningEvent, OutcomeEvidence, OutcomeStatus


class GovernedTransactionTests(unittest.TestCase):
    def test_sanitised_scout_proof_is_valid(self):
        proof = scout_internal_recommendation_proof()
        self.assertTrue(proof.executed)
        self.assertTrue(proof.approved)
        self.assertFalse(proof.outcome.causation_claimed)
        self.assertFalse(proof.learning.approved_for_memory)

    def test_execution_without_approval_is_rejected(self):
        tx = "tx-denied"
        authority = AuthorityLineage(
            commissioned_by="scout",
            built_by="codex",
            deployed_by="anthony",
            supervised_by="stratos",
            deployment_context="test",
            permitted_actions=frozenset({"contact_external_party"}),
            stop_authorities=frozenset({"anthony"}),
        )
        evidence = EvidenceReference("ev", "test", "test://evidence", "2026-09-04T00:00:00Z")
        outcome = OutcomeEvidence(tx, "send message", None, OutcomeStatus.UNKNOWN)
        learning = LearningEvent(tx, OutcomeStatus.UNKNOWN, "private-memory://lesson/denied")
        proof = GovernedTransactionProof(tx, "contact_external_party", authority, evidence, False, True, outcome, learning)
        with self.assertRaises(ValueError):
            proof.validate()

    def test_out_of_authority_action_is_rejected(self):
        proof = scout_internal_recommendation_proof()
        altered = GovernedTransactionProof(
            transaction_id=proof.transaction_id,
            action="contact_external_party",
            authority=proof.authority,
            evidence=proof.evidence,
            approved=True,
            executed=True,
            outcome=proof.outcome,
            learning=proof.learning,
        )
        with self.assertRaises(ValueError):
            altered.validate()


if __name__ == "__main__":
    unittest.main()
