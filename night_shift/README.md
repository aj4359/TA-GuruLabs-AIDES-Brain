# TA GuruLabs | Night Shift V1

**Status:** research prototype; synthetic sandbox only. No market feed, paper broker, real money or live orders.

## KISS workflow
1. **Scout** creates labeled deterministic synthetic prices.
2. **SIGMA** tests 3 moving-average hypotheses on training samples.
3. **Codex** executes unit tests and reproducible code.
4. **Onyx** evaluates holdout metrics and writes an auditable JSON result.
5. **Owner** reviews results; no money can be spent or traded.

Run locally: `python -m unittest discover -s night_shift -p 'test_*.py'` and `python night_shift/engine.py`.

The GitHub Action runs daily at 06:30 **UTC** (not fixed UK wall-clock time across BST/GMT), or on manual dispatch, **after this workflow is merged into the default branch and Actions are enabled**. View the run artifact under GitHub > Actions. This is NOT automatic delivery to email, Telegram or WhatsApp. Scheduled GitHub Actions may be delayed or occasionally skipped.

## Evidence and safety policy
- Only simulated prices are used. Outputs are not financial advice and are never signals to trade.
- Zero brokerage credentials, payout keys, external trades or paid API calls.
- Holdout evaluation is separate from training trade periods; indicators use a warm-up history.
- Cost model is illustrative. No robustness claim, t-stat, 5-year walk-forward, statistical confidence or realistic market slippage is established.
- Promotion criteria for later real-data paper research: provenance, legal data licence, walk-forward, out-of-sample validation, execution costs, stress tests and independent review. Any actual live trading requires separate explicit approval and technical safeguards.
- Review 7 consecutive **successful** runs before considering V2; failures and missing runs count against reliability.

## Reusable AIDE operating contract
Each product unit (PAYE Forensics, HUNTR-X, AURA, Procurement) should expose: `run_id`, `agent`, `input_provenance`, `hypothesis`, `test_result`, `verifier`, `decision`, `exceptions`, `next_action`. Do not report success without independent checks. Respect UK GDPR, confidentiality, approvals, and product-specific professional obligations.

Next implementation milestones: actual market-data integration in isolated paper environment; persistent experiment index; exception notifications; public-safe, gameplay-style read-only viewer. Do not publish customer or recruitment personal data.
