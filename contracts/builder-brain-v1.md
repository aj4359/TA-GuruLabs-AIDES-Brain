# The Builder ↔ AIDES Brain v1

## Goal
Connect the public Builder experience to governed AIDES intelligence without exposing proprietary internals or transmitting unnecessary personal data.

## Public journey
The Builder cinematic → Mission Control → choose mission → Builder Test → Builder Score → Blueprint → optional Builder Session.

## Mission request
```json
{
  "contract_version": "1.0",
  "product": "the-builder",
  "mission_id": "builder-001",
  "path": "business",
  "objective": "Turn a business problem into the smallest useful next mission",
  "builder_test": {
    "problem_clarity": 0,
    "audience_clarity": 0,
    "evidence": 0,
    "testability": 0,
    "next_action": 0
  },
  "constraints": [],
  "privacy": {
    "contains_pii": false,
    "persist": false
  }
}
```

## Routing v1
1. **Aureus** checks strategic fit and desired outcome.
2. **Scout** identifies what evidence is missing.
3. **Socrates** attacks weak assumptions and reduces scope.
4. **Codex** proposes a smallest testable implementation when engineering is required.
5. **Cipher** reviews privacy, security, IP, and release implications before any persistence/integration.

Not every mission requires every AIDE. The orchestrator should select the minimum useful team.

## Response shape
```json
{
  "contract_version": "1.0",
  "mission_id": "builder-001",
  "status": "ready_for_human_review",
  "builder_score": 72,
  "verdict": "BUILD_SMALLER",
  "summary": "The pain appears credible but the first mission is too broad.",
  "aides_used": ["Scout", "Socrates"],
  "blueprint": [
    "Name one real customer with the problem",
    "Document their current workaround",
    "Define one measurable friction point",
    "Prototype one intervention",
    "Test within seven days"
  ],
  "risks": [],
  "human_approval_required": false,
  "memory": {
    "eligible": false,
    "reason": "anonymous preview mission"
  }
}
```

## Trust rules
- Builder Test scores are decision aids, not objective truth.
- No personal data is required to receive a score or initial Blueprint.
- Email/booking details must bypass the Brain unless there is a defined purpose and secure data contract.
- Proprietary AIDE prompts, hidden scoring logic, credentials, and private business context never return to the public client.
- Any future persistent memory must be explicit, minimal, auditable, and deletable.

## Release sequence
### Phase 1 — local simulation
Use deterministic/local routing to validate UX and response shape.

### Phase 2 — Brain adapter
Add a server-side adapter implementing this contract. No secrets in browser code.

### Phase 3 — controlled pilot
Enable for invited Builder Sessions with logs, human review, and rollback.

### Phase 4 — production
Only after privacy, security, evaluation, latency, cost, and failure-mode gates pass.
