# TA GuruLabs Universal Build Pipeline v1

## Purpose
Use shared AIDES/Codex engineering infrastructure across TA GuruLabs products so expensive visual builders are reserved for high-value UX polish, not repetitive heavy engineering.

## Pipeline

`Brief → Mission Router → Codex implementation → automated tests → security/IP gates → PR → visual polish → final QA → deploy`

## Operating principles

1. **One Brain, many products.** Shared orchestration, security, QA and execution contracts live centrally. Product-specific customer experience and business logic stay with the product.
2. **Complex engine, simple experience.** Heavy logic is not exposed merely because it exists.
3. **Codex does the heavy lifting.** Refactors, tests, CI, security hardening, adapters, deterministic engines and API boundaries should happen in source control first.
4. **Visual builders are finishing tools.** Use Lovable or equivalent for product polish, visual iteration and final integration where they add disproportionate value.
5. **No uncontrolled rewrites.** One focused mission/PR at a time.
6. **No automatic production publish or live payment enablement without an explicit release gate.**
7. **Public/protected/proprietary boundaries are mandatory.** Browser code must never be treated as a safe place for trade-secret logic or privileged credentials.

## Required product artefacts

Each product should provide:

- `product-manifest.yaml`
- current source-of-truth repository and branch
- customer-facing product focus
- architecture boundary: public / protected / proprietary
- deterministic-engine inventory where relevant
- mobile/UX QA criteria where relevant
- security/IP baseline
- CI test gate
- deployment-readiness report
- provenance/change log

## Mission Router

Every mission must include:

- product
- objective
- source-of-truth repo/branch
- scope
- explicit stop-building list
- acceptance tests
- security/IP constraints
- whether visual-builder work is allowed
- whether deployment or payments are allowed

If source of truth is unknown or unsynced, mission status is **BLOCKED: SOURCE OF TRUTH** and implementation must not begin.

## Default execution stages

### Stage 0 — Source-of-truth gate
Confirm the exact live product source and current branch/commit. Never implement against stale prototypes when a newer hosted product exists elsewhere.

### Stage 1 — Audit
Inventory routes, components, engines, mocks, integrations, secrets exposure and test coverage. Classify customer-facing features as KEEP / MERGE / HIDE / REDESIGN / DELETE.

### Stage 2 — Engineering
Codex performs focused implementation on a feature branch.

### Stage 3 — Automated gates
Run relevant unit/integration/regression/accessibility/security checks. Deterministic product totals must not change due to presentation refactors.

### Stage 4 — Security/IP gate
Check secrets, browser-visible proprietary logic, auth/authz, data storage, rate limiting, error leakage and dependency risk.

### Stage 5 — Pull request
Return concise change summary, tested journeys, known limitations and live-vs-mocked capability map.

### Stage 6 — Visual polish
Only after engineering is stable, use Lovable or equivalent for high-value presentation/mobile polish. Do not let the visual tool silently replace deterministic engines.

### Stage 7 — Release gate
Production deployment, payment activation and destructive migrations require explicit release approval.

## TA GuruLabs reusable quality gates

### KISS gate
- Does the customer need this?
- Does it solve a defined customer problem?
- Does it duplicate another feature?
- Could a contextual assistant handle it instead?
- Is the wording understandable without specialist knowledge?
- Does it work exceptionally on the primary device?

### Security/IP gate
- no private keys/service credentials in browser code
- no proprietary prompts/weights/scoring leaked unnecessarily
- server-side validation for privileged actions
- least privilege and per-user data access
- safe upload/storage controls for sensitive documents
- rate limiting and abuse monitoring
- secret/dependency scanning
- source-control provenance retained

### Assistant gate
Conversational models may understand intent, route and explain. They must not invent deterministic financial/tax calculations or directly execute arbitrary mutations. Use allow-listed actions and validated engines.

## Current priority implementation

First product mission: **Let's Talk Tax / PAYE Forensics**.

The current focus is not general tax. It is explaining difficult UK PAYE outcomes through five customer-facing entry problems:

1. I owe tax
2. My tax changed
3. Check my tax code
4. Explain a document
5. What can I claim? (PAYE/employment relief initially)

See GitHub issue #5 for the active Codex mission.
