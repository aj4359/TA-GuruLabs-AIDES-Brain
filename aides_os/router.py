"""TA GuruLabs AIDES OS: bounded, deterministic autonomy pilot.
No model calls, downloads, production deployment or shell execution.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROLES = {
    "inspect": ("Scout", "read_only"),
    "prototype": ("Codex", "isolated_branch"),
    "test": ("QA AIDE", "sandbox"),
    "document": ("Haven", "draft_only"),
    "release": ("Human", "approval_required"),
}
BLOCKED = {"spend", "deploy", "merge", "delete", "secrets", "external_message", "live_trade"}
ALLOWED = {"inspect": {"read"}, "prototype": {"read", "write_branch"},
           "test": {"read", "test"}, "document": {"read", "draft"}, "release": set()}

def route(task):
    kind = task.get("type", "")
    if kind not in ROLES:
        return {"id": task.get("id"), "status": "BLOCKED", "reason": "unknown task type"}
    permissions = set(task.get("actions", []))
    forbidden = sorted((permissions & BLOCKED) | (permissions - ALLOWED[kind]))
    if forbidden or kind == "release":
        return {"id": task.get("id"), "status": "APPROVAL_REQUIRED",
                "reason": "controlled action", "restricted_actions": forbidden}
    owner, scope = ROLES[kind]
    return {"id": task.get("id"), "status": "ASSIGNED", "owner": owner,
            "scope": scope, "next": task.get("description", "")}

def plan(tasks):
    seen = set()
    output = []
    for task in tasks:
        identity = task.get("id")
        if not identity or identity in seen:
            output.append({"id": identity, "status": "BLOCKED", "reason": "missing/duplicate id"})
            continue
        seen.add(identity)
        output.append(route(task))
    return {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "mode": "DRY_RUN_NO_EXECUTION", "tasks": output,
            "summary": {state: sum(x["status"] == state for x in output)
                        for state in ("ASSIGNED", "APPROVAL_REQUIRED", "BLOCKED")}}

def main():
    folder = Path(__file__).resolve().parent
    tasks = json.loads((folder / "sample_tasks.json").read_text(encoding="utf-8"))
    report = plan(tasks)
    output = folder / "runs" / "latest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"mode": report["mode"], "summary": report["summary"]}))

if __name__ == "__main__":
    main()
