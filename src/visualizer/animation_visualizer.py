import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from typing import List, Tuple
import sys
import numpy as np


class CombinedAnimationVisualizer:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.fig = None
        self.ax_bfs = None
        self.ax_dfs = None
        self.animation = None
        self.pos = self._calculate_spaced_layout(graph)

    def _calculate_spaced_layout(self, graph, scale=2.0, k=None):
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
        self.fig, (self.ax_bfs, self.ax_dfs) = plt.subplots(1, 2, figsize=(20, 8))

        bfs_frames = self._build_path_frames(bfs_paths, bfs_residual_graphs)
        dfs_frames = self._build_path_frames(dfs_paths, dfs_residual_graphs)

        max_len = max(len(bfs_frames), len(dfs_frames))
        while len(bfs_frames) < max_len:
            bfs_frames.append(([], bfs_residual_graphs[-1] if bfs_residual_graphs else None))
        while len(dfs_frames) < max_len:
            dfs_frames.append(([], dfs_residual_graphs[-1] if dfs_residual_graphs else None))

        combined_frames = list(zip(bfs_frames, dfs_frames))

        self.animation = FuncAnimation(
            self.fig,
            lambda i: self._update_combined_animation(combined_frames[i]),
            frames=len(combined_frames),
            init_func=self._init_combined_animation,
            interval=interval,
            repeat_delay=repeat_delay,
            blit=False
        )

        plt.suptitle(title)
        plt.tight_layout()

    def _build_path_frames(self, paths: List[List[int]], residual_graphs: List[nx.DiGraph]):
        frames = []
        for path, graph in zip(paths, residual_graphs):
            edge_path = [(path[i], path[i+1]) for i in range(len(path)-1)] if len(path) > 1 else []
            frames.append((edge_path, graph))
        return frames

    def _init_combined_animation(self) -> None:
        try:
            self._draw_graph_with_path(self.ax_bfs, "BFS Algorithm", [], self.graph)
            self._draw_graph_with_path(self.ax_dfs, "DFS Algorithm", [], self.graph)
            return []
        except Exception as e:
            print(f"Error in animation initialization: {str(e)}", file=sys.stderr)
            raise

    def _update_combined_animation(self, frame) -> None:
        try:
            (bfs_edges, bfs_residual), (dfs_edges, dfs_residual) = frame
            self._draw_graph_with_path(self.ax_bfs, "BFS Algorithm", bfs_edges, bfs_residual)
            self._draw_graph_with_path(self.ax_dfs, "DFS Algorithm", dfs_edges, dfs_residual)
            return []
        except Exception as e:
            print(f"Error updating animation frame: {str(e)}", file=sys.stderr)
            raise

    def _draw_graph_with_path(self, ax, title, path_edges, residual_graph):
        ax.clear()
        pos = self.pos

        # Draw nodes
        nx.draw_networkx_nodes(residual_graph, pos, ax=ax,
                               node_color='lightblue', node_size=800)
        nx.draw_networkx_labels(residual_graph, pos, ax=ax, font_size=12)

        # Draw all edges in gray
        nx.draw_networkx_edges(residual_graph, pos, ax=ax,
                               edge_color='gray', width=2, arrowstyle='->', arrowsize=20)

        # Highlight path edges
        if path_edges:
            nx.draw_networkx_edges(
                residual_graph, pos, edgelist=path_edges,
                ax=ax, edge_color='red', width=3, arrowstyle='->', arrowsize=20
            )

        # Draw edge labels: flow/capacity
        edge_labels = {
            (u, v): f"{d.get('flow', 0)}/{d.get('capacity', 0)}"
            for u, v, d in residual_graph.edges(data=True)
        }
        nx.draw_networkx_edge_labels(residual_graph, pos,
                                     edge_labels=edge_labels, ax=ax, font_size=10)

        ax.set_title(title, fontsize=14)

    def save(self, filename: str) -> None:
        if hasattr(self, 'animation') and self.animation:
            try:
                self.animation.save(filename, writer='pillow', fps=1, dpi=100)
                print(f"Combined animation saved to {filename}")
            except Exception as e:
                print(f"Error saving animation: {str(e)}", file=sys.stderr)
        else:
            print("No animation to save", file=sys.stderr)

    def close(self) -> None:
        if self.fig:
            plt.close(self.fig)
