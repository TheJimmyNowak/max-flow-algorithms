import networkx as nx
import numpy as np
from typing import List, Tuple, Dict, Optional

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
        max_capacity: float = 10.0
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
        
        # Generate all possible edges
        all_edges = [(i, j) for i in range(num_nodes) for j in range(num_nodes) if i != j]
        np.random.shuffle(all_edges)
        
        # Take the first num_edges edges and assign random capacities
        selected_edges = all_edges[:num_edges]
        edges_with_capacity = [
            (u, v, np.random.uniform(min_capacity, max_capacity))
            for u, v in selected_edges
        ]
        
        # Add edges with capacities
        self.graph.add_weighted_edges_from(edges_with_capacity, weight='capacity')
        
        # Mark sources and sinks
        nodes = list(range(num_nodes))
        np.random.shuffle(nodes)
        
        # Add source and sink attributes
        for i, node in enumerate(nodes):
            if i < num_sources:
                self.graph.nodes[node]['type'] = 'source'
            elif i < num_sources + num_sinks:
                self.graph.nodes[node]['type'] = 'sink'
            else:
                self.graph.nodes[node]['type'] = 'intermediate'
        
        return self.graph
    
    def get_sources(self) -> List[int]:
        """Get list of source nodes."""
        return [node for node, data in self.graph.nodes(data=True) 
                if data.get('type') == 'source']
    
    def get_sinks(self) -> List[int]:
        """Get list of sink nodes."""
        return [node for node, data in self.graph.nodes(data=True) 
                if data.get('type') == 'sink']
    
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
        return self.graph[u][v]['capacity']
