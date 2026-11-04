"""Minimal, fail-closed TA GuruLabs execution harness (standard library only)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone

ALLOWED_CHECKS = {"file_exists", "json_valid"}
MAX_ATTEMPTS = 3


def now():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")
        temp = f.name
    os.replace(temp, path)


def load_contract(path: Path) -> dict:
    contract = json.loads(path.read_text(encoding="utf-8"))
    required = {"task_id", "goal", "root", "checks"}
    if not isinstance(contract, dict) or not required.issubset(contract):
        raise ValueError("Contract requires task_id, goal, root and checks")
    if not isinstance(contract["task_id"], str) or not contract["task_id"].replace("-", "").replace("_", "").isalnum():
        raise ValueError("task_id must be a simple identifier")
    if not isinstance(contract["goal"], str) or not contract["goal"].strip():
        raise ValueError("goal must be nonempty")
    if not isinstance(contract["root"], str) or not contract["root"].strip():
        raise ValueError("root must be nonempty")
    checks = contract["checks"]
    if not isinstance(checks, list) or not checks:
        raise ValueError("At least one check required; no evidence means no pass")
    for check in checks:
        if not isinstance(check, dict) or check.get("type") not in ALLOWED_CHECKS:
            raise ValueError("Unsupported check type")
        target = check.get("path")
        if not isinstance(target, str) or not target.strip():
            raise ValueError("Each check needs a path")
    return contract


def resolve_inside(root: Path, relative: str) -> Path:
    target = Path(relative)
    if target.is_absolute():
        raise ValueError("Absolute paths not allowed")
    resolved = (root / target).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("Path escapes task root")
    return resolved


def verify(contract: dict) -> list[dict]:
    root = Path(contract["root"]).expanduser().resolve()
    evidence = []
    for check in contract["checks"]:
        record = {"type": check["type"], "path": check["path"], "passed": False}
        try:
            target = resolve_inside(root, check["path"])
            if check["type"] == "file_exists":
                record["passed"] = target.is_file()
            elif check["type"] == "json_valid":
                if target.is_file():
                    json.loads(target.read_text(encoding="utf-8"))
                    record["passed"] = True
            record["detail"] = "pass" if record["passed"] else "check failed"
        except (OSError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
            record["detail"] = f"{type(exc).__name__}: {exc}"
        evidence.append(record)
    return evidence


def run(contract_file: Path, state_dir: Path) -> dict:
    contract = load_contract(contract_file)
    task_id = contract["task_id"]
    state_path = state_dir / f"{task_id}.json"
    receipt_path = state_dir / "receipts.jsonl"
    fingerprint = hashlib.sha256(contract_file.read_bytes()).hexdigest()
    state = {"task_id": task_id, "goal": contract["goal"], "contract_sha256": fingerprint,
             "status": "running", "attempts": 0, "started_at": now(), "evidence": []}
    atomic_json(state_path, state)
    # The harness does not silently edit artifacts. Each retry re-verifies; repair
    # belongs to a separate approved builder action, not to this verifier.
    for attempt in range(1, MAX_ATTEMPTS + 1):
        evidence = verify(contract)
        state["attempts"] = attempt
        state["evidence"] = evidence
        if all(item["passed"] for item in evidence):
            state["status"] = "verified_complete"
            break
        # Deterministic checks cannot self-repair; avoid pointless repeated runs.
        state["status"] = "needs_repair"
        break
    state["finished_at"] = now()
    atomic_json(state_path, state)
    receipt = {"task_id": task_id, "goal": contract["goal"],
               "contract_sha256": fingerprint, "status": state["status"],
               "attempts": state["attempts"], "evidence": state["evidence"],
               "completed_at": state["finished_at"], "policy": "harness-v1",
               "human_review_required": state["status"] != "verified_complete"}
    state_dir.mkdir(parents=True, exist_ok=True)
    with receipt_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(receipt, sort_keys=True) + "\n")
    return receipt


def main():
    parser = argparse.ArgumentParser(description="TA GuruLabs evidence-first harness")
    parser.add_argument("contract", type=Path)
    parser.add_argument("--state-dir", type=Path, default=Path(".aides/state"))
    args = parser.parse_args()
    try:
        receipt = run(args.contract, args.state_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Contract error: {exc}\n")
    print(json.dumps(receipt, indent=2))
    if receipt["status"] != "verified_complete":
        parser.exit(1)


if __name__ == "__main__":
    main()
