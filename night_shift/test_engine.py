import unittest
from engine import synthetic_prices, backtest, evaluate

class NightShiftTests(unittest.TestCase):
    def test_reproducible_synthetic_prices(self):
        self.assertEqual(synthetic_prices(),synthetic_prices())
        self.assertNotEqual(synthetic_prices(1),synthetic_prices(2))
    def test_no_live_execution(self):
        report=evaluate()
        self.assertEqual(report["mode"],"SYNTHETIC_PAPER_ONLY")
        self.assertFalse(report["risk"]["live_trading_enabled"])
        self.assertFalse(report["risk"]["auto_spend_enabled"])
        self.assertEqual(len(report["candidates"]),3)
    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            backtest([100]*100,30,10)
    def test_finite_metrics(self):
        import math
        result=backtest(synthetic_prices())
        self.assertTrue(math.isfinite(result["sharpe"]))
        self.assertGreaterEqual(result["max_drawdown_pct"],0)
if __name__=="__main__":
    unittest.main()
