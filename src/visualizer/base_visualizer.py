#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, Tuple, List, Optional

class BaseGraphVisualizer:
    """Base class for graph visualization that handles common drawing logic."""
    
    def __init__(self, graph: nx.DiGraph):
        """
        Initialize the visualizer with a graph.
        
        Args:
            graph: NetworkX directed graph to visualize
        """
        self.graph = graph
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        
        # Calculate and store graph layout
        is_planar, _ = nx.check_planarity(graph)
        self.pos = nx.planar_layout(graph) if is_planar else nx.spring_layout(graph)
        
        # Initialize visualization attributes
        self.edge_colors: List[str] = []
        self.edge_styles: List[str] = []
        self.edge_labels: Dict[Tuple[int, int], str] = {}
        self.node_colors: List[str] = []
    
    def prepare_edge_attributes(self, path: Optional[List[int]] = None, show_flow: bool = False) -> None:
        """
        Prepare edge colors, styles, and labels.
        
        Args:
            path: Optional path to highlight
            show_flow: Whether to show flow values
        """
        self.edge_colors = []
        self.edge_styles = []
        self.edge_labels = {}
        
        for u, v in self.graph.edges():
            if show_flow:
                # Get original capacity from the graph
                original_capacity = self.graph[u][v].get('original_capacity', self.graph[u][v]['capacity'])
                current_capacity = self.graph[u][v]['capacity']
                flow = original_capacity - current_capacity
                
                if current_capacity < original_capacity:
                    # Edge has flow
                    self.edge_colors.append('yellow')
                    self.edge_styles.append('solid')
                    self.edge_labels[(u, v)] = f"{flow:.1f}"
                else:
                    # No flow
                    self.edge_colors.append('black')
                    self.edge_styles.append('dashed')
            else:
                # If path is provided, highlight edges in the path
                if path and (u, v) in zip(path[:-1], path[1:]):
                    self.edge_colors.append('red')
                else:
                    self.edge_colors.append('black')
                self.edge_styles.append('solid')
    
    def update_node_colors(self, path: Optional[List[int]] = None) -> None:
        """
        Prepare node colors.
        
        Args:
            path: Optional path to highlight
        """
        self.node_colors = []
        for node in self.graph.nodes():
            if path and node in path:
                self.node_colors.append('red')
            elif self.graph.nodes[node].get('type') == 'source':
                self.node_colors.append('green')
            elif self.graph.nodes[node].get('type') == 'sink':
                self.node_colors.append('red')
            else:
                self.node_colors.append('lightblue')
    
    def draw_graph(self, title: str = "Maximum Flow Graph") -> None:
        """
        Draw the graph with current attributes.
        
        Args:
            title: Title for the graph
        """
        self.ax.clear()
        
        # Draw edges
        for (u, v), color, style in zip(self.graph.edges(), self.edge_colors, self.edge_styles):
            nx.draw_networkx_edges(
                self.graph, self.pos,
                edgelist=[(u, v)],
                edge_color=color,
                arrows=color == 'yellow' or color == 'red',
                arrowsize=20,
                style=style,
                connectionstyle="arc3,rad=0",
                width=2 if color in ['yellow', 'red'] else 1,
                ax=self.ax
            )
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph,
            self.pos,
            node_color=self.node_colors,
            node_size=500,
            ax=self.ax
        )
        
        # Draw node labels
        nx.draw_networkx_labels(
            self.graph,
            self.pos,
            font_size=10,
            font_weight='bold',
            ax=self.ax
        )
        
        # Draw edge labels if they exist
        if self.edge_labels:
            nx.draw_networkx_edge_labels(
                self.graph,
                self.pos,
                edge_labels=self.edge_labels,
                font_size=8,
                ax=self.ax
            )
        
        # Add source and sink labels
        for node, attr in self.graph.nodes(data=True):
            if attr.get('type') == 'source':
                plt.annotate('Source', xy=self.pos[node], xytext=(0, 30),
                           textcoords='offset points', ha='center', va='bottom',
                           fontsize=12, fontweight='bold', color='green',
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
            elif attr.get('type') == 'sink':
                plt.annotate('Sink', xy=self.pos[node], xytext=(0, -30),
                           textcoords='offset points', ha='center', va='top',
                           fontsize=12, fontweight='bold', color='red',
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        self.ax.set_title(title, pad=20)
        self.ax.axis('off')
    
    def save(self, filename: str) -> None:
        """
        Save the current visualization to a file.
        
        Args:
            filename: Output filename
        """
        plt.savefig(filename, bbox_inches='tight', dpi=300)
    
    def close(self) -> None:
        """Close the current figure."""
        plt.close(self.fig) 