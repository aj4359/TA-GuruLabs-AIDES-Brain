import unittest

from intervention_scenario import run_intervention_scenario_001


class InterventionScenarioTests(unittest.TestCase):
    def test_out_of_envelope_action_is_stopped_and_evidenced(self):
        result = run_intervention_scenario_001()
        self.assertTrue(result.executable_before)
        self.assertFalse(result.executable_after)
        self.assertFalse(result.credentials_active_after)
        self.assertEqual(result.proof.enforcement_status, "EFFECTIVE")
        self.assertEqual(result.proof.mtti_seconds, 3)

    def test_public_proof_does_not_claim_production_mtti(self):
        payload = run_intervention_scenario_001().public_payload()
        self.assertEqual(payload["proofMode"], "DETERMINISTIC_GOVERNED_TEST")
        self.assertFalse(payload["productionMttiClaimed"])
        self.assertEqual(payload["intervention"]["mttiSeconds"], 3)


if __name__ == "__main__":
    unittest.main()
