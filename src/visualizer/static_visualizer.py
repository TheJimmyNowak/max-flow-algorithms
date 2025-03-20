#!/usr/bin/env python3

import networkx as nx
from .base_visualizer import BaseGraphVisualizer


class StaticGraphVisualizer(BaseGraphVisualizer):
    """Static visualizer for maximum flow graphs."""

    def __init__(self, graph: nx.DiGraph):
        super().__init__(graph)

    def visualize(self, title: str = "Maximum Flow Graph", show_flow: bool = False) -> None:
        """
        Create a static visualization of the graph.

        Args:
            title: Title for the graph
            show_flow: Whether to show flow values
        """
        self.prepare_edge_attributes(show_flow=show_flow)
        self.update_node_colors()
        self.draw_graph(title)


def save_graph_visualization(
    graph: nx.DiGraph, filename: str, title: str = "Maximum Flow Graph", show_flow: bool = False
) -> None:
    """
    Save a static visualization of the graph.

    Args:
        graph: NetworkX graph to visualize
        filename: Output filename
        title: Title for the graph
        show_flow: Whether to show flow values
    """
    visualizer = StaticGraphVisualizer(graph)
    visualizer.visualize(title, show_flow)
    visualizer.save(filename)
    visualizer.close()
