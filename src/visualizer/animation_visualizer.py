import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from typing import List, Dict, Optional, Tuple
import sys
import numpy as np


class CombinedAnimationVisualizer:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.fig = None
        self.ax_bfs = None
        self.ax_dfs = None
        self.animation = None
        # Calculate layout once with more space between nodes
        self.pos = self._calculate_spaced_layout(graph)

    def _calculate_spaced_layout(self, graph, scale=2.0, k=None):
        """Calculate layout with more space between nodes."""
        if k is None:
            k = 1 / np.sqrt(len(graph.nodes()))
        pos = nx.spring_layout(graph, k=k, scale=scale, seed=42)
        return pos

    def create_combined_animation(
            self,
            bfs_paths: List[List[int]],
            dfs_paths: List[List[int]],
            bfs_residual_graphs: List[nx.DiGraph],
            dfs_residual_graphs: List[nx.DiGraph],
            title: str = "Maximum Flow Comparison",
            interval: int = 1000,
            repeat_delay: int = 2000
    ) -> None:
        """Create combined animation showing BFS and DFS paths."""
        self.fig, (self.ax_bfs, self.ax_dfs) = plt.subplots(1, 2, figsize=(20, 8))

        # Prepare single path for each algorithm (last found path)
        bfs_path = bfs_paths[-1] if bfs_paths else []
        dfs_path = dfs_paths[-1] if dfs_paths else []

        # Convert to edge paths
        bfs_edge_path = [(bfs_path[i], bfs_path[i + 1]) for i in range(len(bfs_path) - 1)] if len(bfs_path) > 1 else []
        dfs_edge_path = [(dfs_path[i], dfs_path[i + 1]) for i in range(len(dfs_path) - 1)] if len(dfs_path) > 1 else []

        try:
            # Generate frames for single path animation
            frames = list(zip(
                self._generate_single_path_frames(bfs_edge_path,
                                                  bfs_residual_graphs[-1] if bfs_residual_graphs else None),
                self._generate_single_path_frames(dfs_edge_path,
                                                  dfs_residual_graphs[-1] if dfs_residual_graphs else None)
            ))

            self.animation = FuncAnimation(
                self.fig,
                lambda i: self._update_combined_animation(frames[i]),
                frames=len(frames),
                init_func=self._init_combined_animation,
                interval=interval,
                repeat_delay=repeat_delay,
                blit=False
            )

            plt.suptitle(title)
            plt.tight_layout()
        except Exception as e:
            print(f"Error creating animation: {str(e)}", file=sys.stderr)
            raise

    def _generate_single_path_frames(self, edge_path, residual_graph):
        """Generate frames for single path animation."""
        frames = []

        # Initial state - no path highlighted
        frames.append(([], residual_graph))

        # Add edges one by one
        current_path_edges = []
        for edge in edge_path:
            current_path_edges.append(edge)
            frames.append((current_path_edges.copy(), residual_graph))

        # Final state - full path highlighted
        if edge_path:
            frames.append((edge_path.copy(), residual_graph))

        return frames

    def _init_combined_animation(self) -> None:
        """Initialize combined animation."""
        try:
            # Initialize BFS subplot
            self._draw_graph_with_path(self.ax_bfs, "BFS Algorithm", [], 'red')
            # Initialize DFS subplot
            self._draw_graph_with_path(self.ax_dfs, "DFS Algorithm", [], 'blue')
            return []
        except Exception as e:
            print(f"Error in animation initialization: {str(e)}", file=sys.stderr)
            raise

    def _update_combined_animation(self, frame) -> None:
        """Update combined animation frame."""
        try:
            (bfs_edges, bfs_residual), (dfs_edges, dfs_residual) = frame
            # Update BFS subplot
            self._draw_graph_with_path(self.ax_bfs, "BFS Algorithm", bfs_edges, 'red')
            # Update DFS subplot
            self._draw_graph_with_path(self.ax_dfs, "DFS Algorithm", dfs_edges, 'blue')
            return []
        except Exception as e:
            print(f"Error updating animation frame: {str(e)}", file=sys.stderr)
            raise

    def _draw_graph_with_path(self, ax, title, path_edges, path_color):
        """Draw graph with highlighted path."""
        ax.clear()
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, self.pos, ax=ax,
                               node_color='lightblue', node_size=800)
        nx.draw_networkx_labels(self.graph, self.pos, ax=ax, font_size=12)

        # Draw all edges (gray)
        nx.draw_networkx_edges(self.graph, self.pos, ax=ax,
                               edge_color='gray', width=2, arrowstyle='->', arrowsize=20)

        # Highlight path edges
        if path_edges:
            nx.draw_networkx_edges(
                self.graph, self.pos, edgelist=path_edges,
                ax=ax, edge_color=path_color, width=3, arrowstyle='->', arrowsize=20
            )

        # Edge labels
        edge_labels = {(u, v): f"{d['capacity']:.1f}"
                       for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, self.pos,
                                     edge_labels=edge_labels, ax=ax, font_size=10)

        # Title and path info
        ax.set_title(title, fontsize=14)
        if path_edges:
            ax.text(0.5, -0.1, f"Current edge: {path_edges[-1]}",
                    transform=ax.transAxes, ha='center', fontsize=12)

    def save(self, filename: str) -> None:
        """Save animation to file."""
        if hasattr(self, 'animation') and self.animation:
            try:
                self.animation.save(filename, writer='pillow', fps=1, dpi=100)
                print(f"Combined animation saved to {filename}")
            except Exception as e:
                print(f"Error saving animation: {str(e)}", file=sys.stderr)
        else:
            print("No animation to save", file=sys.stderr)

    def close(self) -> None:
        """Close figure."""
        if self.fig:
            plt.close(self.fig)