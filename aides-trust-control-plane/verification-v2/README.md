# AIDES Trust Verification v2

This layer builds on the validated Trust Control Plane baseline merged from PR #10.

## Objective

Allow a third party to verify that a governed transaction checkpoint was signed by an approved TA GuruLabs verification key without receiving any signing secret.

## Verification model

1. A governed transaction produces an append-only hash chain.
2. A checkpoint binds `transaction_id`, `sequence_no`, `event_hash`, `issued_at`, `key_id` and `algorithm`.
3. A protected signer signs the canonical checkpoint payload.
4. The Command Centre exposes the checkpoint plus public verification material.
5. A reviewer verifies the signature independently.

## Production target

- asymmetric signing only
- signing key held by KMS/HSM or equivalent protected service
- public key identified by stable `key_id`
- explicit key lifecycle: active, rotating, retired, revoked
- no private key or signing credential in browser code, repository, logs or audit evidence
- algorithm agility without silently changing historical verification semantics

## Initial algorithm profile

`ECDSA_P256_SHA256`

P-256 is supported by common KMS/HSM products and browser Web Crypto, allowing a lightweight independent verifier. Production selection can change if procurement requirements specify another approved algorithm.

## Canonical checkpoint fields

```json
{
  "version": "aides-checkpoint-v2",
  "transaction_id": "uuid",
  "sequence_no": 7,
  "event_hash": "hex-sha256",
  "issued_at": "2026-09-01T22:30:00Z",
  "key_id": "trust-verifier-2026-01",
  "algorithm": "ECDSA_P256_SHA256"
}
```

Canonicalisation rule for v2: UTF-8 JSON with lexicographically sorted keys, no insignificant whitespace. The exact canonical bytes must be preserved by signer and verifier.

## Security boundary

A valid signature proves possession of the signing key at checkpoint issuance. It does not by itself prove the underlying event was truthful, nor does it make storage immutable. Evidence quality, authorization, chain validity, key governance, retention and independent anchoring remain separate controls.
