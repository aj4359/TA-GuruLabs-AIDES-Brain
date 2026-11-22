# AUREUS proof-of-control — offline security smoke test
# Standard-library only. No credentials, network, AI API calls or repository writes.
# This is a deterministic POLICY test, NOT evidence that a live AIDE resists prompt injection.
from datetime import datetime, timezone
import json

ALLOWED = {"read_public_issue", "summarise_public_issue"}
BLOCKED = {"read_secret", "send_email", "merge_pr", "delete_file", "transfer_funds"}

def authorize(action, source, human_approved=False):
    if source == "untrusted" and action not in ALLOWED:
        return False
    if action in BLOCKED:
        return False  # Approval alone does not grant unconfigured permissions.
    return action in ALLOWED

def main():
    cases = [
        ("authorised public issue summary", "summarise_public_issue", "user", True),
        ("untrusted issue requests secret", "read_secret", "untrusted", False),
        ("untrusted issue requests PR merge", "merge_pr", "untrusted", False),
        ("untrusted issue requests email", "send_email", "untrusted", False),
    ]
    records = []
    for name, action, source, expected in cases:
        actual = authorize(action, source)
        records.append({"case": name, "action": action, "source": source,
                        "expected_allowed": expected, "actual_allowed": actual,
                        "pass": actual == expected})
    report = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "test_type": "deterministic policy simulation; NOT live agent test",
              "results": records, "all_pass": all(x["pass"] for x in records)}
    print(json.dumps(report, indent=2))
    assert report["all_pass"]

if __name__ == "__main__":
    main()
