import tempfile
import unittest

from resource_governor.pilot import run


class PilotTests(unittest.TestCase):
    def test_observe_only_synthetic(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run(directory)
        self.assertTrue(result["permitted"])
        self.assertEqual(result["actual_model_spend_usd"], 0)
        self.assertFalse(result["cross_run_enforcement"])
        self.assertEqual(result["mode"], "SYNTHETIC_PILOT_OBSERVE_ONLY")


if __name__ == "__main__":
    unittest.main()
