#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
from src.graph.input_handler import GraphInputHandler
from src.graph.generator import GraphGenerator
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow
from src.visualizer.animator import MaxFlowAnimator

def create_example_graph():
    """Create an example graph with known maximum flow."""
    handler = GraphInputHandler()
    
    # Add nodes
    handler.add_node(0, 'source')
    handler.add_node(1, 'intermediate')
    handler.add_node(2, 'intermediate')
    handler.add_node(3, 'sink')
    
    # Add edges with capacities
    handler.add_edge(0, 1, 10.0)  # source -> 1
    handler.add_edge(0, 2, 10.0)  # source -> 2
    handler.add_edge(1, 2, 2.0)   # 1 -> 2
    handler.add_edge(1, 3, 4.0)   # 1 -> sink
    handler.add_edge(2, 3, 9.0)   # 2 -> sink
    
    return handler.get_graph()

def create_random_graph():
    """Create a random graph for testing."""
    generator = GraphGenerator()
    return generator.generate_random_graph(
        num_nodes=6,
        num_edges=8,
        num_sources=1,
        num_sinks=1,
        min_capacity=1.0,
        max_capacity=10.0
    )

def save_graph_visualization(graph: nx.DiGraph, filename: str, title: str = "Graph Visualization"):
    """Save a static visualization of the graph."""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    
    # Draw edges
    nx.draw_networkx_edges(graph, pos, edge_color='gray', arrows=True, arrowsize=20)
    
    # Draw nodes with different colors based on type
    node_colors = []
    for node in graph.nodes():
        if graph.nodes[node].get('type') == 'source':
            node_colors.append('green')
        elif graph.nodes[node].get('type') == 'sink':
            node_colors.append('red')
        else:
            node_colors.append('lightblue')
    
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=500)
    
    # Draw labels
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'capacity'))
    
    plt.title(title, pad=20)
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

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
    
    # Run BFS max flow algorithm
    print("\nRunning BFS max flow algorithm...")
    bfs = BFSMaxFlow(graph)
    bfs_flow, bfs_paths, bfs_residuals, bfs_metrics = bfs.compute_max_flow_with_history(source, sink)
    print(f"BFS Maximum flow: {bfs_flow}")
    print(f"Number of augmenting paths found: {len(bfs_paths)}")
    print("\nAugmenting paths:")
    for i, path in enumerate(bfs_paths):
        print(f"Path {i + 1}: {path}")
    
    # Run DFS max flow algorithm
    print("\nRunning DFS max flow algorithm...")
    dfs = DFSMaxFlow(graph)
    dfs_flow = dfs.compute_max_flow(source, sink)
    print(f"DFS Maximum flow: {dfs_flow}")
    
    # Create and save animation
    print("\nCreating flow animation...")
    animator = MaxFlowAnimator(graph)
    animation = animator.create_animation(bfs_paths, bfs_residuals, bfs_metrics)
    
    # Save animation
    print("Saving animation to 'max_flow.gif'...")
    animation.save('max_flow.gif', writer='pillow', fps=1)
    
    # Save final state visualization
    print("Saving final state visualization...")
    final_graph = bfs_residuals[-1]
    save_graph_visualization(final_graph, 'final_graph.png', "Final Graph State")
    
    print("\nAll visualizations have been saved:")
    print("- initial_graph.png: Initial state of the graph")
    print("- max_flow.gif: Animation of the flow computation")
    print("- final_graph.png: Final state of the graph")

if __name__ == "__main__":
    main() 