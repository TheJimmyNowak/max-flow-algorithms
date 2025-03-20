import networkx as nx
from typing import List, Dict, Tuple, Optional, Set
from collections import deque
from ..utils.metrics import MetricsTracker
from ..utils.max_flow_base import MaxFlowBase

class BFSMaxFlow(MaxFlowBase):
    """BFS implementation of maximum flow algorithm."""
    
    def __init__(self, graph: nx.DiGraph):
        super().__init__(graph)
        self.residual_graph = graph.copy()
        self.metrics = MetricsTracker()
        
        # Initialize residual graph with reverse edges
        for u, v, data in self.graph.edges(data=True):
            if not self.residual_graph.has_edge(v, u):
                self.residual_graph.add_edge(v, u, capacity=0)
    
    def find_augmenting_path(self, source: int, sink: int) -> Optional[List[int]]:
        """
        Find an augmenting path using BFS.
        
        Args:
            source: Source node
            sink: Sink node
            
        Returns:
            List of nodes in the path if found, None otherwise
        """
        if not self.residual_graph.has_node(source) or not self.residual_graph.has_node(sink):
            raise KeyError("Source or sink node not in graph")
            
        queue = deque([(source, [source])])
        visited = {source}
        
        while queue:
            current, path = queue.popleft()
            self.metrics.increment_step()
            self.metrics.add_visited_node(current)
            
            if current == sink:
                return path
            
            for neighbor in self.residual_graph.neighbors(current):
                if neighbor not in visited and self.residual_graph[current][neighbor]['capacity'] > 0:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
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
            self.residual_graph[u][v]['capacity'] -= flow
            self.metrics.update_residual_capacity((u, v), self.residual_graph[u][v]['capacity'])
            
            # Backward edge (already exists from initialization)
            self.residual_graph[v][u]['capacity'] += flow
            self.metrics.update_residual_capacity((v, u), self.residual_graph[v][u]['capacity'])
    
    def find_min_capacity(self, path: List[int]) -> float:
        """
        Find minimum capacity along the path.
        
        Args:
            path: List of nodes in the path
            
        Returns:
            Minimum capacity along the path
        """
        min_capacity = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            capacity = self.residual_graph[u][v]['capacity']
            min_capacity = min(min_capacity, capacity)
        return min_capacity
    
    def compute_max_flow(self, source: int, sink: int) -> float:
        """
        Compute maximum flow using BFS-based Ford-Fulkerson algorithm.
        
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
