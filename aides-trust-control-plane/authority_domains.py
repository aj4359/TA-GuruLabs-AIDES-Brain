"""Developer/deployer responsibility domains for governed AIDES transactions.

This public proof records responsibility boundaries without exposing private
orchestration. Technical capability never implies deployment authority.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorityDomains:
    developer_id: str
    developer_controls_ref: str
    deployer_id: str
    deployment_context: str
    permitted_actions: frozenset[str]

    def may_deploy(self, action: str) -> bool:
        """Return True only when the deployer explicitly authorised action."""
        return action in self.permitted_actions


def evaluate_deployment_authority(domains: AuthorityDomains, action: str) -> dict:
    allowed = domains.may_deploy(action)
    return {
        "developer_id": domains.developer_id,
        "developer_controls_ref": domains.developer_controls_ref,
        "deployer_id": domains.deployer_id,
        "deployment_context": domains.deployment_context,
        "action": action,
        "decision": "allow" if allowed else "deny",
        "reason": (
            "explicit deployer authority"
            if allowed
            else "technical capability does not confer deployment authority"
        ),
    }
