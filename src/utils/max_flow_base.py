import networkx as nx
from typing import List, Dict, Tuple, Optional, Set
from .metrics import MetricsTracker

class MaxFlowBase:
    """Base class for maximum flow algorithms."""
    
    def __init__(self, graph: nx.DiGraph):
        """
        Initialize the algorithm with a graph.
        
        Args:
            graph: NetworkX directed graph with capacity attributes
        """
        self.graph = graph
        self.residual_graph = graph.copy()
        self.metrics = MetricsTracker()
        
        # Cache node types for faster access
        self._source_nodes = self._get_nodes_of_type('source')
        self._sink_nodes = self._get_nodes_of_type('sink')
        
        # Initialize residual graph with reverse edges
        for u, v, _ in self.graph.edges(data=True):
            if not self.residual_graph.has_edge(v, u):
                self.residual_graph.add_edge(v, u, capacity=0)
    
    def _get_nodes_of_type(self, node_type: str) -> Set[int]:
        """Get set of nodes of specified type."""
        return {node for node, data in self.graph.nodes(data=True) 
                if data.get('type') == node_type}
    
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
        return min(self.residual_graph[u][v]['capacity'] 
                  for u, v in zip(path[:-1], path[1:]))
    
    def compute_max_flow(self, source: int, sink: int) -> float:
        """
        Compute maximum flow using Ford-Fulkerson algorithm.
        
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
    
    def compute_max_flow_with_history(self, source: int, sink: int) -> Tuple[float, List[List[int]], List[nx.DiGraph], List[Dict]]:
        """
        Compute maximum flow and track history of paths and residual graphs.
        
        Args:
            source: Source node
            sink: Sink node
            
        Returns:
            Tuple containing:
            - Maximum flow value
            - List of augmenting paths found
            - List of residual graphs at each step
            - List of metrics at each step
        """
        if not self.residual_graph.has_node(source) or not self.residual_graph.has_node(sink):
            raise KeyError("Source or sink node not in graph")
        
        self.metrics.start_tracking()
        max_flow = 0.0
        paths = []
        residual_graphs = [self.residual_graph.copy()]
        metrics_history = []
        
        while True:
            path = self.find_augmenting_path(source, sink)
            if not path:
                break
            
            flow = self.find_min_capacity(path)
            self.update_residual_capacities(path, flow)
            max_flow += flow
            self.metrics.add_path(flow)
            
            # Record history
            paths.append(path)
            residual_graphs.append(self.residual_graph.copy())
            metrics_history.append(self.metrics.get_metrics())
        
        return max_flow, paths, residual_graphs, metrics_history
    
    def get_metrics(self) -> Dict:
        """Get algorithm performance metrics."""
        return self.metrics.get_metrics()
    
    def find_augmenting_path(self, source: int, sink: int) -> Optional[List[int]]:
        """
        Abstract method to find an augmenting path.
        Must be implemented by subclasses.
        
        Args:
            source: Source node
            sink: Sink node
            
        Returns:
            List of nodes in the path if found, None otherwise
        """
        raise NotImplementedError("Subclasses must implement find_augmenting_path") 