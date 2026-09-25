from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Capability:
    capability_id: str
    approved: bool
    estimated_cost: float
    evidence_modes: tuple[str, ...]

def select_approved_capability(required_evidence: str, candidates: Iterable[Capability]) -> Capability:
    eligible=[c for c in candidates if c.approved and required_evidence in c.evidence_modes]
    if not eligible:
        raise PermissionError("No approved capability can satisfy the required evidence mode")
    return min(eligible,key=lambda c:c.estimated_cost)
