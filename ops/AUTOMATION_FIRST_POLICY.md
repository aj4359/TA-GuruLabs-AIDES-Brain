# TA GuruLabs — Automation-First Policy
Effective: 2026-11-08 · Owner: TA GuruLabs · Scope: all AIDEs and projects

## Standing decision
**Use TA GuruLabs-owned automation before consuming a ChatGPT scheduled-task slot.** A request to run repeatedly, later, or monitor a condition MUST be routed through this gate before anyone proposes creating a new ChatGPT scheduled task.

Preferred route: reuse an existing GitHub Actions workflow or self-hosted job, then other no-cost/low-cost approved infrastructure. Check whether the work is suitable for GitHub Actions (scheduled jobs may run late and aren't always-on) versus a real worker/queue. Calculate costs and verify credential handling. Do not silently create external schedules or modify existing tasks.

## Mandatory user-facing warning
> ⚠️ TASK SLOT WARNING — This could consume one of our limited ChatGPT scheduled tasks. TA GuruLabs independent automation is the default. Can it run through our own infrastructure instead? Do not create a ChatGPT task unless the owner expressly approves an exception.

Before proposing the exception provide: (1) what is to run; (2) why independent infrastructure cannot reasonably do it; (3) slots available/used if verified; (4) likely runtime/cost/security considerations; (5) existing task to replace if at limit. Never pause/delete an existing task without explicit owner approval.

## Gate states
- DEFAULT: `INDEPENDENT` — no ChatGPT task creation.
- Exception: `CHATGPT_APPROVED` — only after a specific human approval recorded for the *individual* task, with name, reason, timestamp and approver.
- `BLOCKED` — no valid approval, ambiguous instruction, no available slot or unacceptable cost/security.

## Enforcement boundary
AIDES integrated with the task broker MUST call the guard script before requesting a ChatGPT task. It denies by default. This repository-level guard does **not** modify the ChatGPT app's own task creation interface or override ChatGPT's platform tools: integrations must opt into it. The assistant should also respect the policy conversationally.

## Safeguards
- No automatic task creation, schedule migrations or spending.
- No silent replacement/disablement of current tasks.
- Jobs handling secrets, tokens or wallets require minimal permissions, no private-key/seed phrase storage, an explicit security review, and human approval for irreversible action.
- Log rationale and verification evidence; do not claim a job is running until a scheduled run is confirmed.
- Use free-tier quotas prudently; GitHub Actions schedules do not guarantee exact launch timing.
- Priority test case: SIGMA UK Opportunity Hunter (issue #91).

## Integration contract
`python3 ops/task_gate.py check --route independent` : allow.
`python3 ops/task_gate.py check --route chatgpt` : reject unless a validated approval record is supplied.
`python3 ops/task_gate.py warn` : print standard warning.
