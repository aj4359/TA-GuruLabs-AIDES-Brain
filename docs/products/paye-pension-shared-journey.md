# PAYE Detective × Pension Finder — shared customer journey
Status: integration specification; **not deployed**. Date: 2026-11-04.
Owner: TA GuruLabs. © TA GuruLabs. All rights reserved.

## Product boundary
Keep PAYE Detective and Pension Finder independently accessible and branded. Provide a shared **Money History** navigation entry, not a merged regulated financial product. No assumption that any pension has been found, that tax is owed/refundable, or that existing services have production API access.

## MVP flow
1. Visitor chooses **Check my PAYE** or **Find an old pension**.
2. Each service runs separately with separate purpose-specific notices.
3. After a result, offer **Explore related service**. Never preselect.
4. If customer opts in, show exactly which minimal fields could be copied: employer legal/trading names, dates of employment, relevant scheme/employer references; allow edit before confirmation.
5. Create time-stamped, purpose-specific consent/authorisation receipt and show revocation controls. Do **not** pass NI numbers, addresses, tax records, pension balances, credentials or documents by default.
6. Open the other service with customer-approved fields only. Re-verify identity and authority for any external provider enquiry.
7. Show a combined **My Money History** index containing case statuses and source/provenance but do not collapse the underlying records into an unrestricted shared database.

## Suggested API contract (design only)
POST /api/shared-case/previews — authenticated; returns allowlisted proposed data, no persistence or transmission.
POST /api/shared-case/authorisations — authenticated; body: {sourceCaseId,targetService,approvedFieldNames,noticeVersion}; logs receipt, TTL, scope.
POST /api/shared-case/transfers — authenticated; requires active authorisation and ownership checks; server-side allowlist, audit log, replay protection.
DELETE /api/shared-case/authorisations/:id — revoke future transfers; explain retention limits.
GET /api/shared-case/activity — customer-visible audit history.

## Security and privacy gates before production
- Map both existing repositories, data stores, deployed URLs and user identity models; do not build unverified client-side cross-domain token transfer.
- Data protection impact assessment, UK GDPR lawful bases, retention schedule and privacy notices. Consent for optional sharing is distinct from deciding the lawful basis for each underlying processing purpose.
- Server-side authorisation; RLS tenant isolation; encryption in transit and at rest; redaction in logs; rate limiting; abuse testing; user export/deletion routes with legal retention exceptions.
- Pension administrator contact/NI number handling only after narrow signed authorisation and recipient verification. No unsolicited third-party disclosure.
- Legal/regulatory review: tax advice, pension transfer advice, FCA permissions/financial promotions as applicable; no financial recommendation or automated transfer.
- No assumption of eligibility for refunds or entitlement to pension benefits.

## Acceptance tests
- Standalone PAYE and Pension Finder routes remain functional.
- Cross-service transfer is **off by default** and blocked without recorded scope.
- Selecting only employer/date never sends NI number, email, salary or pension information.
- Customer can edit fields, refuse, revoke future sharing and inspect the audit trail.
- Cross-account access fails; expired/replayed transfer fails; logs contain no sensitive values.
- iPhone Safari UI: clear labels, large taps, accessible status messages.
- End-to-end: one synthetic employer history shows only appropriately sourced investigation next steps; no unverified 'found money' claim.

## Commercial experiment
Begin with free self-service searches plus an optional, separately priced paid administrative-assistance experiment after legal review. Measure completed searches, useful verified employer/scheme leads, opt-in rates, paid conversion, complaint rates; do not claim traced pensions or PAYE savings until independently verified.

## Integration dependencies (blocking)
Need to identify authoritative **live source repositories or app backends** for PAYE Detective and Pension Finder; current GitHub repository discovery did not locate an unambiguous Pension Finder codebase. Do not claim the apps are linked, deployed or tested until that access and an end-to-end deployment verification are complete.
