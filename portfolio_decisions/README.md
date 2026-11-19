# AUREUS Portfolio Evidence & Allocation Engine

Scope: **all TA GuruLabs commercial and internal lanes**, including digital retail, PAYE, HUNTR-X, DocuGuard/DocuGod, Pension Finder, DiskReclaim, WMCA transport, JingWu Media, Sicario, BMK, FilmOS, games, SIGMA and AIDES tooling.

This **extends** the Retail Desk's idea scouting into cross-portfolio comparative decisions. No new AIDE runtime has been activated. This is a standalone, pure Python evidence-card evaluator with no network access, no filesystem changes beyond a local JSON report and **no authority to cancel/reallocate projects, publish, buy or trade**.

## Governance / preserve existing work
- AUREUS is portfolio arbiter; ARCHON challenges assumptions; Scout supplies dated independent demand research; ATLAS safeguards existing production and release dependencies; Codex supplies test evidence; AUREUS Finance checks unit economics; Haven captures payment, delivery and support receipts; Compliance checks rights/UK platform rules; Continuity Guard safeguards approved assets and IP.
- Respect `ops/RELEASE_FACTORY_CONTROL.md`: maximum **three production lanes** (revenue-ready software, JingWu release, one production/QA infrastructure blocker). Discovery is not permission to start additional builds. Existing `agents/ATLAS_SUPER_PRODUCT_MANAGER.md` freezes speculative new production until the release backlog moves.
- The founder has authorised evidence-based cross-portfolio prioritisation and reversible research. Major diversion of committed production, cancellations, destructive actions, contracts, payments, live trading, public publishing and sensitive data processing remain governed separately.
- Never treat revenue, developer claims or readiness as verified unless linked to real receipts. Retain prior versions and record decisions transparently. A promising new trend must beat the actual opportunity cost of finishing a nearly ready product.
- Use no new ChatGPT scheduled-task slot. Integrate with the existing Daily Release Control reporting workflow only after its runtime sources and genuine receipts are verified. This script may be run manually or through existing independent CI on demand.

## Decision process
1. **Inventory:** record project name, lane, actual current release status, approved source links, working artifact and delivery path. Unknown is unknown.
2. **Investigate:** Scout finds at least two independent evidence sources of buyer pain or, better, validated purchase records. Media and internal products use the appropriate outcome evidence instead of invented demand.
3. **Validate:** AUREUS Finance checks unit contribution and support cost; Compliance checks rights/privacy and marketplace restrictions; Codex/ATLAS verify actual deliverability.
4. **Rank:** 100-point heuristic: customer evidence 25, verified readiness 20, time-to-revenue 15, economics 15, distribution access 10, strategic fit 10, execution risk 5. Each factor is an evidenced score from 0 to 5. Missing inputs produce RESEARCH rather than a fabricated 0 or maximum.
5. **Recommend:** score >=75 and all hard gates passed -> PROPOSE_PRIORITY; 55–74.9 -> IMPROVE_AND_REVIEW; below 55 -> PARK_CANDIDATE. Hard gate failures -> RESEARCH_OR_UNBLOCK irrespective of score. An internal project may have nonfinancial value but still requires a measurable benefit.
6. **Allocate after review:** retain the three existing lanes unless a concrete better opportunity justifies a formally recorded founder-approved switch. Never auto-abandon an approved creative or software release. Pilot one new retail opportunity only after available capacity is confirmed.
7. **Learn:** update input evidence based on verified purchases, usage, failures, net margin, refunds, social conversion and support burden. Re-score only with new evidence, and log source and date.

A score of 90 **does not mean 90% likelihood of success**. Actual predictive probability estimation requires a calibrated historical dataset we do not yet have.

## Run locally
```bash
cd portfolio_decisions
python3 -m unittest -v test_engine.py
cd ..
python3 portfolio_decisions/engine.py portfolio_decisions/evidence.json portfolio_decisions/output/priorities.json
```

`evidence.json` begins empty rather than inventing proof about the portfolio. See the synthetic `test_engine.py` fixture for the schema. Do not store customers' personal, tax, health or recruitment data in these files. Private evidence should be cited through restricted references, not copied into public repositories.

### Evidence of activation
- Branch + PR = implementation proposed, **not** operational cross-portfolio deployment.
- Unit tests passing = logic check, **not** validation of business predictive power.
- Live portfolio report requires independently checked source evidence for every project and a verified operating schedule; unknown entries must stay visibly unknown.
