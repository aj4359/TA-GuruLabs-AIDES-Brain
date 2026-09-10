"""Public-safe Scout Mission Feed v1.

Transforms governed Scout mission records into a display payload for Mission
Control. It exposes only sanitised references and measured/verified states.
Private prompts, source-selection heuristics, credentials, routing logic and
memory contents remain outside this contract.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from moat import OutcomeStatus


@dataclass(frozen=True)
class ScoutMissionStage:
    name: str
    status: str
    evidence_ref: Optional[str] = None

    def validate(self) -> None:
        if not self.name:
            raise ValueError("stage name required")
        if self.status not in {"COMPLETE", "PENDING", "BLOCKED", "INSUFFICIENT_EVIDENCE"}:
            raise ValueError("unsupported stage status")


@dataclass(frozen=True)
class ScoutMissionFeed:
    mission_id: str
    mission_summary: str
    commissioned_by_ref: str
    worker_id: str
    budget_gbp: Decimal
    measured_cost_gbp: Optional[Decimal]
    outcome_status: OutcomeStatus
    outcome_ref: Optional[str]
    verified_value_gbp: Optional[Decimal]
    learning_status: str
    stages: Tuple[ScoutMissionStage, ...]

    def validate(self) -> None:
        if not self.mission_id or not self.mission_summary or not self.commissioned_by_ref or not self.worker_id:
            raise ValueError("mission identity and public provenance required")
        if self.budget_gbp < 0:
            raise ValueError("budget cannot be negative")
        if self.measured_cost_gbp is not None:
            if self.measured_cost_gbp < 0:
                raise ValueError("measured cost cannot be negative")
            if self.measured_cost_gbp > self.budget_gbp:
                raise ValueError("measured cost exceeds mission budget")
        if self.outcome_status == OutcomeStatus.UNKNOWN:
            if self.verified_value_gbp is not None:
                raise ValueError("unknown outcome cannot expose verified value")
            if self.learning_status == "APPROVED":
                raise ValueError("unknown outcome cannot expose approved learning")
        if self.verified_value_gbp is not None and self.verified_value_gbp < 0:
            raise ValueError("verified value cannot be negative")
        if self.outcome_status != OutcomeStatus.UNKNOWN and not self.outcome_ref:
            raise ValueError("observed outcome requires outcome evidence ref")
        if not self.stages:
            raise ValueError("mission feed requires stages")
        for stage in self.stages:
            stage.validate()

    def public_payload(self) -> dict:
        self.validate()
        return {
            "missionId": self.mission_id,
            "mission": self.mission_summary,
            "commissionedBy": self.commissioned_by_ref,
            "worker": self.worker_id,
            "budgetGbp": str(self.budget_gbp),
            "measuredCostGbp": None if self.measured_cost_gbp is None else str(self.measured_cost_gbp),
            "outcome": self.outcome_status.value,
            "outcomeRef": self.outcome_ref,
            "verifiedValueGbp": None if self.verified_value_gbp is None else str(self.verified_value_gbp),
            "learningStatus": self.learning_status,
            "stages": [
                {"label": s.name, "status": s.status, "evidenceRef": s.evidence_ref}
                for s in self.stages
            ],
        }


def sanitised_scout_example() -> ScoutMissionFeed:
    """Deterministic fixture for demos/tests, explicitly not live telemetry."""
    return ScoutMissionFeed(
        mission_id="scout-proof-001",
        mission_summary="Identify one material market change and prepare an evidence-backed recommendation.",
        commissioned_by_ref="authority://human-deployer",
        worker_id="scout",
        budget_gbp=Decimal("20.00"),
        measured_cost_gbp=Decimal("3.62"),
        outcome_status=OutcomeStatus.ACHIEVED,
        outcome_ref="outcome://scout-proof-001",
        verified_value_gbp=None,
        learning_status="PROPOSED",
        stages=(
            ScoutMissionStage("COMMISSION", "COMPLETE", "authority://scout-proof-001"),
            ScoutMissionStage("ALLOCATE", "COMPLETE", "allocation://scout-proof-001"),
            ScoutMissionStage("PLAN", "COMPLETE", "graph://scout-proof-001"),
            ScoutMissionStage("PARALLELISE", "COMPLETE", "graph://layer-01"),
            ScoutMissionStage("VERIFY", "COMPLETE", "verification://scout-proof-001"),
            ScoutMissionStage("GOVERN", "COMPLETE", "policy://scout-proof-001"),
            ScoutMissionStage("EXECUTE", "COMPLETE", "receipt://scout-proof-001"),
            ScoutMissionStage("MEASURE", "COMPLETE", "cost://scout-proof-001"),
            ScoutMissionStage("OUTCOME", "COMPLETE", "outcome://scout-proof-001"),
            ScoutMissionStage("LEARN", "PENDING", "learning://scout-proof-001"),
        ),
    )
