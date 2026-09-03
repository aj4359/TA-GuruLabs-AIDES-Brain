"""AEGIS conversation-intelligence session policy.

This proof models consent, retention, and isolation controls. It does not capture
real audio or call any speech provider.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ParticipantConsent:
    participant_id: str
    capture: bool
    retain_summary: bool = False


@dataclass(frozen=True)
class SessionPolicy:
    participants: tuple[ParticipantConsent, ...]
    raw_audio_retention: str = "ephemeral"
    transcript_retention: str = "ephemeral"
    memory_scope: str = "aegis_isolated"

    def capture_allowed(self) -> bool:
        return bool(self.participants) and all(p.capture for p in self.participants)

    def summary_retention_allowed(self) -> bool:
        return self.capture_allowed() and all(p.retain_summary for p in self.participants)


def enforce_session_start(policy: SessionPolicy) -> dict:
    if not policy.capture_allowed():
        return {"decision": "deny", "reason": "all participants must explicitly consent before capture"}
    return {
        "decision": "allow",
        "raw_audio_retention": policy.raw_audio_retention,
        "transcript_retention": policy.transcript_retention,
        "memory_scope": policy.memory_scope,
    }


def retention_decision(policy: SessionPolicy) -> dict:
    return {
        "raw_audio": "delete_after_session",
        "transcript": "delete_after_session",
        "derived_summary": "retain" if policy.summary_retention_allowed() else "delete_after_session",
        "memory_scope": policy.memory_scope,
    }
