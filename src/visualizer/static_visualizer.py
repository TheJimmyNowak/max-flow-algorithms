#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
import os

def save_graph_visualization(graph: nx.DiGraph, filename: str, title: str = "Graph Visualization", show_flow: bool = False):
    """
    Save a static visualization of the graph.
    
    Args:
        graph: NetworkX directed graph
        filename: Output filename
        title: Graph title
        show_flow: If True, show flow direction in final graph
    """
    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create full path for the file
    filepath = os.path.join(output_dir, filename)
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    
    # Draw edges with different styles based on flow
    if show_flow:
        # For final graphs, show flow direction using line styles
        edge_styles = []
        for u, v in graph.edges():
            # Get original capacity from the graph
            original_capacity = graph[u][v].get('original_capacity', graph[u][v]['capacity'])
            current_capacity = graph[u][v]['capacity']
            
            if current_capacity < original_capacity:
                # Edge has flow
                if current_capacity > 0:
                    # Partial flow
                    edge_styles.append('solid')
                else:
                    # Full flow
                    edge_styles.append('solid')
            else:
                # No flow
                edge_styles.append('dashed')
        
        # Draw edges with different styles
        for (u, v), style in zip(graph.edges(), edge_styles):
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='black',
                                 arrows=True, arrowsize=20, style=style,
                                 connectionstyle="arc3,rad=0")
    else:
        # For initial graph, use default style
        nx.draw_networkx_edges(graph, pos, edge_color='black', arrows=True, arrowsize=20,
                             connectionstyle="arc3,rad=0")
    
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
    
    # Draw edge labels
    if show_flow:
        # For final graphs, show both capacity and flow
        edge_labels = {}
        for u, v in graph.edges():
            original_capacity = graph[u][v].get('original_capacity', graph[u][v]['capacity'])
            current_capacity = graph[u][v]['capacity']
            flow = original_capacity - current_capacity
            edge_labels[(u, v)] = f"{flow}/{original_capacity}"
    else:
        # For initial graph, show only capacity
        edge_labels = nx.get_edge_attributes(graph, 'capacity')
    
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    # Add source and sink labels
    for node, attr in graph.nodes(data=True):
        if attr.get('type') == 'source':
            # Add "Source" label above the node
            plt.annotate('Source', xy=pos[node], xytext=(0, 0.2), 
                        textcoords='offset points', ha='center', va='bottom',
                        fontsize=12, fontweight='bold', color='green')
        elif attr.get('type') == 'sink':
            # Add "Sink" label below the node
            plt.annotate('Sink', xy=pos[node], xytext=(0, -0.2), 
                        textcoords='offset points', ha='center', va='top',
                        fontsize=12, fontweight='bold', color='red')
    
    plt.title(title, pad=20)
    plt.axis('off')
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close() 