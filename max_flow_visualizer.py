import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from collections import deque

class GraphVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.G = None
        self.pos = None
        self.search_steps = []
        self.current_step = 0

    def generate_network(self, num_nodes, num_edges, cost_variance=1):
        """Generate a random directed network."""
        self.G = nx.DiGraph()
        self.G.add_nodes_from(range(num_nodes))
        
        # Create list of possible edges
        possible_edges = [(u, v) for u in range(num_nodes) for v in range(num_nodes) if u != v]
        np.random.shuffle(possible_edges)
        
        # Add edges with random weights
        for i in range(min(num_edges, len(possible_edges))):
            u, v = possible_edges[i]
            weight = np.random.uniform(1, 1 + cost_variance)
            self.G.add_edge(u, v, weight=weight)
        
        # Calculate layout
        self.pos = nx.spring_layout(self.G, k=1, iterations=50)

    def bfs_search(self, start):
        """Perform BFS and record steps."""
        visited = {start}
        queue = deque([start])
        self.search_steps = [(start, {start})]
        
        while queue:
            current = queue.popleft()
            for neighbor in sorted(self.G.successors(current)):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    self.search_steps.append((neighbor, visited.copy()))

    def dfs_search(self, start):
        """Perform DFS and record steps."""
        visited = {start}
        self.search_steps = [(start, {start})]
        
        def dfs(current):
            for neighbor in sorted(self.G.successors(current)):
                if neighbor not in visited:
                    visited.add(neighbor)
                    self.search_steps.append((neighbor, visited.copy()))
                    dfs(neighbor)
        
        dfs(start)

    def animate_search(self, algorithm='BFS'):
        """Animate the search process."""
        def update(frame):
            self.ax.clear()
            
            # Draw the network
            edge_colors = ['gray'] * len(self.G.edges())
            edge_widths = [1] * len(self.G.edges())
            
            nx.draw_networkx_edges(self.G, self.pos, edge_color=edge_colors, width=edge_widths)
            
            # Draw nodes
            node_colors = ['lightblue'] * len(self.G.nodes())
            if frame < len(self.search_steps):
                current_node, visited = self.search_steps[frame]
                for node in visited:
                    node_colors[node] = 'green'
                node_colors[current_node] = 'red'
            
            nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors, node_size=500)
            nx.draw_networkx_labels(self.G, self.pos, font_size=8)
            
            self.ax.set_title(f"{algorithm} Search - Step {frame + 1}/{len(self.search_steps)}\n"
                            f"Current Node: {current_node if frame < len(self.search_steps) else 'None'}")
            
        anim = FuncAnimation(self.fig, update, frames=len(self.search_steps), interval=500, repeat=False)
        return anim

def main():
    # Create visualizer
    visualizer = GraphVisualizer()
    
    # Generate network
    num_nodes = 10
    num_edges = 20
    visualizer.generate_network(num_nodes, num_edges)
    
    # Run BFS
    print("Running BFS...")
    visualizer.bfs_search(start=0)
    anim_bfs = visualizer.animate_search(algorithm='BFS')
    anim_bfs.save('bfs.mp4', writer='ffmpeg')
    
    # Generate new network for DFS
    visualizer.generate_network(num_nodes, num_edges)
    
    # Run DFS
    print("Running DFS...")
    visualizer.dfs_search(start=0)
    anim_dfs = visualizer.animate_search(algorithm='DFS')
    anim_dfs.save('dfs.mp4', writer='ffmpeg')

if __name__ == "__main__":
    main() 