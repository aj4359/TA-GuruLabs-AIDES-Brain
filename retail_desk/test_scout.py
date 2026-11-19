import unittest
from scout import parse_items,triage,run

class TestRetailDesk(unittest.TestCase):
    def test_rss(self):
        xml=b'<rss><channel><item><title>CV template</title><link>https://example.org/a</link></item></channel></rss>'
        self.assertEqual(parse_items(xml),[("CV template","https://example.org/a")])
    def test_sensitive_review(self):
        item=triage("investment advice","test","https://example.org")
        self.assertEqual(item["status"],"manual-review")
        self.assertFalse(item["buyer_demand_verified"])
    def test_category(self):
        self.assertIn("career",triage("CV interview planner","test","https://example.org")["category_hypotheses"])
    def test_fail_closed_source(self):
        report=run(fetch=lambda url: (_ for _ in ()).throw(RuntimeError("blocked")))
        self.assertEqual(report["items"],[])
        self.assertEqual(len(report["source_errors"]),2)

if __name__=="__main__":unittest.main()
