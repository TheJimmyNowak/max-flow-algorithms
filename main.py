#!/usr/bin/env python3

"""Main script for maximum flow visualization."""

#!/usr/bin/env python3

"""Main script for maximum flow visualization."""

import os
import sys
from typing import List, Tuple
import networkx as nx
from src.graph.generator import GraphGenerator
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow
from src.visualizer.animation_visualizer import CombinedAnimationVisualizer
from src.graph.examples import create_example_graph


def run_combined_visualization(
    graph: nx.DiGraph,
    bfs_paths: List[List[int]],
    dfs_paths: List[List[int]],
    bfs_residual_graphs: List[nx.DiGraph],
    dfs_residual_graphs: List[nx.DiGraph],
    output_file: str = 'output/combined_flow.gif'
) -> None:
    """Run combined BFS and DFS visualization."""
    print("\nCreating combined visualization...")

    try:
        # Create combined animation
        visualizer = CombinedAnimationVisualizer(graph)
        visualizer.create_combined_animation(
            bfs_paths=bfs_paths,
            dfs_paths=dfs_paths,
            bfs_residual_graphs=bfs_residual_graphs,
            dfs_residual_graphs=dfs_residual_graphs,
            title="Maximum Flow: BFS vs DFS"
        )

        # Ensure output directory exists
        os.makedirs('output', exist_ok=True)

        # Save animation
        visualizer.save(output_file)
        visualizer.close()

        print(f"Combined visualization saved to {output_file}")

    except Exception as e:
        print(f"Error in combined visualization: {str(e)}", file=sys.stderr)
        raise


def main() -> None:
    """Main function."""
    # Generate example graph
    graph = create_example_graph()

    print("\nGraph information:")
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")
    print("\nEdge capacities:")
    for u, v, data in graph.edges(data=True):
        print(f"Edge ({u}, {v}): {data['capacity']:.1f}")

    # Get source and sink nodes
    source = next(node for node, attr in graph.nodes(data=True) if attr.get("type") == "source")
    sink = next(node for node, attr in graph.nodes(data=True) if attr.get("type") == "sink")

    # Run BFS algorithm
    print("\nRunning BFS algorithm...")
    bfs = BFSMaxFlow(graph)
    bfs_max_flow, bfs_paths, bfs_residual_graphs = bfs.compute_max_flow(source, sink)
    print(f"BFS Max Flow: {bfs_max_flow}")
    print(f"BFS found {len(bfs_paths)} augmenting paths")

    # Run DFS algorithm
    print("\nRunning DFS algorithm...")
    dfs = DFSMaxFlow(graph)
    dfs_max_flow, dfs_paths, dfs_residual_graphs = dfs.compute_max_flow(source, sink)
    print(f"DFS Max Flow: {dfs_max_flow}")
    print(f"DFS found {len(dfs_paths)} augmenting paths")

    # Create combined visualization
    run_combined_visualization(
        graph=graph,
        bfs_paths=bfs_paths,
        dfs_paths=dfs_paths,
        bfs_residual_graphs=bfs_residual_graphs,
        dfs_residual_graphs=dfs_residual_graphs
    )


if __name__ == "__main__":
    main()