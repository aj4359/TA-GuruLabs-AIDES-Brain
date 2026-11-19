# Retail AIDE opportunity research and portfolio allocation

**Decision support, not autonomous spending or ungrounded prediction.** `prioritize.py` ranks **human/agent researched evidence cards**. The public-feed scanner produces *leads only*; it cannot certify demand. Empty input is deliberate: until researched evidence cards exist, the report recommends zero new opportunities.

## Research workflow for every new idea
1. Scout records the specific consumer, their pain, two genuinely independent dated sources, and actual purchase-intent evidence (not likes or follower counts).
2. Analyst checks competitor prices, reviews/complaints (with privacy and copyright respect), repeat demand, delivery feasibility, and reachable audience on TikTok/Instagram/Telegram. Mark unknowns honestly.
3. AUREUS Finance models net contribution: price minus platform/payment fees, delivery marginal costs and refund reserve; measure actual numbers as soon as available.
4. Compliance checks rights, UK customer protections, suitability of channel/platform and privacy; original deliverable + checkout must actually work.
5. ATLAS builds one reversible, small pilot. Public Learning Desk only publishes after existing media and platform QA.
6. Measure 7-day clicks to purchase, verified net revenue, refunds, support burden, buyer feedback. Reject vanity signals as purchase evidence.
7. Compare with existing near-sale work. Prefer the fastest validated route to the **first verified sale**, not the newest trend.

## Priority score (0–100 points, heuristic only)
- Direct buyer pain and demand evidence: **25**
- Actual purchase-intent evidence: **20**
- Speed to a working offer: **15**
- Gross contribution/margin: **15**
- Accessible no-cost distribution channels: **10**
- Delivery and support reliability: **10**
- Reuse/strategic fit: **5**

Each score is 0–5 and must be supported by an evidence card; unknown scores remain **missing**, not fabricated zeros or fives. A 90 is **not a 90% chance of success**. Do not rank unresearched trends as high-confidence opportunities.

**Hard gates:** two independent sources, independently verified purchase signal, rights cleared, eligible selling platform, tested digital deliverable, tested checkout and privacy review, positive estimated contribution. Missing evidence -> RESEARCH. Failed non-demand gates -> BLOCKED regardless of numeric score. Scores >=75 and all gates passed -> PILOT_CANDIDATE. 55–74.9 -> IMPROVE. Below 55 -> STOP_OR_PARK.

## Resource protection
- One new retail pilot at a time; preserve existing product launch work and cash.
- AIDEs may research and recommend reallocations, queue safe prototypes and compare experiments. **Do not automatically kill projects, change ongoing commitments, buy ads, open wallets, publish products or charge customers.**
- Pilot promotion must use original/licensed media and genuine QA receipts.
- Progress report each cycle: top 3 ranked candidates (or 'none verified'), verified pilot results, reasons for rejection, proposed next 7-day experiment, actual pounds earned (or 'unknown'). Never fabricate buyer counts or performance.
- Decisions are reversible and logged with evidence and dates.

## Usage
```bash
cd retail_desk
python -m unittest -v test_scout.py test_prioritize.py
cd ..
python retail_desk/prioritize.py retail_desk/opportunities.json retail_desk/output/priorities.json
```
The input file starts as an empty array. Add fully sourced evidence-card JSON objects conforming to the documented fields in `test_prioritize.py`. No real customer PII, secrets or sensitive internal pricing should be committed to public branches. Review the scoring thresholds with actual sales outcomes and update calibration when evidence accumulates.

**Activation:** the GitHub Actions schedule is only live after a reviewed merge to the default branch and workflow enablement. No ChatGPT task slot is used. A scheduled research run does not replace deeper buyer validation.
