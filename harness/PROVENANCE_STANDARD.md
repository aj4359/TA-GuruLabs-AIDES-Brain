# TA GuruLabs — Provenance & Creative Attribution Standard (v1.0)

**Owner:** Anthony Johnson, Founder & Executive Producer  
**Purpose:** Create verifiable, independently corroborated records of TA GuruLabs' actual contributions to software, services, music, films, images, video, documentation, business processes and writing.

## Principle

**Provenance is evidence, not automatic ownership.** A registered mark, copyright ownership, priority of invention and entitlement to use a third party's work are distinct legal questions. Hashes prove correspondence to bytes, not legal authorship, time of creation, freedom from infringement or exclusive rights.

## Layered evidence stack

**L1 — Source evidence (private)**
- Store original project files, drafts, stems, scripts, source code, designs, prompts where relevant, Git commit history, version chains, review notes and dated asset logs.
- Record actual human contributions and AIDE/tool contributions accurately; never label an AI model a statutory legal author/director.
- Record licences, permissions, releases, composition/master ownership and contributor agreements. Third-party assets remain identified as third-party.
- Preserve original timestamps without claiming that a self-entered timestamp is independently verified.

**L2 — Cryptographic artifact fingerprint**
- Generate SHA-256 digests of source and released files and a canonical JSON provenance record, with version, project ID, asserted contributor roles, rights status, parent record digest and UTC processing timestamp.
- Keep output records **outside the files they hash** to avoid circular signatures.
- Verify against actual file bytes. Any transformation/transcode changes bytes and requires a fresh record linked to the earlier artifact.
- Record SHA-256 for the record itself separately and protect it from alteration.

**L3 — Independent corroboration**
- Commit the manifest digest or the sanitized manifest to a private Git repository with server-generated timestamps, and/or archive it in a write-once storage system.
- For greater proof strength, obtain a trusted RFC 3161 timestamp token from an independent timestamp authority and/or an externally verifiable digital signature controlled by the actual rightsholder.
- Do not regard a local clock or editable Git commit date as absolute proof of first creation.
- Avoid storing trade secrets in public logs; publish only sanitized proof when appropriate.

**L4 — Media provenance & identity**
- For published images/video/audio, consider standards-based C2PA Content Credentials with signing credentials and an unbroken validation chain; check platform preservation behavior. C2PA does not alone prove copyright ownership.
- Use genuine visible branding, authorised credits and metadata (copyright, producer, label, ISRC where assigned) as context.
- Optional robust perceptual watermarks/fingerprints can help locate transformed copies, but removal/editing/compression can defeat them; do not claim indelibility.
- In software, retain source commit/release tags, SBOM/build details and binary hashes. Avoid covert tracking of end users.

**L5 — Brand & legal**
- Keep evidence of first real commercial/public use for JingWu Media and TA GuruLabs with screenshots, live listings, invoices, catalogues, customer references and dated publication receipts.
- Check trademark availability and use appropriate classes before filing. Use **® only with a valid relevant registration**. A logo/credit alone is not a registration.
- Copyright and ownership depend on the real legal rights holder, not on the imprint name being printed on an asset.
- Record third-party licences and IP transfers signed by authorised human legal parties.

## Required release record
Each release should have a unique project identifier and private provenance entry with:
- asset_id and version
- relative file path and SHA-256
- parent asset/record digest when derived
- declared natural-person contributors and role-specific AIDEs/tools
- rights holder **verified/unverified** status and evidence pointer
- external sources and permission/licence status
- actual creation evidence (commits, recordings, logs, originals)
- publisher channel, public URL, store receipt, release time **only when verified**
- external corroboration references (repository commit ID, timestamp service, certificate ID)
- whether C2PA/visible mark exists, distinguishing intention from verification

## AIDE roles
- **Aureus:** enforces provenance gate and refuses unsupported ownership claims.
- **Compliance:** checks agreements, underlying material licences, trademarks, AI contributions and legal personhood.
- **Codex / engineering:** creates cryptographic records, validates them, preserves immutable build artifacts where possible.
- **Maestro / JingWu:** tracks source stems, music/project history, splits, singers, photographs and borrowed clips.
- **Publishing:** creates a timestamped proof of actual live use; never substitutes scheduled drafts for publication.
- **Finance:** retains genuine invoices, royalties, licensing and deal records.
- **Scout:** monitors suspicious reuse and routes cases to a human legal review, not automatic takedown notices.
- **Anthony:** authorises rights claims, legal escalation, filings, publishing and external attribution.

## Release safety
1. **Never silently discard old source records.**
2. No generated ownership claim without legal rights evidence.
3. No false declaration of independent creation if third-party material contributed.
4. No unverifiable *first in the world* or *legally undeniable* claims.
5. No automatic publication of full prompts, source code, customer data or trade secrets to public ledgers.
6. Every materially edited asset receives a fresh hash and linked version record.
7. No general product should be delayed solely for a provenance technology where appropriate manual evidence collection is available; use pragmatic risk-tiering.

## Practical starter CLI
`python3 harness/provenance/fingerprint.py create --file path/to/artifact --project JWM-001 --asset-id JWM-001-v1 --out private-evidence/JWM-001-v1.json`

`python3 harness/provenance/fingerprint.py verify --file path/to/artifact --manifest private-evidence/JWM-001-v1.json`

This creates/validates a cryptographic *integrity record*. It is **not** digitally signed, independently timestamped, or embedded in the media. Extend using proper independently verifiable infrastructure before treating it as a high-confidence legal evidence package.

## Legal references
- UK IPO, copyright: https://www.gov.uk/copyright
- UK IPO, copyright ownership: https://www.gov.uk/guidance/ownership-of-copyright-works
- UK IPO, trademarks: https://www.gov.uk/how-to-register-a-trade-mark
- UK Government, unregistered passing off: https://www.gov.uk/government/publications/ip-basics/ip-basics
- C2PA specification: https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
