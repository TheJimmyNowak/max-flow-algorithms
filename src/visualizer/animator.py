import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Dict, Tuple, Optional
import numpy as np
from ..utils.metrics import AlgorithmMetrics

class MaxFlowAnimator:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.pos = nx.spring_layout(graph)
        self.edge_colors = []
        self.node_colors = []
        self.edge_labels = {}
        self.node_labels = {}
        
        # Set up the plot
        self.setup_plot()
    
    def setup_plot(self) -> None:
        """Set up the initial plot with graph layout."""
        # Clear the plot
        self.ax.clear()
        
        # Draw edges
        nx.draw_networkx_edges(
            self.graph,
            self.pos,
            ax=self.ax,
            edge_color='gray',
            arrows=True,
            arrowsize=20
        )
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph,
            self.pos,
            ax=self.ax,
            node_color='lightblue',
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
        self.ax.set_title("Maximum Flow Visualization", pad=20)
        self.ax.axis('off')
    
    def update_edge_colors(self, path: Optional[List[int]] = None) -> None:
        """
        Update edge colors based on current path and residual capacities.
        
        Args:
            path: Current augmenting path if any
        """
        self.edge_colors = []
        for u, v in self.graph.edges():
            if path and (u, v) in zip(path[:-1], path[1:]):
                self.edge_colors.append('red')  # Highlight current path
            else:
                self.edge_colors.append('gray')
    
    def update_node_colors(self, path: Optional[List[int]] = None) -> None:
        """
        Update node colors based on current path and node types.
        
        Args:
            path: Current augmenting path if any
        """
        self.node_colors = []
        for node in self.graph.nodes():
            if path and node in path:
                self.node_colors.append('red')  # Highlight current path
            elif self.graph.nodes[node].get('type') == 'source':
                self.node_colors.append('green')
            elif self.graph.nodes[node].get('type') == 'sink':
                self.node_colors.append('red')
            else:
                self.node_colors.append('lightblue')
    
    def update_edge_labels(self, residual_graph: nx.DiGraph) -> None:
        """
        Update edge labels with current flow and capacity.
        
        Args:
            residual_graph: Residual graph with current capacities
        """
        self.edge_labels = {}
        for u, v in self.graph.edges():
            flow = self.graph[u][v]['capacity'] - residual_graph[u][v]['capacity']
            capacity = self.graph[u][v]['capacity']
            self.edge_labels[(u, v)] = f'{flow}/{capacity}'
    
    def create_animation(
        self,
        paths: List[List[int]],
        residuals: List[nx.DiGraph],
        metrics: List[AlgorithmMetrics]
    ) -> FuncAnimation:
        """
        Create an animation showing the flow of the algorithm.
        
        Args:
            paths: List of augmenting paths found
            residuals: List of residual graphs at each step
            metrics: List of metrics at each step
            
        Returns:
            matplotlib.animation.FuncAnimation: The animation object
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Calculate node positions once and reuse them
        pos = nx.spring_layout(self.graph)
        
        def update(frame):
            ax.clear()
            current_graph = residuals[frame]
            current_metrics = metrics[frame]
            
            # Draw edges with different styles based on flow
            edge_styles = []
            for u, v in current_graph.edges():
                # Get original capacity from the graph
                original_capacity = current_graph[u][v].get('original_capacity', current_graph[u][v]['capacity'])
                current_capacity = current_graph[u][v]['capacity']
                
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
            for (u, v), style in zip(current_graph.edges(), edge_styles):
                nx.draw_networkx_edges(current_graph, pos, edgelist=[(u, v)], edge_color='black',
                                     arrows=True, arrowsize=20, style=style,
                                     connectionstyle="arc3,rad=0")
            
            # Draw nodes with different colors based on type and current path
            node_colors = []
            for node in current_graph.nodes():
                if node in paths[frame]:
                    # Node is in current path
                    node_colors.append('yellow')  # Highlight current path
                elif current_graph.nodes[node].get('type') == 'source':
                    node_colors.append('green')
                elif current_graph.nodes[node].get('type') == 'sink':
                    node_colors.append('red')
                else:
                    node_colors.append('lightblue')
            
            # Draw nodes with larger size to ensure labels are visible
            nx.draw_networkx_nodes(current_graph, pos, node_color=node_colors, node_size=500)
            
            # Draw node labels
            nx.draw_networkx_labels(current_graph, pos, font_size=10, font_weight='bold')
            
            # Draw edge labels
            edge_labels = {}
            for u, v in current_graph.edges():
                original_capacity = current_graph[u][v].get('original_capacity', current_graph[u][v]['capacity'])
                current_capacity = current_graph[u][v]['capacity']
                flow = original_capacity - current_capacity
                edge_labels[(u, v)] = f"{flow}/{original_capacity}"
            
            nx.draw_networkx_edge_labels(current_graph, pos, edge_labels=edge_labels)
            
            # Add source and sink labels with background
            for node, attr in current_graph.nodes(data=True):
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
            
            # Add metrics information
            metrics_dict = current_metrics.to_dict()
            metrics_text = f"Step {frame + 1}/{len(paths)}\n"
            metrics_text += f"Total Flow: {metrics_dict['total_flow']:.1f}\n"
            metrics_text += f"Paths Found: {metrics_dict['paths_found']}\n"
            metrics_text += f"Path: {' -> '.join(map(str, paths[frame]))}"
            
            plt.text(0.02, 0.98, metrics_text, transform=ax.transAxes,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.title("Maximum Flow Algorithm Progress", pad=20)
            plt.axis('off')
        
        return FuncAnimation(fig, update, frames=len(paths), interval=2000, repeat=False)
    
    def show(self) -> None:
        """Display the current state of the visualization."""
        plt.show()
