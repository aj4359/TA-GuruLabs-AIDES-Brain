"""Deterministic intervention proof scenario.

This is a controlled contract test, not production telemetry. It proves that an
out-of-envelope consequential action can be denied, authority removed, and MTTI
reported only from evidenced detection and effective-enforcement timestamps.
"""
from dataclasses import dataclass

from intervention_proof import InterventionProof
from runtime_enforcement import RuntimeContext, RuntimeEnforcer


@dataclass(frozen=True)
class InterventionScenarioResult:
    attempted_action: str
    executable_before: bool
    executable_after: bool
    credentials_active_after: bool
    proof: InterventionProof

    def public_payload(self) -> dict:
        return {
            "proofMode": "DETERMINISTIC_GOVERNED_TEST",
            "attemptedAction": self.attempted_action,
            "executableBeforeIntervention": self.executable_before,
            "executableAfterIntervention": self.executable_after,
            "credentialsActiveAfterIntervention": self.credentials_active_after,
            "intervention": self.proof.public_payload(),
            "productionMttiClaimed": False,
        }


def run_intervention_scenario_001() -> InterventionScenarioResult:
    action = "contact_external_party"
    ctx = RuntimeContext(transaction_id="intervention-proof-001", actor_id="aide.scout.v1")
    enforcer = RuntimeEnforcer()

    before = enforcer.can_execute(ctx, action)

    # Simulated detector observes that this consequential action is outside the
    # mission's approved envelope. Runtime controls may only reduce authority.
    detected_at = "2026-09-17T00:00:00Z"
    enforcer.deny(ctx, action, "out-of-envelope consequential action")
    enforcer.revoke_credentials(ctx, "authority revoked after policy violation")
    enforced_at = "2026-09-17T00:00:03Z"

    after = enforcer.can_execute(ctx, action)
    if after or ctx.credentials_active:
        raise RuntimeError("intervention did not become effective")

    proof = InterventionProof(
        intervention_id="int-proof-001",
        transaction_id=ctx.transaction_id,
        worker_id=ctx.actor_id,
        detected_at=detected_at,
        detected_evidence_ref="test-audit://intervention-proof-001/detection",
        requested_action="DENY_AND_REVOKE",
        enforcement_status="EFFECTIVE",
        enforced_at=enforced_at,
        enforcement_evidence_ref="test-audit://intervention-proof-001/enforcement",
    )
    proof.validate()
    return InterventionScenarioResult(action, before, after, ctx.credentials_active, proof)
