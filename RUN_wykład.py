import time
import networkx as nx
import matplotlib.pyplot as plt
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow


def draw_flow_graph(G, flow_dict, title):
    pos = nx.spring_layout(G, seed=42)
    edge_labels = {
        (u, v): f"{flow_dict[u][v]}/{G[u][v]['capacity']}"
        for u, v in G.edges
        if u in flow_dict and v in flow_dict[u]
    }

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_weight='bold', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()


def build_flow_dict(G, residual_graph):
    flow_dict = {u: {} for u in G.nodes}
    for u, v in G.edges:
        original = G[u][v]["capacity"]
        residual = residual_graph[u][v]["capacity"]
        flow_dict[u][v] = original - residual
    return flow_dict


def run_custom_graph():
    # Tworzenie grafu
    G = nx.DiGraph()
    edges = [
        ('z', 'a', 3),
        ('z', 'c', 4),
        ('a', 'b', 2),
        ('a', 'l', 2),
        ('b', 'u', 3),
        ('c', 'l', 2),
        ('l', 'u', 4),
        ('c', 'b', 2)
    ]

    for u, v, w in edges:
        G.add_edge(u, v, capacity=w)

    print("\nTestowany graf:")
    for u, v, data in G.edges(data=True):
        print(f"{u} -> {v}, przepustowość: {data['capacity']}")

    source = 'z'
    sink = 'u'

    print(f"\nŹródło: {source}, Ujście: {sink}")

    # BFS
    print("\n=== Testowanie BFS ===")
    start_time = time.time()
    bfs = BFSMaxFlow(G)
    max_flow_bfs, _, residual_graphs_bfs = bfs.compute_max_flow(source, sink)
    bfs_time = time.time() - start_time
    print(f"Maksymalny przepływ (BFS): {max_flow_bfs}")
    print(f"Czas wykonania (BFS): {bfs_time:.6f} sekund")

    flow_dict_bfs = build_flow_dict(G, residual_graphs_bfs[-1])
    draw_flow_graph(G, flow_dict_bfs, "Przepływ maksymalny - BFS")

    # DFS
    print("\n=== Testowanie DFS ===")
    start_time = time.time()
    dfs = DFSMaxFlow(G)
    max_flow_dfs, _, residual_graphs_dfs = dfs.compute_max_flow(source, sink)
    dfs_time = time.time() - start_time
    print(f"Maksymalny przepływ (DFS): {max_flow_dfs}")
    print(f"Czas wykonania (DFS): {dfs_time:.6f} sekund")

    flow_dict_dfs = build_flow_dict(G, residual_graphs_dfs[-1])
    draw_flow_graph(G, flow_dict_dfs, "Przepływ maksymalny - DFS")

    print("\n=== Podsumowanie ===")
    print(f"Różnica w przepływach: {abs(max_flow_bfs - max_flow_dfs)}")
    print(f"Różnica w czasie: {abs(bfs_time - dfs_time):.6f} sekund")
    print(f"BFS {'szybszy' if bfs_time < dfs_time else 'wolniejszy'} niż DFS")


if __name__ == "__main__":
    run_custom_graph()
