# TA GuruLabs Core: Durable AIDE Memory + Asset Continuity (v1)
Date: 2026-11-23
Owner: founder. Scope: all TA GuruLabs projects and AIDEs. Applies alongside universal IP/data policy, privacy controls, Continuity Guard, and the evidence-first release factory.

## Mandatory intake and handoff
1. **Before work:** identify role/AIDE and project ID; fetch *approved* project facts, applicable team canon and its own private memory from a trusted memory service. Retrieve asset inventory and source locations via permissions. A missing connection is an explicit BLOCKED/WITHOUT_CONTEXT status, not a fictional remembered fact.
2. **During work:** store source assets and approved masters in persistent restricted storage; record canonical asset ID, version, rights, hash, byte count, storage receipt, and approved/rejected status. Never treat chat transcript or model memory as a binary file archive.
3. **After work:** capture lessons, exact technical faults and reproducible test evidence as **draft** memories with source references. Promote to approved shared canon only via a trusted, authorised reviewer. Supersede earlier instructions rather than silently overwriting them.
4. **Before release:** check rights, confirmed file restore, media/playback or software functional QA, human creative approval and publication receipts. A memory isn't proof of a completed job; a stored file isn't proof it passed QA.
5. **At incident:** preserve logs, classify environment/assets/codec/rights/permissions/workflow, assign a real worker session ID or mark blocked. Reuse past solved cases to prevent repeats.

## Ownership and access
- Per-AIDE private memory is scoped by **project + AIDE identity**. No unrelated project or role can query it.
- Team memory is scoped by project; draft facts are not shared. Founder-approved canonical content can be recalled by permitted roles only.
- Secrets, health/tax/candidate records, bank/wallet data, raw faces/voice samples and unreleased masters stay outside free-text AIDE memories. References to restricted external records require independent authorization.
- Runtime must authenticate callers (service identity, not a user-supplied `--actor` flag); enforce authorization on every read/write/approval; encrypt backups, log access and implement deletion/revocation.
- Local SQLite registry in `continuity/aide_memory_store.py` is a **tested development component only**. It is not yet a connected, hardened multi-agent memory service.

## Source of truth and independence
- Media object originals: private owner-controlled [JingWu Media Asset Library](https://drive.google.com/drive/folders/1xxhRXZkQ1LGCxbuZmORNjb8qDNBLYcFh), within existing continuity vault; existing originals remain where found until verified migration.
- Canonical business/project docs: versioned repo manifests, approved issue decisions and authenticated protected storage.
- Portable metadata layer: SQLite, JSON manifests, source refs, checksums, append-only audit; provider-agnostic. May later add approved embeddings/search; embeddings must respect isolation.
- No new recurring ChatGPT task or subscription is required for this policy. Prefer event-driven GitHub Actions/workers already available, with strict cost controls.

## Engineering standard / acceptance before calling rollout 'LIVE'
- Worker persists memory across two independent restarted sessions.
- Role- and project-scoped auth prevents AIDE A from reading AIDE B's private memory or another project's data.
- Draft memory doesn't appear to other agents; approved team memory does within project.
- Store a real protected asset, obtain verified cloud receipt and byte count/hash, restore it on a different worker; never re-upload private IP to public GitHub.
- AIDE can fetch a bounded context packet with approved decisions and references, execute work, log evidence, propose new memory, and request human approval.
- Failure and missing attachment surfaces `BLOCKED` with exact reason and next action.
- Founder's approval and rights gates cannot be bypassed by the memory store.

## Execution order
1. Wire existing core harness and role playbooks to a consistent context packet contract.
2. Implement authenticated persistent worker and backup/restore, then connect CUTLASS, MAESTRO, Continuity Guardian and DAEDALUS as the pilot.
3. Recover previously uploaded Bard × Lady Fair MOV via supported transfer, validate and enter release workflow.
4. Extend project by project across TA GuruLabs. Archive and audit prior work without deleting originals.

**Status:** policy adopted and local prototype committed; private cloud Drive hierarchy exists. Persistent authenticated deployment and uploaded-media bridge remain unverified.
