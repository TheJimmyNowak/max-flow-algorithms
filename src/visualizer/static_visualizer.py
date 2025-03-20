#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx

def save_graph_visualization(graph: nx.DiGraph, filename: str, show_flow: bool = False) -> None:
    """
    Save a static visualization of the graph.
    
    Args:
        graph: NetworkX graph to visualize
        filename: Output filename
        show_flow: Whether to show flow direction and values
    """
    plt.figure(figsize=(12, 8))
    
    # Check if graph is planar
    is_planar, _ = nx.check_planarity(graph)
    
    if is_planar:
        # Use planar layout for planar graphs
        pos = nx.planar_layout(graph)
    else:
        # Use spring layout for non-planar graphs
        pos = nx.spring_layout(graph)
    
    # Draw edges with different styles based on flow
    edge_styles = []
    for u, v in graph.edges():
        if show_flow:
            # Get original capacity from the graph
            original_capacity = graph[u][v].get('original_capacity', graph[u][v]['capacity'])
            current_capacity = graph[u][v]['capacity']
            flow = original_capacity - current_capacity
            
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
        else:
            edge_styles.append('solid')
    
    # Draw edges with different styles
    for (u, v), style in zip(graph.edges(), edge_styles):
        # Only draw arrow if there is flow in that direction
        if show_flow:
            original_capacity = graph[u][v].get('original_capacity', graph[u][v]['capacity'])
            current_capacity = graph[u][v]['capacity']
            flow = original_capacity - current_capacity
            
            if current_capacity < original_capacity:
                # Draw yellow arrow and line for edges with flow
                nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='yellow',
                                     arrows=True, arrowsize=20, style=style,
                                     connectionstyle="arc3,rad=0", width=2)
            else:
                # Draw edge without arrow if no flow
                nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='black',
                                     arrows=False, style=style,
                                     connectionstyle="arc3,rad=0", width=1)
        else:
            # For initial graph, show all arrows
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='black',
                                 arrows=True, arrowsize=20, style=style,
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
    
    # Draw nodes with larger size to ensure labels are visible
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=500)
    
    # Draw node labels
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold')
    
    # Draw edge labels if showing flow
    if show_flow:
        edge_labels = {}
        for u, v in graph.edges():
            original_capacity = graph[u][v].get('original_capacity', graph[u][v]['capacity'])
            current_capacity = graph[u][v]['capacity']
            flow = original_capacity - current_capacity
            edge_labels[(u, v)] = f"{flow:.1f}"  # Only show flow value
        
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    # Add source and sink labels with background
    for node, attr in graph.nodes(data=True):
        if attr.get('type') == 'source':
            # Add "Source" label above the node with white background
            plt.annotate('Source', xy=pos[node], xytext=(0, 30), 
                       textcoords='offset points', ha='center', va='bottom',
                       fontsize=12, fontweight='bold', color='green',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        elif attr.get('type') == 'sink':
            # Add "Sink" label below the node with white background
            plt.annotate('Sink', xy=pos[node], xytext=(0, -30), 
                       textcoords='offset points', ha='center', va='top',
                       fontsize=12, fontweight='bold', color='red',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    plt.title("Maximum Flow Graph", pad=20)
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close() 