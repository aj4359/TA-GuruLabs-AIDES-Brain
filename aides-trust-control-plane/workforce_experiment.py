"""Workforce Economy Experiment #001.

A deterministic simulation of a Scout mission. It tests the accounting and
governance contract only. It does not fabricate live provider costs, revenue,
customer value, crypto settlement, or autonomous payments.
"""
from dataclasses import dataclass
from decimal import Decimal

from workforce_economy import (
    MissionBudget,
    SpendRecord,
    ValueRecord,
    WorkerEconomicIdentity,
    WorkforceEconomyLedger,
)


@dataclass(frozen=True)
class ExperimentResult:
    experiment_id: str
    mission_id: str
    worker_id: str
    budget_gbp: Decimal
    spend_gbp: Decimal
    unverified_attributed_value_gbp: Decimal
    verified_value_gbp: Decimal
    net_verified_value_gbp: Decimal
    conclusion: str


def run_experiment_001(*, verify_outcome_value: bool = False) -> ExperimentResult:
    ledger = WorkforceEconomyLedger()
    ledger.register_worker(WorkerEconomicIdentity(
        worker_id="scout",
        role="market intelligence",
        cost_centre="AIDES-INTEL",
        permitted_spend_categories=frozenset({"model", "search", "runtime"}),
    ))
    ledger.authorise_budget(MissionBudget(
        mission_id="we-001-scout-signal",
        worker_id="scout",
        budget_gbp=Decimal("20.00"),
        authorised_by="deployer:anthony",
    ))

    # Synthetic costs prove the accounting path only. Replace with measured
    # provider/tool/runtime costs when a real mission telemetry adapter exists.
    ledger.record_spend(SpendRecord(
        "we-001-scout-signal", "scout", "model", Decimal("4.80"),
        "simulation://cost/model/001",
    ))
    ledger.record_spend(SpendRecord(
        "we-001-scout-signal", "scout", "search", Decimal("1.20"),
        "simulation://cost/search/001",
    ))

    # Hypothesis value is deliberately NOT counted as verified unless an
    # independent outcome/evidence process promotes it.
    ledger.record_value(ValueRecord(
        mission_id="we-001-scout-signal",
        worker_id="scout",
        attributed_value_gbp=Decimal("300.00"),
        outcome_ref="outcome://we-001/pending-independent-verification",
        evidence_ref="simulation://value-hypothesis/001",
        verified=verify_outcome_value,
    ))

    economics = ledger.worker_economics("scout")
    verified = Decimal(economics["verified_value_gbp"])
    conclusion = (
        "positive verified economics"
        if verified > Decimal(economics["spend_gbp"])
        else "insufficient verified economic evidence"
    )
    return ExperimentResult(
        experiment_id="WE-001",
        mission_id="we-001-scout-signal",
        worker_id="scout",
        budget_gbp=Decimal("20.00"),
        spend_gbp=Decimal(economics["spend_gbp"]),
        unverified_attributed_value_gbp=Decimal("0") if verify_outcome_value else Decimal("300.00"),
        verified_value_gbp=verified,
        net_verified_value_gbp=Decimal(economics["net_verified_value_gbp"]),
        conclusion=conclusion,
    )
