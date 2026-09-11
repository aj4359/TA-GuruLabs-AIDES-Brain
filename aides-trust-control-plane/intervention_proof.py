"""Evidence-backed intervention proof for AIDES runtime governance.

MTTI is only calculated when both detection and effective-enforcement timestamps
are present. A request to stop work is not treated as an effective intervention.
"""
from dataclasses import dataclass
from typing import Optional

from intervention_metrics import intervention_latency_seconds


@dataclass(frozen=True)
class InterventionProof:
    intervention_id: str
    transaction_id: str
    worker_id: str
    detected_at: Optional[str]
    detected_evidence_ref: Optional[str]
    requested_action: str
    enforcement_status: str
    enforced_at: Optional[str] = None
    enforcement_evidence_ref: Optional[str] = None

    def validate(self) -> None:
        if not self.intervention_id or not self.transaction_id or not self.worker_id:
            raise ValueError("intervention identity is required")
        if self.enforcement_status not in {"REQUESTED", "EFFECTIVE", "FAILED", "UNKNOWN"}:
            raise ValueError("unsupported enforcement status")
        if not self.requested_action:
            raise ValueError("requested intervention action is required")
        if self.detected_at and not self.detected_evidence_ref:
            raise ValueError("detection timestamp requires evidence reference")
        if self.enforcement_status == "EFFECTIVE":
            if not self.enforced_at or not self.enforcement_evidence_ref:
                raise ValueError("effective intervention requires timestamp and evidence")
            if not self.detected_at or not self.detected_evidence_ref:
                raise ValueError("MTTI requires evidenced detection")
            intervention_latency_seconds(self.detected_at, self.enforced_at)
        elif self.enforced_at or self.enforcement_evidence_ref:
            raise ValueError("non-effective intervention cannot expose effective enforcement evidence")

    @property
    def mtti_seconds(self) -> Optional[float]:
        self.validate()
        if self.enforcement_status != "EFFECTIVE":
            return None
        return intervention_latency_seconds(self.detected_at, self.enforced_at)

    def public_payload(self) -> dict:
        self.validate()
        return {
            "interventionId": self.intervention_id,
            "transactionId": self.transaction_id,
            "worker": self.worker_id,
            "detectedAt": self.detected_at,
            "detectedEvidenceRef": self.detected_evidence_ref,
            "requestedAction": self.requested_action,
            "enforcementStatus": self.enforcement_status,
            "enforcedAt": self.enforced_at,
            "enforcementEvidenceRef": self.enforcement_evidence_ref,
            "mttiSeconds": self.mtti_seconds,
        }
