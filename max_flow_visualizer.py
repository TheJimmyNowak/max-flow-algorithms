import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from collections import deque

class MaxFlowVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(15, 10))  # Increased figure size
        self.G = None
        self.pos = None
        self.search_steps = []
        self.current_flow = 0
        self.max_flow = 0
        self.flow_history = []

    def generate_network(self, num_nodes, num_edges, cost_variance=1):
        self.G = nx.DiGraph()
        self.G.add_nodes_from(range(num_nodes))
        
        # Create a more interesting network structure
        # First, create a path from source to sink through intermediate nodes
        path_length = np.random.randint(3, num_nodes-1)  # Path length between 3 and n-1
        path_nodes = [0]  # Start with source
        available_nodes = list(range(1, num_nodes-1))  # Exclude source and sink
        np.random.shuffle(available_nodes)
        
        # Add intermediate nodes to the path
        for _ in range(path_length-2):  # -2 because we already have source and will add sink
            if available_nodes:
                path_nodes.append(available_nodes.pop())
        
        # Add sink to the path
        path_nodes.append(num_nodes-1)
        
        # Add edges along the path
        for i in range(len(path_nodes)-1):
            capacity = np.random.uniform(1, 1 + cost_variance)
            self.G.add_edge(path_nodes[i], path_nodes[i+1], capacity=capacity, flow=0)
            self.G.add_edge(path_nodes[i+1], path_nodes[i], capacity=0, flow=0)
        
        # Add random edges to create alternative paths
        remaining_edges = num_edges - (len(path_nodes)-1)
        possible_edges = [(u, v) for u in range(num_nodes) for v in range(num_nodes) 
                         if u != v and not self.G.has_edge(u, v)]
        np.random.shuffle(possible_edges)
        
        for u, v in possible_edges[:remaining_edges]:
            capacity = np.random.uniform(1, 1 + cost_variance)
            self.G.add_edge(u, v, capacity=capacity, flow=0)
            self.G.add_edge(v, u, capacity=0, flow=0)
        
        # Use spring layout with better parameters to minimize edge crossings
        self.pos = nx.spring_layout(self.G, k=2, iterations=100, seed=42)
        
        # Adjust positions to ensure source and sink are on opposite sides
        source_pos = self.pos[0]
        sink_pos = self.pos[num_nodes-1]
        
        # If source and sink are too close, adjust their positions
        if np.linalg.norm(np.array(source_pos) - np.array(sink_pos)) < 1.0:
            # Move source to the left
            self.pos[0] = (-1.0, source_pos[1])
            # Move sink to the right
            self.pos[num_nodes-1] = (1.0, sink_pos[1])
        
        self.source = 0
        self.sink = num_nodes - 1

    def find_augmenting_path(self, algorithm='BFS'):
        if algorithm == 'BFS':
            queue = deque([(self.source, [self.source])])
            visited = {self.source}
            
            while queue:
                current, path = queue.popleft()
                for neighbor in sorted(self.G.successors(current)):
                    if neighbor not in visited and self.G[current][neighbor]['capacity'] > self.G[current][neighbor]['flow']:
                        visited.add(neighbor)
                        new_path = path + [neighbor]
                        if neighbor == self.sink:
                            return new_path
                        queue.append((neighbor, new_path))
        else:  # DFS
            visited = {self.source}
            path = [self.source]
            
            def dfs(current):
                if current == self.sink:
                    return True
                for neighbor in sorted(self.G.successors(current)):
                    if neighbor not in visited and self.G[current][neighbor]['capacity'] > self.G[current][neighbor]['flow']:
                        visited.add(neighbor)
                        path.append(neighbor)
                        if dfs(neighbor):
                            return True
                        path.pop()
                return False
            
            if dfs(self.source):
                return path
        return None

    def update_flow(self, path):
        if not path:
            return 0
            
        # Find bottleneck capacity
        min_capacity = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            min_capacity = min(min_capacity, self.G[u][v]['capacity'] - self.G[u][v]['flow'])
        
        # Augment flow
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            self.G[u][v]['flow'] += min_capacity
            self.G[v][u]['flow'] -= min_capacity
            
        return min_capacity

    def animate_max_flow(self, algorithm='BFS'):
        def update(frame):
            self.ax.clear()
            
            # Restore the state of flows for this frame
            if frame < len(self.flow_history):
                for u, v, flow in self.flow_history[frame]:
                    self.G[u][v]['flow'] = flow
                    self.G[v][u]['flow'] = -flow
            
            # Draw edges with flow information
            edge_colors = []
            edge_widths = []
            edge_labels = {}
            max_flow = max((self.G[u][v]['flow'] for u, v in self.G.edges() if self.G[u][v]['capacity'] > 0), default=0)
            
            # Check if this is the last frame
            is_last_frame = frame == len(self.search_steps) - 1
            
            for u, v in self.G.edges():
                if self.G[u][v]['capacity'] > 0:
                    flow = self.G[u][v]['flow']
                    capacity = self.G[u][v]['capacity']
                    # Calculate edge width based on flow (normalized to max flow)
                    width = 1 + 3 * (flow / max_flow if max_flow > 0 else 0)
                    edge_widths.append(width)
                    
                    if is_last_frame:
                        # On last frame, show only edges with flow in blue
                        if flow > 0:
                            edge_colors.append('blue')
                        else:
                            edge_colors.append('lightgray')
                    else:
                        # On other frames, show current path in yellow and flow in red
                        if flow > 0:
                            edge_colors.append('red')
                        else:
                            edge_colors.append('gray')
                    edge_labels[(u, v)] = f'{flow:.1f}/{capacity:.1f}'
            
            # Draw only forward edges
            forward_edges = [(u, v) for u, v in self.G.edges() if self.G[u][v]['capacity'] > 0]
            nx.draw_networkx_edges(self.G, self.pos, edgelist=forward_edges, 
                                 edge_color=edge_colors, width=edge_widths)
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, font_size=8)
            
            # Draw nodes with different sizes for source and sink
            node_colors = ['lightblue'] * len(self.G.nodes())
            node_sizes = [700] * len(self.G.nodes())  # Increased base node size
            node_colors[self.source] = 'green'  # Source node
            node_colors[self.sink] = 'red'      # Sink node
            node_sizes[self.source] = 1500  # Make source bigger
            node_sizes[self.sink] = 1500    # Make sink bigger
            
            nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors, node_size=node_sizes)
            
            # Draw node labels with special labels for source and sink
            node_labels = {node: str(node) for node in self.G.nodes()}
            node_labels[self.source] = 'Source'
            node_labels[self.sink] = 'Sink'
            nx.draw_networkx_labels(self.G, self.pos, node_labels, font_size=12, font_weight='bold')
            
            title = f"Max Flow Calculation ({algorithm})\n"
            if is_last_frame:
                title += f"Final Max Flow: {self.current_flow:.2f}"
            else:
                title += f"Current Flow: {self.current_flow:.2f}"
            self.ax.set_title(title, fontsize=14)
            
            if not is_last_frame and frame < len(self.search_steps):
                path = self.search_steps[frame]
                # Highlight current path
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    nx.draw_networkx_edges(self.G, self.pos, 
                                         edgelist=[(u, v)], 
                                         edge_color='yellow', 
                                         width=6)  # Increased path width
            
            # Add legend
            if is_last_frame:
                legend_elements = [
                    plt.Line2D([0], [0], color='blue', label='Max Flow Path', linewidth=1),
                    plt.Line2D([0], [0], color='lightgray', label='Unused Edge', linewidth=1),
                    plt.Line2D([0], [0], color='green', label='Source', marker='o', markersize=15, linewidth=0),
                    plt.Line2D([0], [0], color='red', label='Sink', marker='o', markersize=15, linewidth=0),
                    plt.Line2D([0], [0], color='lightblue', label='Other Nodes', marker='o', markersize=15, linewidth=0)
                ]
            else:
                legend_elements = [
                    plt.Line2D([0], [0], color='gray', label='No Flow', linewidth=1),
                    plt.Line2D([0], [0], color='red', label='Has Flow', linewidth=1),
                    plt.Line2D([0], [0], color='yellow', label='Current Path', linewidth=3),
                    plt.Line2D([0], [0], color='green', label='Source', marker='o', markersize=15, linewidth=0),
                    plt.Line2D([0], [0], color='red', label='Sink', marker='o', markersize=15, linewidth=0),
                    plt.Line2D([0], [0], color='lightblue', label='Other Nodes', marker='o', markersize=15, linewidth=0)
                ]
            self.ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
            
        # Ensure we have at least one frame
        if not self.search_steps:
            self.search_steps = [[self.source]]  # Add initial state
            
        # Add extra frames at the end to show the final state
        total_frames = len(self.search_steps) + 5  # Add 5 extra frames at the end
        
        return FuncAnimation(self.fig, update, frames=total_frames, interval=1000, repeat=False)

    def calculate_max_flow(self, algorithm='BFS'):
        self.current_flow = 0
        self.search_steps = []
        self.flow_history = []
        
        # Record initial state
        initial_flows = [(u, v, self.G[u][v]['flow']) for u, v in self.G.edges()]
        self.flow_history.append(initial_flows)
        
        while True:
            path = self.find_augmenting_path(algorithm)
            if not path:
                break
                
            self.search_steps.append(path)
            flow = self.update_flow(path)
            self.current_flow += flow
            
            # Record state after each flow update
            current_flows = [(u, v, self.G[u][v]['flow']) for u, v in self.G.edges()]
            self.flow_history.append(current_flows)

def main():
    visualizer = MaxFlowVisualizer()
    
    for algorithm in ['BFS', 'DFS']:
        print(f"Running {algorithm} Max Flow...")
        visualizer.generate_network(num_nodes=10, num_edges=15)  # Increased network size
        visualizer.calculate_max_flow(algorithm)
        anim = visualizer.animate_max_flow(algorithm)
        anim.save(f'max_flow_{algorithm.lower()}.mp4', writer='ffmpeg')

if __name__ == "__main__":
    main() 