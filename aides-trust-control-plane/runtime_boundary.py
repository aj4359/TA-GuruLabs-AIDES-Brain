from dataclasses import dataclass
from typing import Protocol, Mapping, Any

@dataclass(frozen=True)
class MissionEnvelope:
    mission_id: str
    objective: str
    authority_ref: str
    evidence_obligation: str
    max_cost: float

@dataclass(frozen=True)
class RuntimeReceipt:
    runtime_id: str
    execution_ref: str
    attributable_cost: float
    evidence_refs: tuple[str, ...]
    raw_result: Mapping[str, Any]

class CommodityAgentRuntime(Protocol):
    def execute(self, mission: MissionEnvelope) -> RuntimeReceipt: ...

def accept_runtime_receipt(mission: MissionEnvelope, receipt: RuntimeReceipt) -> RuntimeReceipt:
    if receipt.attributable_cost > mission.max_cost:
        raise PermissionError("Runtime exceeded mission economic envelope")
    if not receipt.evidence_refs:
        raise ValueError("Runtime result rejected: evidence obligation unsatisfied")
    return receipt
