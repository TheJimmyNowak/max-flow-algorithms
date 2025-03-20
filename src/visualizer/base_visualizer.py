#!/usr/bin/env python3

"""Base class for graph visualization with common functionality."""

import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Optional, Tuple, Dict
from matplotlib.collections import LineCollection
from matplotlib.patches import FancyArrowPatch


class BaseGraphVisualizer:
    """Base class for graph visualization with common functionality."""

    def __init__(self, graph: nx.DiGraph):
        """
        Initialize the visualizer.

        Args:
            graph: NetworkX directed graph to visualize
        """
        self.graph = graph
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.pos = self._calculate_layout()
        self.edge_colors = []
        self.edge_labels = {}
        self.node_colors = []
        self.legend_handles = []

    def _calculate_layout(self) -> Dict[int, Tuple[float, float]]:
        """
        Calculate the layout for the graph.

        Returns:
            Dictionary mapping nodes to their positions
        """
        # Try planar layout first
        try:
            pos = nx.planar_layout(self.graph)
        except nx.NetworkXException:
            # If not planar, try spring layout with better parameters
            pos = nx.spring_layout(
                self.graph,
                k=2.0,  # Optimal distance between nodes
                iterations=50,  # More iterations for better layout
                seed=42  # For consistent layout
            )
        return pos

    def _prepare_edge_attributes(
        self,
        path: Optional[List[int]] = None,
        show_flow: bool = False,
        residual_graph: Optional[nx.DiGraph] = None
    ) -> None:
        """
        Prepare edge attributes for visualization.

        Args:
            path: Current augmenting path if any
            show_flow: Whether to show flow values
            residual_graph: Residual graph for flow visualization
        """
        self.edge_colors = []
        self.edge_labels = {}

        for u, v in self.graph.edges():
            # Set edge color based on path
            if path and (u, v) in zip(path[:-1], path[1:]):
                self.edge_colors.append('red')  # Highlight current path
            else:
                self.edge_colors.append('gray')

            # Set edge label
            if show_flow and residual_graph:
                flow = self.graph[u][v]['capacity'] - residual_graph[u][v]['capacity']
                self.edge_labels[(u, v)] = f'{flow:.1f}/{self.graph[u][v]["capacity"]:.1f}'
            else:
                self.edge_labels[(u, v)] = f'{self.graph[u][v]["capacity"]:.1f}'

    def _update_node_colors(self, path: Optional[List[int]] = None) -> None:
        """
        Update node colors based on current path.

        Args:
            path: Current augmenting path if any
        """
        self.node_colors = []
        for node in self.graph.nodes():
            if path and node in path:
                if node == path[0]:  # Source
                    self.node_colors.append('lightgreen')
                elif node == path[-1]:  # Sink
                    self.node_colors.append('lightcoral')
                else:  # Path nodes
                    self.node_colors.append('lightyellow')
            else:
                if node == self.graph.nodes[node].get('type') == 'source':
                    self.node_colors.append('lightgreen')
                elif node == self.graph.nodes[node].get('type') == 'sink':
                    self.node_colors.append('lightcoral')
                else:
                    self.node_colors.append('lightblue')

    def _draw_graph(self, title: str = "Maximum Flow Graph") -> None:
        """
        Draw the graph with all attributes.

        Args:
            title: Title for the graph
        """
        # Clear the plot
        self.ax.clear()

        # Draw edges with arrows
        edges = self.graph.edges()
        for i, (u, v) in enumerate(edges):
            # Draw edge line

            # Draw arrow
            arrow = FancyArrowPatch(
                (self.pos[u][0], self.pos[u][1]),
                (self.pos[v][0], self.pos[v][1]),
                arrowstyle='->',
                color=self.edge_colors[i],
                linewidth=2
            )
            self.ax.add_patch(arrow)

            # Draw edge label
            mid_x = (self.pos[u][0] + self.pos[v][0]) / 2
            mid_y = (self.pos[u][1] + self.pos[v][1]) / 2
            self.ax.text(
                mid_x,
                mid_y,
                self.edge_labels[(u, v)],
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=8
            )

        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph,
            self.pos,
            ax=self.ax,
            node_color=self.node_colors,
            node_size=500
        )

        # Draw node labels
        nx.draw_networkx_labels(
            self.graph,
            self.pos,
            ax=self.ax,
            font_size=10,
            font_weight='bold'
        )

        # Set title and remove axes
        self.ax.set_title(title, pad=20)
        self.ax.axis('off')

    def _update_legend(self) -> None:
        """Update the legend with current flow information."""
        self.legend_handles = [
            plt.Line2D([0], [0], color='gray', label='Edge'),
            plt.Line2D([0], [0], color='red', label='Current Path'),
            plt.Line2D([0], [0], color='lightgreen', label='Source'),
            plt.Line2D([0], [0], color='lightcoral', label='Sink'),
            plt.Line2D([0], [0], color='lightyellow', label='Path Node')
        ]
        self.ax.legend(handles=self.legend_handles, loc='upper left')

    def close(self) -> None:
        """Close the figure."""
        plt.close(self.fig)
