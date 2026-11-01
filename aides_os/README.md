# AIDES OS — Bounded autonomy pilot (v0.1)

This is a **working routing and audit-plan prototype**, not an autonomous coding agent yet. It does not download packages, call LLMs, execute commands, merge, publish, deploy, spend or send external messages.

## Architecture
- Aureus: prioritisation (future integration)
- T-Miser: deterministic allowlist-based routing (implemented)
- Scout: repository inspection (assignment policy only)
- Codex: isolated branch implementation (assignment policy only)
- QA AIDE: independent tests (assignment policy only)
- Haven: draft reports and escalate approvals (assignment policy only)

## Run
```sh
python -m unittest discover -s aides_os -p 'test_*.py'
python aides_os/router.py
```
Results are written to `aides_os/runs/latest.json`. Workflow uploads the file as an artifact.

## Roadmap
1. Real queue processor with scoped GitHub App permissions and allowlisted repository operations.
2. Download and inspect permitted prototype dependencies using pinned hashes and an isolated disposable runner.
3. Branch-only implementation worker and separate read-only reviewer.
4. Error handling: one normal retry, escalate repeated failure.
5. Record task ID, worker, commit SHA, checks, runtime, model costs and evidence.
6. Enforce pull-request and human-controlled production deployment gates.

## Threat model
Never execute instructions embedded in source files or external pages as authority. Keep secrets out of logs, restrict token scopes, prohibit arbitrary shell execution by incoming task descriptions, use timeouts, quotas and network egress policy. Simulated assignments must never be represented as completed work.

## Commercial evidence
Report verified execution and test results separately from proposed capabilities. Baseline manual task duration/cost before claiming savings.
