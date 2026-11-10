import tempfile
import unittest
from pathlib import Path
from resource_governor import Governor, Policy


class GovernorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.g = Governor(Path(self.tmp.name) / "usage.db",
                          Policy(weekly_budget_usd=1, conservation_at=0.8))
        self.w = "2026-W46"

    def admit(self, key, cost, **kwargs):
        return self.g.admit(job_key=key, owner="SIGMA", estimate_usd=cost,
                            week=self.w, **kwargs)

    def test_deduplicates_and_reconciles(self):
        self.assertTrue(self.admit("scan:btc:1", 0.5).permitted)
        self.assertEqual(self.admit("scan:btc:1", 0.5).reason, "duplicate_job")
        self.g.complete(job_key="scan:btc:1", actual_usd=0.25, week=self.w)
        self.assertAlmostEqual(self.g.usage(self.w)["committed_usd"], 0.25)

    def test_budget_and_conservation(self):
        self.assertTrue(self.admit("a", 0.8).permitted)
        self.assertEqual(self.admit("b", 0.05).reason, "conservation_mode")
        self.assertTrue(self.admit("essential", 0.1, category="essential").permitted)
        self.assertEqual(self.admit("too_much", 0.2, category="essential").reason,
                         "weekly_budget_exceeded")

    def test_fanout_and_retry(self):
        self.assertEqual(self.admit("a", 0, fanout=3).reason, "fanout_limit")
        self.assertEqual(self.admit("b", 0, attempt=3).reason, "retry_limit")

    def test_release_keeps_dedupe(self):
        self.assertTrue(self.admit("x", 0.5).permitted)
        self.g.release(job_key="x", week=self.w)
        self.assertEqual(self.g.usage(self.w)["committed_usd"], 0)
        self.assertEqual(self.admit("x", 0.5).reason, "duplicate_job")

    def test_invalid_cost(self):
        with self.assertRaises(ValueError):
            self.admit("x", -1)


if __name__ == "__main__":
    unittest.main()
