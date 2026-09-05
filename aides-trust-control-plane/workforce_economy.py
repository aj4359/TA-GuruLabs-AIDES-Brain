"""AIDES Workforce Economy v1: simulation-only economic accounting.

No cryptocurrency, custody, payroll, legal employment status, or external money
movement is implemented here. Values are internal accounting units used to test
whether governed digital work creates evidence-backed economic value.
"""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class WorkerEconomicIdentity:
    worker_id: str
    role: str
    cost_centre: str
    permitted_spend_categories: frozenset[str]


@dataclass(frozen=True)
class MissionBudget:
    mission_id: str
    worker_id: str
    budget_gbp: Decimal
    authorised_by: str


@dataclass(frozen=True)
class SpendRecord:
    mission_id: str
    worker_id: str
    category: str
    amount_gbp: Decimal
    evidence_ref: str


@dataclass(frozen=True)
class ValueRecord:
    mission_id: str
    worker_id: str
    attributed_value_gbp: Decimal
    outcome_ref: str
    evidence_ref: str
    verified: bool = False


@dataclass
class WorkforceEconomyLedger:
    workers: dict[str, WorkerEconomicIdentity] = field(default_factory=dict)
    budgets: dict[str, MissionBudget] = field(default_factory=dict)
    spends: list[SpendRecord] = field(default_factory=list)
    values: list[ValueRecord] = field(default_factory=list)

    def register_worker(self, worker: WorkerEconomicIdentity) -> None:
        if worker.worker_id in self.workers:
            raise ValueError("worker already registered")
        self.workers[worker.worker_id] = worker

    def authorise_budget(self, budget: MissionBudget) -> None:
        if budget.worker_id not in self.workers:
            raise ValueError("unknown worker")
        if budget.budget_gbp < 0:
            raise ValueError("budget cannot be negative")
        if budget.mission_id in self.budgets:
            raise ValueError("mission budget already exists")
        self.budgets[budget.mission_id] = budget

    def record_spend(self, spend: SpendRecord) -> None:
        worker = self.workers.get(spend.worker_id)
        budget = self.budgets.get(spend.mission_id)
        if worker is None or budget is None or budget.worker_id != spend.worker_id:
            raise ValueError("worker/mission authority mismatch")
        if spend.category not in worker.permitted_spend_categories:
            raise PermissionError("spend category not authorised")
        if spend.amount_gbp < 0:
            raise ValueError("spend cannot be negative")
        if self.mission_spend(spend.mission_id) + spend.amount_gbp > budget.budget_gbp:
            raise PermissionError("mission budget exceeded")
        self.spends.append(spend)

    def record_value(self, value: ValueRecord) -> None:
        if value.worker_id not in self.workers:
            raise ValueError("unknown worker")
        if value.mission_id not in self.budgets:
            raise ValueError("unknown mission")
        if value.attributed_value_gbp < 0:
            raise ValueError("attributed value cannot be negative")
        if not value.outcome_ref or not value.evidence_ref:
            raise ValueError("economic value requires outcome and evidence references")
        self.values.append(value)

    def mission_spend(self, mission_id: str) -> Decimal:
        return sum((s.amount_gbp for s in self.spends if s.mission_id == mission_id), Decimal("0"))

    def verified_value(self, worker_id: str) -> Decimal:
        return sum((v.attributed_value_gbp for v in self.values if v.worker_id == worker_id and v.verified), Decimal("0"))

    def worker_economics(self, worker_id: str) -> dict[str, str]:
        spend = sum((s.amount_gbp for s in self.spends if s.worker_id == worker_id), Decimal("0"))
        verified = self.verified_value(worker_id)
        return {
            "worker_id": worker_id,
            "spend_gbp": str(spend),
            "verified_value_gbp": str(verified),
            "net_verified_value_gbp": str(verified - spend),
        }
