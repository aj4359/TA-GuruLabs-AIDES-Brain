# TA GuruLabs AIDES Brain v1

The AIDES Brain is the shared memory, knowledge, orchestration and governance layer used by TA GuruLabs products. It is not a product front end and should not become a dumping ground for product-specific application code.

## Core principle

One Brain. Many products.

Products own their user experience and product-specific business logic. The Brain owns reusable intelligence, routing, policies, memory contracts, evaluation rules and cross-product learning.

## Proposed structure

- `aides/` — role definitions, operating charters and capability contracts for named AIDES.
- `orchestration/` — mission routing, delegation, handoffs and human-approval rules.
- `knowledge/` — reusable company, product and domain knowledge packages.
- `memory/` — schemas for episodic, semantic and operational memory.
- `evaluations/` — common quality, safety and usefulness tests.
- `security/` — trust, secrets, data-handling and audit requirements.
- `contracts/` — stable product ↔ Brain interfaces.

## Product boundary

Product repositories such as `gurulabs-vision` remain responsible for UI, UX, client-side state and product-specific features. Reusable intelligence may graduate into the Brain only when it is useful across multiple products.

## Current migration note

PAYE Forensics code already in this repository remains untouched during Brain v1 restructuring. No destructive moves will occur until product boundaries are reviewed and a migration plan is agreed.
