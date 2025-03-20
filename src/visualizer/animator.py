import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Dict, Tuple, Optional
from src.utils.metrics import AlgorithmMetrics
from .base_visualizer import BaseGraphVisualizer


class MaxFlowAnimator(BaseGraphVisualizer):
    """Animator for maximum flow algorithm visualization."""
    
    def __init__(self, graph: nx.DiGraph):
        super().__init__(graph)
        self.graph = graph
        self.fig, self.ax = plt.subplots(figsize=(12, 8))

        # Set up the plot
        self.setup_plot()

    def setup_plot(self) -> None:
        """Set up the initial plot with graph layout."""
        # Clear the plot
        self.ax.clear()

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

    def update_edge_labels(self, residual_graph: nx.DiGraph) -> None:
        """
        Update edge labels with current flow and capacity.
        
        Args:
            residual_graph: Residual graph with current capacities
        """
        self.edge_labels = {}
        for u, v in self.graph.edges():
            flow = self.graph[u][v]['capacity'] - residual_graph[u][v]['capacity']
            self.edge_labels[(u, v)] = f'{flow:.1f}'

    def create_animation(
            self,
            paths: List[List[int]],
            residual_graphs: List[nx.DiGraph],
            metrics: List[AlgorithmMetrics]
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
        def update(frame: int) -> None:
            # Update graph attributes for current frame
            current_path = paths[frame] if frame < len(paths) else None
            current_graph = residual_graphs[frame]
            
            # Store original capacities in the current graph for visualization
            for u, v in self.graph.edges():
                if (u, v) in current_graph.edges():
                    current_graph[u][v]['original_capacity'] = self.graph[u][v]['capacity']
                if (v, u) in current_graph.edges():
                    current_graph[v][u]['original_capacity'] = 0  # Reverse edges start with 0 capacity
            
            # Update visualization attributes
            self.prepare_edge_attributes(path=current_path, show_flow=True)
            self.update_node_colors(path=current_path)
            
            # Update metrics in title
            metric = metrics[frame].to_dict()
            title = f"Step {frame + 1}/{len(paths)}\n"
            title += f"Path: {' -> '.join(map(str, paths[frame]))}\n"
            title += f"Flow: {metric['total_flow']:.2f}\n"
            title += f"Paths Found: {metric['paths_found']}"
            
            # Draw the graph
            self.draw_graph(title)
        
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
