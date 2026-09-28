# TA VERIFIED — AIDES 60-Second Proof Demo v0.1

## Claim
The deterministic AIDES demonstrator completes a bounded mission through the governed-work chain and returns an approved capability, evidence-bearing execution receipt, tested recovery contract, PASS verification decision, and Cost per Verified Outcome (CPVO) of 4.00 cost units.

## Acceptance criteria
- unapproved capability is not selected;
- selected capability is approved and eligible for the required evidence mode;
- runtime receipt contains evidence and remains within the mission cost envelope;
- recovery contract is ready and records recovery as tested;
- verification result is PASS with an explicit VERIFIED_LIMITED_RELEASE decision;
- CPVO is calculated from attributable cost and a verified outcome;
- existing AIDES control-plane tests remain green.

## Scenario
`demo-001` in `aides-trust-control-plane/proof_demo.py`.

## Evidence
- AIDES Governed Work Moat run 36445139563 — PASS on commit `2c736e68c39c41d751bce86c271f4d355797be4c`.
- AIDES Trust Control Plane run 36445140473 — PASS on the same commit.
- `aides-trust-control-plane/test_proof_demo.py` asserts approved worker selection, evidence presence, recovery-tested state, PASS verification and CPVO 4.00.

## Failure → correction history
1. The first integration run failed because the demo referenced a recovery-validation function name that did not match the canonical recovery contract. The demo was corrected to use `assert_recovery_ready`.
2. The next run exposed a remaining stale recovery call site. That call was corrected.
3. The following run exposed an incorrect `MissionOutcome` constructor signature. The demo was corrected to include the mission ID before attributable cost and verification state.
4. Both AIDES workflow suites then passed on the corrected head.

The failures are retained as evidence that the proof gate rejected incompatible integration rather than allowing the demonstrator to bypass existing contracts.

## Result
PASS

## Release decision
VERIFIED_LIMITED_RELEASE

## Limitations
- deterministic repository fixture, not a live customer deployment;
- numeric cost values are cost units; no currency is asserted;
- no government certification, procurement approval or external assurance is claimed;
- the selected capability catalogue and evidence references are demonstrator fixtures;
- production integrations must independently re-pass their own acceptance criteria and evidence gates.

## Public-safe statement
“AIDES has a verified deterministic fixture demonstrating a governed outcome chain from authority and approved capability selection through evidence, recovery, verification and outcome economics.”

Do not shorten this to “AIDES is independently certified” or imply that the fixture proves production performance.
