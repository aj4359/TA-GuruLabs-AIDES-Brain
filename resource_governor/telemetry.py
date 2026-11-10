"""Record provider-reported AIDE usage without fabricating provider costs.

A shared SQLite path on persistent storage enables multi-process history;
a hosted ephemeral CI filesystem DOES NOT persist between runs.
"""
from __future__ import annotations
import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class Telemetry:
    def __init__(self, path):
        self.path = str(path)
        if self.path != ":memory:":
            p = Path(self.path)
            if not p.parent.is_dir():
                raise FileNotFoundError("Telemetry database parent directory does not exist")
        with self._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS usage_events (
                event_id TEXT PRIMARY KEY, occurred_utc TEXT NOT NULL,
                workflow TEXT NOT NULL, provider TEXT NOT NULL,
                model TEXT NOT NULL, input_tokens INTEGER, output_tokens INTEGER,
                provider_cost_usd REAL, duration_ms INTEGER,
                success INTEGER NOT NULL, source TEXT NOT NULL
            )""")

    def _db(self):
        db = sqlite3.connect(self.path, timeout=20)
        db.execute("PRAGMA busy_timeout=20000")
        return db

    def record(self, *, event_id, workflow, provider, model, source,
               input_tokens=None, output_tokens=None, provider_cost_usd=None,
               duration_ms=None, success=True, occurred_utc=None):
        if not all(isinstance(v, str) and v.strip() for v in
                   (event_id, workflow, provider, model, source)):
            raise ValueError("event_id, workflow, provider, model, source required")
        for value in (input_tokens, output_tokens, duration_ms):
            if value is not None and (type(value) is not int or value < 0):
                raise ValueError("token counts and duration must be nonnegative integers")
        if provider_cost_usd is not None:
            if (isinstance(provider_cost_usd, bool) or
                not isinstance(provider_cost_usd, (float, int)) or
                not math.isfinite(provider_cost_usd) or provider_cost_usd < 0):
                raise ValueError("provider_cost_usd must be a finite nonnegative number")
        timestamp = occurred_utc or datetime.now(timezone.utc).isoformat()
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        with self._db() as db:
            result = db.execute("""INSERT OR IGNORE INTO usage_events
                (event_id, occurred_utc, workflow, provider, model,
                 input_tokens, output_tokens, provider_cost_usd, duration_ms,
                 success, source) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (event_id, timestamp, workflow, provider, model, input_tokens,
                 output_tokens, provider_cost_usd, duration_ms, int(bool(success)),
                 source))
            return result.rowcount == 1

    def summary(self):
        with self._db() as db:
            db.row_factory = sqlite3.Row
            rows = db.execute("""SELECT workflow, provider,
                    COUNT(*) AS runs, SUM(COALESCE(input_tokens,0)) AS input_tokens,
                    SUM(COALESCE(output_tokens,0)) AS output_tokens,
                    SUM(provider_cost_usd) AS reported_spend_usd,
                    SUM(CASE WHEN provider_cost_usd IS NULL THEN 1 ELSE 0 END)
                        AS unknown_cost_events,
                    SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) AS failures
                FROM usage_events GROUP BY workflow, provider
                ORDER BY workflow, provider""").fetchall()
        return [dict(x) for x in rows]


def import_json(path, db_path):
    """Import a JSON list of verified provider usage events.

    Expected fields match Telemetry.record(). Cost is null unless the
    source reports cost explicitly; token usage is NOT converted to USD here.
    """
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Input must be a list of usage events")
    db = Telemetry(db_path)
    return sum(db.record(**item) for item in payload)
