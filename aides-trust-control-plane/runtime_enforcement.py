"""Runtime enforcement primitives for governed AIDES execution.

This module deliberately contains no vendor-specific endpoint/security integration.
It defines the control contract that adapters must implement.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class RuntimeState(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    QUARANTINED = "quarantined"
    TERMINATED = "terminated"


class EnforcementAction(str, Enum):
    DENY = "deny"
    PAUSE = "pause"
    REVOKE_CREDENTIALS = "revoke_credentials"
    QUARANTINE = "quarantine"
    TERMINATE = "terminate"


@dataclass
class RuntimeContext:
    transaction_id: str
    actor_id: str
    state: RuntimeState = RuntimeState.ACTIVE
    credentials_active: bool = True
    denied_actions: List[str] = field(default_factory=list)
    interventions: List[dict] = field(default_factory=list)

    def record(self, action: EnforcementAction, reason: str) -> None:
        self.interventions.append({"action": action.value, "reason": reason})


class RuntimeEnforcer:
    """Fail-closed intervention engine.

    Runtime enforcement may reduce or remove authority. It must never grant new
    authority. Authority expansion belongs to the policy/approval plane.
    """

    def deny(self, ctx: RuntimeContext, requested_action: str, reason: str) -> RuntimeContext:
        if requested_action not in ctx.denied_actions:
            ctx.denied_actions.append(requested_action)
        ctx.record(EnforcementAction.DENY, reason)
        return ctx

    def pause(self, ctx: RuntimeContext, reason: str) -> RuntimeContext:
        if ctx.state == RuntimeState.TERMINATED:
            return ctx
        ctx.state = RuntimeState.PAUSED
        ctx.record(EnforcementAction.PAUSE, reason)
        return ctx

    def revoke_credentials(self, ctx: RuntimeContext, reason: str) -> RuntimeContext:
        ctx.credentials_active = False
        ctx.record(EnforcementAction.REVOKE_CREDENTIALS, reason)
        return ctx

    def quarantine(self, ctx: RuntimeContext, reason: str) -> RuntimeContext:
        if ctx.state == RuntimeState.TERMINATED:
            return ctx
        ctx.state = RuntimeState.QUARANTINED
        ctx.credentials_active = False
        ctx.record(EnforcementAction.QUARANTINE, reason)
        return ctx

    def terminate(self, ctx: RuntimeContext, reason: str) -> RuntimeContext:
        ctx.state = RuntimeState.TERMINATED
        ctx.credentials_active = False
        ctx.record(EnforcementAction.TERMINATE, reason)
        return ctx

    @staticmethod
    def can_execute(ctx: RuntimeContext, action: str) -> bool:
        return (
            ctx.state == RuntimeState.ACTIVE
            and ctx.credentials_active
            and action not in ctx.denied_actions
        )
