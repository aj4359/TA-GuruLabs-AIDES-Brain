# TA GuruLabs — Independence-First Engineering and Internal Tools Charter
Date: 2026-11-17
Status: Adopted founder direction; implementation pilots not yet proven.

## The founding rule
Scratch our own itch first. Build internal tools that solve a real, repeated TA GuruLabs operational problem. Run them in ordinary operations and verify their reliability before considering external sales. A potentially marketable service is a byproduct, not the initial justification.

## Non-negotiable independence requirements
1. **No ChatGPT runtime dependency:** core operational workflows must be executable without a ChatGPT conversation, ChatGPT memory, or ChatGPT scheduled tasks. ChatGPT can be one optional user interface/assistant.
2. **Swappable models:** expose a narrow model-provider adapter, supporting an external paid API, other hosted providers and locally hosted models as capability, hardware and quality permit. Never assume models offer identical function calling or output reliability.
3. **Open and portable data:** use documented JSON/JSONL/CSV/SQLite/PostgreSQL formats; retain export and restore scripts; favour open standards and published interfaces.
4. **Portable automation:** workflow definitions, prompts, policy checks and test fixtures live in version-controlled repositories, not only in a proprietary automation dashboard.
5. **Cost discipline:** evaluate free/open-source software, free tiers and trials first, but respect licence and terms; track trial expiry and measured usage. No surprise renewals. Any recurring spend requires a benefit, cap, off-switch and explicit approval.
6. **Exit test:** every critical external dependency gets an alternative, an estimated switching cost, and a periodic realistic export/restore or provider swap test.
7. **Trust and safety:** task-scoped permissions, domain allowlists, dry runs, secret storage, audit trails, rate limits, spend caps and human approval on financial transactions, destructive changes, sensitive data exports and external publication where required.
8. **No false readiness claims:** distinguish documented, prototyped, tested locally, deployed, used daily, and commercially validated.

## Build-versus-rent scorecard
For a necessary capability compare:
- Cost now and after trial (including compute, inference and maintenance).
- Time to first useful verified result.
- Data ownership and export quality.
- Security and access scope.
- Reliability and support burden.
- Legal, licence and platform terms.
- Ability to replace the service in 30 days.

Decision: **Rent temporarily when it accelerates validated internal work without trapping our data or risking unapproved spend. Build when the capability is recurring, strategic, technically feasible and cheaper to own over its lifespan.** Do not build substitutes merely for ideological reasons.

## Minimal target architecture
- **Web UI:** mobile-friendly operations console; replaceable front end.
- **Workflow engine:** simple persisted queue + state machine; start with local SQLite and background worker. Consider heavier orchestration only after demonstrated need.
- **Agent runner:** executes versioned task definitions and structured steps with timeouts, retries, idempotency keys and logs.
- **Model gateway:** provider interface; policy-controlled tool permissions; deterministic scripts first for predictable tasks.
- **Browser adapter:** Playwright for reproducible automated tests; OpenCode Browse MCP as optional experimental adapter for authenticated, human-supervised sessions.
- **Tool adapters:** MCP and direct APIs where available; browser interactions only when compliant and stable.
- **Storage:** repo for code/config; local encrypted/private backups for data; off-ChatGPT recovery procedures.
- **Observability:** each job returns status, timings, evidence links, cost estimate/actual, error and next permitted action.

## Pilot 01 — Browser-powered launch-hub QA (no account login)
**Objective:** Prove a repeatable TA GuruLabs browser test that runs without ChatGPT and detects a real regression.
1. Identify the canonical public TA GuruLabs Launch Hub URL and existing repo.
2. Verify the domain and baseline current behaviour, take timestamped screenshots and record errors.
3. Implement Playwright tests for home-page navigation, at least two product/demo links, broken resources and narrow-screen viewport.
4. Simulate one harmless failing case to prove the checker reports a failure instead of falsely declaring green.
5. Save test definitions, artefacts and machine-readable results in GitHub-compatible tooling.
6. Run again after a change and compare results.
7. Evaluate OpenCode Browse separately, in an isolated Chromium profile with explicit domain allowlist, for one human-supervised test that genuinely benefits from a signed-in browser.

**Acceptance criteria:** repeatable from a terminal/CI without ChatGPT; 2 sequential successful runs; intentional fault caught; working screenshots and logs; zero new paid subscription; no unsafe permissions.

## Pilot 02 — Independent AIDE task runner
Start with one harmless task: fetch a public page or run the QA workflow; record JSON audit event; expose pause/cancel and a manual approval queue. Only then add model routing or authenticated browser actions. Never assume an AIDE role document means a running agent exists.

## Pilot 03 — Exit exercise
Disconnect the preferred AI-provider integration, run the deterministic QA task, export its results and rebuild a runnable environment from README + repo. Log any missing dependency.

## Internal success metrics
- Number of internal tasks successfully run without ChatGPT.
- Time saved against manual baseline, including maintenance time.
- Failed-task detection and recovery.
- Monthly vendor/API spend and projected post-trial spend.
- Backup restore success.
- Continuous daily/weekly usefulness over 30 days.
- Only after sustained internal success: external buyer interviews and willingness-to-pay tests.

## Implementation governance
AUREUS owns priority/cost tradeoffs. Codex owns engineering on a branch/PR. Continuity Guard owns preservation and evidence checks. Scout researches licence and alternatives. Haven records trial expiration and renewals. No financial execution, live trading, account publishing, destructive file operations or subscription signup without required controls and approval. Follow AGENTS.md, existing continuity/security standards and automation-first task gate.

## First actions
- Reuse the existing AIDES Brain repo and its governance rather than duplicate an OS.
- Inventory existing browser test/runtime tools and avoid replacing working pieces.
- Open a branch and implement Pilot 01 with executable tests; do not label it live until verified.
- Maintain a concise dependency ledger: provider, purpose, credentials scope, price, renewal, export path, replacement, last exit-test date.
