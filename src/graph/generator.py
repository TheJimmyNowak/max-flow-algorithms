import networkx as nx
import numpy as np
from typing import List, Tuple, Dict, Optional
import random


class GraphGenerator:
    def __init__(self):
        self.graph = nx.DiGraph()

    def generate_random_graph(
        self,
        num_nodes: int,
        num_edges: int,
        num_sources: int,
        num_sinks: int,
        min_capacity: float = 1.0,
        max_capacity: float = 10.0,
    ) -> nx.DiGraph:
        """
        Generate a random directed graph with multiple sources and sinks.

        Args:
            num_nodes: Number of nodes in the graph
            num_edges: Number of edges to generate
            num_sources: Number of source nodes
            num_sinks: Number of sink nodes
            min_capacity: Minimum edge capacity
            max_capacity: Maximum edge capacity

        Returns:
            NetworkX directed graph with capacity attributes

        Raises:
            ValueError: If it's impossible to generate the requested number of edges
        """
        if num_edges > num_nodes * (num_nodes - 1):
            raise ValueError(f"Cannot generate {num_edges} unique edges with {num_nodes} nodes")

        # Clear existing graph
        self.graph.clear()

        # Add nodes
        self.graph.add_nodes_from(range(num_nodes))

        # Generate all possible edges and shuffle them
        all_edges = [(i, j) for i in range(num_nodes) for j in range(num_nodes) if i != j]
        np.random.shuffle(all_edges)

        # Take the first num_edges edges and assign random capacities
        edges_with_capacity = [
            (u, v, np.random.uniform(min_capacity, max_capacity)) for u, v in all_edges[:num_edges]
        ]

        # Add edges with capacities
        self.graph.add_weighted_edges_from(edges_with_capacity, weight="capacity")

        # Mark sources and sinks
        nodes = list(range(num_nodes))
        np.random.shuffle(nodes)

        # Add source and sink attributes
        for i, node in enumerate(nodes):
            if i < num_sources:
                self.graph.nodes[node]["type"] = "source"
            elif i < num_sources + num_sinks:
                self.graph.nodes[node]["type"] = "sink"
            else:
                self.graph.nodes[node]["type"] = "intermediate"

        return self.graph

    def get_sources(self) -> List[int]:
        """Get list of source nodes."""
        return [node for node, data in self.graph.nodes(data=True) if data.get("type") == "source"]

    def get_sinks(self) -> List[int]:
        """Get list of sink nodes."""
        return [node for node, data in self.graph.nodes(data=True) if data.get("type") == "sink"]

    def get_edge_capacity(self, u: int, v: int) -> float:
        """
        Get capacity of edge (u,v).

        Args:
            u: Source node
            v: Target node

        Returns:
            float: Edge capacity

        Raises:
            KeyError: If edge (u,v) does not exist
        """
        if not self.graph.has_edge(u, v):
            raise KeyError(f"Edge ({u}, {v}) does not exist in the graph")
        return self.graph[u][v]["capacity"]

    def generate_path_bias_graph(self, num_nodes, num_edges, num_sources, num_sinks, min_capacity, max_capacity):
        G = nx.DiGraph()

        # Stwórz podstawową ścieżkę
        for i in range(num_nodes - 1):
            G.add_edge(i, i + 1, capacity=random.uniform(min_capacity, max_capacity))

        # Dodaj dodatkowe losowe krawędzie do zwiększenia złożoności
        remaining_edges = num_edges - (num_nodes - 1)
        while remaining_edges > 0:
            u = random.randint(0, num_nodes - 2)
            v = random.randint(u + 1, num_nodes - 1)
            if not G.has_edge(u, v):
                G.add_edge(u, v, capacity=random.uniform(min_capacity, max_capacity))
                remaining_edges -= 1

        for node in G.nodes():
            G.nodes[node]['type'] = 'intermediate'

        self._assign_source_sink(G, num_sources, num_sinks)
        return G

    def _assign_source_sink(self, G, num_sources, num_sinks):
        nodes = list(G.nodes())
        random.shuffle(nodes)

        for i in range(num_sources):
            G.nodes[nodes[i]]['type'] = 'source'
        for i in range(num_sinks):
            G.nodes[nodes[-(i + 1)]]['type'] = 'sink'
