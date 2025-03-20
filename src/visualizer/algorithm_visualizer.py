#!/usr/bin/env python3

import networkx as nx
import os
from typing import Type, List, Tuple
from ..utils.max_flow_base import MaxFlowBase
from ..utils.metrics import AlgorithmMetrics
from .static_visualizer import save_graph_visualization
from .animator import MaxFlowAnimator

def run_algorithm_visualization(
    graph: nx.DiGraph,
    algorithm_name: str,
    algorithm_class: Type[MaxFlowBase],
    source: int,
    sink: int
) -> Tuple[float, List[List[int]], List[nx.DiGraph], List[AlgorithmMetrics]]:
    """
    Run the specified algorithm and create visualizations.
    
    Args:
        graph: NetworkX graph
        algorithm_name: Name of the algorithm (for visualization titles)
        algorithm_class: Algorithm class to use
        source: Source node
        sink: Sink node
        
    Returns:
        Tuple containing:
        - Maximum flow value
        - List of augmenting paths
        - List of residual graphs
        - List of metrics
    """
    print(f"\nRunning {algorithm_name} max flow algorithm...")
    
    # Create algorithm instance
    algorithm = algorithm_class(graph)
    
    # Compute maximum flow with history
    max_flow, paths, residuals, metrics = algorithm.compute_max_flow_with_history(source, sink)
    
    print(f"{algorithm_name} Maximum flow: {max_flow}")
    print(f"Number of augmenting paths found: {len(paths)}\n")
    
    print("Augmenting paths:")
    for i, path in enumerate(paths, 1):
        print(f"Path {i}: {path}")
    
    # Create animator
    animator = MaxFlowAnimator(graph)
    
    # Create and save animation
    print(f"\nCreating {algorithm_name} flow animation...")
    animation = animator.create_animation(paths, residuals, metrics)
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    print(f"Saving {algorithm_name} animation to 'output/{algorithm_name.lower()}_flow.gif'...")
    animation.save(f'output/{algorithm_name.lower()}_flow.gif', writer='pillow')
    
    # Store original capacities in the final graph for visualization
    final_graph = residuals[-1]
    for u, v in graph.edges():
        if (u, v) in final_graph.edges():
            final_graph[u][v]['original_capacity'] = graph[u][v]['capacity']
        if (v, u) in final_graph.edges():
            final_graph[v][u]['original_capacity'] = 0  # Reverse edges start with 0 capacity
    
    # Save final state visualization
    print(f"Saving {algorithm_name} final state visualization...")
    save_graph_visualization(
        final_graph,
        f'output/{algorithm_name.lower()}_final_graph.png',
        title=f"{algorithm_name} Final State",
        show_flow=True
    )
    
    return max_flow, paths, residuals, metrics 