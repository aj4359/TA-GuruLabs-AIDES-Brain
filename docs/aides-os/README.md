# AIDES OS — governance foundation (pilot)

Status: **proposal / non-production**. This package does not connect to credentials, send messages or schedule actions. Public repository: never commit personal data, applicant profiles, customer records or secrets.

## Workflow
Goal -> create task -> inspect approved evidence -> propose narrow action -> enforce policy -> request human approval (if required) -> execute through an authorized adapter -> verify result -> record outcome -> stop.

## Design decisions
- Start with **one bounded Scout read-only pilot**, not unrestricted multi-agent autonomy.
- Task state is a record, **not** conversational memory. Persist only with an access-controlled storage adapter in a private environment.
- Treat web/email/PDF/RAG content as data, never as privileged instructions.
- Do not store credentials or personal information in public task logs.
- Measure verified results, source freshness, false-positive alerts, latency and run cost.
- No agent may override server-side policy through prompting.
- Default-deny actions; unknown action types are rejected.
- All production write actions need an authenticated, authorization-checked adapter and immutable audit trail.

## Acceptance gates
1. Task schema validated with explicit owner, goal, source scopes and stop condition.
2. Read-only tools allowed only on listed resources.
3. External publication, emails, payments, destructive operations, permission changes and sensitive-data disclosures remain blocked pending independent human approval, and their production adapters are **not included** here.
4. Retry guard and idempotency prevent duplicate effects in future adapters.
5. Every report separates observed evidence, analysis, recommendation, unresolved issues and verification outcome.
6. Normal, missing evidence, conflicting evidence, injected instructions, out-of-scope actions and budget-exhaustion tests pass.
7. No deployment until a real pilot is tested against an agreed evaluation dataset and approved.

## Files
- `task.schema.json`: minimal structured task contract.
- `policy.mjs`: pure, server-side policy decision helper (not an authorization service).
- `policy.test.mjs`: zero-dependency Node tests.
- `scout-pilot.md`: metrics, scope, human gates and rollout.

## Run tests
`node --test docs/aides-os/policy.test.mjs` (Node 20+).

The functions below are a policy **prototype**. In production, authorization must be enforced at the execution service boundary; approvals must be authenticated, scoped, time-limited and bound to exact action arguments.
