"""Neutral structural pattern extraction for AEGIS conversations.

This module measures observable conversation structure only. It must not infer
emotion, deception, mental state, compatibility, relationship quality, intent,
or personality traits.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections import Counter, defaultdict
import re


@dataclass(frozen=True)
class Segment:
    speaker_id: str
    start_seconds: float
    end_seconds: float
    text: str

    @property
    def duration(self) -> float:
        return max(0.0, self.end_seconds - self.start_seconds)


def _token_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def _question_count(text: str) -> int:
    return text.count("?")


def extract_patterns(segments: list[Segment], long_silence_seconds: float = 3.0) -> dict:
    if not segments:
        return {
            "turn_counts": {},
            "talk_time_seconds": {},
            "talk_time_share": {},
            "question_counts": {},
            "overlap_count": 0,
            "long_silence_count": 0,
            "speaker_switch_count": 0,
            "total_segments": 0,
            "total_words": 0,
        }

    ordered = sorted(segments, key=lambda s: (s.start_seconds, s.end_seconds))
    turn_counts = Counter()
    talk_time = defaultdict(float)
    question_counts = Counter()
    overlap_count = 0
    long_silence_count = 0
    speaker_switch_count = 0
    total_words = 0

    previous: Segment | None = None
    for segment in ordered:
        if segment.end_seconds < segment.start_seconds:
            raise ValueError("segment end cannot precede start")

        turn_counts[segment.speaker_id] += 1
        talk_time[segment.speaker_id] += segment.duration
        question_counts[segment.speaker_id] += _question_count(segment.text)
        total_words += _token_count(segment.text)

        if previous is not None:
            if segment.start_seconds < previous.end_seconds:
                overlap_count += 1
            elif segment.start_seconds - previous.end_seconds >= long_silence_seconds:
                long_silence_count += 1

            if segment.speaker_id != previous.speaker_id:
                speaker_switch_count += 1

        previous = segment

    total_talk = sum(talk_time.values())
    talk_time_share = {
        speaker: (duration / total_talk if total_talk else 0.0)
        for speaker, duration in talk_time.items()
    }

    return {
        "turn_counts": dict(turn_counts),
        "talk_time_seconds": {k: round(v, 3) for k, v in talk_time.items()},
        "talk_time_share": {k: round(v, 4) for k, v in talk_time_share.items()},
        "question_counts": dict(question_counts),
        "overlap_count": overlap_count,
        "long_silence_count": long_silence_count,
        "speaker_switch_count": speaker_switch_count,
        "total_segments": len(ordered),
        "total_words": total_words,
    }


def render_neutral_observations(patterns: dict) -> list[str]:
    """Render descriptive observations without evaluative or diagnostic labels."""
    observations: list[str] = []

    shares = patterns.get("talk_time_share", {})
    if shares:
        for speaker, share in sorted(shares.items()):
            observations.append(f"{speaker} accounted for approximately {share:.0%} of measured speaking time.")

    observations.append(f"Measured speaker switches: {patterns.get('speaker_switch_count', 0)}.")
    observations.append(f"Measured overlaps: {patterns.get('overlap_count', 0)}.")
    observations.append(f"Measured long silences: {patterns.get('long_silence_count', 0)}.")

    questions = patterns.get("question_counts", {})
    for speaker, count in sorted(questions.items()):
        observations.append(f"{speaker} asked {count} marked question(s).")

    return observations
