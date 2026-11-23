# JingWu Media — Delivery register and evidence gates
Updated: 2026-11-23. **Never label a video 'released' on the strength of a prompt, issue, screenshot, or teaser.**

## Production policy
- Freeze **new video concepts** until existing priorities are finished or explicitly parked.
- Active work-in-progress limit: **2 video masters + 1 infrastructure blocker**. All other titles remain on the visible backlog.
- Source-of-truth for status: this register + real renderer run IDs + asset hashes + public links.
- Stages: `BACKLOG -> ASSET VERIFIED -> EDIT LOCKED -> RENDER RUNNING -> MP4 VERIFIED -> CREATIVE APPROVED -> RELEASED (URL)`, or `BLOCKED: reason`.
- 'Owner' means a named human, or a connected agent with an **actual accepted job ID**. A persona/role title alone is not a worker.
- Each blocker must give the reproduction/evidence, cheapest remedy, explicit next action, and checkable outcome.
- Publishing needs rights checks, complete playable full version, verified sound/image sync, iPhone save test, a stable public link and founder final creative approval.
- Use existing TA GuruLabs release-control cadence; do not claim automatic monitoring is running until a schedule or runner is confirmed.

| Rank | Production | Best evidenced state | Release blocker | Next evidence needed |
|---|---|---|---|---|
| P0 | Before You Leave V4 | 6:03 V3 demonstrator produced in chat; founder rejected inaccurate opening likeness, scene casting and beat timing; new test renderer CI passed 2026-11-23 | No approved V4 master; persistent source asset pipeline missing | Audio-reviewed speech/end/downbeat timestamp, real reference-based portrait and approved narrative cast, corrected full export, iPhone test, founder approval |
| P0 | I Need It Tonight | Prior visualiser and tests, no approved full dance film | Movement quality, source choreography and rhythm sync; no end-to-end full film | One original 15–30s synchronized dance master with approved lead and motion, then full-song cut |
| P1 | Turn On/Out the Light (Punjabi) | Prior full 3:14 render reported, stored in expiring build artifact | Existing master not secured and rechecked | Recover and preserve source/render by 2026-11-30, decode, scene audit and creative approval |
| P1 | Sicario — Dead Man Walking | Comic and teaser prototypes; latest moving-comic test not approved | Actual character animation and fight/SFX continuity absent | Approved shot bible + real 10–15s action test, then finish trailer |
| P2 | The Bard's Bold Beat x A Lady Fair | Hybrid versions | Widescreen, cast continuity, motion vs slideshow, musical join | Recover approved scenes, render full coherent sequence |
| P2 | Habibi | Public teasers reported | No verified full master/release | Source audio/video inventory, rights and release links |
| P2 | Haunted | Early tests | No approved master | Reopen source assets and motion plan |
| P2 | BMK | Anthem and concept | No approved fight film | 15s action capability test after Sicario |
| P2 | Operation Newland, Wounded | Development backlog | No approved master | Verify assets, narrative and priorities |

## Two distinct technical tracks
**Track A — stills/music editing:** versioned approved scene manifests, real audio, beat/downbeat log, eased dissolves, Ken Burns, mobile h264/aac export. A synthetic GitHub Actions smoke test passed, but full user-media runtime is **not connected**. `runtime/jingwu_production.py`.
**Track B — animated action and dance:** requires real moving footage or an approved external video generator; FFmpeg cannot manufacture convincing martial arts choreography from stills. Use Manus/HeyGen only with accessible reference assets, verified permitted credits, and reviewable outputs; never claim costless generation or automatic transfer of chat files.

## Minimum daily evidence digest
Only report changed facts. For each active production: title/version; source manifest location (private); render session/job ID; artifact URL/hash; observed duration/codecs; founder sign-off; next exact blocker; risk of expiring build storage. An unchanged 'still blocked' is honest.

## TA GuruLabs engineering storytelling — Built at the Kitchen Table
For every meaningful actual problem and fix, create a **long-form Tea Time LinkedIn story** and a derivative narrated multimedia piece.
Use five source-backed sections: (1) idea and customer/creative goal, (2) observed failure and screenshots, (3) root cause with code and reproducible evidence, (4) engineering remedy and test results, (5) what remains unverified and next criteria. Never invent numbers, agent autonomy, successful deployment, earnings or releases.
Maintain an evidence pack with media samples, rights-cleared illustrations, original problem screenshots, commit SHA, CI run URL, dates and published link. Reuse only clips/photos with permission. Keep credentials, source voice samples and unreleased likeness assets in **private** storage, not this public repository.
Voice edition: user's own recording if sourced; consent before third-party voice cloning, and identify synthetic voice transparently. No reusable clone has been created/verified as of this entry.
First story: *When AI Can Create the Pictures but Can't Finish the Film*; article draft produced in conversation 23 November, **not yet verified published**.
