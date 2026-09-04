# TA GuruLabs Build Routing Policy

## Default engineering route

For every TA GuruLabs software build, Codex is an approved primary engineering route and the default alternative whenever a visual builder, hosted agent, credit-based platform, or external build tool is unavailable, blocked, too expensive, too limited, or unsuitable.

### Core rule

**Do not let a project stop because Lovable, Manus, Claude, a plugin, credits, or another external builder is unavailable. Route the build to Codex + GitHub instead.**

## Build order

1. Start from the product brief / PRD and the existing repository if one exists.
2. Prefer direct repository work through Codex for implementation, refactors, testing, debugging, integrations, CI, documentation, and deployment preparation.
3. Use visual builders such as Lovable only when they materially accelerate the job and credits/access are available.
4. Use Manus primarily for specialist media/research tasks or when explicitly preferable, not as a dependency for core product engineering.
5. If a hosted builder fails, immediately continue through Codex rather than asking the user to repeat setup steps.
6. Preserve existing working code. Build on branches, test changes, and use pull requests for material changes.
7. Avoid dead-end prototypes. A “working prototype” must have functioning interactions, routes, state, and a credible path to deployment.

## TA GuruLabs engineering loop

**Idea → PRD → Codex Task → Branch → Build → Test → Review → Deploy → Launch**

AIDES may contribute product, research, risk, security, legal/compliance, content, QA, and go-to-market input, but Codex is the engineering execution layer by default.

## Fallback hierarchy

For product engineering, use this order unless the task strongly suggests otherwise:

**Codex + GitHub → existing local/repo tooling → visual builder (Lovable) → specialist external agent (Manus) → manual workaround**

If one route is blocked, move to the next route without stalling the project.

## Quality gates

Before calling a build complete:

- Core flows work.
- Buttons and navigation are not dead.
- Responsive/mobile behaviour is checked where relevant.
- Errors fail clearly and safely.
- Sensitive credentials are not committed.
- Compliance/risk claims are not fabricated.
- Tests or deterministic validation exist for critical logic.
- A README or handoff note explains how to run and continue the project.

## Operating principle

**Codex is not the emergency backup. Codex is part of the standard TA GuruLabs build system.**

This policy applies across TA GuruLabs products, including SIGMA, ASR, JobGenius, AEGIS, BMK, DocuGod, Token Miser, MigrateIQ, and future products.