"""Sanitised outcome ledger for governed autonomous work.

The ledger records evidence-backed outcome summaries. It is not a causal inference
engine and does not expose private learning content or orchestration internals.
"""
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from moat import OutcomeEvidence, OutcomeStatus


@dataclass(frozen=True)
class OutcomeLedgerEntry:
    transaction_id: str
    intended_result: str
    status: OutcomeStatus
    observed_result: Optional[str]
    evidence_count: int
    confidence: Optional[float]
    causation_claimed: bool
    learning_ref: Optional[str]
    recorded_at: str


class OutcomeLedger:
    def __init__(self) -> None:
        self._entries: dict[str, OutcomeLedgerEntry] = {}

    def record(
        self,
        outcome: OutcomeEvidence,
        *,
        learning_ref: Optional[str],
        recorded_at: str,
    ) -> OutcomeLedgerEntry:
        outcome.validate()
        if outcome.transaction_id in self._entries:
            raise ValueError("outcome already recorded for transaction")
        entry = OutcomeLedgerEntry(
            transaction_id=outcome.transaction_id,
            intended_result=outcome.intended_result,
            status=outcome.status,
            observed_result=outcome.observed_result,
            evidence_count=outcome.evidence_count,
            confidence=outcome.confidence,
            causation_claimed=outcome.causation_claimed,
            learning_ref=learning_ref,
            recorded_at=recorded_at,
        )
        self._entries[entry.transaction_id] = entry
        return entry

    def get(self, transaction_id: str) -> Optional[OutcomeLedgerEntry]:
        return self._entries.get(transaction_id)

    def entries(self) -> Tuple[OutcomeLedgerEntry, ...]:
        return tuple(self._entries.values())

    def status_counts(self) -> dict[str, int]:
        counts = {status.value: 0 for status in OutcomeStatus}
        for entry in self._entries.values():
            counts[entry.status.value] += 1
        return counts

    def evidence_coverage(self) -> dict[str, int]:
        entries = self.entries()
        return {
            "total": len(entries),
            "with_evidence": sum(1 for e in entries if e.evidence_count > 0),
            "without_evidence": sum(1 for e in entries if e.evidence_count == 0),
        }
