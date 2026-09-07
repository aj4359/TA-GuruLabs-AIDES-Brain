import unittest
from decimal import Decimal

from execution_graph import ExecutionEnvelope, ExecutionGraphPlan, GraphEdge, NodeContract, VerificationRequirement
from scout_execution_graph import scout_intelligence_graph


def envelope(workers=5, depth=5):
    return ExecutionEnvelope(workers, depth, Decimal("20"), 900, "policy://stop")


def verification(fresh=True):
    return VerificationRequirement(fresh, frozenset({"correctness", "current", "source_real"}), 2)


class ExecutionGraphTests(unittest.TestCase):
    def test_scout_fans_out_five_research_workers(self):
        plan = scout_intelligence_graph()
        plan.validate()
        self.assertEqual(plan.layers()[0], ("competitor", "customer", "market", "regulatory", "technology"))
        self.assertEqual(plan.layers()[1], ("verify",))
        self.assertEqual(plan.layers()[-1], ("action",))

    def test_fake_edge_is_rejected(self):
        a = NodeContract("a", "produce", frozenset(), frozenset({"x"}))
        b = NodeContract("b", "independent", frozenset(), frozenset({"y"}))
        gate = NodeContract("gate", "gate", frozenset(), frozenset({"approved"}))
        plan = ExecutionGraphPlan((a, b, gate), (GraphEdge("a", "b", "x"),), envelope(), verification(), "gate")
        with self.assertRaisesRegex(ValueError, "fake edge"):
            plan.validate()

    def test_fresh_context_verification_is_required(self):
        plan = scout_intelligence_graph()
        broken = ExecutionGraphPlan(plan.nodes, plan.edges, plan.envelope, verification(False), plan.human_gate_node_id)
        with self.assertRaisesRegex(ValueError, "fresh context"):
            broken.validate()

    def test_parallel_worker_cap_is_enforced(self):
        plan = scout_intelligence_graph()
        broken = ExecutionGraphPlan(plan.nodes, plan.edges, envelope(workers=4), plan.verification, plan.human_gate_node_id)
        with self.assertRaisesRegex(ValueError, "worker cap"):
            broken.validate()

    def test_depth_cap_is_enforced(self):
        plan = scout_intelligence_graph()
        broken = ExecutionGraphPlan(plan.nodes, plan.edges, envelope(depth=4), plan.verification, plan.human_gate_node_id)
        with self.assertRaisesRegex(ValueError, "depth cap"):
            broken.validate()

    def test_machine_consumed_output_must_be_structured(self):
        bad = NodeContract("a", "free text", frozenset(), frozenset({"x"}), structured_output=False)
        gate = NodeContract("gate", "gate", frozenset({"x"}), frozenset({"approved"}))
        plan = ExecutionGraphPlan((bad, gate), (GraphEdge("a", "gate", "x"),), envelope(), verification(), "gate")
        with self.assertRaisesRegex(ValueError, "structured output"):
            plan.validate()

    def test_cycle_is_rejected(self):
        a = NodeContract("a", "a", frozenset({"y"}), frozenset({"x"}))
        b = NodeContract("b", "b", frozenset({"x"}), frozenset({"y"}))
        gate = NodeContract("gate", "gate", frozenset(), frozenset({"approved"}))
        plan = ExecutionGraphPlan((a, b, gate), (GraphEdge("a", "b", "x"), GraphEdge("b", "a", "y")), envelope(), verification(), "gate")
        with self.assertRaisesRegex(ValueError, "cycle"):
            plan.validate()


if __name__ == "__main__":
    unittest.main()
