# AIDES Harness v1 — evidence before completion

This is a **minimal verification harness**, not a deployed autonomous agent. It is built exclusively with the Python standard library and does not need paid tools, API keys, production access or a database.

## Scope and guarantees

- Explicit JSON contract containing a task ID, goal, bounded project root and one or more checks
- Built-in read-only checks: `file_exists` and `json_valid`
- Fail-closed status: `verified_complete` only if **every** check passes
- Durable JSON task state (atomic replacement) and append-only JSONL receipts
- File paths constrained to the declared project root, including resolved symlinks
- No deployment, editing, posting, wallet activity, external API calls or secrets access
- No automatic retries for deterministic failures: report `needs_repair` instead

## Quick start

From repository root:

```bash
python -m unittest discover -s harness -p 'test_*.py'
python -m harness.runner harness/examples/brain-readme.json --state-dir .aides/state
```

The example contract checks this repository's README. The CLI exits 0 on verification success, 1 for failed checks and 2 for invalid contracts.

## Contract example

```json
{
  "task_id": "brain_readme_001",
  "goal": "Verify the existing repo README",
  "root": ".",
  "checks": [
    {"type": "file_exists", "path": "README.md"}
  ]
}
```

The root is resolved relative to the process working directory. The caller must trust the contract author; contracts are **not** an authentication or authorization layer.

## Next engineering increment

Add a separate builder interface, explicit approval policies, append-only tamper-evident receipts, independent UI/browser checks, resume semantics, budget limits, and deployment gates. Do not describe this v1 verifier as supporting those capabilities yet.

## Operations

- State is written locally under `.aides/state` (keep it out of version control).
- Treat receipts as operational records; exclude personal information and credentials.
- Failed verification requires a builder repair and a new run.
- A successful file-existence check alone does **not** prove mobile compatibility, business correctness or live availability.
