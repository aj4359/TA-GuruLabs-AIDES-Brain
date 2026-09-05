import unittest
from decimal import Decimal

from workforce_economy import (
    MissionBudget, SpendRecord, ValueRecord, WorkerEconomicIdentity,
    WorkforceEconomyLedger,
)


class WorkforceEconomyTests(unittest.TestCase):
    def setUp(self):
        self.ledger = WorkforceEconomyLedger()
        self.ledger.register_worker(WorkerEconomicIdentity(
            worker_id="scout",
            role="market intelligence",
            cost_centre="AIDES-INTEL",
            permitted_spend_categories=frozenset({"model", "search", "runtime"}),
        ))
        self.ledger.authorise_budget(MissionBudget("mission-1", "scout", Decimal("20.00"), "deployer:anthony"))

    def test_authorised_spend_within_budget(self):
        self.ledger.record_spend(SpendRecord("mission-1", "scout", "model", Decimal("4.80"), "audit://spend/1"))
        self.assertEqual(self.ledger.mission_spend("mission-1"), Decimal("4.80"))

    def test_unauthorised_spend_category_is_rejected(self):
        with self.assertRaises(PermissionError):
            self.ledger.record_spend(SpendRecord("mission-1", "scout", "crypto_transfer", Decimal("1"), "audit://spend/2"))

    def test_budget_overrun_is_rejected(self):
        with self.assertRaises(PermissionError):
            self.ledger.record_spend(SpendRecord("mission-1", "scout", "model", Decimal("20.01"), "audit://spend/3"))

    def test_value_requires_evidence_and_outcome_reference(self):
        with self.assertRaises(ValueError):
            self.ledger.record_value(ValueRecord("mission-1", "scout", Decimal("300"), "", "", True))

    def test_only_verified_value_counts_as_verified_economics(self):
        self.ledger.record_spend(SpendRecord("mission-1", "scout", "model", Decimal("5"), "audit://spend/4"))
        self.ledger.record_value(ValueRecord("mission-1", "scout", Decimal("300"), "outcome://1", "evidence://1", False))
        self.assertEqual(self.ledger.verified_value("scout"), Decimal("0"))
        self.ledger.record_value(ValueRecord("mission-1", "scout", Decimal("100"), "outcome://2", "evidence://2", True))
        economics = self.ledger.worker_economics("scout")
        self.assertEqual(economics["verified_value_gbp"], "100")
        self.assertEqual(economics["net_verified_value_gbp"], "95")


if __name__ == "__main__":
    unittest.main()
