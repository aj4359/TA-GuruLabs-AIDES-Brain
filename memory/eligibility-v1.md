# Memory Eligibility Schema v1

## Purpose
Define what the AIDES Brain may remember, what it must forget, and what requires explicit human approval before persistence.

## Memory classes

### M0 — Ephemeral
Use for temporary working context needed only to complete the current mission.
Examples: intermediate calculations, draft options, transient tool outputs.
Retention: session only.

### M1 — Product-safe learning
Reusable, non-sensitive lessons that improve future execution.
Examples: validated workflow patterns, approved templates, generic failure modes, product-safe evaluation results.
Retention: allowed when provenance and date are recorded.

### M2 — User-approved preference/context
Personal or business context that may improve future assistance but should persist only when the user has clearly asked for or accepted persistence.
Retention: explicit approval required.

### M3 — Restricted
Personal data, credentials, secrets, financial records, confidential client data, private commercial strategy, unpublished IP, internal security details.
Retention: prohibited by default in shared Brain memory. Store only in an approved secure system with purpose limitation and access controls.

## Required metadata for persistent memory
- memory_id
- class
- source
- created_at
- last_verified_at
- product
- purpose
- owner
- expiry_or_review_date
- sensitivity
- confidence

## Write rules
1. Default to M0 when classification is uncertain.
2. Never persist chain-of-thought or hidden reasoning.
3. Never persist credentials, tokens, passwords, private keys, or secret values.
4. Never move customer PII into a shared Brain layer merely because it may be useful later.
5. Persistent knowledge must record provenance and freshness.
6. Time-sensitive facts require a review/expiry date.
7. Human correction overrides prior learned conclusions.
8. Deletion requests must be enforceable at the storage layer.

## Builder example
A visitor's raw email address is M3 and must not enter shared Brain memory. A non-identifying lesson such as `independent businesses frequently report recurring admin friction around appointment follow-up` may qualify as M1 only after evidence and provenance are recorded.
