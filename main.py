#!/usr/bin/env python3

"""Main script for maximum flow visualization."""

import os
from typing import List, Tuple
import networkx as nx
from src.graph.generator import GraphGenerator
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow
from src.visualizer.static_visualizer import StaticGraphVisualizer
from src.visualizer.animation_visualizer import AnimationGraphVisualizer
from src.graph.examples import create_example_graph


def run_algorithm_visualization(
    algorithm_class: type,
    graph: nx.DiGraph,
    algorithm_name: str
) -> None:
    """
    Run algorithm visualization.

    Args:
        algorithm_class: Algorithm class to use
        graph: Input graph
        algorithm_name: Name of the algorithm
    """
    print(f"Running {algorithm_name} visualization...")

    # Get source and sink nodes
    source = next(node for node, attr in graph.nodes(data=True) if attr.get("type") == "source")
    sink = next(node for node, attr in graph.nodes(data=True) if attr.get("type") == "sink")

    # Create algorithm instance
    algorithm = algorithm_class(graph)

    # Compute maximum flow and get augmenting paths
    max_flow, augmenting_paths, residual_graphs = algorithm.compute_max_flow(source, sink)

    print(f"Maximum flow: {max_flow}")
    print(f"Number of augmenting paths: {len(augmenting_paths)}")

    # Create animation
    animator = AnimationGraphVisualizer(graph)
    animator.create_animation(
        paths=augmenting_paths,
        residual_graphs=residual_graphs,
        title=f"{algorithm_name} Maximum Flow"
    )

    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Save animation
    animator.save(f'output/{algorithm_name.lower()}_flow.gif')

    # Create static visualizer for final state
    static_visualizer = StaticGraphVisualizer(graph)
    static_visualizer.visualize(
        title=f"{algorithm_name} Final State (Flow: {max_flow:.1f})",
        show_flow=True,
        residual_graph=residual_graphs[-1]
    )
    static_visualizer.save(f'output/{algorithm_name.lower()}_final.png')

    # Clean up
    animator.close()
    static_visualizer.close()

    print(f"Visualization saved to output/{algorithm_name.lower()}_flow.gif")
    print(f"Final state saved to output/{algorithm_name.lower()}_final.png")


def main() -> None:
    """Main function."""
    # Generate example graph
    generator = GraphGenerator()
    graph = generator.generate_random_graph(
        num_nodes=5,
        num_edges=7,
        num_sources=1,
        num_sinks=1,
        min_capacity=1.0,
        max_capacity=10.0
    )

    graph = create_example_graph()

    print("\nGraph information:")
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")
    print("\nEdge capacities:")
    for u, v, data in graph.edges(data=True):
        print(f"Edge ({u}, {v}): {data['capacity']:.1f}")

    # Run visualizations for both algorithms
    run_algorithm_visualization(BFSMaxFlow, graph, "BFS")
    run_algorithm_visualization(DFSMaxFlow, graph, "DFS")


if __name__ == "__main__":
    main()
