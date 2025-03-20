import time
from dataclasses import dataclass
from typing import List, Dict, Any
from collections import defaultdict


@dataclass
class AlgorithmMetrics:
    """Class to store algorithm performance metrics."""

    execution_time: float
    steps_count: int
    paths_found: int
    total_flow: float
    visited_nodes: List[int]
    residual_capacities: Dict[tuple, float]

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary format."""
        return {
            "execution_time": self.execution_time,
            "steps_count": self.steps_count,
            "paths_found": self.paths_found,
            "total_flow": self.total_flow,
            "visited_nodes": self.visited_nodes,
            "residual_capacities": self.residual_capacities,
        }


class MetricsTracker:
    """Class to track algorithm performance metrics."""

    def __init__(self):
        self.start_time = None
        self.steps = 0
        self.paths = 0
        self.visited = []
        self.residual_caps = defaultdict(float)
        self.total_flow = 0.0

    def start_tracking(self) -> None:
        """Start tracking metrics."""
        self.start_time = time.time()
        self.steps = 0
        self.paths = 0
        self.visited = []
        self.residual_caps.clear()
        self.total_flow = 0.0

    def increment_step(self) -> None:
        """Increment step counter."""
        self.steps += 1

    def add_path(self, flow: float) -> None:
        """Record a found path and its flow."""
        self.paths += 1
        self.total_flow += flow

    def add_visited_node(self, node: int) -> None:
        """Record a visited node."""
        if node not in self.visited:
            self.visited.append(node)

    def update_residual_capacity(self, edge: tuple, capacity: float) -> None:
        """Update residual capacity for an edge."""
        self.residual_caps[edge] = capacity

    def get_metrics(self) -> AlgorithmMetrics:
        """Get current metrics."""
        if self.start_time is None:
            raise RuntimeError("Metrics tracking not started")

        execution_time = time.time() - self.start_time

        return AlgorithmMetrics(
            execution_time=execution_time,
            steps_count=self.steps,
            paths_found=self.paths,
            total_flow=self.total_flow,
            visited_nodes=self.visited,
            residual_capacities=dict(self.residual_caps),
        )
