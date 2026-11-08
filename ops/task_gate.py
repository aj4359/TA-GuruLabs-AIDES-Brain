#!/usr/bin/env python3
"""TA GuruLabs automation-first guard. Defaults to rejecting ChatGPT task requests.

This only enforces policy for callers invoking this script; it cannot intercept
the ChatGPT application's native task-create endpoint.
"""
import argparse
import datetime
import json
import sys

WARNING = ("TASK SLOT WARNING: This may consume a limited ChatGPT scheduled-task slot. "
           "Use TA GuruLabs independent automation first. "
           "A ChatGPT task needs explicit, task-specific human approval.")

def check(route, approval_path):
    if route == "independent":
        print("ALLOW: independent infrastructure is the default.")
        return 0
    if not approval_path:
        print("BLOCKED: " + WARNING)
        return 2
    try:
        with open(approval_path, encoding="utf-8") as f:
            approval = json.load(f)
        required = ("task_name", "reason_independent_unfit", "approver",
                    "approved_at_utc", "explicit_approval", "approval_scope")
        if not all(approval.get(k) for k in required):
            raise ValueError("missing fields")
        if approval["explicit_approval"] is not True or approval["approval_scope"] != "single_task":
            raise ValueError("approval must be explicitly scoped to one task")
        timestamp = datetime.datetime.fromisoformat(approval["approved_at_utc"].replace("Z", "+00:00"))
        if timestamp.tzinfo is None or timestamp > datetime.datetime.now(datetime.timezone.utc):
            raise ValueError("invalid timestamp")
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: invalid approval record ({exc}). " + WARNING)
        return 2
    print("APPROVED FOR REVIEW ONLY: confirm live available slots and owner intent before native task creation.")
    return 0

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("warn")
    chk = sub.add_parser("check")
    chk.add_argument("--route", required=True, choices=["independent", "chatgpt"])
    chk.add_argument("--approval", default=None)
    args = parser.parse_args()
    if args.cmd == "warn":
        print(WARNING)
        return 0
    return check(args.route, args.approval)

if __name__ == "__main__":
    sys.exit(main())
