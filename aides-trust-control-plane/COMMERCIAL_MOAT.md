# AIDES OS Commercial Moat Boundary

## What we should assume will commoditise
The following controls are becoming baseline infrastructure and should not be treated as the core moat on their own:

- human-in-the-loop approval
- basic policy gates
- simple allow/deny rules
- hash-chained audit logs
- generic agent identity records
- standard kill switches
- single-agent observability dashboards

TA GuruLabs should implement these well, prove them, and make them interoperable. It should not rely on them as the principal source of defensibility.

## Where proprietary value should concentrate

### 1. Organisational memory
The system remembers prior signals, decisions, corrections, outcomes and unresolved questions so the workforce improves its organisational understanding rather than repeatedly starting from zero.

### 2. Cross-AIDE orchestration
The valuable layer is not one agent performing one task. It is governed coordination across intelligence, product, engineering, sales, operations, finance, legal/security and support roles.

### 3. Authority architecture
Permissions are contextual: who may act, on which resource, for which purpose, at what materiality, under what evidence threshold, for how long, and with which escalation path.

### 4. Evidence lineage
Important decisions should be traceable from external/internal signal through interpretation, recommendation, approval, action and outcome.

### 5. Runtime intervention
The organisation can reduce authority while work is in flight: deny, pause, revoke credentials, quarantine or terminate execution.

### 6. Outcome learning
The system should compare expected vs actual outcomes and feed this back into future recommendations, confidence and operating policy.

### 7. External verification
Customers, auditors and procurement reviewers can independently verify selected governance evidence without receiving proprietary internals or signing secrets.

## Public product principle
**Governance primitives are visible. Orchestration intelligence remains protected.**

## Strategic consequence
AIDES OS should be sold as a governed organisational operating layer, not as a collection of agents and not as another security product. Security platforms, identity providers, observability products and workflow tools should be treated as integration surfaces where appropriate.
