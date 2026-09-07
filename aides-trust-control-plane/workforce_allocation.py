"""Governed Workforce Allocation v1.

Ranks only configurations already eligible under external authority/policy.
Allocation can recommend; it cannot grant authority, invent evidence, or turn
unknown economics into a score. Proprietary routing heuristics stay private.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple


@dataclass(frozen=True)
class AllocationCandidate:
    candidate_id: str
    worker_id: str
    configuration_ref: str
    authority_eligible: bool
    risk_within_limit: bool
    measured_cost_gbp: Optional[Decimal]
    median_latency_seconds: Optional[int]
    verified_outcomes: int
    successful_verified_outcomes: int
    evidence_ref: str

    def validate(self) -> None:
        if not self.candidate_id or not self.worker_id or not self.configuration_ref or not self.evidence_ref:
            raise ValueError("candidate identity, configuration and evidence ref required")
        if self.measured_cost_gbp is not None and self.measured_cost_gbp < 0:
            raise ValueError("measured cost cannot be negative")
        if self.median_latency_seconds is not None and self.median_latency_seconds < 0:
            raise ValueError("latency cannot be negative")
        if self.verified_outcomes < 0 or self.successful_verified_outcomes < 0:
            raise ValueError("outcome counts cannot be negative")
        if self.successful_verified_outcomes > self.verified_outcomes:
            raise ValueError("successful outcomes cannot exceed verified outcomes")

    @property
    def evidence_complete(self) -> bool:
        return self.measured_cost_gbp is not None and self.median_latency_seconds is not None and self.verified_outcomes > 0

    @property
    def success_rate(self) -> Optional[Decimal]:
        if self.verified_outcomes == 0:
            return None
        return Decimal(self.successful_verified_outcomes) / Decimal(self.verified_outcomes)


@dataclass(frozen=True)
class AllocationRecommendation:
    selected_candidate_id: Optional[str]
    status: str
    eligible_candidate_ids: Tuple[str, ...]
    insufficient_evidence_candidate_ids: Tuple[str, ...]
    rationale_ref: str


def recommend(candidates: Tuple[AllocationCandidate, ...], *, rationale_ref: str) -> AllocationRecommendation:
    if not rationale_ref:
        raise ValueError("rationale provenance required")
    if len({c.candidate_id for c in candidates}) != len(candidates):
        raise ValueError("duplicate candidate id")
    for candidate in candidates:
        candidate.validate()

    eligible = tuple(c for c in candidates if c.authority_eligible and c.risk_within_limit)
    if not eligible:
        return AllocationRecommendation(None, "NO_AUTHORISED_CANDIDATE", (), (), rationale_ref)

    complete = tuple(c for c in eligible if c.evidence_complete)
    incomplete = tuple(c.candidate_id for c in eligible if not c.evidence_complete)
    if not complete:
        return AllocationRecommendation(None, "INSUFFICIENT_EVIDENCE", tuple(c.candidate_id for c in eligible), incomplete, rationale_ref)

    # Public-safe deterministic baseline, not TA GuruLabs' proprietary router.
    # Evidence quality is primary; cost and latency only break equivalent-history ties.
    selected = sorted(
        complete,
        key=lambda c: (
            -c.success_rate,
            -c.verified_outcomes,
            c.measured_cost_gbp,
            c.median_latency_seconds,
            c.candidate_id,
        ),
    )[0]
    return AllocationRecommendation(
        selected.candidate_id,
        "RECOMMENDATION_ONLY",
        tuple(c.candidate_id for c in eligible),
        incomplete,
        rationale_ref,
    )
