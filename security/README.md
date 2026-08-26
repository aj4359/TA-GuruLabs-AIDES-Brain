# Security and Trust Baseline

Brain v1 defaults to least privilege, minimum necessary data and explicit human control.

## Baseline rules

- Never commit secrets, credentials, private keys or production tokens.
- Product requests should send the minimum context needed for a mission.
- Personal data is not shared across products by default.
- Confidential and internal missions must not be promoted into public knowledge.
- High-impact external actions require a human-approval gate unless a separately approved policy exists.
- Memory writes are deliberate and auditable, not automatic.
- Reusable knowledge must be separated from product-specific customer data.
- Public repositories must not contain proprietary prompts, scoring logic or implementation details that create unnecessary IP exposure.

## Repository visibility

This repository is currently public. Before storing proprietary AIDES behaviour, internal operating logic or confidential product intelligence, review repository visibility and move sensitive implementation into a private repository or private infrastructure.

## Cipher responsibility

Cipher owns policy checks for secret exposure, data sensitivity, IP leakage and release gating. Cipher may block a mission from memory persistence or external execution when safeguards are not satisfied.
