# Product ↔ AIDES Brain Contract v1

This contract defines the first stable boundary between TA GuruLabs product experiences and the shared AIDES Brain.

## Product sends

A product may submit a mission envelope containing:

- `mission_id`
- `product`
- `actor_type` (for example visitor, customer, founder, operator)
- `intent`
- `context_summary`
- `constraints`
- `requested_outcome`
- `sensitivity` (`public`, `internal`, `confidential`)
- `human_approval_required`

Products should send the minimum information necessary. Secrets, unnecessary personal data and raw private history must not be included by default.

## Brain returns

The Brain returns a governed mission response containing:

- `mission_id`
- `route`
- `assigned_aides`
- `recommended_actions`
- `evidence_or_assumptions`
- `risk_flags`
- `human_approval_gate`
- `memory_write_recommendation`
- `status`

## Human control

The Brain may recommend, draft, analyse, rank or route. High-impact external actions remain behind an explicit human-approval gate unless a separately approved automation policy allows them.

## Memory rule

A product may request a memory write, but the Brain decides whether the information belongs in reusable memory. Product telemetry and personal information are not automatically promoted into shared memory.

## Example: The Builder

Input:

```json
{
  "mission_id": "builder-001",
  "product": "gurulabs-vision",
  "actor_type": "visitor",
  "intent": "Build My Business",
  "context_summary": "Visitor completed the Builder Test and wants a practical first blueprint.",
  "constraints": ["small first version", "no perfection requirement"],
  "requested_outcome": "30-day blueprint",
  "sensitivity": "public",
  "human_approval_required": false
}
```

Possible Brain response:

```json
{
  "mission_id": "builder-001",
  "route": "builder.business.discovery",
  "assigned_aides": ["Scout", "Codex", "Socrates"],
  "recommended_actions": [
    "Name the customer pain in one sentence",
    "Validate it with three real users",
    "Prototype the smallest useful intervention"
  ],
  "evidence_or_assumptions": ["Customer evidence not yet supplied"],
  "risk_flags": [],
  "human_approval_gate": false,
  "memory_write_recommendation": "none",
  "status": "ready"
}
```

## Versioning

Breaking changes require a new contract version. Product code should never depend on undocumented Brain behaviour.
