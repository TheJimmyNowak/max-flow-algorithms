#!/usr/bin/env python3

"""Static visualizer for maximum flow graphs."""

from typing import Optional, List
import networkx as nx
from .base_visualizer import BaseGraphVisualizer
import matplotlib.pyplot as plt


class StaticGraphVisualizer(BaseGraphVisualizer):
    """Static visualizer for maximum flow graphs."""

    def __init__(self, graph: nx.DiGraph):
        """
        Initialize the static visualizer.

        Args:
            graph: NetworkX directed graph to visualize
        """
        super().__init__(graph)

    def visualize(
        self,
        title: str = "Maximum Flow Graph",
        show_flow: bool = False,
        path: Optional[List[int]] = None,
        residual_graph: Optional[nx.DiGraph] = None
    ) -> None:
        """
        Create a static visualization of the graph.

        Args:
            title: Title for the graph
            show_flow: Whether to show flow values
            path: Current augmenting path if any
            residual_graph: Residual graph for flow visualization
        """
        self._prepare_edge_attributes(path, show_flow, residual_graph)
        self._update_node_colors(path)
        self._draw_graph(title)
        self._update_legend()

    def save(self, filename: str) -> None:
        """
        Save the current visualization to a file.

        Args:
            filename: Output filename
        """
        plt.savefig(filename, bbox_inches='tight', dpi=300)


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
