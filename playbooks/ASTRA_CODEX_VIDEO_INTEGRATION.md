# Astra + Codex video-production integration (draft implementation contract)

Status: SPECIFIED, NOT DEPLOYED. This document is an engineering handoff, not evidence of a working runtime integration.

## Goal
Give TA GuruLabs' JingWu Media production workflow an optional model-agnostic reasoning and code-assistance layer to improve 60-second demo production, continuity, audio sync, render reliability and QA. Keep all existing project assets and approved edits intact.

## Agents / boundaries
- AUREUS: coordinates work and budget.
- MAESTRO + CUTLASS: shot list, storyboard, choreography, creative intent and protected continuity.
- CIT/Continuity Guard: enforce founder DNA, likeness, agreed scenes and non-destructive revisions.
- GPT-6.2 Astra (where the account/API enables it): complex breakdowns, prompt evaluation, debugging and structured editorial decisions; does NOT render video.
- Codex: code engineering and test work through an authorized coding environment; not a video renderer.
- Deterministic tools (FFmpeg/ffprobe plus approved video-generation providers): actual media processing and rendering.

## OpenAI integration
Use the Responses API, not undocumented ChatGPT session automation.
Model IDs must be configured, not assumed. Prefer GPT-6.2 Astra for difficult tasks, a lower-cost supported model for routine classification, and manual/no-AI fallback when unavailable.
Required environment variables (never commit real values):
OPENAI_API_KEY (server side only)
OPENAI_VIDEO_REASONING_MODEL (e.g. model verified as available to account)
AI_ENABLED=false (default)
AI_MAX_COST_GBP_PER_JOB=0 (default: do not incur spend)
Do not rely on a ChatGPT Plus subscription to cover API charges.
Do not activate paid API operations without explicit budget authorization.

## Media pipeline and gates
1. Ingest asset manifest: original music, reference video, founder likeness references, permissions, approved storyboards and last-good render; checksum source assets.
2. Produce structured 60-second edit decision list with scene IDs, in/out points and protected shots.
3. Validate total duration, source provenance, licensing and identity likeness instructions (bald main character; tattoos shown only where supported by visual references).
4. Render: 16:9 master with 9:16 derived cut when required; use approved generation source and FFmpeg, preserve source audio.
5. Run automatic tests: ffprobe playable output, duration target ~60s, dimensions, stream presence, silence/peaking/duplicate-audio checks, freezes/black-frame checks, consistent aspect ratio.
6. Human visual pass on rhythm, continuity, resemblance, choreographic quality, narrative and musical sync. Automated checks cannot prove good visuals.
7. Deliver a verified URL / file with checksum and playback status. No publication until all release gates pass.

## Acceptance tests for pilot
- 'I Need It Tonight': stable beat alignment; no repeated unapproved shots, founder likeness checked against user-supplied references; single audio track, 60-sec demo.
- 'Before You Leave': diverse believable characters, consistent tone and playback.
- 'Falling / Jookin': select an intentional 60-second cut avoiding repeated structure.
- Sicario / BMK: character design continuity, ordered fight choreography and SFX aligned with action.
- No destructive changes to originals; easy rollback to last approved revision.
- Automatic retry only on transient render failures; log every failure and its resolution.

## Codex engineering sequence
1. Locate running video-studio repo and existing scripts, test commands, assets and provider connections.
2. Build an environment-gated provider adapter with OpenAI Responses API, structured JSON schema outputs and explicit errors; test with mocked responses at zero API cost.
3. Implement asset manifest + edit decision list schema, ffprobe QA and a renderer adapter.
4. Integrate into AIDE workflow behind a feature flag; compare against current process with the same 3 trial clips.
5. Switch on API access only after verifying credentials, model entitlement and founder-approved spending cap.
6. Publish nothing until actual playable outputs and destination checks succeed.

## Success measures
Playable 60-sec output rate; human-approved likeness/continuity rate; beat sync errors; repeat-frame frequency; editing iterations; API/provider cost per approved minute; time to produce verified download.

## Constraints
Avoid vendor lock-in; support alternate LLM providers; protect personal photographs and music; never copy reference likeness or licensed media without appropriate rights; do not disclose API keys; do not infer that the model/API can create video directly.
