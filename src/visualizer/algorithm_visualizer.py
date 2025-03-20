#!/usr/bin/env python3

import networkx as nx
import os
from .static_visualizer import save_graph_visualization
from .animator import MaxFlowAnimator

def run_algorithm_visualization(graph: nx.DiGraph, algorithm_name: str, algorithm_class, source: int, sink: int):
    """Run and visualize a specific algorithm."""
    print(f"\nRunning {algorithm_name} max flow algorithm...")
    algorithm = algorithm_class(graph)
    
    # Run algorithm with history tracking
    flow, paths, residuals, metrics = algorithm.compute_max_flow_with_history(source, sink)
    print(f"{algorithm_name} Maximum flow: {flow}")
    print(f"Number of augmenting paths found: {len(paths)}")
    print("\nAugmenting paths:")
    for i, path in enumerate(paths):
        print(f"Path {i + 1}: {path}")
    
    # Create and save animation
    print(f"\nCreating {algorithm_name} flow animation...")
    animator = MaxFlowAnimator(graph)
    animation = animator.create_animation(paths, residuals, metrics)
    
    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save animation
    animation_path = os.path.join(output_dir, f'{algorithm_name.lower()}_flow.gif')
    print(f"Saving {algorithm_name} animation to '{animation_path}'...")
    animation.save(animation_path, writer='pillow', fps=1)
    
    # Save final state visualization
    print(f"Saving {algorithm_name} final state visualization...")
    final_graph = residuals[-1]
    # Store original capacities in the final graph
    for u, v in graph.edges():
        if final_graph.has_edge(u, v):
            final_graph[u][v]['original_capacity'] = graph[u][v]['capacity']
        if final_graph.has_edge(v, u):
            final_graph[v][u]['original_capacity'] = 0  # Reverse edges start with 0 capacity
    
    save_graph_visualization(final_graph, f'{algorithm_name.lower()}_final_graph.png', 
                           f"{algorithm_name} Final Graph State", show_flow=True)
    
    return flow, paths, residuals, metrics 