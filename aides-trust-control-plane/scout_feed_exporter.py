"""Export validated Scout mission state for the Mission Control public surface.

The exporter is deliberately narrow. It accepts the public-safe ScoutMissionFeed
contract, validates it, adds schema/feed provenance, and writes JSON. It never
reads private prompts, credentials, private memory, source-selection heuristics
or proprietary routing state.
"""
import json
from pathlib import Path
from typing import Mapping

from scout_mission_feed import ScoutMissionFeed

SCHEMA_VERSION = "1.0"
ALLOWED_FEED_MODES = frozenset({"SANITISED_DEMO", "RECORDED_OPERATIONAL"})


def export_public_feed(feed: ScoutMissionFeed, destination: Path, *, feed_mode: str, stage_details: Mapping[str, str] | None = None) -> dict:
    if feed_mode not in ALLOWED_FEED_MODES:
        raise ValueError("unsupported public feed mode")
    feed.validate()
    details = dict(stage_details or {})
    payload = feed.public_payload()
    public = {
        "schema_version": SCHEMA_VERSION,
        "feed_mode": feed_mode,
        "mission_id": payload["missionId"],
        "mission": payload["mission"],
        "commissioned_by_ref": payload["commissionedBy"],
        "worker_id": payload["worker"],
        "budget_gbp": payload["budgetGbp"],
        "measured_cost_gbp": payload["measuredCostGbp"],
        "outcome_status": payload["outcome"],
        "outcome_ref": payload["outcomeRef"],
        "verified_value_gbp": payload["verifiedValueGbp"],
        "learning_status": payload["learningStatus"],
        "stages": [
            {
                "label": stage["label"],
                "detail": details.get(stage["label"], "Governed mission stage"),
                "status": stage["status"],
                "evidence_ref": stage["evidenceRef"],
            }
            for stage in payload["stages"]
        ],
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(public, indent=2) + "\n", encoding="utf-8")
    return public
