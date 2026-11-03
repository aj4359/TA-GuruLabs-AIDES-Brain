# Payhip integration contract (not connected)

Verified against Payhip's public documentation on 2026-11-03:
- Public API: coupons and software license keys only; **no general product create/update endpoint**.
- Webhooks: `paid`, `refunded`, `subscription.created`, `subscription.deleted`; configure at Payhip Settings > Developer.
- Documented signature: SHA256(API key). Verify server-side with constant-time comparison against configuration secret; never store or expose the key in browser/GitHub.
- Retries: Payhip expects HTTP 200 and may retry hourly up to 3 hours.
- Currency amounts are in minor units (pennies/cents).

Sources: https://help.payhip.com/article/115-webhooks and https://payhip.com/api-reference

## Safe implementation requirements
1. Create a private HTTPS endpoint with server-side API key stored in host secret manager. No public inbound endpoint is deployed yet.
2. Enforce POST, JSON size limit, signature equality using constant-time comparison, and allowlisted types. **Warning:** static hash signature is not bound to payload, so do not treat as sufficient integrity protection against a replay or insider with captured webhook. Keep endpoint secret, add operational monitoring and reconcile against Payhip's actual export/report.
3. Persist an idempotency key for all webhook events; return 200 on duplicates. Do not infer payouts or final revenue from webhook alone.
4. Minimise customer PII; store transaction IDs, product keys and totals only in general ledger.
5. Product pages and paid product files must be prepared and reviewed in Payhip UI until a documented authorised API exists. No browser automation circumventing terms.
6. Reconciliation: source-of-truth Payhip sales/payment reports and bank payouts, not demo fixtures.
7. Never activate live checkout for Sicario before original video, audio, rights, tax, mobile purchase and download tests are complete.
