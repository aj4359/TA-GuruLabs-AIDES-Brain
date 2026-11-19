import unittest
from engine import assess, report, WEIGHTS
def card():
    return {"id":"TEST","name":"Synthetic completed demo","lane":"retail",
        "scores":{k:5 for k in WEIGHTS},
        "evidence":[{"publisher":"A","url":"https://example.com/a"},{"publisher":"B","url":"https://example.org/b"}],
        "receipts":{"verified_sale":False,"working_artifact":True,"delivery_or_usage_path":True},
        "gates":{"rights_and_privacy":True,"commercial_and_platform":True},
        "estimated_unit_contribution_gbp":2.0}
class DecisionTests(unittest.TestCase):
    def test_qualified(self):
        self.assertEqual(assess(card())["decision"],"PROPOSE_PRIORITY")
    def test_no_sales_claim(self):
        self.assertIsNone(assess(card())["probability_of_success"])
    def test_missing_artifact_fails(self):
        c=card();c["receipts"]["working_artifact"]=False
        self.assertEqual(assess(c)["decision"],"RESEARCH_OR_UNBLOCK")
    def test_one_source_fails(self):
        c=card();c["evidence"]=c["evidence"][:1]
        self.assertEqual(assess(c)["decision"],"RESEARCH_OR_UNBLOCK")
    def test_weak_margin_fails(self):
        c=card();c["estimated_unit_contribution_gbp"]=-1
        self.assertEqual(assess(c)["decision"],"RESEARCH_OR_UNBLOCK")
    def test_unknown_score_not_assumed(self):
        c=card();del c["scores"]["customer_evidence"]
        self.assertIsNone(assess(c)["priority_score"])
    def test_no_cards_no_winners(self):
        self.assertEqual(report([])["proposals"],[])
    def test_reject_non_list(self):
        with self.assertRaises(ValueError):report({})
if __name__=="__main__":unittest.main()
