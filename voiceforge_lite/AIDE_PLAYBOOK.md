# TA GuruLabs VoiceForge — AIDE integration playbook

**Stage:** draft prototype, not merged or deployed. **Budget:** £0 additional API/subscription spend. **Architecture:** local MCP over stdio; no public endpoint.

## AIDE roles and permission boundaries

| Agent | Allowed | Not allowed |
| --- | --- | --- |
| Scout | Draft scripts, request local narration and transcription, locate approved audio assets | Publish without existing release controls; invent verified facts |
| Maestro | Prepare audio, look up approved effects, assemble original cues and continuity manifest | Replace an approved clip silently; use unlicensed tracks |
| Navigator | Use pre-approved audio introductions and product explanations | Give personalised tax/investment advice or claim unverified software features |
| AUREUS | Read cost, provenance and QA checklist, request releases via established gates | Authorise paid generations automatically |

## Pilot 1 — Founder audio post
1. Scout prepares a factual 90–130-word original script, including a working public demo URL.
2. Narration uses an explicitly licensed local Piper model, NOT an imitation of the founder's voice.
3. Audio goes through `prepare_audio`, then a human listens for timing, intelligibility and emphasis.
4. Attach a visual and captions; do not publish until both licence and link checks pass.
5. Preserve source script, local output file, revision and approval.

## Pilot 2 — Sicario scene
1. Create a 20-second sound cue sheet: gunshot, footstep, knife contact, impact, ambience.
2. Register *original or documented-licensed* effects with `register_asset`; initially unapproved.
3. Review usage rights, mark cleared assets approved, then retrieve with `list_assets`.
4. Maestro builds an edit with explicit timecodes and references to approved source files.
5. Maintain original approved footage; each replacement has a written before/after checklist. No repeated loops without narrative reason.
6. Compare speech peaks, action synchronisation, scene pace and audible story arc.

## Pilot 3 — Navigator support
Start with prerecorded, approved audio answers on the demonstration site. Do not imply VoiceForge supplies real-time conversational agents: streaming ASR/TTS, turn-taking, authentication, latency testing and operational safeguards would be a **separate product**. Avoid sending HMRC, applicant, banking or customer personal records to third-party services.

## Pilot 4 — AIDE identities
Scout: concise informative narrator. Maestro: creative studio producer. Navigator: calm helpful guide. Save approved text descriptions and local model identifiers, not misleading cloned voices.

## Optional ElevenLabs hosted MCP — OFF BY DEFAULT
Official remote endpoint: https://api.elevenlabs.io/v1/mcp .
OAuth sign-in and workspace permissions are required. Creative generations consume workspace credits. **Do not configure or authenticate the connection in this prototype**, and do not call credit-consuming tools automatically. The no-spend policy requires independent inspection of current terms/allowances before any trial, plus explicit founder approval to activate. No payment methods or API secrets in source control.

## Acceptance gates
- [ ] Tests pass on intended developer computer.
- [ ] Piper executable and licensed model installed, `capabilities` reports correctly.
- [ ] Test narration renders, sounds usable and is saved.
- [ ] FFmpeg can process a sample without overwriting it.
- [ ] Local transcription works only with cached model, with transcript reviewed.
- [ ] Catalogue refuses traversal and hides uncleared assets.
- [ ] All outputs comply with asset/voice model licence, including commercial rights.
- [ ] No paid services or production integrations enabled.
- [ ] No client data, draft files or secrets exposed via public repository or logs.
- [ ] No deployment until QA and integration review.

## Project limits and next engineering work
- Local desktop MCP client must be configured; having GitHub code alone does not connect the AIDEs.
- No free automated premium voice cloning, video editing or live phone support is promised.
- Need source-code review, media duration/file-size limits, deployment guidance and optional CI before broad use.
- Enforce hardware/CPU/time limits and disk quota ahead of unattended AIDE workloads.
