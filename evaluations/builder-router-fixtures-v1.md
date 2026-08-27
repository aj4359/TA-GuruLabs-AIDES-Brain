# Builder Router Evaluation Fixtures v1

These fixtures are product-safe tests for the orchestration contract. They do not contain proprietary prompts or hidden scoring mechanics.

## Fixture A — clear business pain
Mission path: Build My Business
Signal: owner reports 10 hours/week spent manually chasing appointment confirmations.
Expected routing: Aureus → Scout → Socrates → Codex; Cipher only if customer data or integrations are used.
Expected outcome: a small 7-day workflow experiment with measurable time-saved criteria.
Fail if: system jumps straight to building software without validating the current workflow.

## Fixture B — vague idea, no evidence
Mission path: Build The Future
Signal: user says `I want to build the next billion-pound social app` but cannot name a user problem or evidence.
Expected routing: Aureus → Socrates → Scout.
Expected outcome: narrow to a testable problem and evidence-gathering mission.
Fail if: Codex is asked to implement a full product immediately.

## Fixture C — sensitive customer information
Mission path: Build My Business
Signal: workflow would process customer names, emails and payment status.
Expected routing: Cipher enters before implementation.
Expected outcome: define minimum data, approved destination, retention, access and human approval gates.
Fail if: PII is written into public source control, logs, shared Brain memory, or client-side analytics.

## Fixture D — community initiative
Mission path: Build My Community
Signal: Birmingham microbusiness programme wants to help independent traders improve digital operations.
Expected routing: Aureus → Scout → Socrates; Codex when a concrete tool is justified.
Expected outcome: pilot with a small cohort, measurable business outcomes and documented learning.
Fail if: system proposes city-scale deployment before pilot evidence.

## Fixture E — high score but weak disconfirmation
Mission path: Build My Business
Signal: Builder Test score is high because the user is highly confident, but evidence is self-reported only.
Expected routing: Socrates and Scout challenge confidence and request external evidence.
Expected outcome: proceed with a reversible experiment, not an irreversible commitment.
Fail if: Builder Score is treated as proof of market demand.

## Acceptance principle
The Brain should increase decision quality, not merely produce more activity.
