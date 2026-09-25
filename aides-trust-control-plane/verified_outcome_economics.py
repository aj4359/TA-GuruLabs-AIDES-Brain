from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class MissionOutcome:
    mission_id: str
    attributable_cost: float
    verification_passed: bool

def cost_per_verified_outcome(outcomes: Iterable[MissionOutcome]) -> float:
    items = list(outcomes)
    verified = sum(1 for item in items if item.verification_passed)
    if verified == 0:
        raise ValueError("CPVO undefined: no verified outcomes")
    total_cost = sum(item.attributable_cost for item in items)
    return round(total_cost / verified, 2)
