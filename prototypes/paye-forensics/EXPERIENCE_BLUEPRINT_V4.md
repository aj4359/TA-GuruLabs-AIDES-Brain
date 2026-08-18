# PAYE Forensics v4 — Experience Blueprint

## Product promise
**HMRC gives you the number. We help you understand how they may have got there.**

The product should feel like a financial detective story, not a calculator. Every visual must map to the deterministic result object.

## Signature interactions

### 1. Tax MRI
A vertical scan of the case that lights up each layer: income sources, Personal Allowance, tax-code allowance, savings, ISA, dividends, tax due, tax collected, underpayment gap. The customer can scrub up/down to revisit any layer.

### 2. Tax Time Machine
Side-by-side previous vs current estimates. Animate only the fields that changed, with impact labels such as “possible +£X tax effect”. Never claim HMRC changed the figure unless supplied by the customer or evidence.

### 3. Code Decoder Lens
Show old and new tax codes as two cards. Highlight the numeric allowance change, prefixes/suffixes and special-code caveats. Provide “This code may mean…” rather than “This code means…” when context is incomplete.

### 4. Pay-Day Road
For an in-year adjustment, display remaining paydays as stepping stones. The total possible adjustment flows across them. Mark Week 1/Month 1 as a possible coding basis only when evidence or HMRC-manual logic supports that scenario.

### 5. Mystery Board
Rank possible causes with three separate dimensions:
- Evidence strength
- Financial impact
- Reconciliation contribution

Do not collapse these into one opaque confidence number in customer view. The proprietary combined ranking can remain internal.

### 6. Reconciliation Bridge
Left side: HMRC stated amount. Right side: PAYE Forensics reconstruction. The bridge fills as the difference narrows. End states:
- Strong match: difference ≤ £5
- Plausible match: small absolute/relative difference
- Does not reconcile: material difference

Copy must state that a strong match supports plausibility, not proof.

### 7. Missing Piece Mode
If the numbers do not reconcile, turn the experience into a guided search rather than failure. Ask the user to check likely missing items one at a time: second job, State Pension, private pension, benefit in kind, savings estimate, earlier adjustment, tax deducted, code basis, previous employer, taxable redundancy/payment, other untaxed income.

### 8. Customer Calm Layer
Every alarming number is paired with context. Example: “HMRC says £640” should immediately be followed by “We’ll break this down. We won’t assume the figure is right or wrong.” Avoid red warning screens unless the product is identifying a genuine data conflict.

## Data model additions
Future result objects should include:
- caseFingerprint
- evidenceItems[]
- missingDataPrompts[]
- estimateChanges[]
- taxCodeEvents[]
- payPeriodModel
- reconciliationContribution by scenario
- sourceProvenance by calculation step
- certaintyClass: observed / inferred / illustrative

## Adviser Mode
Adviser view should show every assertion with one of three badges:
- Observed: directly entered or sourced
- Inferred: calculated or deduced from observed data
- Illustrative: hypothetical scenario used to explain a possible HMRC route

This is a core trust mechanism and should be preserved in exports/audit logs.

## Future creative extensions
- Voice narration generated from the Storyteller scene object
- “Explain this to me like I’m new to tax” reading mode
- “Adviser language” toggle
- Screenshot/PDF coding notice parser with human confirmation before figures enter the calculation
- Shareable case summary that contains no sensitive identifiers by default
- Annual tax story replay showing how a case evolved through the year

## Guardrail
Animation may simplify presentation, but never simplify the underlying arithmetic. One calculation object, one audit trail, many views.