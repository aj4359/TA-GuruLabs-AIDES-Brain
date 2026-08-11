# PAYE Forensics — Animated Underpayment Detective

Working standalone prototype for issue #1.

## Purpose
Help a UK PAYE customer understand a **possible reconstruction** of how an HMRC underpayment, in-year adjustment or tax-code result may have arisen. It must never claim access to HMRC's internal reasoning.

## Run
Open `index.html` in a browser. Use **Load example case** to replay the animated Tax Story immediately.

## Current prototype scope
- Customer case inputs for tax year, jurisdiction, non-savings income, savings, ISA income, dividends, tax deducted and HMRC stated amount.
- Purposeful animated calculation timeline.
- Tax Stack visual.
- HMRC stated amount vs reconstruction vs difference.
- Confidence states: Likely explanation / Possible explanation / Unable to reconcile.
- Adviser-style JSON audit object generated from the same calculation that drives the animation.
- ISA income explicitly excluded from ordinary taxable savings.
- Deliberate fail-safe for Scotland: the prototype refuses to silently reuse England/NI non-savings bands.
- Reduced-motion support through the browser accessibility preference.

## Production requirements
This is an integration prototype, not production tax software. Before public release:
1. Move all tax rules to source-controlled, versioned tax-year + jurisdiction rule files.
2. Verify every current and historical figure against authoritative HMRC/GOV.UK sources.
3. Implement Scottish and Welsh jurisdiction logic completely.
4. Add PAYE tax-code/IYA reconstruction rules, pensions, multiple employments and benefits-in-kind.
5. Add unit/golden tests for every rule and scenario.
6. Add provenance metadata and rule IDs to each calculation step.
7. Keep proprietary scenario ranking/scoring server-side or otherwise out of public client code.
8. Integrate with the customer-facing PAYE app once its deployment repository is identified.

Core proposition: **HMRC gives you the number. We help you understand how they may have got there.**
