# TA GuruLabs PAYE Forensics — IP Protection Strategy

Status: internal working document. Not legal advice.

## Protect the product as a stack
Use overlapping protection rather than relying on one right.

### Brand / trade marks
Candidate names to clear before filing:
- PAYE Forensics™
- Tax Visual Engine™
- Underpayment Detective™
- Tax Time Machine™
- Reconciliation Bridge™
- Personal Allowance Map™
- Allowance Collision™
- New Job PAYE Guardian™
- Payslip Movie™
- Cash Flow Story™
- Missing Piece Mode™
- Tax MRI™

Do not use ® unless and until registration is granted. Use ™ only as a brand claim while clearance/registration is pending.

Before filing, search the UK trade mark database for identical and confusingly similar marks, choose only classes/terms genuinely intended for use, and obtain professional advice where conflicts appear.

### Copyright
Treat original source code, written explanations, animation scripts, UI copy, graphics, documentation and original visual assets as copyright assets where applicable.

Recommended notice:
`© 2026 TA GuruLabs. All rights reserved.`

Keep dated Git history, design exports, scripts, requirements and provenance records as evidence of creation and ownership.

Any contractor or collaborator should sign written confidentiality and IP-assignment terms covering work created for the project.

### Trade secrets / confidential know-how
Treat these as confidential by default:
- diagnostic scoring and ranking logic
- journey orchestration/routing rules
- reconstruction heuristics
- Missing Piece prioritisation logic
- evidence-confidence rules
- narrative-generation mappings
- rule/provenance graph structure
- PAYE edge-case test corpus
- scenario library
- tax-rule-to-animation compiler logic
- prompt libraries and AIDES orchestration patterns
- non-public roadmap and commercial strategy

Use private production repositories, least-privilege access, NDAs/confidentiality clauses, IP assignment, secret management, audit logs, access revocation and clear confidentiality markings.

## Public / private architecture split
Public demos should expose only enough logic to demonstrate the experience.

Production target:
- Client renders signed/structured scene objects.
- Private rules engine computes tax and PAYE reconstruction.
- Private forensic engine ranks explanations and missing pieces.
- Private visual compiler converts calculation/evidence objects into animation scenes.
- Public UI never contains the complete proprietary scoring, orchestration or scenario library.

The browser should receive outputs, not the complete recipe.

## Patent review
Do not assume the product is patentable. UK patent law generally excludes software with a non-technical purpose and presentation of information as such. If a genuinely technical invention emerges, obtain advice from a UK patent attorney before public disclosure.

## Evidence of ownership
Maintain an internal IP register recording asset name, creator, creation date, repository/commit, public/private status, proposed protection, disclosure history, third-party dependencies, assignment status and trade mark clearance status.

## Third-party hygiene
Before production release:
- maintain a software bill of materials
- record dependency licences
- review licence compatibility
- record sources/licences for icons, fonts, photos, audio, animation assets and data
- do not present GOV.UK/HMRC wording, branding or visual identity as TA GuruLabs-owned IP

Official tax rules remain public information. Protect the original implementation, arrangement, visualisation, explanatory language, workflow, software and brand, not the underlying law or HMRC rules themselves.

## Immediate actions
1. Mark architecture/scoring documents confidential.
2. Keep production tax/forensic/visual compiler server-side.
3. Add copyright notices to production source and original creative assets.
4. Maintain the IP asset register.
5. Perform UKIPO clearance searches before filing principal marks.
6. Shortlist one umbrella mark and 2–4 flagship feature marks rather than filing everything immediately.
7. Use written IP assignment + confidentiality terms with all collaborators.
8. Ask a UK trade mark attorney to review classes/conflicts before filing.
9. Ask a patent attorney only if a genuinely technical invention is identified.
10. Do not publish internal scoring/reconstruction mechanics.

## Public messaging rule
Explain what the product does and why it helps. Do not disclose how the forensic ranking, evidence graph, visual compiler or scenario-selection system works internally.
