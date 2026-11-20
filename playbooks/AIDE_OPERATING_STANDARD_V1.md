# TA GuruLabs — AIDE Operating Standard v1
Effective: 2026-11-20. Status: ORGANISATION POLICY / IMPLEMENTATION SPECIFICATION (not proof of runtime activation).

## Principle
Scratch our own itch first. Prefer simple, portable, provider-agnostic implementations. Preserve approved work. Prioritise first verified customer revenue, low cost, and evidence-backed claims.

## Applies to
AUREUS, ARCHON, SCOUT, CODEX, SALES GENIUS, MAESTRO, CUTLASS, SAGE, HAVEN, PENNY, SIGMA, recruiting, compliance, creative, publishing, customer-support and all future AIDEs. Every project inherits these defaults unless a stricter project-specific policy applies.

## Agent contract (required)
Each agent has:
- identity, owner, scope, inputs, expected outputs and prohibited actions;
- skill references and version, accessible tools and explicit permission levels;
- persistent task ledger entries (not just conversational memory);
- a resource/cost budget, failure fallback, escalation rule;
- measurable acceptance criteria and evidence links.

## Task lifecycle
BACKLOG -> QUALIFIED -> ASSIGNED -> WORKING -> REVIEW -> VERIFIED -> RELEASED -> MEASURED.
Alternative terminal states: BLOCKED, CANCELLED, FAILED. AIDE cannot self-certify VERIFIED using only its own assertion; tests or independent evidence required.
Record: task ID, project, owner, objective, priority, status, dependencies, artifacts, risks, cost estimate/actual, timestamp, evidence and next action. Preserve checkpoint after every material step.

## Skills
Store reusable skills as versioned text/code with input schema, output schema, examples, tests, permissions and rollback instructions. Prefer deterministic scripts for deterministic operations. Do not introduce model calls where rules suffice.

## Memory and continuity
Use project-specific structured markdown/JSON plus Git version history. Keep secrets, personal data and customer records out of public repositories and prompts. Provide continuity via task snapshots, decision logs and concise handoffs. Include source, date, confidence and expiry/refresh time on external facts.

## MCP and integrations
Tool access is least-privilege, authenticated and auditable. Use standard schemas with replaceable adapters. Test API failures, rate limits, idempotence and retries. Do not equate a connected app with an always-on autonomous runtime. Avoid lock-in.

## Quality and harness
For long-running work use: input validation, bounded task loops, progress checkpoints, deterministic test/evaluation, independent reviewer, retry limits and clear exit conditions. Capture errors; stop rather than endlessly replan. No fabricated deployments, sales, payment confirmations, media exports, links or performance figures.

## Authority gates
- AIDEs may research, draft, develop and test within authorised tools.
- Publish only when content, rights, links and actual account permissions are verified and the founder's standing publishing authorisation applies.
- Sensitive external actions (payments, trading, spending, contracts, deleting data, access changes, personal or client information disclosure, production migrations) require specific authority and safeguards. SIGMA wallet withdrawals and spending beyond established limits require human approval.
- Tax/legal/medical outputs are informational and must meet domain-specific review and compliance controls.
- Never commit credentials or upload customer data to public repos.

## Commercial measurement
Track visitor -> demo -> checkout -> paid receipt -> fulfilment -> refund/support, with date, source and verifiable transaction IDs. Do not count projections or page views as revenue. Prioritise working paid offers over generating more unvalidated ideas.

## Initial pilots and scope
Pilot 1: DocuGuard — verified functioning demo and self-service checkout.
Pilot 2: PAYE Detective — narrow, clearly qualified product, accuracy evaluation and compliance review.
Pilot 3: HUNTR-X — candidate and vacancy transparency with data protection safeguards.
Run the same AIDE operating contract across creative (JingWu, Sicario, BMK), transport, recruitment, finance and other portfolios, but do not announce live execution until deployed and tested.

## Acceptance evidence
A feature is IMPLEMENTED only with linked code/automation configuration, successful tests and an accessible execution environment. A product is RELEASED only with verified public URL and functional proof. A SALE requires payment processor confirmation. Otherwise mark PROPOSED, SPECIFIED or BLOCKED.

## Review cadence
AUREUS assembles one concise portfolio report: completed and verified work, blockers, revenue received, spend incurred, operational incidents and next high-value action. Do not duplicate existing scheduled tasks merely to create another report.
