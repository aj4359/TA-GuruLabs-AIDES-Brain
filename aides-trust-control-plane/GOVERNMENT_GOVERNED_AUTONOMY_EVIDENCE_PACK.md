# TA GuruLabs Governed Autonomy Evidence Pack

## Purpose
A sanitised, procurement-ready evidence pack for government and regulated-enterprise conversations. It demonstrates the governance contract without disclosing proprietary orchestration, prompts, routing heuristics, private memory structures, credentials, customer data, or production topology.

## Core proposition
Autonomous work should be permitted only when the organisation can answer:

1. Who or what is acting?
2. What authority does it have?
3. What evidence triggered the action?
4. Is human approval required?
5. Can execution be denied, paused, quarantined or terminated?
6. Can credentials be revoked immediately?
7. What happened?
8. Can the historical record be independently verified?

## Demonstrated control model

**Identity → Authority → Evidence → Runtime Enforcement → Intervention → Audit → Verification**

### Identity
Every governed transaction carries an attributable actor identity and role/version context.

### Authority
Unknown capabilities default to deny. Consequential actions require explicit policy authority and, where defined, human approval.

### Evidence
Material actions carry an evidence envelope sufficient to explain the trigger without exposing proprietary decision mechanics.

### Runtime enforcement
The control plane defines vendor-neutral intervention primitives:
- deny a requested action
- pause execution
- revoke credentials
- quarantine the actor/execution context
- terminate execution

Runtime enforcement may reduce or remove authority. It never grants new authority.

### Human intervention
Consequential external actions remain approval-gated. Approval is scope-limited and recorded as an event.

### Audit
Events are sequence-linked and hash chained. Production-oriented Postgres persistence uses an atomic append path and prevents direct browser/authenticated mutation.

### Verification
Signed checkpoints provide an external verification path. The current baseline proves tamper detection; the next verification profile moves toward asymmetric public-key verification.

## Evidence available in the repository
- Default-deny policy
- Governed Scout transaction fixture
- Runtime enforcement state machine
- Unit tests covering deny/pause/revoke/quarantine/terminate paths
- Tamper-evident audit chain
- Atomic Postgres append RPC
- Client write-denial CI test
- Signed checkpoint proof
- Command Centre governed-transaction evidence surface

## Procurement mapping

### Safe agent adoption / operational risk management
Relevant evidence:
- explicit authority boundaries
- least privilege
- human approval gates
- runtime monitoring/intervention contract
- attributable audit history
- chain verification
- external checkpoint verification path

### Planning, automation and autonomous systems
Relevant evidence:
- governed autonomous execution
- intervention before/during execution
- bounded credentials
- explicit outcome recording
- post-action evidence suitable for operational review

## Security and IP boundary

Safe to disclose:
- governance primitives
- event semantics
- control states
- policy outcomes
- test evidence
- narrow demonstrator flows
- verification interfaces

Retain as proprietary:
- internal orchestration/routing strategy
- private prompts and decision heuristics
- memory architecture beyond public contracts
- customer-specific policies and data
- production credentials
- production automation topology

## What this pack does not claim
- It does not claim endpoint detection/response functionality.
- It does not claim hash chaining makes storage immutable.
- It does not claim a valid signature proves the underlying evidence was truthful.
- It does not claim a proof demonstrator is equivalent to a fully accredited production deployment.

## Reviewer test
A reviewer should be able to inspect one transaction and answer:

**Who acted? Under what authority? Based on what evidence? Who approved it? What runtime controls existed? Could it be stopped? What happened? Has the evidence trail been altered?**
