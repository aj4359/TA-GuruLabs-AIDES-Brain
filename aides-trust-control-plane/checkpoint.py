"""Signed audit checkpoints for the AIDES Trust Control Plane proof.

This demonstrator uses HMAC-SHA256 so it remains zero-dependency and easy to
validate in CI. Production should replace the shared-secret signer with an
asymmetric KMS/HSM-backed signature so third parties can verify checkpoints
without receiving signing authority.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class AuditCheckpoint:
    transaction_id: str
    sequence_no: int
    event_hash: str
    created_at: str
    signer_id: str
    algorithm: str = "HMAC-SHA256"

    def payload(self) -> dict[str, Any]:
        return asdict(self)


def create_checkpoint(
    *,
    transaction_id: str,
    sequence_no: int,
    event_hash: str,
    signer_id: str,
    signing_key: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    if not signing_key:
        raise ValueError("signing_key is required")
    checkpoint = AuditCheckpoint(
        transaction_id=transaction_id,
        sequence_no=sequence_no,
        event_hash=event_hash,
        created_at=created_at or datetime.now(timezone.utc).isoformat(),
        signer_id=signer_id,
    )
    payload = checkpoint.payload()
    signature = hmac.new(
        signing_key.encode("utf-8"),
        canonical_json(payload).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return {"checkpoint": payload, "signature": signature}


def verify_checkpoint(document: dict[str, Any], signing_key: str) -> bool:
    checkpoint = document.get("checkpoint")
    signature = document.get("signature")
    if not isinstance(checkpoint, dict) or not isinstance(signature, str):
        return False
    expected = hmac.new(
        signing_key.encode("utf-8"),
        canonical_json(checkpoint).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
