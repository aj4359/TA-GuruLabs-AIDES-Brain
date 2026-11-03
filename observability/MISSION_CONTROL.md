# AIDES Mission Control — Phase 1

Status: design and initial observability specification; NOT live product monitoring.

## Rule
A product is not verified merely because its agent reported DONE, an API returned 200, or a third-party integration is connected. Verification requires a recent successful test of the complete critical user journey with evidence.

## Priorities
1. Publishing Studio: compose -> attach video/image -> submit -> receive provider ID -> confirm public post, media and link.
2. Pension Finder: open on mobile -> follow guidance -> navigate search and results -> check outbound official tracing links.

## Observability pillars
- Synthetic browser checks using Playwright, iPhone-size viewport, test accounts and safe data.
- Application/backend metrics: API latency, errors, provider responses and retry counts.
- User experience telemetry: consent-aware, privacy-preserving failure and web-vitals tracking; session recording OFF by default.
- Business results: confirmed publications, downloads, test transactions and verified real revenue, kept separate.

## Evidence contract
Each check records UTC timestamp, product, journey, unique correlation ID, step, outcome (passed/failed/unknown), elapsed milliseconds, safe error code, and evidence reference. Never record passwords, access tokens, NI numbers, health information or user content.

## Status semantics
- UNTESTED: no real journey check yet.
- VERIFIED: all essential steps passed recently and evidence retained.
- DEGRADED: important flow works only partially.
- FAILED: critical step failed.
- UNKNOWN: evidence is unavailable, monitoring unavailable, or a provider cannot be verified.

## Minimum acceptance tests
- Publishing Studio: provider reports published with durable ID, independently check public URL where access allows, verify required image/video and CTA link. Failure to check public media is UNKNOWN, not VERIFIED.
- Pension Finder: open and complete key flows on mobile, no broken buttons, correct official references, no personal data in telemetry.
- Record screenshots, sanitized browser traces, server events and CI run ID where possible.
- Never make live posts or purchases in an automated test without a dedicated controlled environment.

## Rollout
1. Confirm actual live product URLs and repository owners.
2. Build Playwright smoke tests and safe backend health checks.
3. Join frontend and backend events with correlation IDs.
4. Produce a mobile dashboard showing status, timestamp, incident summary and evidence links.
5. Apply a verified-release gate separately from demo/prototype publication.
6. Assess SME product opportunity only after the internal monitor is reliable.

## KPIs
Critical journey pass rate, time to detection, time to resolution, last verified publishing result, media presence, working downloads, test checkout completion. A homepage 200 alone means reachability, not business success.

## Cost and safety
Use free GitHub Actions and lightweight open-source instrumentation initially. Store secrets in encrypted repository secrets; redact logs and artifacts. Do not expose user data in public repository or dashboards.