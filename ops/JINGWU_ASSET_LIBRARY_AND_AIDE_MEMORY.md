# JingWu Asset Library + TA GuruLabs AIDE Memory v0.1 — 23 Nov 2026

## Real assets already provisioned
- Private owner-only Google Drive Continuity Vault (owner shown as JingWuMedia@gmail.com): https://drive.google.com/drive/folders/1w4C4v5sXJzsXSQ8E-MOTgLgGwtTn-UJ4
- New **JingWu_Media_Asset_Library**: https://drive.google.com/drive/folders/1xxhRXZkQ1LGCxbuZmORNjb8qDNBLYcFh
- `00_Inbox_Unverified`: 1oFy-s4z0oEyjoo-vgPYiTp5oKPlSbbz-
- `01_Original_Media`: 1LQw_2xTPHIikzCXfda1x3dBP0kBMWkec
- `02_Project_Masters`: 1-rH_R7F_AJP85jPCYR2YNjCiS5NZ-mJb
- `03_Approved_References`: 1DlBdc-6MTfdEhXZvlmMzsjsGjcdRAJD3
- `04_Production_Manifests`: 1dHbhaTFnVPO_bdPFsM3ErR2GC8zCepLi
- `05_Release_Receipts`: 1qdPQ4RprXuoOybotnIopnnk-Hyy5Den8
- `06_Archive_Backups`: 1WZHAE95KUumSI2D2DriLWHj-5YpYlW9R

These folders were actually created using connected Drive and reside under the private owner vault. Existing vault originals have NOT been copied/moved into the new hierarchy; their older locations remain canonical until verified migration.

## Executable local AIDE/asset registry
- `continuity/aide_memory_store.py`: SQLite standard library, no paid hosted dependency; asset identity (project/title/version/rights/SHA256/size), user-approved scoped per-agent memory, audit log.
- `continuity/test_aide_memory_store.py`: synthetic tests for project isolation, owner isolation, draft-not-shared and asset REGISTERED status. GitHub Actions: https://github.com/aj4359/TA-GuruLabs-AIDES-Brain/actions/runs/45283596427 — **passed**.
- This is a **local library**, not a live multi-user service or an actual memory tool connected to all AIDEs. Running it in a persistent private host with authenticated identities and backups is the next step.
- The SQLite file should live only on a private encrypted host, **never in the public repository**. Do not store raw personal voice training clips, face images, customer PII, secrets, unpublished films or health/tax data inside memory text fields. Store privacy-appropriate REFERENCES to separate authorised vault objects instead.

## Memory model
Each AIDE has:
1. **Private memory** — assigned role context, experiments, failures, source links and learned lessons. Scoped to both owner AIDE and project. Other AIDEs cannot read it through the library.
2. **Shared team memory** — approved facts, canonical creative decisions, versioned style bibles, validated interface contracts and asset references. Same-project AIDEs can access it only when status=approved. Shared does not mean public.
3. **Audit/provenance** — source_ref, actor, timestamps, supersession/version links, approval. Distinguish user-approved canon, measured machine result, conjecture, and agent drafts.

Example: CUTLASS remembers approved character design for SICARIO with source record; MAESTRO recalls approved song timing; Continuity Guardian reads shared, approved canon, not a draft. Another project like PAYE may NEVER receive JingWu private memories by default.

## Required before production (not complete)
- Authenticated server-side caller identity + role permissions before calling SQLite. **Current CLI's `--actor` is self-asserted, not secure authentication.** Do not expose CLI directly to public network clients.
- Encrypt memory data at rest and in transit; restrict filesystem/database access and keep audit logging protected; implement founder-approval token/RBAC in service wrapper.
- Stable server with `GET/PUT` APIs and per-AIDE scoped service accounts, retention, backups, restore test, revisions and deletion.
- Credentialed Drive uploader: authenticated upload + readback size/hash + save server receipt; never mark `copied` merely because a folder exists. First migration must recover Bard/Lady Fair uploaded MOV from chat source through a supported authenticated transfer, then inspect with ffprobe and only subsequently approve/publish.
- Sync and immutable evidence ledger: store approved canonical story in versioned manifests, not only in LLM memory, with conflict resolution and author signoff.
- Audit existing vault items and map original media to named projects before moving; never overwrite/delete originals until backed up and restore-tested.
- Rights/classification gate for generated likenesses/voice samples; record explicit cloning authority and revocation options.
- 3-2-1 copies and a regular restore verification. Google Drive folders alone are not 3-2-1 protection.

## Immediate creative priority
1. Find/verify exact Bard x Lady Fair two-act MOV (chat file ID `file_0000000002d88210be1746d5bf7be0ce`, ~65.6MB) via authenticated asset bridge. It is **not** automatically in Drive.
2. Recover approved project master, no forced rebuild. Once read and reviewed, release only with valid playback and founder approval.
3. Preserve Before You Leave V3/V4 work and user references, I Need It Tonight movement source clips and Sicario source/approved trailers in private vault as versioned assets.
4. Let the owner see a simple asset inventory, file version, storage copy status, acceptance approval and release proof for each production.
