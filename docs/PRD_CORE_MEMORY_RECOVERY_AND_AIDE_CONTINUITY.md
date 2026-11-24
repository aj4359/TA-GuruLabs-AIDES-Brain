# PRD-001 | TA GuruLabs Memory Recovery & Autonomous Continuity
**Status:** Proposed for engineering acceptance | **Priority:** P0 | **Date:** 24 November 2026 | **Version:** 1.0
**Product owner:** Founder / AUREUS Release Control | **Technical lead:** Codex engineering route, *not yet verified as a live assignee*
**Source documents:** `ops/CORE_AIDE_MEMORY_AND_ASSET_STANDARD.md`, `ops/JINGWU_ASSET_LIBRARY_AND_AIDE_MEMORY.md`, `harness/CONTINUITY_RECOVERY.md`, `harness/UNIVERSAL_IP_DATA_RECOVERY.md`, `continuity/aide_memory_store.py`, `continuity/context_packet.py`, `harness/runner.py`, issues #109, #127, #128, #129.

## 1. The problem
TA GuruLabs relies on conversations and temporary tool environments for long-lived projects. Conversations may contain remembered instructions but **not reliably complete assets, canonical state or executable job sessions**. AIDE roles have been described, but not all are running autonomous services. Offline SQLite memory and scoped context-packet tests passed, yet there is **no confirmed deployed authenticated multi-AIDE memory runtime**, and no verified chat-upload-to-private-vault bridge. A 65.6 MB Bard x Lady Fair MOV was registered by ChatGPT but media sandbox tools returned `ClientError`, blocking inspection and distribution. Our systems lack verified portability, recovery and observable execution, so the founder repeats creative decisions and projects stall.

### User pain
- Repeatedly re-explaining approved character designs, songs, video edits and business decisions.
- Lost access to media stored in a previous chat, temporary filesystem or generator session.
- AIDE forgetfulness, conflicting instructions and false completion claims.
- Lack of a reliable explanation when a tool/provider fails.
- Fear of vendor dependence and unnecessary subscriptions.

### Out of scope
- Replacing ChatGPT's native memory or changing OpenAI account-level features.
- Retaining every chat automatically without supported consented export/connectors.
- Publicly hosting original assets, identity/voice source media, tax/candidate records or credentials.
- Creating another AIDE persona, starting new film production, or enabling unapproved spending.
- Autonomous publishing or customer data access without existing specific permissions.

## 2. Product goals
1. **Recover approved context:** a trusted AIDE can fetch accurate, attributable approved facts and source records at job start, across independently restarted sessions.
2. **Secure per-AIDE memory:** private scope per AIDE and project plus project-shared approved canon; no cross-tenant/project leakage; drafts excluded.
3. **Reliable binary asset continuity:** originals and approved masters recorded with immutable IDs, version, SHA256, byte size, rights, retention, source, separate verified storage and restore receipts.
4. **Execution + observability:** accepted jobs have worker/session ID, stage logs, clear failure, resumability and output evidence; no fake running agent.
5. **Provider-agnostic design:** Python/SQLite or Postgres, portable JSON, local FFmpeg/media workers and standard authenticated APIs; avoid vendor lock-in.
6. **Founder-light UX:** simple mobile view for approved memory, asset status, exact blocker, verified evidence and only necessary approvals.
7. **Integrity and safety:** creative decisions aren't overwritten by model guesses; appropriate deletion, revocation, role-based access, encryption and audit.

### Success metrics (evidence, not estimates)
- **Scenario S1:** CUTLASS saves a sourced memory, owner approves it, worker restarts, CUTLASS retrieves exact value; MAESTRO cannot retrieve CUTLASS-private memory.
- **S2:** project-shared approved canon accessible to authorised CUTLASS and MAESTRO; draft never shared, other project fails closed.
- **S3:** obsolete creative decision superseded with linked approval and rollback; no simultaneous contradictory 'current' canon.
- **S4:** one real authorised asset uploaded to private vault, cloud ID + metadata readback, local and restored SHA256 match, previous version remains.
- **S5:** previously uploaded Bard MOV retrieved through an authorised supported transfer, analysed by FFprobe and full decode, and media QC report stored; if bridge impossible, precise block with tested path and responsible owner.
- **S6:** two independent worker sessions execute task using context packet, save a source-backed outcome and recover after restart; audit log visible.
- **S7:** off-host encrypted backup restored from second recovery location; integrity and permissions verified.
- **S8:** one end-to-end test from ingestion -> memory -> render -> QC -> founder approval -> publication receipt using synthetic/private test assets without publishing them.

## 3. Users and permissions
| User / AIDE | Rights |
|---|---|
| Founder | Owner. Approves canon, creative releases, rights, paid access, irreversible deletion and credentials. |
| AUREUS | Coordinates queue, budgets, evidence gates. No unilateral publication or privilege escalation. |
| DAEDALUS / Codex | Implements infrastructure and repairs; may write approved code and run tests via actual connected runtime; no raw production secrets in repo. |
| CONTINUITY GUARD | Monitors hash drift, version history, source provenance, restores, expired artifacts and canon inconsistencies. |
| CUTLASS | Reads approved JingWu character/edit canon, uploads authorized media and draft editing lessons. |
| MAESTRO | Reads approved JingWu audio/beat canon, writes proposed timing/audio lessons. |
| HAVEN / SCOUT | May search approved non-sensitive task context and report exceptions; cannot see unrelated restricted records. |
| Other AIDEs | Project-specific least-privilege accounts only; deny by default. |

**AIDE persona assignment isn't a live worker session.** Engineering dispatch can begin only after verifying the authenticated Codex/runner integration and job ID. GitHub issue owner is accountable for connecting it.

## 4. Functional requirements

### FR-01 Canonical knowledge
- Memory fields: `memory_id, project_id, aide_id, type, content_or_ref, source_ref, confidence_state, approval_state, approved_by, created_at, supersedes_id, expiry_or_review_at`.
- `confidence_state`: user_decision, verified_test, source_claim, working_hypothesis, rejected. A speculative output can never silently become approved canon.
- Full-text retrieval v1 with source links and newest approved version; optional semantic index later, respecting permissions.
- Approved team memory shared only within project; private memory only to owner AIDE; leave auditable amendments not silent mutation.
- Never write confidential personal details in general free-text memory. Separate regulated data storage and UK GDPR handling.

### FR-02 Asset registry and intake
- Preserve originals, versioned masters, rights status, parent-child derivatives, SHA256, byte counts and authenticity status.
- Register -> uploaded with cloud receipt -> readback -> restore_verified as distinct states.
- Controlled Drive intake using existing private vault `JingWu_Media_Asset_Library` and proper authenticated connectors; support chunked transfers and resumable uploads for large files.
- Maintain no-copy/no-delete status for files with missing cloud receipt; no public GitHub uploads for private footage or voice/faces.
- Stable worker can access authorised asset bytes without relying on ChatGPT mount.

### FR-03 Independent persistent service
- Host authenticated private service with per-AIDE service identity, scoped OAuth/session tokens or equivalent trusted identity.
- Encrypt data at rest/in transit; secrets in secure secret store; audit access; backup/restore.
- API contract: `GET /v1/projects/{id}/context`, `POST /v1/memory/drafts`, `POST /v1/memory/{id}/approve`, `POST /v1/assets/intake`, `GET /v1/jobs/{id}`; host may adapt final design but must preserve auth gates.
- Support offline/degraded mode: provider unavailable -> queued or blocked, never fabricated completion.

### FR-04 Real worker handoff
- State machine: QUEUED -> ACCEPTED(worker ID) -> RUNNING -> ARTIFACT_READY(hash/URI) -> QC_PASSED -> FOUNDER_APPROVED -> PUBLISHED(receipt); or BLOCKED(reason) / FAILED(log).
- Idempotent job IDs; retry policy with caps; failure notification; source/reference manifests.
- Each assigned AIDE receives bounded approved context; after completing work writes factual source-backed draft, not permanent canon without approval.
- Track and cap per-job model/video/cloud costs. No recurring paid services by default.

### FR-05 Founder experience
- Phone-readable search: project -> assets -> version -> approved decisions -> last issue -> exact blocker -> observed next action.
- Approval controls for promotion/supersession of canon, media release and spend; clear 'unverified' label.
- Simple 'export my project' with assets, metadata, approved instructions, provenance and restore guide.

### FR-06 Support and incident diagnosis
- Capture provider, tool invocation, timestamp, operation, reported error ID/log, input file metadata, sanitized stack trace, retry outcome.
- Classify error origin as hypothesis unless logs prove it; never say OpenAI intentionally changed/restricted access without evidence.
- Repeatable incident postmortem suitable for truthful public 'Built at the Kitchen Table' series, with confidential content redacted.

## 5. Nonfunctional requirements
- **Privacy:** least-privilege RBAC per caller/project, explicit approvals, audit log, GDPR data minimisation/retention, credential rotation and incident response.
- **Security negative tests:** spoofed AIDE ID rejected, alternate-project ID rejected, draft not visible, private memory cannot be retrieved by another role, injection content cannot override approval rules, secrets never logged.
- **Reliability:** atomic writes, crash-safe idempotency, reproducible restoration, checksums and separate backups; encrypted storage and key restoration drill.
- **Cost:** use existing GitHub, Drive and open-source components before purchasing new services; show maximum estimated cost and approval if unavoidable.
- **Accessibility:** mobile-first, understandable errors, no developer-only diagnostics required of founder.
- **Portability:** downloadable versioned JSON/SQLite manifests, immutable media files, independent restore without ChatGPT access.
- **Observability:** task states, logs, timestamps, verified artefacts, storage receipts, version history.

## 6. Delivery plan and accountable roles

### Sprint 0: Reliable inventory and incident recovery (P0)
- **AUREUS (product owner):** inventory all active projects; freeze unsupported 'complete' statuses; unify release queue in #109.
- **CONTINUITY GUARD + CUTLASS:** map approved JingWu source and final masters from existing private vault; register absent files explicitly. Do not delete or overwrite existing versions.
- **Codex / DAEDALUS (engineering):** reproduce #128 media sandbox ClientError with benign synthetic asset; implement/choose authenticated transfer to independent FFprobe worker; process Bard source when authorized bytes reachable.
**Exit:** one exact Bard master located and verified or a reproducible precise blocker and working replacement access path.

### Sprint 1: Secure memory runtime (P0)
- **Codex / DAEDALUS:** harden `continuity/aide_memory_store.py` and `context_packet.py` behind trusted identities and durable storage; remove self-asserted caller privileges; add role checks, migrations, encryption/backup, full tests.
- **CONTINUITY GUARD:** build source, canon supersession, conflict and retention tests.
- **AUREUS:** validate scope/requirements and handle approvals.
**Exit:** actual service deployment URL/worker ID (private), S1-S3 verified across restart; code-only CI is insufficient.

### Sprint 2: Asset bridge + backup (P0)
- **Codex / DAEDALUS:** authenticated Drive/private storage uploader, checksums, readback and download/restore; stage final media outside chat.
- **CUTLASS + MAESTRO:** bring in approved creative assets using rights-checked manifests, verify correct song and picture.
- **CONTINUITY GUARD:** S4, S5 and S7 independent restore proof.
**Exit:** one actual media file survives worker restart and recovery; with verified digest, Cloud receipt and private location.

### Sprint 3: Working AIDE integration (P0)
- **Codex:** integrate first actual AIDE worker with memory and job state endpoints, logs and retries; not merely a persona spec.
- **CUTLASS:** pilot creative continuity, retrieve approved Sicario/Bard canon.
- **MAESTRO:** pilot music timing decisions and team-shared canon.
- **AUREUS:** enforce evidence-based release gate.
**Exit:** S6 and S8; user sees actual finished test artifacts and approval flow.

### Sprint 4: All TA GuruLabs products (P1)
- **AUREUS + HAVEN:** onboard specialists by sensitivity/data class, report owner decisions and exceptions only.
- **SCOUT:** produce a sourced engineering lesson/postmortem record from each verified failure.
- **Codex:** migration/export, monitoring, failure alerts, tests and rollback.
**Exit:** documented zero-invention rollout across designated projects; no AIDE falsely claims live status.

## 7. Acceptance and launch gate
**Not DONE** for a PRD, GitHub ticket, mocked agent, passing synthetic CI test, folder creation or model assertion. Every milestone requires source commit/PR, independent CI, authenticated runtime session/job ID, actual artefact/receipt, negative auth tests and founder-visible validation as specified above.

**Must not ship:** unapproved voice cloning, media uploads to a public repo, paid subscriptions/credits without consent, generic model prompts containing sensitive customer data, unsourced memories promoted to canon.

## 8. Dependencies and risks
- ChatGPT conversation attachments may be inaccessible to external systems. Work around via verified supported bridge; do not invent URL.
- Google Drive is externally hosted; backup must include an independent second recovery target and tested restore.
- Existing sqlite CLI relies on self-asserted `--actor`. It is a development tool, **not security**. Must not expose on public network.
- AIDE runtime/deployment and Codex worker may not be connected. Verify permissions before dispatch, otherwise leave ASSIGNMENT_PENDING and owner escalation.
- Overlapping release queue priorities: one actively finishing video; maintain separate infrastructure and commercial lanes.
- Memory corruption and canon conflict risk; use provenance, human approval and reversible supersession.
- Potential operational cost; start with free/open-source and preapprove paid services.

## 9. Sprint-zero immediate actions
1. Open this PRD for review and acceptance.
2. Assign GitHub issue ownership to a **real** account with repo access, and the specialist workstreams as role assignments in linked engineering issues.
3. Confirm whether connected Codex execution is available. If not, mark dispatch blocked and leave cut-and-paste ready Codex instructions in tickets.
4. Start with existing source code rather than a new greenfield system.
5. Prioritise Bard master verification and persistent scoped AIDE memory demonstration over creating additional concepts.
