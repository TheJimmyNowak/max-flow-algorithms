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

    def create_animation(
        self,
        paths: List[List[int]],
        residual_graphs: List[nx.DiGraph],
        metrics: List[AlgorithmMetrics],
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
                    current_graph[u][v]["original_capacity"] = self.graph[u][v]["capacity"]
                if (v, u) in current_graph.edges():
                    current_graph[v][u][
                        "original_capacity"
                    ] = 0  # Reverse edges start with 0 capacity

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
            self.fig, update, frames=len(paths), interval=1000, repeat=False  # 1 second per frame
        )

        return anim

    def show(self) -> None:
        """Display the current state of the visualization."""
        plt.show()
