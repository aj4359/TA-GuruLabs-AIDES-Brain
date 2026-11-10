"""Local, dependency-free admission control for non-critical AIDE jobs.

Costs are reported by callers AFTER execution. This governor reserves the
caller-supplied estimated cost, then reconciles it with actual cost. It cannot
enforce external provider quotas unless all callers use this gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from typing import Optional


@dataclass(frozen=True)
class Policy:
    weekly_budget_usd: float = 5.0
    conservation_at: float = 0.80
    max_retries: int = 2
    max_fanout: int = 2

    def __post_init__(self):
        if self.weekly_budget_usd <= 0:
            raise ValueError("weekly_budget_usd must be positive")
        if not 0 < self.conservation_at <= 1:
            raise ValueError("conservation_at must be in (0, 1]")
        if self.max_retries < 0 or self.max_fanout < 1:
            raise ValueError("invalid retry/fanout policy")


@dataclass(frozen=True)
class Decision:
    permitted: bool
    reason: str
    week: str
    fraction_used: float


def utc_week() -> str:
    return datetime.now(timezone.utc).strftime("%G-W%V")


class Governor:
    def __init__(self, path: str | Path, policy: Optional[Policy] = None):
        self.path = str(path)
        self.policy = policy or Policy()
        with self._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS jobs (
                week TEXT NOT NULL,
                job_key TEXT NOT NULL,
                owner TEXT NOT NULL,
                category TEXT NOT NULL,
                state TEXT NOT NULL,
                reserved_usd REAL NOT NULL,
                actual_usd REAL,
                attempts INTEGER NOT NULL DEFAULT 0,
                created_utc TEXT NOT NULL,
                PRIMARY KEY (week, job_key)
            )""")

    def _db(self):
        connection = sqlite3.connect(self.path, timeout=20, isolation_level=None)
        connection.execute("PRAGMA busy_timeout=20000")
        return connection

    def usage(self, week: Optional[str] = None) -> dict:
        w = week or utc_week()
        with self._db() as db:
            row = db.execute("""SELECT COALESCE(SUM(
                CASE WHEN state='completed' THEN actual_usd ELSE reserved_usd END
            ),0), COUNT(*) FROM jobs WHERE week=?""", (w,)).fetchone()
        amount = float(row[0])
        return {"week": w, "committed_usd": round(amount, 6),
                "budget_usd": self.policy.weekly_budget_usd,
                "fraction_used": amount / self.policy.weekly_budget_usd,
                "job_count": row[1]}

    def admit(self, *, job_key: str, owner: str, estimate_usd: float,
              category: str = "optional", fanout: int = 1,
              attempt: int = 0, week: Optional[str] = None) -> Decision:
        """Atomically reserve budget and deduplicate jobs.

        Critical jobs still respect the hard budget. Risk controls and trading
        execution should NEVER rely on this optional-work admission gate.
        """
        if not job_key or not owner:
            raise ValueError("job_key and owner are required")
        if estimate_usd < 0 or fanout < 1 or attempt < 0:
            raise ValueError("invalid request")
        if category not in ("optional", "essential"):
            raise ValueError("category must be optional or essential")
        w = week or utc_week()
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            previous = db.execute("SELECT 1 FROM jobs WHERE week=? AND job_key=?",
                                  (w, job_key)).fetchone()
            total = db.execute("""SELECT COALESCE(SUM(
                CASE WHEN state='completed' THEN actual_usd ELSE reserved_usd END
            ),0) FROM jobs WHERE week=?""", (w,)).fetchone()[0]
            fraction = float(total) / self.policy.weekly_budget_usd
            reason = None
            if previous:
                reason = "duplicate_job"
            elif attempt > self.policy.max_retries:
                reason = "retry_limit"
            elif fanout > self.policy.max_fanout:
                reason = "fanout_limit"
            elif total + estimate_usd > self.policy.weekly_budget_usd:
                reason = "weekly_budget_exceeded"
            elif category == "optional" and fraction >= self.policy.conservation_at:
                reason = "conservation_mode"
            if reason:
                return Decision(False, reason, w, fraction)
            db.execute("""INSERT INTO jobs
                (week, job_key, owner, category, state, reserved_usd,
                 actual_usd, attempts, created_utc)
                VALUES (?,?,?,?, 'reserved', ?,NULL,?,?)""",
                (w, job_key, owner, category, estimate_usd, attempt,
                 datetime.now(timezone.utc).isoformat()))
            return Decision(True, "reserved", w, fraction)

    def complete(self, *, job_key: str, actual_usd: float,
                 week: Optional[str] = None) -> None:
        if actual_usd < 0:
            raise ValueError("actual_usd cannot be negative")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            result = db.execute("""UPDATE jobs SET state='completed', actual_usd=?
                WHERE week=? AND job_key=? AND state='reserved'""",
                (actual_usd, week or utc_week(), job_key))
            if result.rowcount != 1:
                raise KeyError("job reservation not found or already completed")

    def release(self, *, job_key: str, week: Optional[str] = None) -> None:
        """Release a failed reservation while preserving its dedupe key."""
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            result = db.execute("""UPDATE jobs SET state='released',
                reserved_usd=0 WHERE week=? AND job_key=? AND state='reserved'""",
                (week or utc_week(), job_key))
            if result.rowcount != 1:
                raise KeyError("active reservation not found")
