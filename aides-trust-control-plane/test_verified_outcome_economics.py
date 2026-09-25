import unittest
from verified_outcome_economics import MissionOutcome, cost_per_verified_outcome

class VerifiedOutcomeEconomicsTests(unittest.TestCase):
    def test_cpvo_counts_only_verified_outcomes(self):
        outcomes=[MissionOutcome("m1",10.0,True),MissionOutcome("m2",20.0,False),MissionOutcome("m3",30.0,True)]
        self.assertEqual(cost_per_verified_outcome(outcomes),30.0)
    def test_cpvo_requires_verified_outcome(self):
        with self.assertRaises(ValueError):
            cost_per_verified_outcome([MissionOutcome("m1",5.0,False)])

if __name__=="__main__": unittest.main()
