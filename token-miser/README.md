# Token Miser™

**Intelligence spend control for TA GuruLabs and external customers.**

Token Miser is a provider-neutral control layer that sits before model execution and decides how much intelligence a task deserves before money is spent.

> Spend intelligence where intelligence creates value. Never spend tokens merely because tokens are available.

## Product thesis

Most model-cost tooling reports spend after it happens. Token Miser is designed to govern spend before and during execution while preserving task quality.

## Decision ladder

1. REUSE — return an approved cached result when safe.
2. COMPUTE — use deterministic code/rules when generation is unnecessary.
3. LEAN — route simple generation/extraction/classification to a low-cost model tier.
4. REASON — escalate genuinely difficult work to a stronger reasoning tier.
5. PREMIUM — use the highest-cost tier only where policy and task value justify it.

## v1 capabilities

- Per-request token budgets
- Context deduplication and truncation
- Task complexity classification
- Model-tier routing
- Deterministic-work detection
- Cache/reuse decisioning
- Budget and quota enforcement hooks
- Usage/cost telemetry contract
- Explainable routing decisions
- Product/AIDE attribution
- Quality floor and escalation controls

## Architecture

`Product / AIDE -> Token Miser Gateway -> Policy Engine -> Context Miser -> Cache/Compute check -> Model Router -> Provider -> Telemetry + Audit`

Token Miser belongs beside the AIDES Trust Control Plane rather than inside an individual product. TA GuruLabs products should integrate through one shared gateway so policy changes propagate across the estate.

## Commercial direction

Token Miser should also be capable of operating independently as a multi-tenant SaaS/API gateway for organisations running model-heavy products, agents and internal workflows.

Potential customer promise: **Use the intelligence you need. Pay for as little waste as possible.**

The commercial moat should be built around policy, historical execution data, quality/cost optimisation, workload-specific routing profiles and measurable savings rather than a simple model proxy.

## Status

Foundation specification created. This does **not** yet mean every TA GuruLabs model call is routed through Token Miser. Estate integration must be verified product by product and measured through telemetry before claiming organisation-wide coverage.
