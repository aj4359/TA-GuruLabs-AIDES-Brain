"""AIDES Mission Control v1: end-to-end governed mission proof.

Connects existing public-safe primitives without exposing private prompts,
routing heuristics, customer data or production topology. This module proves
state transitions and evidence boundaries; it is not a production executor.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from moat import OutcomeStatus


@dataclass(frozen=True)
class MissionControlRecord:
    mission_id: str
    commissioned_by: str
    authorised_worker_id: str
    allocation_ref: str
    graph_ref: str
    budget_gbp: Decimal
    measured_cost_gbp: Decimal
    human_gate_required: bool
    human_gate_approved: bool
    executed: bool
    outcome_status: OutcomeStatus
    outcome_ref: str
    verified_value_gbp: Optional[Decimal]
    learning_ref: Optional[str]
    learning_approved: bool

    def validate(self) -> None:
        required = (self.mission_id, self.commissioned_by, self.authorised_worker_id,
                    self.allocation_ref, self.graph_ref, self.outcome_ref)
        if not all(required):
            raise ValueError("mission identity and provenance references required")
        if self.budget_gbp < 0 or self.measured_cost_gbp < 0:
            raise ValueError("budget and measured cost cannot be negative")
        if self.measured_cost_gbp > self.budget_gbp:
            raise ValueError("mission spend exceeds authorised budget")
        if self.human_gate_required and self.executed and not self.human_gate_approved:
            raise ValueError("consequential execution cannot bypass human gate")
        if not self.executed and self.outcome_status not in (OutcomeStatus.UNKNOWN, OutcomeStatus.NOT_ACHIEVED):
            raise ValueError("unexecuted mission cannot claim achieved outcome")
        if self.outcome_status == OutcomeStatus.UNKNOWN and self.verified_value_gbp is not None:
            raise ValueError("unknown outcome cannot carry verified economic value")
        if self.verified_value_gbp is not None and self.verified_value_gbp < 0:
            raise ValueError("verified value cannot be negative")
        if self.learning_approved and not self.learning_ref:
            raise ValueError("approved learning requires provenance ref")
        if self.outcome_status == OutcomeStatus.UNKNOWN and self.learning_approved:
            raise ValueError("unknown outcome cannot create authoritative learning")

    @property
    def net_verified_value_gbp(self) -> Optional[Decimal]:
        if self.verified_value_gbp is None:
            return None
        return self.verified_value_gbp - self.measured_cost_gbp

    @property
    def economic_status(self) -> str:
        net = self.net_verified_value_gbp
        if net is None:
            return "INSUFFICIENT_VERIFIED_VALUE"
        return "POSITIVE_VERIFIED_ECONOMICS" if net > 0 else "NON_POSITIVE_VERIFIED_ECONOMICS"

    def proof_chain(self) -> Tuple[str, ...]:
        chain = (
            f"mission:{self.mission_id}",
            f"commissioned_by:{self.commissioned_by}",
            f"worker:{self.authorised_worker_id}",
            f"allocation:{self.allocation_ref}",
            f"graph:{self.graph_ref}",
            f"outcome:{self.outcome_ref}",
        )
        if self.learning_ref:
            chain += (f"learning:{self.learning_ref}",)
        return chain
