# AIDES Resource Governor (pilot)

Dependency-free Python + SQLite admission control for **optional** AIDE work.
No paid services, no external API calls, no modifications to live schedules,
wallets or orders. This is a reusable component, **not yet active across AIDES**.

## Controls
- Per-ISO-week estimated USD reservations and reconciliation with actual costs.
- One owner + unique job key per unit of work (deduplication).
- 80% conservation mode: optional tasks stop; essential tasks can still run if budget permits.
- Hard weekly estimate cap, retry limit (2), fan-out cap (2).
- Durable SQLite audit ledger and budget usage.

## Local quick start
Run `python -m unittest discover -s resource_governor -p 'test_*.py'` at repo root.

```python
from resource_governor import Governor, Policy

g = Governor("aides_usage.db", Policy(weekly_budget_usd=5.0))
decision = g.admit(job_key="scout:2026-11-10:morning",
                   owner="Scout", estimate_usd=0.02)
if decision.permitted:
    try:
        # Execute the real work using your existing workflow.
        actual_cost_from_provider = 0.013
        g.complete(job_key="scout:2026-11-10:morning",
                   actual_usd=actual_cost_from_provider)
    except Exception:
        g.release(job_key="scout:2026-11-10:morning")
        raise
```

## Integration requirements
1. Wrap every actual external model/API action with `admit()` prior to execution.
2. Use a shared persistent SQLite volume **or replace SQLite with a transactional central DB**.
   GitHub-hosted ephemeral runners do not share a SQLite ledger; no cross-run enforcement there.
3. Measure provider-reported tokens and cost. Avoid estimated savings claims without a baseline.
4. Give scheduled tasks stable occurrence keys, not permanent task names. For event workflows,
   use source event IDs; dedupe scope is one ISO week.
5. Treat `conservation_mode` as a pause for optional work, not market-data ingestion,
   trading risk checks, emergency notifications or payment/webhook acknowledgements.
6. Record real outcomes, elapsed time, errors and missed events separately; this module only
   tracks budget commitments and completions.
7. Enforce strict broker/wallet approvals outside this governor; it is not an order or funds gate.

## Limitations and rollout
- The weekly dollar budget is a **placeholder configuration** (not your actual ChatGPT limits).
- Actual cost higher than reserved cost can push recorded spend above threshold;
  upstream provider hard caps remain necessary.
- This module is not wired into existing production runners or dashboards.
- Test in sandbox first, then integrate one low-risk workflow and compare 7-day baselines.
- Do not claim 80% savings until measured.

## Provider usage telemetry (second-stage pilot)

`telemetry.py` adds a persistent SQLite usage-event ledger that deduplicates
events by provider request ID and groups reported input/output tokens, costs,
failures and unknown-cost records. It does **not** call paid APIs, invent token
prices or claim the model calls in other apps are already instrumented.

```python
from resource_governor.telemetry import Telemetry
telemetry = Telemetry("/persistent/aides/usage.sqlite3")
telemetry.record(
    event_id="provider-request-unique-id",
    workflow="Scout", provider="your-provider", model="model-from-response",
    input_tokens=120, output_tokens=30,
    provider_cost_usd=None,
    source="provider_usage_response",
)
print(telemetry.summary())
```

- Configure the database path to an **existing backed-up persistent filesystem**
  shared by the actual runner(s). Never use GitHub Actions' temporary workspace
  to claim cross-run durability. SQLite on a network filesystem may need a
  different transactional database.
- Log `provider_cost_usd` only when known from a genuine provider billing
  source. Null means unknown, not zero. Never equate token count to money
  without explicit provider/model tariff and caching terms.
- Source request IDs must be globally unique; prefix them with provider and
  workflow if necessary. Avoid storing prompts, API keys, user data or secrets.
- Do not connect any production provider until credentials, data retention,
  backup and access controls have been reviewed.
- Run: `python -m unittest discover -s resource_governor -p 'test_*.py' -v`.
- The admission controller and usage telemetry are separate components for
  now. Integration with an actual paid provider needs its execution wrapper,
  confirmed pricing source, and an atomic budget configuration.
