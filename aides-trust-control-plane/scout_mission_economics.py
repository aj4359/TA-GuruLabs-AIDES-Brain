"""Scout mission economics proof contract.

Joins governed cost telemetry to an outcome reference without claiming ROI that
has not been independently verified. Public-safe contract only: no provider
credentials, private prompts, billing records, routing logic or memory content.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Optional

from cost_telemetry import MeasuredCostEvent


@dataclass(frozen=True)
class ScoutMissionEconomics:
    mission_id: str
    worker_id: str
    elapsed_seconds: int
    measured_cost_gbp: Decimal
    outcome_ref: str
    outcome_verified: bool
    verified_value_gbp: Optional[Decimal]
    net_verified_value_gbp: Optional[Decimal]
    economic_status: str


def build_scout_mission_economics(
    *,
    mission_id: str,
    worker_id: str,
    elapsed_seconds: int,
    cost_events: Iterable[MeasuredCostEvent],
    outcome_ref: str,
    outcome_verified: bool,
    verified_value_gbp: Optional[Decimal] = None,
) -> ScoutMissionEconomics:
    if elapsed_seconds < 0:
        raise ValueError("elapsed time cannot be negative")
    if not outcome_ref:
        raise ValueError("outcome reference required")

    events = tuple(cost_events)
    for event in events:
        event.validate()
        if event.mission_id != mission_id or event.worker_id != worker_id:
            raise ValueError("cost telemetry does not belong to mission/worker")

    evidence_refs = [event.evidence_ref for event in events]
    if len(evidence_refs) != len(set(evidence_refs)):
        raise ValueError("duplicate cost evidence")

    measured_cost = sum((event.amount_gbp for event in events), Decimal("0"))

    if not outcome_verified:
        if verified_value_gbp is not None:
            raise ValueError("unverified outcome cannot carry verified value")
        return ScoutMissionEconomics(
            mission_id=mission_id,
            worker_id=worker_id,
            elapsed_seconds=elapsed_seconds,
            measured_cost_gbp=measured_cost,
            outcome_ref=outcome_ref,
            outcome_verified=False,
            verified_value_gbp=None,
            net_verified_value_gbp=None,
            economic_status="OUTCOME_UNVERIFIED",
        )

    if verified_value_gbp is None:
        return ScoutMissionEconomics(
            mission_id=mission_id,
            worker_id=worker_id,
            elapsed_seconds=elapsed_seconds,
            measured_cost_gbp=measured_cost,
            outcome_ref=outcome_ref,
            outcome_verified=True,
            verified_value_gbp=None,
            net_verified_value_gbp=None,
            economic_status="VALUE_UNVERIFIED",
        )
    if verified_value_gbp < 0:
        raise ValueError("verified value cannot be negative")

    net = verified_value_gbp - measured_cost
    status = "POSITIVE_VERIFIED_ECONOMICS" if net > 0 else "NON_POSITIVE_VERIFIED_ECONOMICS"
    return ScoutMissionEconomics(
        mission_id=mission_id,
        worker_id=worker_id,
        elapsed_seconds=elapsed_seconds,
        measured_cost_gbp=measured_cost,
        outcome_ref=outcome_ref,
        outcome_verified=True,
        verified_value_gbp=verified_value_gbp,
        net_verified_value_gbp=net,
        economic_status=status,
    )
