import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Dict, Tuple, Optional
import numpy as np

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
        residual_graphs: List[nx.DiGraph],
        metrics: List[Dict]
    ) -> FuncAnimation:
        """
        Create animation of the max flow algorithm.
        
        Args:
            paths: List of augmenting paths found
            residual_graphs: List of residual graphs at each step
            metrics: List of metrics at each step
            
        Returns:
            Matplotlib animation object
        """
        def update(frame):
            self.ax.clear()
            
            # Update colors and labels
            self.update_edge_colors(paths[frame] if frame < len(paths) else None)
            self.update_node_colors(paths[frame] if frame < len(paths) else None)
            self.update_edge_labels(residual_graphs[frame])
            
            # Draw the graph
            nx.draw_networkx_edges(
                self.graph,
                self.pos,
                ax=self.ax,
                edge_color=self.edge_colors,
                arrows=True,
                arrowsize=20
            )
            
            nx.draw_networkx_nodes(
                self.graph,
                self.pos,
                ax=self.ax,
                node_color=self.node_colors,
                node_size=500
            )
            
            nx.draw_networkx_labels(
                self.graph,
                self.pos,
                ax=self.ax,
                font_size=10,
                font_weight='bold'
            )
            
            nx.draw_networkx_edge_labels(
                self.graph,
                self.pos,
                edge_labels=self.edge_labels,
                ax=self.ax,
                font_size=8
            )
            
            # Update title with metrics
            metric = metrics[frame]
            title = f"Step {frame + 1}/{len(paths)}\n"
            title += f"Total Flow: {metric['total_flow']:.2f}\n"
            title += f"Paths Found: {metric['paths_found']}"
            self.ax.set_title(title, pad=20)
            
            self.ax.axis('off')
        
        # Create animation
        anim = FuncAnimation(
            self.fig,
            update,
            frames=len(paths),
            interval=1000,  # 1 second per frame
            repeat=False
        )
        
        return anim
    
    def show(self) -> None:
        """Display the current state of the visualization."""
        plt.show()
