import unittest
from proof_demo import run_demo

class ProofDemoTests(unittest.TestCase):
    def test_customer_story_is_complete_and_verified(self):
        d=run_demo()
        self.assertEqual(d.workforce["selected"],"worker-approved")
        self.assertTrue(d.workforce["approved"])
        self.assertTrue(d.work["evidence_refs"])
        self.assertTrue(d.recovery["tested"])
        self.assertEqual(d.verification["result"],"PASS")
        self.assertEqual(d.economics["cpvo"],4.0)

if __name__=="__main__":
    unittest.main()
