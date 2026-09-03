# AEGIS Conversation Intelligence Experiment

Purpose: test whether speaker-aware live conversation signals can help people understand communication patterns without turning AEGIS into surveillance, diagnosis, or an artificial partner.

## Non-negotiable privacy boundary
- Explicit participant consent before capture starts.
- Visible recording/transcription state while active.
- Raw audio is ephemeral by default and is not written to long-term AIDES memory.
- Full transcripts are ephemeral by default.
- Only derived, low-sensitivity communication-pattern summaries may be retained when participants explicitly opt in.
- Participants can stop capture immediately and request deletion of session-derived data.
- No covert recording, emotion diagnosis, deception scoring, mental-health diagnosis, relationship scoring, or automatic adverse decisions.
- Intimate-content data remains isolated from the general AIDES organisational memory plane.

## Initial signals
The experiment may derive neutral interaction features such as:
- speaker turn counts
- approximate talk-time balance
- interruption/overlap counts
- long-silence counts
- question counts
- topic-shift markers
- recurring non-sensitive phrases

These are observations, not diagnoses. AEGIS must not label a person as toxic, dishonest, abusive, avoidant, narcissistic, compatible, incompatible, or similar based on these signals.

## Architecture
`consent gate -> streaming ASR/diarisation adapter -> ephemeral transcript -> pattern extractor -> participant review -> optional retained summary -> raw audio/transcript deletion`

The speech provider remains replaceable. Provider-specific models must sit behind an adapter so privacy and retention policy do not depend on one vendor.

## Success test
The experiment succeeds only if participants can understand a useful communication pattern while the system preserves clear consent, deletion, and data-isolation guarantees.
