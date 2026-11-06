# TA GuruLabs — Universal IP, Data and Recovery Policy (v1)
**Status: mandatory for all AIDEs and projects.** Applies to product code, PRDs, contracts, music masters, comics, film footage, games, designs, prompts when business-critical, research and operational/customer records.

## Principle
**Continuity preserves authenticity. Recovery preserves existence. Security protects access. Provenance documents contributions.** All four must be treated as independent release controls.

## What belongs where
| Class | Examples | Storage rule |
| --- | --- | --- |
| PUBLIC | Published marketing text and approved downloads | Public stores only after rights/compliance signoff |
| INTERNAL | Non-sensitive project specs, design notes and source metadata | Private Git repository + independent backup; preserve change history |
| CONFIDENTIAL IP | Original songs, stems, unpublished art, film masters, source code, product algorithms, contracts | Restricted private vault plus independent versioned storage; never expose via public repo/IPFS |
| RESTRICTED DATA | Customer/candidate records, tax/health information, credentials, access tokens, banking data | Approved encrypted, access-controlled systems only; no general media vault, repository or unrestricted ZIP. Data minimisation, UK GDPR retention rules, deletion procedures and recoverability must be documented |

Never copy secrets, PII or customer records into GitHub build artifacts, public logs or a shared creative archive. Do not place credential files or encryption keys in the same backup as encrypted data.

## At creation, before an AIDE declares BACKED UP
1. Assign project ID / asset ID / version and rights status.
2. Identify original/source-of-truth and canonical relationships, owners, contributors and licences.
3. Register confidentiality class, approved physical storage locations, access owners and retention/deletion policy.
4. For actual binary files record SHA-256, byte count, source receipt and parent-version lineage.
5. Verify authenticated second copy by **metadata readback**; for critical masters also download and verify SHA-256 and open/restore (readback is not a full recovery test).
6. Keep originals immutable, append new versions and maintain a reversible history.
7. Track three evidence states separately: REGISTERED, COPIED, RESTORE_VERIFIED. Never upgrade status without proof.
8. Require security/privacy/legal/continuity checks before public delivery. Store publication receipts apart from drafts.

## Automation & ownership
- **Continuity Guardian** verifies repository canon, registry schema, evidence fields and approved-version drift; logs incomplete projects. It cannot reach unconnected external accounts.
- **Maestro / FilmOS / Director** register original audio/image/video/comic sources and their derivative lineages, check licensed inspiration rather than copying protected appearances.
- **Engineering / Codex** record source history, build artifacts, dependency manifests, database schemas and restoration procedures.
- **Compliance** defines handling and retention of regulated data; Finance handles financial records; the Founder controls access and rights claims.
- **Launch AIDE** cannot claim permanent preservation based on an unsaved chat artifact or a link alone.

## Recovery / lifecycle standards
- 3-2-1 target: three recoverable copies, two independent media/storage systems, one independently accessible. Initial partial backup must not be presented as meeting this target.
- Verify backup success, restore a representative sample periodically, test disaster recovery without ChatGPT, rotate access, and document revocation/deletion.
- Schedule checks in GitHub, but do not describe periodic CI as a process running 24/7.
- Track each product or media universe separately using the JSON registry. A project without a verified source copy is **PENDING**, not complete.
- For GDPR-covered records record lawful basis, purpose, retention, data subject processes, processor/access agreements and secure deletion; backups must honour agreed deletion/retention.
- Keep rights claims grounded; hashes prove file identity, not ownership or registration.

## Source-of-truth links
- Protected vault (private): https://drive.google.com/drive/folders/1w4C4v5sXJzsXSQ8E-MOTgLgGwtTn-UJ4
- Studio creative continuity standard: https://github.com/aj4359/TA-GuruLabs-Studio/blob/main/policies/CREATIVE_CONTINUITY_STANDARD.md
- Technical continuity recovery: harness/CONTINUITY_RECOVERY.md
- Provenance standard: harness/PROVENANCE_STANDARD.md
- Universal inventory: `harness/ip_registry/projects.json`
- Guardian: `continuity/guardian.py`; registry validator: `harness/ip_registry/validate.py`.

**Scope disclaimer:** Registering a project does not mean its assets have been imported or backed up. The vault currently has verified Sicario packages and selected older media; full coverage of all TA GuruLabs projects/data is an ongoing audit, not a completed transfer.
