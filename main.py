#!/usr/bin/env python3

import os
from src.graph.examples import create_example_graph, create_random_graph
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow
from src.visualizer.static_visualizer import StaticGraphVisualizer
from src.visualizer.animator import MaxFlowAnimator


def run_algorithm_visualization(
    graph,
    algorithm_name: str,
    algorithm_class,
    source: int,
    sink: int,
    save_animation: bool = True,
    save_final_state: bool = True,
) -> tuple:
    """
    Run a maximum flow algorithm with visualization.

    Args:
        graph: NetworkX graph
        algorithm_name: Name of the algorithm (for visualization titles)
        algorithm_class: Algorithm class to use
        source: Source node
        sink: Sink node
        save_animation: Whether to save the animation
        save_final_state: Whether to save the final state visualization

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

    # Run algorithm and collect results
    max_flow, paths, residuals, metrics = algorithm.compute_max_flow_with_history(source, sink)

    print(f"{algorithm_name} Maximum flow: {max_flow}")
    print(f"Number of augmenting paths found: {len(paths)}\n")

    print("Augmenting paths:")
    for i, path in enumerate(paths, 1):
        print(f"Path {i}: {path}")

    # Create output directory if needed
    if save_animation or save_final_state:
        os.makedirs("output", exist_ok=True)

    # Create and save animation if requested
    if save_animation:
        print(f"\nCreating {algorithm_name} flow animation...")
        animator = MaxFlowAnimator(graph)
        animation = animator.create_animation(paths, residuals, metrics)
        print(f"Saving {algorithm_name} animation to 'output/{algorithm_name.lower()}_flow.gif'...")
        animation.save(f"output/{algorithm_name.lower()}_flow.gif", writer="pillow")
        animator.close()

    # Save final state visualization if requested
    if save_final_state:
        print(f"Saving {algorithm_name} final state visualization...")
        # Create a copy of the final residual graph for visualization
        final_graph = graph.copy()
        for u, v in final_graph.edges():
            final_graph[u][v]["capacity"] = residuals[-1][u][v]["capacity"]

        visualizer = StaticGraphVisualizer(final_graph)
        visualizer.visualize(
            title=f"{algorithm_name} Final State\nMax Flow: {max_flow:.2f}", show_flow=True
        )
        visualizer.save(f"output/{algorithm_name.lower()}_final_state.png")
        visualizer.close()

    return max_flow, paths, residuals, metrics


def main():
    # Create both example and random graphs
    example_graph = create_example_graph()
    random_graph = create_random_graph()

    # For demonstration, we'll use the example graph
    graph = example_graph

    # Get source and sink nodes
    source = next(node for node, attr in graph.nodes(data=True) if attr.get("type") == "source")
    sink = next(node for node, attr in graph.nodes(data=True) if attr.get("type") == "sink")

    print(f"Graph information:")
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")
    print(f"Source node: {source}")
    print(f"Sink node: {sink}")
    print("\nEdge capacities:")
    for u, v, data in graph.edges(data=True):
        print(f"Edge ({u}, {v}): {data['capacity']}")

    # Save initial graph visualization
    print("\nSaving initial graph visualization...")
    visualizer = StaticGraphVisualizer(graph)
    visualizer.visualize(title="Initial Graph State")
    visualizer.save("output/initial_graph.png")
    visualizer.close()

    # Run and visualize BFS algorithm
    bfs_flow, bfs_paths, bfs_residuals, bfs_metrics = run_algorithm_visualization(
        graph, "BFS", BFSMaxFlow, source, sink
    )

    # Run and visualize DFS algorithm
    dfs_flow, dfs_paths, dfs_residuals, dfs_metrics = run_algorithm_visualization(
        graph, "DFS", DFSMaxFlow, source, sink
    )

    print("\nAll visualizations have been saved to the 'output' directory:")
    print("- output/initial_graph.png: Initial state of the graph")
    print("- output/bfs_flow.gif: BFS algorithm animation")
    print("- output/bfs_final_state.png: BFS final state")
    print("- output/dfs_flow.gif: DFS algorithm animation")
    print("- output/dfs_final_state.png: DFS final state")

    # Compare results
    print("\nAlgorithm Comparison:")
    print(f"BFS Maximum Flow: {bfs_flow}")
    print(f"DFS Maximum Flow: {dfs_flow}")
    print(f"Number of paths (BFS): {len(bfs_paths)}")
    print(f"Number of paths (DFS): {len(dfs_paths)}")


if __name__ == "__main__":
    main()
