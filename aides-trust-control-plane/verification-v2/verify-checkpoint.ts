export type AidesCheckpointV2 = {
  version: 'aides-checkpoint-v2';
  transaction_id: string;
  sequence_no: number;
  event_hash: string;
  issued_at: string;
  key_id: string;
  algorithm: 'ECDSA_P256_SHA256';
};

export type VerificationBundle = {
  checkpoint: AidesCheckpointV2;
  signature_base64: string;
  public_key_jwk: JsonWebKey;
};

function canonicalCheckpoint(checkpoint: AidesCheckpointV2): string {
  const ordered: Record<string, string | number> = {
    algorithm: checkpoint.algorithm,
    event_hash: checkpoint.event_hash,
    issued_at: checkpoint.issued_at,
    key_id: checkpoint.key_id,
    sequence_no: checkpoint.sequence_no,
    transaction_id: checkpoint.transaction_id,
    version: checkpoint.version,
  };
  return JSON.stringify(ordered);
}

function base64ToBytes(input: string): Uint8Array {
  const binary = atob(input);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

export async function verifyCheckpointBundle(bundle: VerificationBundle): Promise<boolean> {
  const { checkpoint, signature_base64, public_key_jwk } = bundle;
  if (checkpoint.version !== 'aides-checkpoint-v2') return false;
  if (checkpoint.algorithm !== 'ECDSA_P256_SHA256') return false;

  const key = await crypto.subtle.importKey(
    'jwk',
    public_key_jwk,
    { name: 'ECDSA', namedCurve: 'P-256' },
    false,
    ['verify'],
  );

  const payload = new TextEncoder().encode(canonicalCheckpoint(checkpoint));
  const signature = base64ToBytes(signature_base64);

  return crypto.subtle.verify(
    { name: 'ECDSA', hash: 'SHA-256' },
    key,
    signature,
    payload,
  );
}

export function explainVerification(result: boolean): string {
  return result
    ? 'VERIFIED: the checkpoint signature matches the supplied public verification key.'
    : 'NOT VERIFIED: the checkpoint, signature or public verification key does not match.';
}
