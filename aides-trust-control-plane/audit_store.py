from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

GENESIS_HASH = "0" * 64


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AuditEvent:
    sequence: int
    transaction_id: str
    event_type: str
    actor_id: str
    authority: dict[str, Any]
    evidence: dict[str, Any]
    decision: dict[str, Any]
    outcome: dict[str, Any] | None
    timestamp: str
    previous_hash: str
    event_hash: str


class AuditChain:
    """Append-only JSONL audit chain with hash linking.

    This is a demonstrator, not a substitute for production WORM storage,
    database controls, key management, signing or independent timestamping.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read_raw(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    @staticmethod
    def _hash_payload(payload: dict[str, Any]) -> str:
        return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()

    def append(
        self,
        *,
        transaction_id: str,
        event_type: str,
        actor_id: str,
        authority: dict[str, Any],
        evidence: dict[str, Any],
        decision: dict[str, Any],
        outcome: dict[str, Any] | None = None,
        timestamp: str | None = None,
    ) -> AuditEvent:
        rows = self._read_raw()
        previous_hash = rows[-1]["event_hash"] if rows else GENESIS_HASH
        payload = {
            "sequence": len(rows) + 1,
            "transaction_id": transaction_id,
            "event_type": event_type,
            "actor_id": actor_id,
            "authority": authority,
            "evidence": evidence,
            "decision": decision,
            "outcome": outcome,
            "timestamp": timestamp or utc_now(),
            "previous_hash": previous_hash,
        }
        event_hash = self._hash_payload(payload)
        row = {**payload, "event_hash": event_hash}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(row) + "\n")
        return AuditEvent(**row)

    def verify(self) -> tuple[bool, str]:
        rows = self._read_raw()
        previous_hash = GENESIS_HASH
        for expected_sequence, row in enumerate(rows, start=1):
            if row.get("sequence") != expected_sequence:
                return False, f"sequence mismatch at event {expected_sequence}"
            if row.get("previous_hash") != previous_hash:
                return False, f"previous_hash mismatch at event {expected_sequence}"
            stored_hash = row.get("event_hash")
            payload = dict(row)
            payload.pop("event_hash", None)
            calculated = self._hash_payload(payload)
            if stored_hash != calculated:
                return False, f"event_hash mismatch at event {expected_sequence}"
            previous_hash = stored_hash
        return True, f"verified {len(rows)} event(s)"

    def events(self) -> Iterable[AuditEvent]:
        for row in self._read_raw():
            yield AuditEvent(**row)


if __name__ == "__main__":
    chain = AuditChain("audit-demo.jsonl")
    chain.append(
        transaction_id="scout-demo-001",
        event_type="RECOMMENDATION_CREATED",
        actor_id="AIDE:SCOUT",
        authority={"policy":"scout-v1","result":"require-human-approval"},
        evidence={"confidence":94,"materiality":96,"source":"public-source-ref"},
        decision={"requested_action":"external_contact","status":"blocked_pending_approval"},
    )
    print(chain.verify())
