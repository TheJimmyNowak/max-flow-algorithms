#!/usr/bin/env python3

"""Research script for comparing BFS and DFS algorithms performance."""

import time
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from src.graph.generator import GraphGenerator
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow
import networkx as nx


def measure_algorithm_metrics(
    algorithm_class: type,
    graph: nx.DiGraph,
    source: int,
    sink: int
) -> Tuple[float, int]:
    """
    Get metrics from algorithm execution.

    Args:
        algorithm_class: Algorithm class to use
        graph: Input graph
        source: Source node
        sink: Sink node

    Returns:
        Tuple containing:
        - Execution time in seconds
        - Number of steps taken
    """
    algorithm = algorithm_class(graph)
    algorithm.compute_max_flow(source, sink)
    metrics = algorithm.get_metrics()
    # Clean up to free memory
    algorithm.residual_graph.clear()
    del algorithm
    return metrics.execution_time, metrics.steps_count


def run_vertices_experiment(
    num_vertices_range: List[int],
    num_edges: int,
    num_sources: int,
    num_sinks: int,
    num_trials: int = 5
) -> Tuple[List[float], List[float], List[float], List[float]]:
    """
    Run experiment with varying number of vertices.

    Args:
        num_vertices_range: List of numbers of vertices to test
        num_edges: Base number of edges (will be adjusted based on vertices)
        num_sources: Number of source nodes
        num_sinks: Number of sink nodes
        num_trials: Number of trials for each configuration

    Returns:
        Tuple containing:
        - BFS execution times
        - DFS execution times
        - BFS steps counts
        - DFS steps counts
    """
    generator = GraphGenerator()
    bfs_times = []
    dfs_times = []
    bfs_steps = []
    dfs_steps = []

    for num_vertices in num_vertices_range:
        print(f"Testing with {num_vertices} vertices...")
        bfs_trial_times = []
        dfs_trial_times = []
        bfs_trial_steps = []
        dfs_trial_steps = []

        # Calculate maximum possible edges for this number of vertices
        max_possible_edges = num_vertices * (num_vertices - 1)
        # Use either the requested number of edges or 20% of max possible edges, whichever is smaller
        actual_edges = min(num_edges, max_possible_edges // 5)

        for _ in range(num_trials):
            graph = generator.generate_random_graph(
                num_nodes=num_vertices,
                num_edges=actual_edges,
                num_sources=num_sources,
                num_sinks=num_sinks
            )
            source = generator.get_sources()[0]
            sink = generator.get_sinks()[0]

            bfs_time, bfs_step = measure_algorithm_metrics(BFSMaxFlow, graph, source, sink)
            dfs_time, dfs_step = measure_algorithm_metrics(DFSMaxFlow, graph, source, sink)

            bfs_trial_times.append(bfs_time)
            dfs_trial_times.append(dfs_time)
            bfs_trial_steps.append(bfs_step)
            dfs_trial_steps.append(dfs_step)

        bfs_times.append(np.mean(bfs_trial_times))
        dfs_times.append(np.mean(dfs_trial_times))
        bfs_steps.append(np.mean(bfs_trial_steps))
        dfs_steps.append(np.mean(dfs_trial_steps))

    return bfs_times, dfs_times, bfs_steps, dfs_steps


def run_edges_experiment(
    num_vertices: int,
    num_edges_range: List[int],
    num_sources: int,
    num_sinks: int,
    num_trials: int = 5
) -> Tuple[List[float], List[float], List[float], List[float]]:
    """
    Run experiment with varying number of edges.

    Args:
        num_vertices: Number of vertices
        num_edges_range: List of numbers of edges to test
        num_sources: Number of source nodes
        num_sinks: Number of sink nodes
        num_trials: Number of trials for each configuration

    Returns:
        Tuple containing:
        - BFS execution times
        - DFS execution times
        - BFS steps counts
        - DFS steps counts
    """
    generator = GraphGenerator()
    bfs_times = []
    dfs_times = []
    bfs_steps = []
    dfs_steps = []

    for num_edges in num_edges_range:
        print(f"Testing with {num_edges} edges...")
        bfs_trial_times = []
        dfs_trial_times = []
        bfs_trial_steps = []
        dfs_trial_steps = []

        for _ in range(num_trials):
            graph = generator.generate_random_graph(
                num_nodes=num_vertices,
                num_edges=num_edges,
                num_sources=num_sources,
                num_sinks=num_sinks
            )
            source = generator.get_sources()[0]
            sink = generator.get_sinks()[0]

            bfs_time, bfs_step = measure_algorithm_metrics(BFSMaxFlow, graph, source, sink)
            dfs_time, dfs_step = measure_algorithm_metrics(DFSMaxFlow, graph, source, sink)

            bfs_trial_times.append(bfs_time)
            dfs_trial_times.append(dfs_time)
            bfs_trial_steps.append(bfs_step)
            dfs_trial_steps.append(dfs_step)

        bfs_times.append(np.mean(bfs_trial_times))
        dfs_times.append(np.mean(dfs_trial_times))
        bfs_steps.append(np.mean(bfs_trial_steps))
        dfs_steps.append(np.mean(dfs_trial_steps))

    return bfs_times, dfs_times, bfs_steps, dfs_steps


def run_capacity_experiment(
    num_vertices: int,
    num_edges: int,
    num_sources: int,
    num_sinks: int,
    capacity_ranges: List[Tuple[float, float]],
    num_trials: int = 5
) -> Tuple[List[float], List[float], List[float], List[float]]:
    """
    Run experiment with varying edge capacity ranges.

    Args:
        num_vertices: Number of vertices
        num_edges: Number of edges
        num_sources: Number of source nodes
        num_sinks: Number of sink nodes
        capacity_ranges: List of (min_capacity, max_capacity) tuples
        num_trials: Number of trials for each configuration

    Returns:
        Tuple containing:
        - BFS execution times
        - DFS execution times
        - BFS steps counts
        - DFS steps counts
    """
    generator = GraphGenerator()
    bfs_times = []
    dfs_times = []
    bfs_steps = []
    dfs_steps = []

    for min_cap, max_cap in capacity_ranges:
        print(f"Testing with capacity range [{min_cap}, {max_cap}]...")
        bfs_trial_times = []
        dfs_trial_times = []
        bfs_trial_steps = []
        dfs_trial_steps = []

        for _ in range(num_trials):
            graph = generator.generate_random_graph(
                num_nodes=num_vertices,
                num_edges=num_edges,
                num_sources=num_sources,
                num_sinks=num_sinks,
                min_capacity=min_cap,
                max_capacity=max_cap
            )
            source = generator.get_sources()[0]
            sink = generator.get_sinks()[0]

            bfs_time, bfs_step = measure_algorithm_metrics(BFSMaxFlow, graph, source, sink)
            dfs_time, dfs_step = measure_algorithm_metrics(DFSMaxFlow, graph, source, sink)

            bfs_trial_times.append(bfs_time)
            dfs_trial_times.append(dfs_time)
            bfs_trial_steps.append(bfs_step)
            dfs_trial_steps.append(dfs_step)

        bfs_times.append(np.mean(bfs_trial_times))
        dfs_times.append(np.mean(dfs_trial_times))
        bfs_steps.append(np.mean(bfs_trial_steps))
        dfs_steps.append(np.mean(dfs_trial_steps))

    return bfs_times, dfs_times, bfs_steps, dfs_steps


def plot_results(
    x_values: List[float],
    bfs_times: List[float],
    dfs_times: List[float],
    bfs_steps: List[float],
    dfs_steps: List[float],
    x_label: str,
    title_prefix: str,
    filename_prefix: str
) -> None:
    """
    Plot and save results for both time and steps.

    Args:
        x_values: Values for x-axis
        bfs_times: BFS execution times
        dfs_times: DFS execution times
        bfs_steps: BFS step counts
        dfs_steps: DFS step counts
        x_label: Label for x-axis
        title_prefix: Prefix for plot titles
        filename_prefix: Prefix for output filenames
    """
    # Plot execution times
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, bfs_times, 'b-o', label='BFS')
    plt.plot(x_values, dfs_times, 'r-o', label='DFS')
    plt.xlabel(x_label)
    plt.ylabel('Execution Time (seconds)')
    plt.title(f'{title_prefix} - Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'output/{filename_prefix}_time.png')
    plt.close()

    # Plot steps
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, bfs_steps, 'b-o', label='BFS')
    plt.plot(x_values, dfs_steps, 'r-o', label='DFS')
    plt.xlabel(x_label)
    plt.ylabel('Number of Steps')
    plt.title(f'{title_prefix} - Steps Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'output/{filename_prefix}_steps.png')
    plt.close()


def main() -> None:
    """Run all experiments and generate plots."""
    # Experiment 1: Varying number of vertices
    num_vertices_range = range(10, 800, 10)
    bfs_times, dfs_times, bfs_steps, dfs_steps = run_vertices_experiment(
        num_vertices_range=num_vertices_range,
        num_edges=50,  # Smaller number of edges for smaller graphs
        num_sources=1,
        num_sinks=1,
        num_trials=3  # Reduce number of trials to save memory
    )
    plot_results(
        num_vertices_range,
        bfs_times,
        dfs_times,
        bfs_steps,
        dfs_steps,
        'Number of Vertices',
        'Execution Time vs Number of Vertices',
        'vertices_comparison'
    )

    # Experiment 2: Varying number of edges
    num_edges_range = range(10, 600, 10)
    bfs_times, dfs_times, bfs_steps, dfs_steps = run_edges_experiment(
        num_vertices=200,  # Smaller number of vertices for edge experiment
        num_edges_range=num_edges_range,
        num_sources=1,
        num_sinks=1,
        num_trials=3  # Reduce number of trials to save memory
    )
    plot_results(
        num_edges_range,
        bfs_times,
        dfs_times,
        bfs_steps,
        dfs_steps,
        'Number of Edges',
        'Execution Time vs Number of Edges',
        'edges_comparison'
    )

    # Experiment 3: Varying edge capacity ranges
    capacity_ranges = [
        (1, i) for i in range(1, 1000, 10)
    ]
    bfs_times, dfs_times, bfs_steps, dfs_steps = run_capacity_experiment(
        num_vertices=200,  # Smaller number of vertices for capacity experiment
        num_edges=200,     # Smaller number of edges for capacity experiment
        num_sources=1,
        num_sinks=1,
        capacity_ranges=capacity_ranges,
        num_trials=3  # Reduce number of trials to save memory
    )
    x_values = [max_cap - min_cap for min_cap, max_cap in capacity_ranges]
    plot_results(
        x_values,
        bfs_times,
        dfs_times,
        bfs_steps,
        dfs_steps,
        'Edge Capacity Range',
        'Execution Time vs Edge Capacity Range',
        'capacity_comparison'
    )


if __name__ == "__main__":
    main() 