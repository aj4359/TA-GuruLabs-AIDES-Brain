from dataclasses import dataclass
from typing import Any, Mapping, Sequence

ALLOWED_INTERVENTION_STATES = {"ALLOW", "DENY", "STOP", "ESCALATE", "HUMAN_REVIEW"}
VERIFIED_RELEASES = {"VERIFIED_RELEASE", "VERIFIED_LIMITED_RELEASE"}

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
    identity: str = ""
    authority: Mapping[str, Any] | None = None
    action: str = ""
    cost: Mapping[str, Any] | None = None
    outcome: Mapping[str, Any] | None = None
    value: Mapping[str, Any] | None = None
    intervention_state: str = "HUMAN_REVIEW"

def assert_verified(record: VerificationRecord) -> None:
    if record.result != "PASS":
        raise ValueError("TA VERIFIED requires PASS")
    if not record.identity.strip():
        raise ValueError("TA VERIFIED requires identity")
    if not record.authority:
        raise ValueError("TA VERIFIED requires authority")
    if not record.action.strip():
        raise ValueError("TA VERIFIED requires action")
    if not record.cost:
        raise ValueError("TA VERIFIED requires cost evidence")
    if not record.evidence_refs:
        raise ValueError("TA VERIFIED requires evidence")
    if not record.outcome:
        raise ValueError("TA VERIFIED requires outcome")
    if not record.value:
        raise ValueError("TA VERIFIED requires value")
    if record.intervention_state not in ALLOWED_INTERVENTION_STATES:
        raise ValueError("TA VERIFIED requires a valid intervention state")
    if record.intervention_state != "ALLOW":
        raise ValueError("TA VERIFIED cannot release while intervention is unresolved")
    if record.release_decision not in VERIFIED_RELEASES:
        raise ValueError("TA VERIFIED requires an explicit verified release decision")
