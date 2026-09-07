"""Sanitised Scout graph proving fan-out -> verify -> merge -> human gate."""
from decimal import Decimal

from execution_graph import (
    ExecutionEnvelope, ExecutionGraphPlan, GraphEdge, NodeContract,
    VerificationRequirement,
)


def scout_intelligence_graph() -> ExecutionGraphPlan:
    research = (
        NodeContract("market", "collect market signals", frozenset(), frozenset({"market_findings"})),
        NodeContract("competitor", "collect competitor changes", frozenset(), frozenset({"competitor_findings"})),
        NodeContract("regulatory", "collect regulatory changes", frozenset(), frozenset({"regulatory_findings"})),
        NodeContract("customer", "collect public customer signals", frozenset(), frozenset({"customer_findings"})),
        NodeContract("technology", "collect technology changes", frozenset(), frozenset({"technology_findings"})),
    )
    verify_inputs = frozenset({
        "market_findings", "competitor_findings", "regulatory_findings",
        "customer_findings", "technology_findings",
    })
    verifier = NodeContract("verify", "independently verify findings", verify_inputs, frozenset({"verified_findings"}))
    merge = NodeContract("merge", "deduplicate and rank material changes", frozenset({"verified_findings"}), frozenset({"ranked_brief"}))
    gate = NodeContract("human_gate", "review consequential recommendation", frozenset({"ranked_brief"}), frozenset({"approved_brief"}))
    action = NodeContract("action", "execute approved consequential action", frozenset({"approved_brief"}), frozenset({"action_receipt"}), consequential_action=True)
    nodes = research + (verifier, merge, gate, action)
    edges = tuple(GraphEdge(node.node_id, "verify", next(iter(node.produced_outputs))) for node in research) + (
        GraphEdge("verify", "merge", "verified_findings"),
        GraphEdge("merge", "human_gate", "ranked_brief"),
        GraphEdge("human_gate", "action", "approved_brief"),
    )
    return ExecutionGraphPlan(
        nodes=nodes,
        edges=edges,
        envelope=ExecutionEnvelope(
            max_workers=5,
            max_depth=5,
            max_cost_gbp=Decimal("20.00"),
            max_runtime_seconds=900,
            stop_condition_ref="policy://scout/material-change-or-budget-stop",
        ),
        verification=VerificationRequirement(
            fresh_context=True,
            lenses=frozenset({"correctness", "current", "source_real"}),
            minimum_passes=2,
        ),
        human_gate_node_id="human_gate",
    )
