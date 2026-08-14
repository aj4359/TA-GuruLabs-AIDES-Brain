# PAYE Forensics — Animated Underpayment Detective

Working standalone prototype for issue #1.

## Purpose
Help a UK PAYE customer understand a **possible reconstruction** of how an HMRC underpayment, in-year adjustment or tax-code result may have arisen. It must never claim access to HMRC's internal reasoning.

Core proposition: **HMRC gives you the number. We help you understand how they may have got there.**

## Run
Open `v3.html` in a browser for the latest interactive Tax Story experience. `v2.html` remains available for the earlier engine/UI pass and `index.html` for the first prototype.

## Current prototype scope
- Versioned 2026/27 rules separated from presentation.
- England/NI/Wales and Scottish non-savings handling.
- Employment, second job, private pension, State Pension, benefits and other non-savings income.
- Savings starting-rate, Personal Savings Allowance, dividends and ISA exclusion.
- Personal Allowance taper handling.
- Deterministic underpayment reconstruction.
- HMRC stated amount vs reconstruction vs difference.
- Confidence states: Likely explanation / Possible explanation / Unable to reconcile.
- Ranked possible-cause signals using entered evidence.
- Indicative in-year adjustment per remaining payday.
- Customer Tax Story narration generated from the same result object as Adviser Mode.
- Reconciliation Bridge and Mystery Board concepts in v3.
- Adviser-style JSON audit object generated from the same calculation that drives the story.
- Browser regression test runner.
- Reduced-motion support.

## Creative product direction
See `EXPERIENCE_BLUEPRINT_V4.md` for the next experience layer, including:
- Tax MRI
- Tax Time Machine
- Code Decoder Lens
- Pay-Day Road
- Mystery Board
- Reconciliation Bridge
- Missing Piece Mode
- Customer Calm Layer

## Production requirements
This remains an integration prototype, not production tax software. Before public release:
1. Run and fix the regression suite against all supported scenarios.
2. Attach official-source provenance metadata to each rule and calculation step.
3. Deepen PAYE tax-code/IYA modelling, including code basis and payroll timing.
4. Expand historical tax-year support.
5. Add stronger tax-code parsing and special-code handling.
6. Preserve Observed / Inferred / Illustrative certainty labels through the audit trail.
7. Keep proprietary scenario ranking/scoring server-side or otherwise out of public client code.
8. Integrate with the customer-facing PAYE app once its deployment repository is identified.
9. Add privacy-safe case persistence and exports before storing customer data.

## Guardrail
A close numerical match is evidence of a plausible route, not proof of HMRC's internal calculation. One calculation object should drive every customer animation, adviser view and audit record.