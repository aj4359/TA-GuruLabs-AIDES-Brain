"""Measured-cost telemetry contract for the AIDES Workforce Economy.

This module normalises externally measured provider/tool/runtime costs into
SpendRecord objects. It intentionally does not estimate missing prices or
invent costs. Unknown/unpriced usage stays unknown until a trusted adapter
provides an explicit monetary amount and evidence reference.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from workforce_economy import SpendRecord


@dataclass(frozen=True)
class MeasuredCostEvent:
    mission_id: str
    worker_id: str
    category: str
    provider: str
    amount_gbp: Decimal
    evidence_ref: str
    measured_at: str
    usage_ref: str | None = None

    def validate(self) -> None:
        if not self.mission_id or not self.worker_id:
            raise ValueError("mission_id and worker_id are required")
        if not self.category or not self.provider:
            raise ValueError("category and provider are required")
        if self.amount_gbp < 0:
            raise ValueError("measured cost cannot be negative")
        if not self.evidence_ref:
            raise ValueError("measured cost requires an evidence reference")
        if not self.measured_at:
            raise ValueError("measured_at is required")

    def to_spend_record(self) -> SpendRecord:
        self.validate()
        return SpendRecord(
            mission_id=self.mission_id,
            worker_id=self.worker_id,
            category=self.category,
            amount_gbp=self.amount_gbp,
            evidence_ref=self.evidence_ref,
        )


class CostTelemetryLedger:
    """Append-only in-memory proof ledger for normalised measured costs."""

    def __init__(self) -> None:
        self._events: list[MeasuredCostEvent] = []
        self._evidence_refs: set[str] = set()

    def record(self, event: MeasuredCostEvent) -> None:
        event.validate()
        if event.evidence_ref in self._evidence_refs:
            raise ValueError("cost evidence already recorded")
        self._events.append(event)
        self._evidence_refs.add(event.evidence_ref)

    def events(self) -> tuple[MeasuredCostEvent, ...]:
        return tuple(self._events)

    def total_gbp(self, mission_id: str | None = None) -> Decimal:
        return sum(
            (
                event.amount_gbp
                for event in self._events
                if mission_id is None or event.mission_id == mission_id
            ),
            Decimal("0"),
        )

    def spend_records(self, mission_id: str | None = None) -> tuple[SpendRecord, ...]:
        return tuple(
            event.to_spend_record()
            for event in self._events
            if mission_id is None or event.mission_id == mission_id
        )


def record_measured_costs(
    ledger: CostTelemetryLedger,
    events: Iterable[MeasuredCostEvent],
) -> None:
    for event in events:
        ledger.record(event)
