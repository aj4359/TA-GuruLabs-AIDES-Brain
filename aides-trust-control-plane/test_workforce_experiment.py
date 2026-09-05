import unittest
from decimal import Decimal

from workforce_experiment import run_experiment_001


class WorkforceExperiment001Tests(unittest.TestCase):
    def test_unverified_value_does_not_create_positive_economics(self):
        result = run_experiment_001()
        self.assertEqual(result.spend_gbp, Decimal("6.00"))
        self.assertEqual(result.unverified_attributed_value_gbp, Decimal("300.00"))
        self.assertEqual(result.verified_value_gbp, Decimal("0"))
        self.assertEqual(result.net_verified_value_gbp, Decimal("-6.00"))
        self.assertEqual(result.conclusion, "insufficient verified economic evidence")

    def test_independently_verified_value_can_count(self):
        result = run_experiment_001(verify_outcome_value=True)
        self.assertEqual(result.verified_value_gbp, Decimal("300.00"))
        self.assertEqual(result.net_verified_value_gbp, Decimal("294.00"))
        self.assertEqual(result.conclusion, "positive verified economics")


if __name__ == "__main__":
    unittest.main()
