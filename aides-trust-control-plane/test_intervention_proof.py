import unittest

from intervention_proof import InterventionProof


class InterventionProofTests(unittest.TestCase):
    def test_effective_intervention_calculates_mtti(self):
        proof = InterventionProof(
            "int-001", "tx-001", "scout",
            "2026-09-12T00:00:00Z", "audit://detection-001",
            "REVOKE_EXTERNAL_ACTION", "EFFECTIVE",
            "2026-09-12T00:00:07Z", "audit://enforcement-001",
        )
        self.assertEqual(proof.mtti_seconds, 7)
        self.assertEqual(proof.public_payload()["enforcementStatus"], "EFFECTIVE")

    def test_requested_only_does_not_manufacture_mtti(self):
        proof = InterventionProof(
            "int-002", "tx-002", "scout",
            "2026-09-12T00:00:00Z", "audit://detection-002",
            "REVOKE_EXTERNAL_ACTION", "REQUESTED",
        )
        self.assertIsNone(proof.mtti_seconds)

    def test_effective_requires_enforcement_evidence(self):
        proof = InterventionProof(
            "int-003", "tx-003", "scout",
            "2026-09-12T00:00:00Z", "audit://detection-003",
            "STOP", "EFFECTIVE", "2026-09-12T00:00:04Z", None,
        )
        with self.assertRaisesRegex(ValueError, "timestamp and evidence"):
            proof.validate()

    def test_timestamp_without_detection_evidence_is_rejected(self):
        proof = InterventionProof(
            "int-004", "tx-004", "scout",
            "2026-09-12T00:00:00Z", None,
            "STOP", "REQUESTED",
        )
        with self.assertRaisesRegex(ValueError, "detection timestamp requires evidence"):
            proof.validate()

    def test_non_effective_cannot_claim_enforcement_timestamp(self):
        proof = InterventionProof(
            "int-005", "tx-005", "scout",
            "2026-09-12T00:00:00Z", "audit://detection-005",
            "STOP", "FAILED", "2026-09-12T00:00:02Z", "audit://attempt-005",
        )
        with self.assertRaisesRegex(ValueError, "non-effective"):
            proof.validate()


if __name__ == "__main__":
    unittest.main()
