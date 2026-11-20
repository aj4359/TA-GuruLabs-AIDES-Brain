#!/usr/bin/env python3
"""Standard-library validation for TA GuruLabs AIDE task records."""
import json
import sys
from pathlib import Path

STATUSES = {"BACKLOG", "QUALIFIED", "ASSIGNED", "WORKING", "REVIEW", "VERIFIED", "RELEASED", "MEASURED", "BLOCKED", "CANCELLED", "FAILED"}
REQUIRED = {"schema_version", "task_id", "project", "agent", "objective", "status", "permissions", "budget", "acceptance_criteria", "checkpoint", "evidence"}

def validate(task):
    errors = []
    if not isinstance(task, dict):
        return ["task must be a JSON object"]
    for field in sorted(REQUIRED - task.keys()):
        errors.append(f"missing required field: {field}")
    for field in ("task_id", "project", "agent", "objective"):
        if not isinstance(task.get(field), str) or not task[field].strip():
            errors.append(f"{field} must be a nonempty string")
    if task.get("status") not in STATUSES:
        errors.append("unrecognised lifecycle state")
    perms = task.get("permissions")
    if not isinstance(perms, dict):
        errors.append("permissions must be an object")
    else:
        for action in ("deploy", "publish", "spend"):
            if not isinstance(perms.get(action), bool):
                errors.append(f"permissions.{action} must be explicit boolean")
    budget = task.get("budget")
    if (not isinstance(budget, dict)
        or any(not isinstance(budget.get(k), (int, float)) or isinstance(budget.get(k), bool) for k in ("cap", "actual"))):
        errors.append("budget.cap and actual must be numbers")
    elif budget["cap"] < 0 or budget["actual"] < 0 or budget["actual"] > budget["cap"]:
        errors.append("budget must be nonnegative and within authorised cap")
    if not isinstance(task.get("acceptance_criteria"), list):
        errors.append("acceptance_criteria must be a list")
    if not isinstance(task.get("checkpoint"), dict):
        errors.append("checkpoint must be an object")
    evidence = task.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence must be an object")
    elif task.get("status") in {"VERIFIED", "RELEASED", "MEASURED"}:
        if not evidence.get("tests"):
            errors.append("verification requires test evidence")
        if task["status"] in {"RELEASED", "MEASURED"} and not evidence.get("deployment_url"):
            errors.append("release requires deployment URL")
    if task.get("status") in {"VERIFIED", "RELEASED", "MEASURED"} and not task.get("reviewer"):
        errors.append("verification requires independent reviewer")
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python validate_task.py TASK.json [...]")
    failed = False
    for name in sys.argv[1:]:
        try:
            issues = validate(json.loads(Path(name).read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as exc:
            issues = [str(exc)]
        print(f'{"FAIL" if issues else "PASS"} {name}' + (": " + "; ".join(issues) if issues else ""))
        failed |= bool(issues)
    sys.exit(int(failed))
