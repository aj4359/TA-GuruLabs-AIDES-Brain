# TA GuruLabs Build Routing Policy

## Default engineering route

For every TA GuruLabs software build, Codex is an approved primary engineering route and the default alternative whenever a visual builder, hosted agent, credit-based platform, or external build tool is unavailable, blocked, too expensive, too limited, or unsuitable.

### Core rule

**Do not let a project stop because Lovable, Manus, Claude, a plugin, credits, or another external builder is unavailable. Route the build to Codex + GitHub instead.**

## Build order

1. Start from the product brief / PRD and the existing repository if one exists.
2. Prefer direct repository work through Codex for implementation, refactors, testing, debugging, integrations, CI, documentation, and deployment preparation.
3. Use visual builders such as Lovable only when they materially accelerate the job and credits/access are available.
4. Use Manus primarily for specialist media/research tasks or when explicitly preferable, not as a dependency for core product engineering.
5. If a hosted builder fails, immediately continue through Codex rather than asking the user to repeat setup steps.
6. Preserve existing working code. Build on branches, test changes, and use pull requests for material changes.
7. Avoid dead-end prototypes. A “working prototype” must have functioning interactions, routes, state, and a credible path to deployment.

## TA GuruLabs engineering loop

**Idea → PRD → Codex Task → Branch → Build → Test → Review → Deploy → Launch**

AIDES may contribute product, research, risk, security, legal/compliance, content, QA, and go-to-market input, but Codex is the engineering execution layer by default.

## Fallback hierarchy

For product engineering, use this order unless the task strongly suggests otherwise:

**Codex + GitHub → existing local/repo tooling → visual builder (Lovable) → specialist external agent (Manus) → manual workaround**

If one route is blocked, move to the next route without stalling the project.

## Quality gates

Before calling a build complete:

- Core flows work.
- Buttons and navigation are not dead.
- Responsive/mobile behaviour is checked where relevant.
- Errors fail clearly and safely.
- Sensitive credentials are not committed.
- Compliance/risk claims are not fabricated.
- Tests or deterministic validation exist for critical logic.
- A README or handoff note explains how to run and continue the project.

## Operating principle

**Codex is not the emergency backup. Codex is part of the standard TA GuruLabs build system.**

This policy applies across TA GuruLabs products, including SIGMA, ASR, JobGenius, AEGIS, BMK, DocuGod, Token Miser, MigrateIQ, and future products.
## Required TA GuruLabs Creative Fingerprint (all AIDEs)

Before researching, engineering, reviewing, publishing or operating any TA GuruLabs product, **read and apply [Human-Centred Creative Fingerprint](harness/HUMAN_CREATIVE_FINGERPRINT.md)**.

This cross-portfolio operating doctrine is not optional decoration: identify the real human problem; interpret Anthony's creative intent; preserve approved work; propose at least one imaginative but practical solution; apply KISS; verify tangible outcomes, privacy, rights and accessibility. A technical success that produces a confusing or generic user experience is not a finished product.

For implementation handoffs record: **person/problem · intended feeling/outcome · keep/change · inventive approach · KISS constraint · test evidence · rights/risk · customer value**. Use a human review of the fingerprint scorecard; never claim that a model's score is user research. Mandatory safety, legal, reliability and human-signoff gates always take precedence.


## Required provenance fingerprint and attribution controls

For **every** TA GuruLabs software release, song, video, film, image, article, document, service or commercially relevant concept, follow [Provenance & Creative Attribution Standard](harness/PROVENANCE_STANDARD.md).

Before publishing, record the actual source assets and contributors, licensing/ownership status, version history, production evidence and SHA-256 hash manifest. The reference tool is `harness/provenance/fingerprint.py`. Save evidence privately, create a newly linked record for each revision and keep the associated independent publication/commit/archive receipts. Where supported, consider cryptographically signed C2PA Content Credentials for published media.

**Strict distinction:** integrity fingerprint ≠ copyright ownership, prior art, first creation, trade mark registration or independently verified timestamp. Do not publish unverified legal claims or assert proprietary rights over unlicensed third-party input. Preserve user and contributor privacy. Route disputes to human legal review. This policy complements, and does not replace, IP due diligence and statutory registration where appropriate.


## Disaster recovery and out-of-ChatGPT continuity — mandatory

A creation is not considered safely preserved merely because it appears in a chat. At **creation/export/commit time**, register its owner, source location, SHA-256, project, version and verified off-ChatGPT recovery route.

- For Git-managed files, each push to `main` triggers the independent `continuity-snapshot.yml` GitHub Actions workflow and maintains a downloadable Git bundle release with checksums.
- For important audio/video/image masters and user-approved document bundles, preserve originals and an encrypted/private off-platform copy. The current designated vault is the PRIVATE Google Drive folder `TA_GuruLabs/TA_GuruLabs_Continuity_Vault`, ID `1w4C4v5sXJzsXSQ8E-MOTgLgGwtTn-UJ4`. Do not publish its files or share publicly by default.
- If Google Drive transfer is unavailable, record a **backup pending** gate and exact source location; do not silently treat a generated chat attachment as durable off-platform storage. When using connected tools, confirm upload and readback; copying is complete only with evidence.
- Keep source and derived artifacts separately, and preserve older versions where possible. Reversible edits only.
- Never put secrets, customer PII, private unreleased masters or licence-sensitive footage on public IPFS. Decentralized storage requires encryption *before* upload, controlled recovery key, pinning at >=2 independent providers, and a verified download/decryption test. IPFS alone offers no retention guarantee.
- Include a short disaster recovery link/instructions on project release handoff. Periodically test restoring both code and media WITHOUT ChatGPT.

See `harness/PROVENANCE_STANDARD.md` for ownership and hashing, and `harness/CONTINUITY_RECOVERY.md` for backups. This is a working repository policy; it cannot automatically intercept or save arbitrary ChatGPT conversations or disconnected apps.


## Continuity Guardian — mandatory for all AIDEs
**CONTINUITY PRESERVES AUTHENTICITY.** Before any Maestro, Director, FilmOS, engineering, music, writing, game, product or publishing change, follow [the central Creative Continuity Guard](harness/CREATIVE_CONTINUITY_GUARD.md). Start with the actual approved original material and canonical character/product/music records; preserve prior accepted versions, log changes and verify continuity with security and IP controls as an independent release gate. Genre influence may convey the essence of films or performers, but cannot claim licensed actor or character cameos or use unauthorised identifiable likenesses. Automated repository checks run under `.github/workflows/continuity-guardian.yml`; they do not automatically inspect untransferred off-repo media or replace human visual/audio QA.
