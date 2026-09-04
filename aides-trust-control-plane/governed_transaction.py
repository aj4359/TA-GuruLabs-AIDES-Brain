"""Sanitised end-to-end governed work proof."""
from dataclasses import dataclass
from moat import AuthorityLineage, EvidenceReference, LearningEvent, OutcomeEvidence, OutcomeStatus


@dataclass(frozen=True)
class GovernedTransactionProof:
    transaction_id: str
    action: str
    authority: AuthorityLineage
    evidence: EvidenceReference
    approved: bool
    executed: bool
    outcome: OutcomeEvidence
    learning: LearningEvent

    def validate(self) -> None:
        if not self.authority.deployment_permitted(self.action):
            raise ValueError("action is outside deployer authority")
        if self.executed and not self.approved:
            raise ValueError("consequential execution requires approval")
        if self.outcome.transaction_id != self.transaction_id:
            raise ValueError("outcome transaction mismatch")
        if self.learning.transaction_id != self.transaction_id:
            raise ValueError("learning transaction mismatch")
        self.outcome.validate()


def scout_internal_recommendation_proof() -> GovernedTransactionProof:
    tx = "proof-scout-001"
    authority = AuthorityLineage(
        commissioned_by="scout",
        built_by="codex",
        deployed_by="anthony",
        supervised_by="stratos",
        deployment_context="sanitised-proof",
        permitted_actions=frozenset({"create_internal_recommendation"}),
        stop_authorities=frozenset({"anthony", "cipher"}),
    )
    evidence = EvidenceReference(
        evidence_id="ev-scout-001",
        source_type="public_signal",
        source_ref="sanitised://signal/material-change",
        observed_at="2026-09-04T00:00:00Z",
    )
    outcome = OutcomeEvidence(
        transaction_id=tx,
        intended_result="produce an internal recommendation for human review",
        observed_result="recommendation recorded for review",
        status=OutcomeStatus.ACHIEVED,
        evidence=(evidence,),
        confidence=0.95,
        causation_claimed=False,
    )
    learning = LearningEvent(
        transaction_id=tx,
        outcome_status=OutcomeStatus.ACHIEVED,
        lesson_ref="private-memory://lesson/proof-scout-001",
        approved_for_memory=False,
    )
    proof = GovernedTransactionProof(
        transaction_id=tx,
        action="create_internal_recommendation",
        authority=authority,
        evidence=evidence,
        approved=True,
        executed=True,
        outcome=outcome,
        learning=learning,
    )
    proof.validate()
    return proof
