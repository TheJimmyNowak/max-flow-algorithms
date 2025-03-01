import math

import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.nodes = set()  # Store nodes as a set
        self.edges = {}  # Store edges with flow using a nested dictionary

    def add_node(self, node):
        """Add a node to the graph."""
        self.nodes.add(node)

    def add_edge(self, from_node, to_node, flow):
        """
        Add an edge to the graph with a flow value.
        Args:
            from_node: Starting node of the edge.
            to_node: Ending node of the edge.
            flow: Flow value of the edge.
        """
        if from_node not in self.edges:
            self.edges[from_node] = {}
        self.edges[from_node][to_node] = flow

    def get_nodes(self):
        """
        Get all nodes in the graph.
        Returns:
            A list of all nodes.
        """
        return list(self.nodes)

    def get_edges(self):
        """
        Get all edges in the graph with their flow.
        Returns:
            A list of tuples (from_node, to_node, flow).
        """
        result = []
        for from_node, destinations in self.edges.items():
            for to_node, flow in destinations.items():
                result.append((from_node, to_node, flow))
        return result

    def _dfs(self, residual_graph, current, visited, sink, path):
        """
        Perform depth-first search to find an augmenting path.
        Args:
            residual_graph: The graph with current residual capacities.
            current: The current node in the DFS.
            visited: A set of visited nodes.
            sink: The sink node.
            path: The path traversed so far.
        Returns:
            A list representing the path from source to sink, or None if no path exists.
        """
        if current == sink:
            return path
        visited.add(current)
        for neighbor, capacity in residual_graph.get(current, {}).items():
            if neighbor not in visited and capacity > 0:
                result = self._dfs(residual_graph, neighbor, visited, sink, path + [(current, neighbor)])
                if result:
                    return result
        return None

    def __str__(self):
        """
        String representation of the graph (nodes and edges).
        Returns:
            A string describing the graph.
        """
        nodes_str = f"Nodes: {', '.join(map(str, self.get_nodes()))}"
        edges_str = "Edges: " + ", ".join(
            f"({from_node} -> {to_node}, flow={flow})"
            for from_node, to_node, flow in self.get_edges()
        )
        return f"{nodes_str}\n{edges_str}"

    def plot_graph(self):
        """
        Visualize the graph using Matplotlib.
        """
        plt.figure(figsize=(8, 6))
        positions = {}  # Store arbitrary positions in 2D space for nodes

        # Generate simple positions for the nodes in a circle
        for i, node in enumerate(self.nodes):
            angle = 2 * 3.14159 * i / len(self.nodes)
            positions[node] = (0.5 + 0.4 * math.cos(angle), 0.5 + 0.4 * math.sin(angle))

        # Plot edges with arrows
        for from_node, to_node, flow in self.get_edges():
            x_start, y_start = positions[from_node]
            x_end, y_end = positions[to_node]
            plt.arrow(
                x_start, y_start,
                x_end - x_start, y_end - y_start,
                head_width=0.02, head_length=0.03, fc='blue', ec='blue', length_includes_head=True, alpha=0.7
            )
            plt.text(
                (x_start + x_end) / 2,
                (y_start + y_end) / 2,
                str(flow),
                fontsize=10,
                color="red",
            )
        # Plot nodes
        for node, (x, y) in positions.items():
            plt.scatter(x, y, c="blue", s=200)
            plt.text(x, y, f"{node}", fontsize=12, ha="center", va="center", color="white")

        # Plot styling
        plt.axis("off")
        plt.title("Graph Visualization")
        plt.show()

    def ford_fulkerson(self, source, sink):
        """
        Implement the Ford-Fulkerson algorithm to compute the maximum flow.
        Args:
            source: The source node.
            sink: The sink node.
        Returns:
            The value of the maximum flow.
        """
        residual_graph = {node: {} for node in self.nodes}
        for from_node, to_node, capacity in self.get_edges():
            residual_graph[from_node][to_node] = capacity
            if to_node not in residual_graph:
                residual_graph[to_node] = {}
            if from_node not in residual_graph[to_node]:
                residual_graph[to_node][from_node] = 0

        max_flow = 0

        while True:
            path = self._dfs(residual_graph, source, set(), sink, [])
            if not path:
                break

            path_flow = min(residual_graph[u][v] for u, v in path)

            for u, v in path:
                residual_graph[u][v] -= path_flow
                residual_graph[v][u] += path_flow

            max_flow += path_flow

        return max_flow


if __name__ == "__main__":
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    g.add_node("F")

    g.add_edge("A", "B", 5)
    g.add_edge("A", "C", 10)
    g.add_edge("B", "C", 15)
    g.add_edge("B", "D", 10)
    g.add_edge("C", "D", 20)
    g.add_edge("A", "D", 20)
    g.add_edge("A", "E", 20)
    g.add_edge("E", "F", 20)
    g.add_edge("F", "D", 20)

    print("Graph:")
    g.plot_graph()

    max_flow = g.ford_fulkerson("A", "D")
    print(f"Maximum flow from A to D: {max_flow}")
    print("Visualizing graph...")
    g.plot_graph()


