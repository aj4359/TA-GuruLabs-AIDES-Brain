# Jingwu Media — Agentic Economy Pilot v0.1
Date: 2026-11-02 | Owner: TA GuruLabs | Status: pilot specification, not deployed

## Thesis
Use one small commercial release (Sicario motion comic + original soundtrack) to demonstrate a repeatable, auditable agentic business workflow: asset intake -> rights/QA -> packaging -> human approval -> publishing -> fulfilment -> reconciliation -> learning. Secondary goal: first verified revenue. Never claim sales/streams without evidence. Do not expose private IP.

## Initial offer (hypotheses, not tested prices)
- Spotify/Apple/etc: eligible original soundtrack through an approved distributor, not video-comic paywall.
- YouTube/TikTok/Instagram: free short trailers driving qualified interest.
- Existing Payhip store: Episode 1 video comic £2.99; Episode 1 + audio £4.99; collector bundle £8.99, subject to fees, VAT/tax settings, format and fulfilment checks.
- A minimum viable paid release must contain an actually watchable, original video comic with working audio and a mobile-tested download/playback. No static-image or synthetic-audio placeholder sold as finished product.

## Assigned AIDE functions (logical roles, not assertions of running agents)
1. **Maestro / Media QA**: music/video asset manifest, loudness/audio QA, codec, duration, mobile playback, alternate formats. Outputs evidence links and explicit pass/fail.
2. **Scout / Rights & Metadata**: chain-of-title, model licence/commercial rights, voice/likeness permissions, soundtrack licence, credits, original-character check, platform eligibility. Escalate unclear rights.
3. **Publisher / Distribution**: construct platform-specific uploads, titles, ISRC/UPC where assigned by distributor, thumbnails, descriptions; use APIs only with authorised scopes and policies. Record platform status; never mark published until verified URL.
4. **Pulse / Marketing**: build permitted trailer/shorts schedule with labelled demonstrations; no fabricated customers/claims, cold outreach, or fabricated urgency.
5. **Commerce / Payhip Ops**: prepare products, secure download delivery, digital VAT/tax config checks, support/refund procedure, order confirmation; do not access payment details unnecessarily.
6. **Ledger / Analytics**: ingest platform reports, calculate net revenue after fees, attribute campaigns, reconcile payouts; distinguish views, streams, orders and actual paid settlement.
7. **Guardian / Trust**: least privilege, scoped tokens, audit logs, prompt-injection checks, approval gates, rate limiting, revoke credentials, no secrets committed.
8. **Codex / Engineering**: implement tested connectors, durable task queue, idempotent actions, retry/dead-letter handling, dashboard, simulations and deployment.

## State machine & approval gates
DRAFT -> ASSETS_VERIFIED -> RIGHTS_APPROVED -> QA_PASSED -> LISTING_PREPARED -> APPROVED_FOR_RELEASE -> PUBLISHED_VERIFIED -> RECONCILED.
Any failed check moves to BLOCKED with evidence. Automation may prepare/schedule; first production upload/payment listing requires explicit rights and human approval. Future low-risk repeat publishing may be pre-authorised under an agreed policy; never bypass terms, copyright, payment or account controls.

## Minimal data contracts
Release {id, title, kind, version, asset_uri, sha256, owner, rights_status, qa_status, approval_status, platforms[], price_gbp, release_date, provenance}
Action {idempotency_key, release_id, aide, action, requested_at, status, attempt_count, evidence_uri, error}
Publication {release_id, platform, remote_id, verified_url, published_at, state}
Settlement {period, platform, gross, fees, tax, net, currency, payment_status, evidence_uri}
Security: sensitive personal/account/payment data excluded from publicly readable files; metadata may be public only when approved.

## Build: incremental and mobile-first
M0 Inventory: audit existing Sicario audio/video sources and rights; mark missing files; do not assume earlier attachments are available in GitHub.
M1 Local dry-run: dashboard with release cards, real state transitions, sample fixtures explicitly labelled, manifest validation, QA checklist, log and tests; no external publishing.
M2 Payhip: set up authorised secure connection if supported; create one draft product and prove test checkout/download before launch.
M3 YouTube/Audiomack: authorised uploads, verify output URL and mobile playback. Music streaming distributor may require manual account workflow; no screen-scraping to bypass protections.
M4 Analytics: daily status, signed order/payout evidence, basic conversion dashboard, lessons learned.
M5 Template: extract generic Agentic Release Engine with adapters for creative products, recruitment tools and other SME products.

## Success criteria / evidence
- 1 full original video comic deliverable; 1 audio deliverable; rights and QA checks passed.
- 1 verified public trailer link; 1 verified paid listing; 1 mobile-tested purchase/download flow.
- First **verified** paid transaction (not projections), net proceeds and platform fees logged.
- Human minutes per release, agent attempts, failure/retry rate, cost per release, customer support load measured.
- Publish candid case study: what worked, what failed, what AIDEs did versus human approvals.

## Constraints & risk
Use existing Payhip and GitHub before buying tools. No paid services by default, no credential sharing in chats, never use borrowed film clips/celebrity likenesses or third-party music without licences. AI-generation licence and distributor acceptance must be verified per asset. No platform availability or earnings guaranteed. £0 fixed-cost aspiration does not eliminate processing fees, commission or taxes.
