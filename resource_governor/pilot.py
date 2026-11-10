"""Non-billing synthetic Night Shift pilot. Never blocks research execution.

One GitHub Actions runner has only ephemeral local state: this is an audit
demonstration, NOT a cross-run quota enforcement service.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from resource_governor import Governor, Policy


def run(report_dir="night_shift/runs"):
    output = Path(report_dir)
    output.mkdir(parents=True, exist_ok=True)
    db_path = output / "governor-pilot.sqlite3"
    governor = Governor(db_path, Policy(weekly_budget_usd=5))
    occurrence = os.environ.get("GITHUB_RUN_ID") or datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    decision = governor.admit(
        job_key=f"night-shift-synthetic:{occurrence}",
        owner="night_shift",
        estimate_usd=0,
        category="optional"
    )
    if decision.permitted:
        governor.complete(job_key=f"night-shift-synthetic:{occurrence}", actual_usd=0,
                          week=decision.week)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "workflow": "night_shift",
        "mode": "SYNTHETIC_PILOT_OBSERVE_ONLY",
        "decision": decision.reason,
        "permitted": decision.permitted,
        "estimated_model_spend_usd": 0,
        "actual_model_spend_usd": 0,
        "cost_basis": "No model API is called by night_shift/engine.py; does not include runner costs",
        "cross_run_enforcement": False,
        "policy": {"weekly_budget_usd": 5, "conservation_at": 0.8,
                   "max_retries": 2, "max_fanout": 2},
        "usage": governor.usage(decision.week),
    }
    report = output / f"governor-pilot-{occurrence}.json"
    report.write_text(json.dumps(record, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"report": str(report), "decision": decision.reason,
                      "mode": record["mode"]}))
    return record


if __name__ == "__main__":
    run()
