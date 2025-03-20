#!/usr/bin/env python3

import networkx as nx
from .base_visualizer import BaseGraphVisualizer

def save_graph_visualization(graph: nx.DiGraph, filename: str, title: str = "Maximum Flow Graph", show_flow: bool = False) -> None:
    """
    Save a static visualization of the graph.
    
    Args:
        graph: NetworkX graph to visualize
        filename: Output filename
        title: Title for the graph
        show_flow: Whether to show flow values
    """
    visualizer = BaseGraphVisualizer(graph)
    visualizer.prepare_edge_attributes(show_flow=show_flow)
    visualizer.update_node_colors()
    visualizer.draw_graph(title)
    visualizer.save(filename)
    visualizer.close()