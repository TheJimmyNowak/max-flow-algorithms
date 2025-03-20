import networkx as nx
from typing import List, Dict, Tuple, Optional, Set
from ..utils.metrics import MetricsTracker
from ..utils.max_flow_base import MaxFlowBase


class DFSMaxFlow(MaxFlowBase):
    """DFS implementation of maximum flow algorithm."""

    def __init__(self, graph: nx.DiGraph):
        super().__init__(graph)
        self.residual_graph = graph.copy()
        self.metrics = MetricsTracker()

        # Initialize residual graph with reverse edges
        for u, v, data in self.graph.edges(data=True):
            if not self.residual_graph.has_edge(v, u):
                self.residual_graph.add_edge(v, u, capacity=0)

    def find_augmenting_path(
        self,
        source: int,
        sink: int,
        visited: Optional[Set[int]] = None,
        path: Optional[List[int]] = None,
    ) -> Optional[List[int]]:
        """
        Find an augmenting path using DFS.

        Args:
            source: Source node
            sink: Sink node
            visited: Set of visited nodes (used in recursion)
            path: Current path (used in recursion)

        Returns:
            List of nodes in the path if found, None otherwise
        """
        if not self.residual_graph.has_node(source) or not self.residual_graph.has_node(sink):
            raise KeyError("Source or sink node not in graph")

        # Initialize visited set and path for first call
        if visited is None:
            visited = set()
        if path is None:
            path = [source]

        current = path[-1]
        self.metrics.increment_step()
        self.metrics.add_visited_node(current)

        if current == sink:
            return path

        visited.add(current)

        for neighbor in self.residual_graph.neighbors(current):
            if neighbor not in visited and self.residual_graph[current][neighbor]["capacity"] > 0:
                new_path = self.find_augmenting_path(source, sink, visited, path + [neighbor])
                if new_path:
                    return new_path

        visited.remove(current)
        return None

    def update_residual_capacities(self, path: List[int], flow: float) -> None:
        """
        Update residual capacities along the path.

        Args:
            path: List of nodes in the path
            flow: Flow value to push along the path
        """
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            # Forward edge
            self.residual_graph[u][v]["capacity"] -= flow
            self.metrics.update_residual_capacity((u, v), self.residual_graph[u][v]["capacity"])

            # Backward edge (already exists from initialization)
            self.residual_graph[v][u]["capacity"] += flow
            self.metrics.update_residual_capacity((v, u), self.residual_graph[v][u]["capacity"])

    def find_min_capacity(self, path: List[int]) -> float:
        """
        Find minimum capacity along the path.

        Args:
            path: List of nodes in the path

        Returns:
            Minimum capacity along the path
        """
        min_capacity = float("inf")
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            capacity = self.residual_graph[u][v]["capacity"]
            min_capacity = min(min_capacity, capacity)
        return min_capacity

    def compute_max_flow(self, source: int, sink: int) -> float:
        """
        Compute maximum flow using DFS-based Ford-Fulkerson algorithm.

        Args:
            source: Source node
            sink: Sink node

        Returns:
            Maximum flow value
        """
        if not self.residual_graph.has_node(source) or not self.residual_graph.has_node(sink):
            raise KeyError("Source or sink node not in graph")

        self.metrics.start_tracking()
        max_flow = 0.0

        while True:
            path = self.find_augmenting_path(source, sink)
            if not path:
                break

            flow = self.find_min_capacity(path)
            self.update_residual_capacities(path, flow)
            max_flow += flow
            self.metrics.add_path(flow)

        return max_flow

    def get_metrics(self):
        """Get algorithm performance metrics."""
        return self.metrics.get_metrics()
