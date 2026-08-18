# PAYE Forensics v3 — Creative Experience Layer

## Product idea
PAYE should feel less like reading a tax calculation and more like watching a mystery being solved.

Customer promise:

> HMRC gives you the number. We help you understand one possible route to it.

The experience deliberately avoids pretending that PAYE Forensics can see HMRC's internal calculation history. It builds an evidence-based reconstruction from the information available.

## Signature interaction: The Tax Story

The customer starts with one intimidating figure in the centre of the screen, for example:

**£640 UNDERPAYMENT**

The interface then says:

**Let's see how this may have happened.**

Each stage is revealed as a scene, not a spreadsheet row.

1. Income sources enter the stage individually.
2. Allowances visually shield or remove income from the taxable stack.
3. ISA income is visibly moved outside the taxable stack.
4. Savings and dividend rules reshape what remains.
5. Tax due is assembled.
6. Tax already paid moves against it.
7. The remaining possible shortfall appears.
8. The screen splits: HMRC stated amount vs our reconstruction.
9. Ranked possible causes appear as evidence cards.
10. The experience ends with a clear next action.

## Creative motifs

### The Tax Stack
Income appears as physical blocks. Allowances slide across and cover parts of those blocks. Taxable portions remain illuminated. This makes allowances understandable without requiring the customer to know tax terminology first.

### The ISA Shield
Where ISA income is entered, it is separated from ordinary taxable savings with a visible shield animation. The product says what it did, not merely the result.

### The Reconciliation Bridge
At the end, two large amounts sit on opposite sides:

HMRC says → £640
PAYE Forensics reconstruction → £637

A bridge fills according to the closeness of the figures. The text status, not colour alone, communicates:
- Strong match
- Plausible match
- We found a mismatch

The bridge is a visual metaphor only. It must never imply certainty.

### The Mystery Board
Ranked possible causes appear as evidence cards connected to the reconstructed result:

- Savings estimate changed
- Income estimate changed
- Pension income present
- Second employment present
- Tax-code allowance appears to have changed
- Tax deducted below reconstructed liability

Cards show evidence and confidence without exposing proprietary ranking logic.

### Time Machine
If previous HMRC estimates are supplied, the customer can scrub between "Before" and "After" states. Changed figures animate rather than merely displaying two columns. This is particularly useful for explaining why a tax code or projected liability may have changed during the year.

### Pay-Day Road
For an in-year adjustment, remaining paydays appear as stops along a horizontal route. An illustrative amount is distributed across them to show the concept of collecting extra tax over the rest of the year. It must be labelled as illustrative because actual collection depends on coding instructions, payroll timing and code basis.

## Customer language
Prefer:
- "We found a possible explanation"
- "This figure changed"
- "Here's what that could have done to your tax"
- "These numbers do not quite match"
- "Check this figure first"

Avoid:
- "HMRC did this because..." unless directly evidenced
- "You definitely owe..."
- "HMRC made an error" unless the evidence is sufficient
- unexplained terms such as IYA, IYAR, ANI, W1/M1 in customer mode

Adviser Mode can display the technical term alongside a plain-English explanation.

## End states

### Strong match
"Our reconstruction is very close to the HMRC amount. This looks like a plausible route to the figure shown."

### Plausible match
"Some of the figures line up, but there is still a gap. There may be an estimate, coding adjustment or payroll detail we have not been given."

### Mismatch
"We could not reproduce the HMRC amount from the information entered. That is useful. It tells us which figures to check before accepting the explanation."

## Next-action cards
Every story ends with actions rather than a dead-end result:

- Check the income estimate HMRC used
- Check savings interest
- Check State Pension/private pension
- Check taxable benefits
- Check tax already deducted
- Check old and new tax codes
- Compare latest coding notice
- Show adviser audit trail

## Adviser Forensics companion
The animation and adviser screen must use the exact same calculation result object. Adviser mode adds:

- rule IDs
- source metadata
- tax-year and jurisdiction
- assumptions
- warnings
- tax-band slices
- previous vs current figures
- ranked scenario evidence
- reconciliation difference
- audit JSON

## Accessibility
- reduced-motion mode becomes a narrated stepper rather than removing information
- every animated value also exists as text
- keyboard replay and step controls
- status never communicated by colour alone
- customer can pause at every scene

## IP boundary
Public UI may reveal the evidence used for each possible cause but should not disclose proprietary weighting, ranking heuristics or future probabilistic scoring implementation.
