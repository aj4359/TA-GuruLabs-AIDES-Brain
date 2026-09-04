"""Public proof contracts for the TA GuruLabs governed-work moat.

These structures expose verifiable governance semantics without exposing private
orchestration, prompts, memory contents, routing logic, credentials or topology.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Optional, Tuple


class OutcomeStatus(str, Enum):
    UNKNOWN = "unknown"
    OBSERVED = "observed"
    PARTIAL = "partial"
    ACHIEVED = "achieved"
    NOT_ACHIEVED = "not_achieved"
    REVERSED = "reversed"


@dataclass(frozen=True)
class AuthorityLineage:
    commissioned_by: str
    built_by: str
    deployed_by: str
    supervised_by: str
    deployment_context: str
    permitted_actions: FrozenSet[str] = field(default_factory=frozenset)
    stop_authorities: FrozenSet[str] = field(default_factory=frozenset)

    def deployment_permitted(self, action: str) -> bool:
        return action in self.permitted_actions

    def stoppable_by(self, actor_id: str) -> bool:
        return actor_id in self.stop_authorities


@dataclass(frozen=True)
class EvidenceReference:
    evidence_id: str
    source_type: str
    source_ref: str
    observed_at: str


@dataclass(frozen=True)
class OutcomeEvidence:
    transaction_id: str
    intended_result: str
    observed_result: Optional[str]
    status: OutcomeStatus
    evidence: Tuple[EvidenceReference, ...] = ()
    confidence: Optional[float] = None
    causation_claimed: bool = False
    correction_ref: Optional[str] = None

    def validate(self) -> None:
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if self.status != OutcomeStatus.UNKNOWN and not self.observed_result:
            raise ValueError("observed_result is required for a non-unknown outcome")
        if self.status == OutcomeStatus.UNKNOWN and self.causation_claimed:
            raise ValueError("causation cannot be claimed when outcome is unknown")

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)


@dataclass(frozen=True)
class LearningEvent:
    transaction_id: str
    outcome_status: OutcomeStatus
    lesson_ref: str
    correction_ref: Optional[str] = None
    approved_for_memory: bool = False

    def public_record(self) -> dict:
        """Return safe metadata only. Private lesson content stays outside this repo."""
        return {
            "transaction_id": self.transaction_id,
            "outcome_status": self.outcome_status.value,
            "lesson_ref": self.lesson_ref,
            "correction_ref": self.correction_ref,
            "approved_for_memory": self.approved_for_memory,
        }
