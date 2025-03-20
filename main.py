#!/usr/bin/env python3

import networkx as nx
import os
from src.graph.examples import create_example_graph, create_random_graph
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow
from src.visualizer.static_visualizer import save_graph_visualization
from src.visualizer.algorithm_visualizer import run_algorithm_visualization

def main():
    # Create both example and random graphs
    example_graph = create_example_graph()
    random_graph = create_random_graph()
    
    # For demonstration, we'll use the example graph
    graph = example_graph
    
    # Get source and sink nodes
    source = next(node for node, attr in graph.nodes(data=True) 
                 if attr.get('type') == 'source')
    sink = next(node for node, attr in graph.nodes(data=True) 
               if attr.get('type') == 'sink')
    
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
    save_graph_visualization(graph, 'initial_graph.png', "Initial Graph State")
    
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
    print("- output/bfs_final_graph.png: BFS final state")
    print("- output/dfs_flow.gif: DFS algorithm animation")
    print("- output/dfs_final_graph.png: DFS final state")
    
    # Compare results
    print("\nAlgorithm Comparison:")
    print(f"BFS Maximum Flow: {bfs_flow}")
    print(f"DFS Maximum Flow: {dfs_flow}")
    print(f"Number of paths (BFS): {len(bfs_paths)}")
    print(f"Number of paths (DFS): {len(dfs_paths)}")

if __name__ == "__main__":
    main() 