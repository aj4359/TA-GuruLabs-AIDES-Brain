# Project Constellation — Institutional Memory Layer v0.1

Status: internal / confidential architecture.

## Objective
Turn AIDES OS from a collection of capable agents into an organisation that retains evidence, decisions, corrections and outcomes across runs.

Core loop:

`Trigger -> Sources -> Retrieve relevant current view -> Detect delta -> Evidence gate -> Recommend -> Human correction -> Mission -> Outcome -> Memory`

Models are replaceable workers. TA GuruLabs institutional memory remains TA GuruLabs property.

## First proving slice

Start deliberately small: Scout watches 10 defined competitors/products. Each run compares fresh evidence with the accepted current market state and returns only material NEW, CHANGED, CONTRADICTED or STALE findings. Aureus converts useful findings into OBSERVE, INVESTIGATE, RESPOND, BUILD or ESCALATE recommendations. Human corrections update durable rules rather than merely editing today's prose. Accepted actions become AIDES missions. Mission outcomes return to memory.

## Working v0.1 implementation

The dependency-free Node.js implementation now provides:

- an atomic JSON persistence adapter that can later be replaced by PostgreSQL/Supabase without changing the memory contract;
- a delta engine that classifies evidence as NEW, CHANGED, CONFIRMED or CONTRADICTED;
- temporal supersession: changed facts remain in history but no longer appear in the current view;
- a materiality gate, initially set to 0.5;
- correction ingestion that converts approved human judgement into a durable rule for later runs;
- scoped retrieval by domain and subject;
- executable behavioural tests.

Run the proof:

```bash
cd constellation-memory
npm test
```

The key acceptance test records a human correction raising Scout's materiality threshold to 0.75. A later 0.70 finding is then suppressed. This demonstrates that the next run behaves differently because of the previous correction.

The JSON adapter is a proving implementation, not the production concurrency layer. The next storage adapter should use PostgreSQL/Supabase transactions, row-level security and an append-only audit log.

## Canonical memory states

- NEW
- CURRENT
- CONFIRMED
- CONTRADICTED
- DISPUTED
- STALE
- SUPERSEDED
- EXPERIMENTAL
- APPROVED
- REJECTED

## Canonical memory types

- fact
- hypothesis
- decision
- experiment
- correction
- outcome
- lesson

## Required provenance

Every durable record must preserve its evidence/source, observed date, validity interval where known, confidence, product/domain, permissions, review date and supersession history. Never silently overwrite history.

## Decision memory

Store the chain:

`Evidence -> Interpretation -> Decision -> Action -> Outcome -> Lesson`

The objective is retrieval of the useful lesson, not indiscriminate replay of old research.

## Memory boundaries

Separate scopes by default:

- corporate
- product
- operational
- research
- AIDE performance
- restricted/customer

Do not create one indiscriminate vector pool. Restricted/customer data must never leak into general competitive research.

## Forgetting lifecycle

`CURRENT -> STALE -> SUPERSEDED -> ARCHIVED`

Historical facts remain available for temporal reasoning but stop contaminating current decisions.

## Seven-day acceptance test

Measure useful deltas, false positives, duplicate findings, correction rate, evidence quality, actions generated/completed, retrieval accuracy and whether a correction changes the next run.

The proving question is:

> What have we learned this week, which assumptions changed, what decisions did those changes produce, and what should TA GuruLabs do differently next week?

A successful answer must be reconstructable from evidence and decision history rather than generated from today's web alone.

## IP rule

The internal memory schema, scoring/materiality rules, evidence weighting, routing, correction logic, graph relationships and AIDES orchestration are confidential implementation details. Public demonstrations should explain outcomes without publishing the recipe.

© 2026 TA GuruLabs. All rights reserved.
