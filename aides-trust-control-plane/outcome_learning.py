"""Governed Outcome Learning v1.

Outcomes may propose learning, but no learning becomes authoritative memory
without explicit approval and provenance. Public-safe metadata only: no private
memory contents, prompts, customer data or proprietary learning heuristics.
"""
from dataclasses import dataclass, replace
from enum import Enum
from typing import Optional, Tuple

from moat import OutcomeStatus


class LearningStatus(str, Enum):
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"
    REVOKED = "REVOKED"


@dataclass(frozen=True)
class LearningCandidate:
    learning_id: str
    transaction_id: str
    outcome_status: OutcomeStatus
    lesson_ref: str
    evidence_refs: Tuple[str, ...]
    status: LearningStatus = LearningStatus.PROPOSED
    approved_by: Optional[str] = None
    decision_ref: Optional[str] = None
    supersedes_learning_id: Optional[str] = None
    correction_ref: Optional[str] = None

    def validate(self) -> None:
        if not self.learning_id or not self.transaction_id or not self.lesson_ref:
            raise ValueError("learning, transaction and lesson references required")
        if not self.evidence_refs:
            raise ValueError("learning requires outcome evidence references")
        if self.outcome_status == OutcomeStatus.UNKNOWN:
            raise ValueError("unknown outcome cannot become a learning candidate")
        if self.status == LearningStatus.APPROVED and (not self.approved_by or not self.decision_ref):
            raise ValueError("approved learning requires approver and decision provenance")
        if self.status != LearningStatus.APPROVED and self.approved_by:
            raise ValueError("only approved learning may carry approver")

    @property
    def authoritative(self) -> bool:
        return self.status == LearningStatus.APPROVED


class OutcomeLearningLedger:
    def __init__(self) -> None:
        self._history = []
        self._latest = {}

    def propose(self, candidate: LearningCandidate) -> LearningCandidate:
        candidate.validate()
        if candidate.learning_id in self._latest:
            raise ValueError("duplicate learning id")
        self._history.append(candidate)
        self._latest[candidate.learning_id] = candidate
        return candidate

    def approve(self, learning_id: str, *, approved_by: str, decision_ref: str) -> LearningCandidate:
        current = self._require(learning_id)
        if current.status != LearningStatus.PROPOSED:
            raise ValueError("only proposed learning can be approved")
        if not approved_by or not decision_ref:
            raise ValueError("approval requires human/deployer identity and decision ref")
        updated = replace(current, status=LearningStatus.APPROVED, approved_by=approved_by, decision_ref=decision_ref)
        updated.validate()
        return self._record(updated)

    def reject(self, learning_id: str, *, decision_ref: str) -> LearningCandidate:
        current = self._require(learning_id)
        if current.status != LearningStatus.PROPOSED or not decision_ref:
            raise ValueError("proposed learning and decision ref required")
        return self._record(replace(current, status=LearningStatus.REJECTED, decision_ref=decision_ref))

    def supersede(self, old_learning_id: str, replacement: LearningCandidate) -> LearningCandidate:
        old = self._require(old_learning_id)
        if old.status != LearningStatus.APPROVED:
            raise ValueError("only approved learning can be superseded")
        if not replacement.correction_ref or replacement.supersedes_learning_id != old_learning_id:
            raise ValueError("replacement requires correction provenance and supersedes ref")
        replacement.validate()
        self._record(replace(old, status=LearningStatus.SUPERSEDED))
        return self.propose(replacement)

    def revoke(self, learning_id: str, *, correction_ref: str) -> LearningCandidate:
        current = self._require(learning_id)
        if current.status != LearningStatus.APPROVED or not correction_ref:
            raise ValueError("approved learning and correction ref required")
        return self._record(replace(current, status=LearningStatus.REVOKED, correction_ref=correction_ref))

    def authoritative(self) -> Tuple[LearningCandidate, ...]:
        return tuple(item for item in self._latest.values() if item.authoritative)

    def history(self) -> Tuple[LearningCandidate, ...]:
        return tuple(self._history)

    def _require(self, learning_id: str) -> LearningCandidate:
        if learning_id not in self._latest:
            raise KeyError(learning_id)
        return self._latest[learning_id]

    def _record(self, candidate: LearningCandidate) -> LearningCandidate:
        self._history.append(candidate)
        self._latest[candidate.learning_id] = candidate
        return candidate
