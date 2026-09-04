import unittest

from moat import (
    AuthorityLineage,
    EvidenceReference,
    LearningEvent,
    OutcomeEvidence,
    OutcomeStatus,
)


class MoatContractTests(unittest.TestCase):
    def test_authority_is_explicit_and_stoppable(self):
        lineage = AuthorityLineage(
            commissioned_by="scout",
            built_by="codex",
            deployed_by="anthony",
            supervised_by="stratos",
            deployment_context="sanitised-proof",
            permitted_actions=frozenset({"create_internal_recommendation"}),
            stop_authorities=frozenset({"anthony", "cipher"}),
        )
        self.assertTrue(lineage.deployment_permitted("create_internal_recommendation"))
        self.assertFalse(lineage.deployment_permitted("contact_external_party"))
        self.assertTrue(lineage.stoppable_by("cipher"))

    def test_outcome_requires_observation_for_known_status(self):
        outcome = OutcomeEvidence(
            transaction_id="tx-001",
            intended_result="create a reviewed internal recommendation",
            observed_result=None,
            status=OutcomeStatus.ACHIEVED,
        )
        with self.assertRaises(ValueError):
            outcome.validate()

    def test_outcome_records_evidence_without_claiming_causation(self):
        evidence = EvidenceReference(
            evidence_id="ev-001",
            source_type="audit_event",
            source_ref="audit://tx-001/result",
            observed_at="2026-09-04T08:00:00Z",
        )
        outcome = OutcomeEvidence(
            transaction_id="tx-001",
            intended_result="create a reviewed internal recommendation",
            observed_result="recommendation created and review recorded",
            status=OutcomeStatus.ACHIEVED,
            evidence=(evidence,),
            confidence=0.95,
            causation_claimed=False,
        )
        outcome.validate()
        self.assertEqual(outcome.evidence_count, 1)
        self.assertFalse(outcome.causation_claimed)

    def test_unknown_outcome_cannot_claim_causation(self):
        outcome = OutcomeEvidence(
            transaction_id="tx-002",
            intended_result="improve conversion",
            observed_result=None,
            status=OutcomeStatus.UNKNOWN,
            causation_claimed=True,
        )
        with self.assertRaises(ValueError):
            outcome.validate()

    def test_confidence_is_bounded(self):
        outcome = OutcomeEvidence(
            transaction_id="tx-003",
            intended_result="reduce intervention latency",
            observed_result="latency measured",
            status=OutcomeStatus.OBSERVED,
            confidence=1.1,
        )
        with self.assertRaises(ValueError):
            outcome.validate()

    def test_learning_event_exposes_reference_not_private_lesson(self):
        event = LearningEvent(
            transaction_id="tx-001",
            outcome_status=OutcomeStatus.ACHIEVED,
            lesson_ref="private-memory://lesson/123",
            correction_ref="private-memory://correction/9",
            approved_for_memory=True,
        )
        public = event.public_record()
        self.assertEqual(public["lesson_ref"], "private-memory://lesson/123")
        self.assertNotIn("lesson", public)
        self.assertTrue(public["approved_for_memory"])


if __name__ == "__main__":
    unittest.main()
