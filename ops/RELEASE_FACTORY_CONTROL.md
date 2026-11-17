# TA GuruLabs — RELEASE FACTORY / single-source production control
Status: operating charter and initial evidence-based triage, 2026-11-17. NOT an activated autonomous runtime.

## Mandate
Finish, verify, distribute, fulfil and support existing products before creating new marketing campaigns or speculative features. Mobile/social discovery first; websites are optional utility infrastructure, not the goal. An accessible verified buyer path and support route are mandatory before an offer is called buyable.

## State machine (one state only per deliverable)
IDEA -> SPECIFIED -> PRODUCING -> QA_BLOCKED / QA_PASSED -> RELEASE_PACKAGED -> DISTRIBUTION_PENDING -> RELEASED_VERIFIED -> SUPPORTED.
PAUSED and CANCELLED are explicit alternatives. Unknown is not complete. Never infer completion from a previous AIDE message.
Each transition requires a receipt: artifact link/hash/version, operator, time, test evidence, blocker, next action and reviewer.
No RELEASED_VERIFIED without real accessible public URL or actual customer delivery. No sale without tested purchase -> receipt -> delivery -> help route.

## Work-in-progress limit
At most 3 active production lanes at a time: (1) first verified revenue / ready-to-buy software, (2) one JingWu release, (3) one QA / distribution infrastructure blocker. Remaining work remains on the shelf, not silently abandoned. Prioritize releases that need the fewest critical steps and have the most evidence. Retire duplicate or misleading status reports. Do not add a sixth ChatGPT scheduled task.

## Standard release checks
- Product: one-sentence user outcome; actual file/build URL and reproducible test; mobile experience; link check; terms, price and licensed assets where relevant; receipt/delivery test; staffed or documented support path; rollback.
- Music: approved master, artwork, credits, rights, metadata, distributor/account confirmation, submission ID, public streaming URL; teaser != commercial release.
- Film/comic/video: playable full artifact; CIT protected assets; sound timing, continuity, aspect ratio and iPhone playback; rights; final length; actual public URL; concept preview correctly labelled.
- Games: downloadable or browser-playable build verified on target device; first-play controls, crash checks and obvious defects; trailer never called playable game.
- Support: each offering lists who receives the enquiry, expected routing, troubleshooting playbook, refund policy where relevant and escalation. No fictitious 24/7 support claims.

## Roles (assignments, not proof of agents running)
AUREUS = portfolio arbitration, WIP and first revenue; Haven = inbox/fulfilment/support; Codex = software build and QA automation; Maestro/Cutlass/CIT = creative finishing and continuity; Echo/SIGNAL = media packaging and verified distribution; Continuity Guard = evidence and release gate. Any actual autonomous execution requires runtime configuration and permissions.

## Initial triage — audit required; statuses NOT invented
| Lane | Deliverable | Evidence now | Gate / next verifiable action | Tracking |
|---|---|---|---|---|
| Revenue | One existing software product end-to-end checkout | GitHub issue says not yet verified | Select current best demo, test on mobile: demo -> checkout -> receipt -> delivery -> support. Do not claim first sale | #100 |
| Media | JingWu audio distribution, including Habibi | Teaser URLs verified, full DSP distribution unverified in issue | Collect approved master/metadata/rights, select distributor, submit and verify public URL | #97 |
| Media | Sicario comic retail edition | Teaser held; checkout not verified | Find final source file, QA numbered edition, test buyer delivery | #97 |
| Media | Sicario moving footage | Engine and continuity blocker documented | Capture source assets, produce genuinely moving test, verify duration/audio; no still montage disguised as moving footage | #86 #71 |
| Media | BMK and Operation Neuland | Cinematic work tracked; no release evidence in current check | Inventory source files; identify one minimal clip and test playback | #86 |
| Media | I Need It Tonight / Haunted / Turn Out the Light | User reported unfinished revisions; final release not verified | Identify authoritative master and preserved footage; listen/view from start to finish; close only reproducible defects | #97 |
| Software | HUNTR-X | Demo and consent gate open | Verify mobile journey, data consent and functioning buyer/user path | #69 #81 |
| Software | PAYE Forensics | Research and gated pilot work | Validate user outcome, avoid unsupported tax or HMRC affiliation claims; choose if closest to paid delivery | #58 #59 |
| Software | Pension Scout | MVP and scope gates open | Verify local-first workflow and provider claims; location-only boundary | #72 #75 |
| Software | DocuGod | Narrated concept demo pending real capture | Real screen recording and feature QA before commercial claim | #108 |
| Internal tools | Distribution / support and QA | Editorial and publishing instructions exist | Ensure tested purchase/delivery/support plus link ledger rather than posting unfulfilled offers | #96 #97 #100 |
| Internal tools | RESILIENCE OS / SIGNAL | Concept and prototype work; not approved commercial release | Keep on shelf until first-sale and media release lanes move; internal test only | this document |

## Daily factory brief (replace repeated "what's happening?")
For each of maximum 3 active items output:
1. DELIVERABLE + version
2. STATE + timestamp of latest verified evidence
3. PROOF link or explicitly 'no proof yet'
4. ONE blocker
5. NEXT concrete action + accountable AIDE
6. ETA only if evidence based, otherwise no invented promise
7. PUBLIC and CUSTOMER claim allowed? yes/no
Include: orders verified, fulfilment failures, inbound support items, unresolved incidents, spend, and stalled >48h. Automated summaries must derive from actual tool/file results, not assumed activity.

## Stage-gate discipline
- AIDE may draft and run reversible internal tests where permitted.
- No purchases, subscriptions, live financial actions, release of untested claims or destructive data operations without controls.
- At release, test platform availability and policy compliance. Social discovery -> short demonstration -> native/hosted trusted checkout where available -> entitlement/delivery -> support ticket. Offer no complex marketing website as prerequisite.
- All failures stay visible; improvement cannot erase approved creative assets.
- The 'factory' itself is not deployed until it reads genuine issue/file state and produces receipts. This charter is a starting contract, not evidence of an autonomous production team.
