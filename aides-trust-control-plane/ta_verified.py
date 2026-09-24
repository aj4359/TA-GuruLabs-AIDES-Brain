from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class VerificationRecord:
    claim: str
    acceptance_criteria: str
    scenario: str
    evidence_refs: Sequence[str]
    failure_correction_history: Sequence[str]
    result: str
    version: str
    timestamp: str
    limitations: Sequence[str]
    release_decision: str

def assert_verified(record: VerificationRecord) -> None:
    if record.result != "PASS":
        raise ValueError("TA VERIFIED requires PASS")
    if not record.evidence_refs:
        raise ValueError("TA VERIFIED requires evidence")
    if record.release_decision not in {"VERIFIED_RELEASE","VERIFIED_LIMITED_RELEASE"}:
        raise ValueError("TA VERIFIED requires an explicit verified release decision")
