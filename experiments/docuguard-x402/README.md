# DocuGuard x402-style agent commerce experiment

**Simulation only. Not x402-protocol-compliant. No real payments, wallet, blockchain, Cloudflare managed gateway or external deployment.**

An isolated standard-library Python API exercises: request -> HTTP 402 example price -> simulated receipt -> synthetic document-field completeness result. No changes to existing DocuGod or Payhip products.

## Run (Python 3)
```bash
cd experiments/docuguard-x402
python3 -m unittest -v test_server.py
python3 server.py
curl -i -X POST http://127.0.0.1:8765/v1/docuguard/check -H 'Content-Type: application/json' -d '{"text":"Date: example"}'
curl -i -X POST http://127.0.0.1:8765/v1/docuguard/check -H 'Content-Type: application/json' -H 'X-Demo-Payment: demo-paid' -d '{"text":"Date: example\nRef: X\nSigned: Example"}'
```
Only listens on 127.0.0.1. The publicly known `demo-paid` marker is **NOT authentication**; never deploy this server for real customers. Only use fictional data. Presence of labels is not legal, tax, security, identity or fraud validation.

## Before a real x402 integration
1. Verify current official x402 version/SDK, buyer/seller UK eligibility, supported network/currency, facilitators, terms and regulated-service implications; do not assume Cloudflare closed beta is available in the UK.
2. Replace *all* demo token logic with protocol-compliant server-side payment verification and settlement. Test missing, forged, expired, reused, failed and duplicated receipts.
3. Require idempotency, replay defenses, signed price and expiry, least-privilege private key management, usage metering, rate limiting, reconciliation, charge failures, refunds and incident response.
4. Conduct GDPR/security assessment, lawful processing, storage and deletion before accepting personal documents. Run on testnet or simulated local mode until human approval for live financial operations.
5. Preserve the existing Payhip checkout for human customers and the original DocuGod site. Never state real sales without payment receipts.

## Human-centred creative fingerprint
**Person/problem:** small developers need a safe test of per-request payments. **Outcome:** understand the process in two requests. **Keep:** working sites and existing checkout. **Change:** standalone proof only. **Invent:** cost-free synthetic payment path. **KISS:** no dependencies, one test command. **Evidence:** five unittest cases. **Rights/risk:** original demonstration code; no real payments or personal data. **Customer value:** assess viable usage-based product pricing only after demand validation.

**Continuity:** GitHub branch/PR is a source history, not an independently restore-verified backup. Record eventual release in the portfolio IP registry and run required provenance, safety and QA gates before public deployment.
