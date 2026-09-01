# Procurement Evidence Matrix — Safe Agent Adoption

| Requirement area | Proof artifact | Evidence produced | Status |
|---|---|---|---|
| Agent identity | `examples/scout-signal.json` | Immutable actor ID, role, version | Implemented |
| Least privilege / authority | `policy.json` | Default deny + explicit action rules | Implemented |
| Human oversight | `policy.json`, `demo.py` | `approval.required`, grant/deny events | Implemented |
| Monitoring / observability | `demo.py` | Structured transaction event stream | Implemented proof |
| Intervention | `demo.py` | Authority revoke + kill path | Implemented proof |
| Evidence lineage | signal fixture + audit events | Source metadata, confidence, materiality | Implemented proof |
| Auditability | `demo.py` | Attributable timestamped event history | Implemented proof |
| Failure/denial state | `demo.py` | Default-deny and human-denial paths | Implemented proof |
| Real external integration | none by design | No external side effect in proof slice | Next |
| Tamper-evident persistence | not yet wired | Hash/chained or append-only store | Next |
| Independent reproducibility | README + zero-dependency Python | Reviewer can run locally | Ready for validation |

## IP boundary

Safe to disclose: governance contract, control concepts, event semantics, test evidence and the narrow demonstration flow.

Retain as proprietary: internal AIDES routing/orchestration strategies, project-specific prompts, private memory structures, decision heuristics, credentials, customer data and production automation topology.
