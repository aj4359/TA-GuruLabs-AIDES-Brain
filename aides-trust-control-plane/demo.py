from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text())


def emit(events: list[dict[str, Any]], event_type: str, **data: Any) -> None:
    events.append({"event_type": event_type, "timestamp": now(), **data})


def evaluate(policy: dict[str, Any], actor_role: str, action: str) -> str:
    consequential = set(policy["consequential_actions"])
    if action in consequential:
        return "require_human_approval"
    for rule in policy["rules"]:
        if rule.get("actor_role") == actor_role and rule.get("action") == action:
            return rule["effect"]
    return policy.get("default", "deny")


def run(approve: bool = True, kill_before_execution: bool = False) -> list[dict[str, Any]]:
    policy = load_json("policy.json")
    fixture = load_json("examples/scout-signal.json")
    events: list[dict[str, Any]] = []

    actor = fixture["actor"]
    action = fixture["requested_action"]
    tx = fixture["transaction_id"]

    emit(events, "transaction.started", transaction_id=tx, actor=actor)
    emit(events, "evidence.attached", transaction_id=tx, signal=fixture["signal"])

    decision = evaluate(policy, actor["role"], action["type"])
    emit(events, "policy.evaluated", transaction_id=tx, action=action, result=decision)

    if decision == "deny":
        emit(events, "execution.denied", transaction_id=tx, reason="policy_default_deny")
        return events

    if decision == "require_human_approval":
        emit(events, "approval.required", transaction_id=tx, action=action)
        if not approve:
            emit(events, "approval.denied", transaction_id=tx, approver="human.founder")
            emit(events, "execution.denied", transaction_id=tx, reason="human_denial")
            return events
        emit(events, "approval.granted", transaction_id=tx, approver="human.founder")

    if kill_before_execution:
        emit(events, "authority.revoked", transaction_id=tx, by="human.founder")
        emit(events, "execution.killed", transaction_id=tx, reason="intervention")
        return events

    emit(events, "execution.started", transaction_id=tx, action=action)
    # The proof deliberately does not perform a real external side effect.
    emit(events, "execution.simulated", transaction_id=tx, result="success")
    emit(events, "outcome.recorded", transaction_id=tx, outcome="demo_completed_without_external_side_effect")
    return events


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
