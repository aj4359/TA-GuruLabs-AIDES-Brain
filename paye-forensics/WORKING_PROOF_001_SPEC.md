# PAYE Forensics — Working Proof #001

Status: implementation acceptance specification
Priority: P0

## Purpose
Demonstrate that PAYE Forensics reconstructs a difficult PAYE history and identifies where an investigator should focus. It is an investigation/readiness product, not HMRC filing software.

## Required synthetic case
Use fictional/synthetic data only for the proof. Include:
- multiple employments with overlapping or ambiguous end/start events
- P45/P60 and starter-declaration events
- at least one tax-code change
- pension income or withdrawal event
- benefit-in-kind transition (for example medical insurance or company car) with historical treatment captured as coded, payrolled or other supported state
- an apparent discrepancy that cannot be explained by a single-period calculator

## Required output
1. Tax History Graph / chronological event ledger
2. source/evidence attached to each material event
3. deterministic calculation/audit JSON where calculation is supported
4. discrepancy hypotheses clearly separated from proven findings
5. confidence and missing-evidence flags
6. recommended investigation steps for payroll/tax professional
7. TA VERIFIED proof chain:
   MISSION -> WORK -> EVIDENCE -> COST -> RESULT -> VERIFIED

## Pass criteria
- same inputs reproduce the same deterministic outputs
- no unsupported claim is presented as fact
- benefit-in-kind transition is visible in the longitudinal history
- a reviewer can trace each conclusion to evidence
- output is understandable without HMRC-internal knowledge
- no filing/submission to HMRC occurs

## Commercial demo
Show BEFORE (fragmented records / unclear discrepancy) and AFTER (reconstructed history / evidence / investigation path). Do not lead with feature inventory.
