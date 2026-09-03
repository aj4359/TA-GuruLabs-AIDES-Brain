"""Operational governance metrics for AIDES runtime intervention."""

from datetime import datetime, timezone
from statistics import mean


def _parse(timestamp: str) -> datetime:
    value = timestamp.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def intervention_latency_seconds(detected_at: str, enforced_at: str) -> float:
    latency = (_parse(enforced_at) - _parse(detected_at)).total_seconds()
    if latency < 0:
        raise ValueError("enforcement cannot precede detection")
    return latency


def mean_time_to_intervention(events: list[dict]) -> float | None:
    """Mean seconds from risk/control detection to effective intervention."""
    latencies = [
        intervention_latency_seconds(event["detected_at"], event["enforced_at"])
        for event in events
        if event.get("detected_at") and event.get("enforced_at")
    ]
    return mean(latencies) if latencies else None


def intervention_slo_status(mtti_seconds: float | None, target_seconds: float) -> str:
    if mtti_seconds is None:
        return "insufficient_evidence"
    return "within_target" if mtti_seconds <= target_seconds else "outside_target"
