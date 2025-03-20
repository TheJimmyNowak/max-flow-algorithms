#!/usr/bin/env python3

"""Animation visualizer for maximum flow graphs."""

from typing import List, Optional, Tuple
import networkx as nx
import matplotlib.animation as animation
from .base_visualizer import BaseGraphVisualizer


class AnimationGraphVisualizer(BaseGraphVisualizer):
    """Animation visualizer for maximum flow graphs."""

    def __init__(self, graph: nx.DiGraph):
        """
        Initialize the animation visualizer.

        Args:
            graph: NetworkX directed graph to visualize
        """
        super().__init__(graph)
        self.animation = None

    def create_animation(
        self,
        paths: List[List[int]],
        residual_graphs: List[nx.DiGraph],
        title: str = "Maximum Flow Animation",
        interval: int = 1000
    ) -> None:
        """
        Create an animation showing the flow augmentation process.

        Args:
            paths: List of augmenting paths
            residual_graphs: List of residual graphs
            title: Title for the animation
            interval: Time between frames in milliseconds
        """
        def update(frame: int) -> Tuple[object, ...]:
            """
            Update function for animation.

            Args:
                frame: Current frame number

            Returns:
                Tuple of updated artists
            """
            self._prepare_edge_attributes(
                paths[frame] if frame < len(paths) else None,
                show_flow=True,
                residual_graph=residual_graphs[frame] if frame < len(residual_graphs) else None
            )
            self._update_node_colors(paths[frame] if frame < len(paths) else None)
            self._draw_graph(f"{title} - Step {frame + 1}/{len(paths)}")
            self._update_legend()
            return self.ax.get_children()

        # Create animation
        self.animation = animation.FuncAnimation(
            self.fig,
            update,
            frames=len(paths),
            interval=interval,
            blit=True
        )

    def save(self, filename: str) -> None:
        """
        Save the animation to a file.

        Args:
            filename: Output filename
        """
        if self.animation is None:
            raise RuntimeError("No animation has been created yet")
        self.animation.save(filename, writer='pillow') 