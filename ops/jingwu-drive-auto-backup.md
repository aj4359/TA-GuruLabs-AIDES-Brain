# JingWu Media Automatic Original-Asset Backup — Operational Contract
Updated: 2026-11-07
Destination: private Google Drive folder TA_GuruLabs/TA_GuruLabs_Continuity_Vault (folder ID 1w4C4v5sXJzsXSQ8E-MOTgLgGwtTn-UJ4).

## Non-negotiable
- Original footage, music masters, owner photographs, illustration assets, source manifests, and approved masters MUST be copied to the Drive continuity vault and verified BEFORE deletion of local copies.
- Temporary renders v1…vN are not automatically retained forever. Preserve source assets and the last approved working master; optional milestone review exports only.
- A local ChatGPT sandbox ZIP is NOT a verified Google Drive backup, and ChatGPT memory cannot preserve original video bytes.
- Never claim an upload occurred without an authenticated Drive file ID and read-back metadata, including size. Compare SHA-256 locally when available, or keep hashes in manifest and verify download when practical.
- Restrict permissions/private access. Never embed Google credentials in source; use secret storage.
- Deduplicate content by checksum; version retained master and append manifest. Retention/deletion only after verified remote copy.
- Account has a five-active-scheduled-task cap: DO NOT create a separate ChatGPT scheduled task for every upload. The upload event should trigger directly from the editing/storage workflow or a GitHub Actions run; existing Night Brief audits proof.

## Intended no-additional-slot pipeline
1. CUTLASS (or editor) completes/render asset, writes source manifest with sha256/size/rights/source timecodes.
2. Put exported artifact into an authenticated persistent source accessible to the backup worker (e.g. private GitHub Release artifact, object storage or a supported connector file reference). A ChatGPT sandbox local filepath is not automatically accessible to external runtimes.
3. Trigger event-based uploader on each new protected source/master or release. Use a securely configured Google Drive upload integration; avoid public upload endpoints.
4. Drive confirms file ID in Continuity Vault; read back name, size and location. Save receipt in private continuity audit.
5. Mark backup VERIFIED only after successful readback. Retry safely with deduplication and exponential backoff.
6. Only now propose deletion of local review/export copies. Never automatically delete irreplaceable originals.

## Current state / work required
- Drive continuity folder confirmed accessible by connected metadata search on 7 Nov 2026.
- Current JingWu_ORIGINAL_SOURCES_Backup.zip exists as a local ChatGPT artifact, ~155.6 MB. NO verified upload or Drive receipt exists for this archive as of this document.
- Connected Google Drive upload_file requires a connector file_uri; the local /mnt/data path is not supported as such. External backup worker needs an accessible source and authorised Drive credentials or a supported connector transfer.
- The existing TA GuruLabs Night Brief should audit archive receipts and report missing uploads without saying an audit equals an upload.
- Completion criterion: one full archive uploaded to the private vault; Drive file ID and metadata readback; a second new source auto-uploaded by trigger without manually asking for a copy.

## Failure behavior
- A failed upload blocks source deletion but not creative work.
- Never silently replace a master with a lower-quality rendition; keep originals unchanged.
- Confirm the user can open cloud backup before removing phone files.
