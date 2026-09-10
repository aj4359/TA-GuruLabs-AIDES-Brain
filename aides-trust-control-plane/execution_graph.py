"""Public-safe AIDES Adaptive Execution Graph contracts.

The graph expresses bounded jobs and real data dependencies. It does not expose
private prompts, routing heuristics, memory contents, credentials or production
topology. Runtime execution remains governed by the Trust Control Plane.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import FrozenSet, Tuple


@dataclass(frozen=True)
class NodeContract:
    node_id: str
    job: str
    required_inputs: FrozenSet[str]
    produced_outputs: FrozenSet[str]
    structured_output: bool = True
    consequential_action: bool = False

    def validate(self) -> None:
        if not self.node_id or not self.job:
            raise ValueError("node id and bounded job are required")
        if not self.structured_output:
            raise ValueError("machine-consumed nodes require structured output")
        if self.required_inputs & self.produced_outputs:
            raise ValueError("node cannot require and produce the same artifact")


@dataclass(frozen=True)
class GraphEdge:
    from_node: str
    to_node: str
    artifact: str


@dataclass(frozen=True)
class ExecutionEnvelope:
    max_workers: int
    max_depth: int
    max_cost_gbp: Decimal
    max_runtime_seconds: int
    stop_condition_ref: str
    human_gate_required_for_consequential_actions: bool = True

    def validate(self) -> None:
        if self.max_workers <= 0 or self.max_depth <= 0 or self.max_runtime_seconds <= 0:
            raise ValueError("worker, depth and runtime caps must be positive")
        if self.max_cost_gbp < 0:
            raise ValueError("cost cap cannot be negative")
        if not self.stop_condition_ref:
            raise ValueError("explicit stop condition required")


@dataclass(frozen=True)
class VerificationRequirement:
    fresh_context: bool
    lenses: FrozenSet[str]
    minimum_passes: int

    def validate(self) -> None:
        allowed = {"correctness", "current", "source_real"}
        if not self.fresh_context:
            raise ValueError("verifier must use fresh context")
        if not self.lenses or not self.lenses.issubset(allowed):
            raise ValueError("unsupported or empty verification lenses")
        if self.minimum_passes <= 0 or self.minimum_passes > len(self.lenses):
            raise ValueError("invalid verification pass threshold")


@dataclass(frozen=True)
class ExecutionGraphPlan:
    nodes: Tuple[NodeContract, ...]
    edges: Tuple[GraphEdge, ...]
    envelope: ExecutionEnvelope
    verification: VerificationRequirement
    human_gate_node_id: str

    def validate(self) -> None:
        self.envelope.validate()
        self.verification.validate()
        node_map = {node.node_id: node for node in self.nodes}
        if len(node_map) != len(self.nodes):
            raise ValueError("duplicate node id")
        for node in self.nodes:
            node.validate()
        if self.human_gate_node_id not in node_map:
            raise ValueError("human gate node must exist")

        incoming = {node.node_id: set() for node in self.nodes}
        successors = {node.node_id: set() for node in self.nodes}
        for edge in self.edges:
            if edge.from_node not in node_map or edge.to_node not in node_map:
                raise ValueError("edge references unknown node")
            producer = node_map[edge.from_node]
            consumer = node_map[edge.to_node]
            if edge.artifact not in producer.produced_outputs:
                raise ValueError("edge artifact is not produced upstream")
            if edge.artifact not in consumer.required_inputs:
                raise ValueError("fake edge: downstream node does not require artifact")
            incoming[edge.to_node].add(edge.artifact)
            successors[edge.from_node].add(edge.to_node)

        for node in self.nodes:
            missing = node.required_inputs - incoming[node.node_id]
            if missing:
                raise ValueError(f"missing dependency artifacts for {node.node_id}: {sorted(missing)}")
            if node.consequential_action and self.envelope.human_gate_required_for_consequential_actions:
                if node.node_id == self.human_gate_node_id:
                    raise ValueError("human gate cannot itself be the consequential action")
                if not self._reachable(self.human_gate_node_id, node.node_id, successors):
                    raise ValueError("consequential action must be downstream of human gate")

        layers = self.layers()
        if len(layers) > self.envelope.max_depth:
            raise ValueError("graph exceeds depth cap")
        if max((len(layer) for layer in layers), default=0) > self.envelope.max_workers:
            raise ValueError("graph exceeds parallel worker cap")

    @staticmethod
    def _reachable(start: str, target: str, successors) -> bool:
        pending = [start]
        seen = set()
        while pending:
            current = pending.pop()
            if current == target:
                return True
            if current in seen:
                continue
            seen.add(current)
            pending.extend(successors[current] - seen)
        return False

    def layers(self) -> Tuple[Tuple[str, ...], ...]:
        node_ids = {node.node_id for node in self.nodes}
        deps = {node_id: set() for node_id in node_ids}
        for edge in self.edges:
            deps[edge.to_node].add(edge.from_node)
        remaining = set(node_ids)
        completed = set()
        result = []
        while remaining:
            ready = sorted(node for node in remaining if deps[node].issubset(completed))
            if not ready:
                raise ValueError("execution graph contains a cycle")
            result.append(tuple(ready))
            completed.update(ready)
            remaining.difference_update(ready)
        return tuple(result)
