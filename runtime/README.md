# AIDES OS execution foundation (pilot)

This is an **initial, non-deployed, local queue**, not a live autonomous agent workforce. It extends the existing AIDES Brain role and knowledge files without changing them. It uses only Python standard library + SQLite and does not consume API credits.

## Run locally

```bash
python -m unittest discover -s runtime -p 'test_*.py'
python runtime/queue.py add --title "Test DocuGuard demo" --kind quality_check --owner CONTINUITY_GUARD --project DocuGuard --acceptance "Capture passing checks and a demo URL"
python runtime/queue.py list
python runtime/queue.py set TASK_ID running
python runtime/queue.py set TASK_ID done --evidence "test-results/docuguard.txt"
```

A task transitions pending -> running -> done/failed/blocked; blocked and failed can return to pending. Done requires evidence, blocked requires a reason. Changes are persisted in a local SQLite database with append-only audit entries (application-level; a database administrator can still modify them). No remote execution is included.

## Governance and safety

- The queue is **not** a permission system for external tools. No executor is connected.
- An approval-required task is blocked from running. A separate authenticated approval service with auditable identity checks must be designed and tested before enabling approved execution.
- Never place secrets, personal data, tax records, passwords or private commercial material in Git-tracked task data. This repository is public.
- SQLite databases in `runtime/data/` must remain local and untracked.
- External publishing, spending, financial transactions, deletion and production deployment are out of scope for this pilot.
- Model providers and worker connectors must be independently swappable; never put credentials inside model prompts.
- Completion evidence must be independently validated before any public release claim.

## Next engineering gates

1. Build a **private, authenticated host** and scoped worker identities.
2. Implement atomic worker claim + lease expiry + retry ceilings; current `set running` is administrative, not a multi-worker dispatcher.
3. Add connector adapters for GitHub/Codex and read-only calendar/mail, with tests and approval boundaries.
4. Add signed approval decisions and immutable external audit retention.
5. Deploy an operator dashboard and verified daily briefing. Verify cost and reliability before paid scale.

## Commercial priority

First validated, self-service TA GuruLabs purchase; never assert revenue before payment-provider evidence.
