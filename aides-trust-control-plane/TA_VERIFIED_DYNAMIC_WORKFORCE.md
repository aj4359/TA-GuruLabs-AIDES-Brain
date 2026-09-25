# TA VERIFIED v0.1 — Dynamic Approved Workforce
Claim: AIDES selects only approved capabilities satisfying the evidence obligation, then minimizes estimated cost among eligible choices; TA VERIFIED fails closed without evidence/pass/release decision.
Acceptance: focused tests plus both repository workflows pass.
Evidence: AIDES Governed Work Moat run 35968514895 — PASS; AIDES Trust Control Plane run 35968514880 — PASS.
Failure/correction: first CI attempt failed because tests imported pytest in a unittest-only harness; tests were converted to unittest and re-run green.
Result: PASS.
Version/timestamp: branch head 4ebd4989c79376940e54d189858b5b83f2ab4ba7 / 2026-09-24.
Limitations: selection uses an abstract capability catalogue; external ARD/MCP discovery adapters remain separate.
Release decision: VERIFIED_LIMITED_RELEASE.
