import networkx as nx
from typing import List, Tuple, Dict, Optional, Set


class GraphInputHandler:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._source_nodes: Set[int] = set()
        self._sink_nodes: Set[int] = set()

    def add_node(self, node_id: int, node_type: str = "intermediate") -> None:
        """
        Add a node to the graph with specified type.

        Args:
            node_id: Unique identifier for the node
            node_type: Type of node ('source', 'sink', or 'intermediate')
        """
        if node_type not in ["source", "sink", "intermediate"]:
            raise ValueError("Node type must be 'source', 'sink', or 'intermediate'")

        self.graph.add_node(node_id, type=node_type)
        if node_type == "source":
            self._source_nodes.add(node_id)
        elif node_type == "sink":
            self._sink_nodes.add(node_id)

    def add_edge(self, from_node: int, to_node: int, capacity: float) -> None:
        """
        Add a directed edge with capacity.

        Args:
            from_node: Source node ID
            to_node: Target node ID
            capacity: Edge capacity (must be positive)
        """
        if capacity <= 0:
            raise ValueError("Edge capacity must be positive")

        if not self.graph.has_node(from_node) or not self.graph.has_node(to_node):
            raise ValueError("Both nodes must exist in the graph")

        self.graph.add_edge(from_node, to_node, capacity=capacity)

    def get_graph(self) -> nx.DiGraph:
        """Get the current graph."""
        return self.graph

    def validate_graph(self) -> bool:
        """
        Validate the graph structure.

        Returns:
            bool: True if graph is valid

        Raises:
            ValueError: If graph structure is invalid
        """
        if not self.graph.is_directed():
            raise ValueError("Graph must be directed")

        if not self._source_nodes:
            raise ValueError("Graph must have at least one source")
        if not self._sink_nodes:
            raise ValueError("Graph must have at least one sink")

        # Check if all edges have capacity
        for u, v, data in self.graph.edges(data=True):
            if "capacity" not in data or data["capacity"] <= 0:
                raise ValueError(f"Edge ({u}, {v}) must have positive capacity")

        return True

    def get_sources(self) -> List[int]:
        """Get list of source nodes."""
        return list(self._source_nodes)

    def get_sinks(self) -> List[int]:
        """Get list of sink nodes."""
        return list(self._sink_nodes)

    def get_edge_capacity(self, u: int, v: int) -> float:
        """Get capacity of edge (u,v)."""
        return self.graph[u][v]["capacity"]
