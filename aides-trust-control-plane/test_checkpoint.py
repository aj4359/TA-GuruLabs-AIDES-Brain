import copy
import unittest

from checkpoint import create_checkpoint, verify_checkpoint


class CheckpointTests(unittest.TestCase):
    def test_valid_checkpoint_verifies(self):
        document = create_checkpoint(
            transaction_id="11111111-1111-1111-1111-111111111111",
            sequence_no=4,
            event_hash="abc123",
            signer_id="trust-control-plane-ci",
            signing_key="test-secret",
            created_at="2026-09-01T22:00:00+00:00",
        )
        self.assertTrue(verify_checkpoint(document, "test-secret"))

    def test_tampered_checkpoint_fails(self):
        document = create_checkpoint(
            transaction_id="11111111-1111-1111-1111-111111111111",
            sequence_no=4,
            event_hash="abc123",
            signer_id="trust-control-plane-ci",
            signing_key="test-secret",
            created_at="2026-09-01T22:00:00+00:00",
        )
        tampered = copy.deepcopy(document)
        tampered["checkpoint"]["event_hash"] = "changed"
        self.assertFalse(verify_checkpoint(tampered, "test-secret"))

    def test_wrong_key_fails(self):
        document = create_checkpoint(
            transaction_id="11111111-1111-1111-1111-111111111111",
            sequence_no=1,
            event_hash="abc123",
            signer_id="trust-control-plane-ci",
            signing_key="correct-key",
        )
        self.assertFalse(verify_checkpoint(document, "wrong-key"))


if __name__ == "__main__":
    unittest.main()
