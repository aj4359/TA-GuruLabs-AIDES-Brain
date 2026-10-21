# Builder Mission Router v1

## Purpose
Translate a Builder journey selection into a governed AIDES mission package without exposing private internal reasoning or proprietary implementation details.

## Mission paths

### Build Myself
Default AIDES: Aureus, Socrates
Optional: Scout
Use when the user needs clarity, prioritisation, readiness, or a practical next step.

### Build My Business
Default AIDES: Aureus, Scout, Socrates, Codex
Optional: Cipher
Use when the user is trying to improve a business, validate an opportunity, remove friction, or create a testable product/workflow.

### Build My Community
Default AIDES: Aureus, Scout, Socrates
Optional: Codex, Cipher
Use when the mission affects a neighbourhood, network, local business ecosystem, city initiative, or public-facing community programme.

### Build The Future
Default AIDES: Aureus, Scout, Socrates, Codex, Cipher
Use for ambitious product, platform, infrastructure, or experimental missions where technical, strategic and trust risks must be considered together.

## Routing sequence
1. Receive product mission envelope.
2. Cipher performs an initial privacy/IP/data boundary check when sensitive data or external integrations are present.
3. Aureus evaluates strategic fit and mission scope.
4. Scout validates evidence and identifies material unknowns.
5. Socrates pressure-tests assumptions and proposes a disconfirming experiment.
6. Codex produces a technical execution path only when engineering is justified.
7. Router assembles the product-safe response.
8. Human approval is requested when a configured release, legal, privacy, financial, security, or irreversible-action gate is triggered.

## Product-safe response
Return only:
- mission summary
- Builder Score inputs or evaluation outcome
- recommended next action
- first blueprint
- named AIDES involved
- confidence and key uncertainty
- approval requirement

Do not return chain-of-thought, confidential prompts, proprietary weighting, internal security details, credentials, or private memory.

## Example
Input path: `Build My Business`
Objective: reduce 10 hours of weekly admin for an independent Birmingham business.

Possible routing:
- Aureus: clarify strategic objective and measurable value.
- Scout: identify the current workflow and evidence of recurring friction.
- Socrates: challenge whether automation is actually the cheapest intervention.
- Codex: propose the smallest safe prototype if engineering is warranted.
- Cipher: join only if customer data, credentials, payments, or external integrations are involved.

Output: a concise 7-day experiment and 30-day Blueprint suitable for Mission Control.
