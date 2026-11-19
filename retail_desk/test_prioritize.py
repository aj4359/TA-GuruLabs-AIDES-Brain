import unittest
from prioritize import evaluate,rank

def case(id="a",score=5):
    return {"id":id,"name":"Synthetic example","buyer":"illustrative user","product":"fictional digital kit",
    "sources":[{"publisher":"A","url":"https://example.com/a"},{"publisher":"B","url":"https://example.org/b"}],
    "purchase_signal_verified":True,
    "scores":{x:score for x in ("buyer_demand","purchase_evidence","speed_to_market","margin","organic_distribution","delivery_reliability","strategic_fit")},
    "economics":{"price_gbp":4.99,"fees_gbp":0.6,"fulfilment_gbp":0.1,"refund_reserve_gbp":0.3},
    "gates":{x:True for x in ("rights_cleared","platform_eligible","deliverable_verified","checkout_verified","privacy_review")}}
class PrioritizeTests(unittest.TestCase):
    def test_good_candidate(self):
        r=evaluate(case());self.assertEqual(r["decision"],"PILOT_CANDIDATE");self.assertEqual(r["score"],100)
    def test_single_source_not_eligible(self):
        x=case();x["sources"]=x["sources"][:1];self.assertEqual(evaluate(x)["decision"],"RESEARCH")
    def test_no_purchase_signal(self):
        x=case();x["purchase_signal_verified"]=False;self.assertEqual(evaluate(x)["decision"],"RESEARCH")
    def test_failed_release_gate(self):
        x=case();x["gates"]["platform_eligible"]=False;self.assertEqual(evaluate(x)["decision"],"BLOCKED")
    def test_negative_margin(self):
        x=case();x["economics"]["fees_gbp"]=7;self.assertEqual(evaluate(x)["decision"],"BLOCKED")
    def test_unknown_score_not_zero(self):
        x=case();del x["scores"]["margin"];self.assertIsNone(evaluate(x)["score"])
    def test_rank_eligible_before_unverified_even_high_score(self):
        x=case("unverified",5);x["purchase_signal_verified"]=False
        y=case("verified",4)
        self.assertEqual(rank([x,y])["candidates"][0]["id"],"verified")
    def test_empty_no_fake_winners(self):
        self.assertEqual(rank([])["candidates"],[])
if __name__=="__main__":unittest.main()
