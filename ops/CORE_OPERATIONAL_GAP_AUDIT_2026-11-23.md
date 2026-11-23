# TA GuruLabs — Core Operational Gap Audit and Recovery Order
**Date:** 2026-11-23
**Applies to:** AIDES OS / AURA, JingWu Media, FilmOS, TA GuruLabs apps, research, marketing, commercial and internal operations.
**Purpose:** Identify what is actually missing between written AIDE policies and real, evidence-backed delivery. Avoid creating more names, dashboards and unowned tasks.

## Grounded findings
Existing implementation evidence:
- Public AIDES-Brain repo has `AGENTS.md`, `harness/runner.py`, `continuity/aide_memory_store.py`, `continuity/context_packet.py` and related offline tests.
- Local memory tests and scoped context-packet tests passed in GitHub Actions; these do NOT establish a hosted trusted caller-authenticated service or actual autonomous agent usage.
- Private JingWu Drive folder and subfolders were provisioned; previous vault contained selected masters, but new conversation uploads are not automatically transferred into Drive.
- `runtime/jingwu_production.py` passed a synthetic MP4 smoke test. This does NOT show production song/approved assets connected, final video QC or approved publication.
- Bard × Lady Fair real MOV upload is present in conversation inventory but model-side Python/container execution returned ClientError before meaningful file probes; issue #128 open.
- Release Factory issue #109, AIDE memory deployment issue #129 and FilmOS issue #127 still open; don't pretend ticket creation is an agent worker.

## Operational priorities and acceptance evidence
| Urgency | Control | Required proof | Existing tracked work |
|---|---|---|---|
| P0 | **Job scheduler + actual worker execution** | Persistent job ID; worker/session ID; state transition; logs; retry/fallback; executable artifact; survives restarted chat | #126 #127 #129 |
| P0 | **Authenticated media intake and retrieval** | Uploaded *exact* existing MOV to restricted asset store, Drive ID/readback and hash; authorized runner FFprobe and decode; no public source exposure | #128 #129 |
| P0 | **One release gate** | One project/version per master, rights, source hash, technical QA, creative signoff, stable URL and platform receipt, rollback | #109 #127 |
| P0 | **Failure escalation and monitoring** | Synthetic health check plus real failed job trigger; structured error, retry budget, incident owner, owner notification only when action is needed | #125 #128 |
| P1 | **Memory accuracy + conflict handling** | Trusted identity claims; project isolation; proposed-draft versus approved canon; supersession; negative test for forged source; rollback | #129 |
| P1 | **Independent backup and restore** | Verified second copy + restored hashes on another worker; key recovery; explicit retention/deletion policy | #129, recovery guides |
| P1 | **Cost and credit budgets** | Per-job maximum spend, provider price/credits before dispatch, cut-off, recorded actual cost; no surprise subscription | existing Token Miser / independence policy |
| P1 | **Licensing, consent and publication rights** | Approved music/visuals/likeness/voice provenance; permission to use, distribute and relicense; checks before public release | provenance, sound and marketing standards |
| P1 | **Supply-chain/security maintenance** | Pin dependencies; scan vulnerabilities/secrets; least privilege/service credentials; never use untrusted retrieved content as executable instructions | existing trust controls |
| P2 | **Simple founder-facing delivery view** | Mobile board showing verified state and next exact blocker; no estimated deliverable timestamp presented as actual readiness | #109 |
| P2 | **Postmortem knowledge publishing** | Real failure logs and fix evidence converted to article/audio; avoid confidential material and false 'solved' claims | Built at the Kitchen Table brief |

## Resolve overlapping WIP rules
Until there is a live system synchronizing different queues:
- Global Release Factory (#109) retains **3 organisation-wide active lanes**: first payable product; one JingWu release; one shared infrastructure blocker.
- Within the JingWu release lane, maintain **one active finishing master** at a time. A second video may undergo non-rendering source audit in parallel, but is not another active release.
- Immediate active finishing master: **Bard × Lady Fair** (user-approved publication intent; pending actual file inspection). Infrastructure blocker: **MOV upload → authorized runner inspection** (#128).
- Before You Leave and I Need It Tonight are next in ranked queue; preserve Turn On the Light render before expiry; Sicario animation work can resume when production lane rotates or gets explicitly reprioritised.
- No freeze on preserving source material, fixing security issues or continuing verified commercial launch gates.

## Escalation rule
If a foundational tool returns ClientError before processing: check whether provider service/worker unavailable, report precisely what was and wasn't observed, and route through a **verified** alternative worker. No more than one controlled retry without new diagnostic evidence. A GitHub ticket without an accepted agent session stays `BLOCKED`.

## First acceptance sequence
A. Restore a reliable FFprobe-capable worker with access to the existing Bard MOV. Obtain duration, streams, full decode result and sampled-frame contact sheet.
B. Store the exact MOV in the private vault, read back object and bytes/hash; persist the evidence in an authorised private manifest.
C. Complete creative/technical review, secure distribution permissions, produce iPhone-safe MP4 only if necessary, publish via authorised account and verify live video URL.
D. In parallel on infrastructure lane, authenticate CUTLASS/Continuity Guardian to query project-approved memories across two worker restarts. Prove private memory inaccessible to MAESTRO and unrelated projects.
E. Add an end-to-end system test combining memory retrieval → asset retrieval → render → QA → archive → publish receipt (use **synthetic/authorized test media**, never post it publicly).
F. Only when all evidence exists describe the system as `LIVE`; otherwise label exactly which steps are `DESIGNED`, `TESTED OFFLINE`, `RUNNING` or `VERIFIED`.

No additional paid plan or new ChatGPT scheduled slot is approved by this audit. Keep original footage, restricted data and credentials out of the public repository.
