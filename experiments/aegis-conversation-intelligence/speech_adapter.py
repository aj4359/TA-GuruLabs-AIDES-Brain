"""Provider-neutral streaming speech adapter for the AEGIS experiment.

The adapter contract sits behind the existing consent and retention policy.
No provider credentials, endpoint details, or real audio are included here.
"""

from dataclasses import dataclass
from typing import Iterable, Protocol

from session_policy import SessionPolicy, enforce_session_start


@dataclass(frozen=True)
class SpeechSegment:
    speaker_id: str
    text: str
    started_ms: int
    ended_ms: int
    is_final: bool = True


class StreamingSpeechProvider(Protocol):
    provider_name: str

    def transcribe(self, audio_chunks: Iterable[bytes]) -> Iterable[SpeechSegment]:
        ...


class ConsentRequiredError(PermissionError):
    pass


def transcribe_with_policy(
    policy: SessionPolicy,
    provider: StreamingSpeechProvider,
    audio_chunks: Iterable[bytes],
) -> list[SpeechSegment]:
    """Open transcription only after unanimous participant capture consent."""
    gate = enforce_session_start(policy)
    if gate["decision"] != "allow":
        raise ConsentRequiredError(gate["reason"])

    # The provider receives only the ephemeral stream. Persistence decisions are
    # handled separately by the session retention policy.
    return list(provider.transcribe(audio_chunks))
