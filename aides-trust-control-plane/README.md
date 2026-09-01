# AIDES Trust Control Plane — Proof Slice

This proof implements the minimum governed-autonomy contract required to demonstrate a safe AIDES transaction without exposing proprietary orchestration mechanics.

## Governing primitives

1. Identity — every AIDE has an immutable identifier, role and version.
2. Authority — every action is checked against explicit permissions and approval boundaries.
3. Evidence — every recommendation carries sources, confidence, materiality and rationale metadata.
4. Intervention — any running transaction can be paused, denied, revoked or escalated.
5. Audit — every decision, approval, denial, execution and outcome emits a structured event.

## Proof transaction

Scout detects a material signal and recommends an external action.

The Control Plane must answer:
- Who acted?
- Under what authority?
- Based on what evidence?
- Was human approval required?
- Who approved or denied it?
- What happened afterward?
- Could execution be stopped or revoked?

## Safety boundary

The demonstration is deliberately narrow. Spending money, publishing, contacting outsiders, legal/regulatory representations, destructive data actions, pricing changes, agreements and material production/security changes require human approval.

Unknown capabilities default to DENY.

## Demo sequence

1. Load `examples/scout-signal.json`.
2. Evaluate the requested action against `policy.json`.
3. If approval is required, emit `approval.required` and block execution.
4. Record approval or denial.
5. Execute only after a valid approval event.
6. Emit outcome and audit events.
7. Demonstrate `pause`, `revoke` and `kill` states.

This directory is intended to become the independently reproducible evidence slice for Issue #7 and Issue #8.
