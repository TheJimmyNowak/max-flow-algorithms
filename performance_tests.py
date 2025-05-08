import time
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import gc
import networkx as nx
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow
from src.graph.generator import GraphGenerator


class IncrementalFlowTester:
    def __init__(self):
        self.generator = GraphGenerator()
        self.max_nodes = 600
        self.max_edges = 1500
        self.step = 100
        self.graph = None
        self.base_nodes = []
        self.base_edges = []

    def prepare_base_graph(self):
        print("Generating base graph...")
        self.graph = self.generator.generate_random_graph(
            num_nodes=self.max_nodes,
            num_edges=self.max_edges,
            num_sources=1,
            num_sinks=1,
            min_capacity=1.0,
            max_capacity=10.0
        )
        self.base_nodes = list(self.graph.nodes())
        self.base_edges = list(self.graph.edges())
        print("Base graph ready.")

    def run_all_tests(self):
        self.prepare_base_graph()

        self._run_test(
            test_type="edges",
            varying_range=range(500, self.max_edges + 1, self.step),
            fixed_value=self.max_nodes,
            is_fixed_nodes=True,
            filename="output/incremental_fixed_nodes.png"
        )

        self._run_test(
            test_type="nodes",
            varying_range=range(500, self.max_nodes + 1, self.step),
            fixed_value=self.max_edges,
            is_fixed_nodes=False,
            filename="output/incremental_fixed_edges.png"
        )

        self._run_combined_node_edge_test()

        self.test_varying_capacities()

    def _run_test(self, test_type, varying_range, fixed_value, is_fixed_nodes, filename):
        dfs_times = []
        bfs_times = []

        for val in varying_range:
            try:
                if is_fixed_nodes:
                    active_nodes = self.base_nodes[:fixed_value]
                    active_edges = self.base_edges[:val]
                    x_label = "Number of Edges"
                    title = f"Fixed Nodes = {fixed_value}"
                else:
                    active_nodes = self.base_nodes[:val]
                    active_edges = [
                        (u, v) for u, v in self.base_edges
                        if u in active_nodes and v in active_nodes
                    ]
                    x_label = "Number of Nodes"
                    title = f"Fixed Edges = {fixed_value}"

                subgraph = self._get_active_subgraph(active_nodes, active_edges)
                source, sink = self._ensure_source_sink(subgraph)

                dfs_time = self._time_algorithm(DFSMaxFlow, subgraph, source, sink)
                bfs_time = self._time_algorithm(BFSMaxFlow, subgraph, source, sink)

                dfs_times.append(dfs_time)
                bfs_times.append(bfs_time)

                print(f"{test_type.capitalize()}={val} | DFS={dfs_time:.3f}s | BFS={bfs_time:.3f}s")

            except Exception as e:
                print(f"Error at {test_type}={val}: {e}")
                dfs_times.append(0)
                bfs_times.append(0)

            gc.collect()

        self._plot_results(
            x_values=list(varying_range),
            dfs_times=dfs_times,
            bfs_times=bfs_times,
            x_label=x_label,
            title=title,
            filename=filename
        )

        # Dodane: Generowanie wykresu liniowego
        line_filename = filename.replace(".png", "_line.png")
        self._plot_line_results(
            x_values=list(varying_range),
            dfs_times=dfs_times,
            bfs_times=bfs_times,
            x_label=x_label,
            title=title,
            filename=line_filename
        )

    def _run_combined_node_edge_test(self):
        print("\n=== Combined Nodes + Edges Test ===")
        dfs_times = []
        bfs_times = []
        x_vals = list(range(500, min(self.max_nodes, self.max_edges) + 1, self.step))

        for val in x_vals:
            try:
                active_nodes = self.base_nodes[:val]
                active_edges = self.base_edges[:val]

                subgraph = self._get_active_subgraph(active_nodes, active_edges)
                source, sink = self._ensure_source_sink(subgraph)

                dfs_time = self._time_algorithm(DFSMaxFlow, subgraph, source, sink)
                bfs_time = self._time_algorithm(BFSMaxFlow, subgraph, source, sink)

                dfs_times.append(dfs_time)
                bfs_times.append(bfs_time)

                print(f"Nodes+Edges={val} | DFS={dfs_time:.3f}s | BFS={bfs_time:.3f}s")

            except Exception as e:
                print(f"Error at size={val}: {e}")
                dfs_times.append(0)
                bfs_times.append(0)

            gc.collect()

        self._plot_results(
            x_values=x_vals,
            dfs_times=dfs_times,
            bfs_times=bfs_times,
            x_label="Nodes and Edges Count",
            title="Growing Nodes and Edges Together",
            filename="output/incremental_combined.png"
        )

        # Dodane: Generowanie wykresu liniowego
        line_filename = "output/incremental_combined_line.png"
        self._plot_line_results(
            x_values=x_vals,
            dfs_times=dfs_times,
            bfs_times=bfs_times,
            x_label="Nodes and Edges Count",
            title="Growing Nodes and Edges Together (Linear Scale)",
            filename=line_filename
        )

    def test_varying_capacities(self):
        print("\n=== Capacity Range Test ===")
        capacity_ranges = [
            (1.0, 5.0),
            (1.0, 10.0),
            (1.0, 50.0),
            (1.0, 100.0),
            (1.0, 500.0),
            (1.0, 1000.0)
        ]
        fixed_nodes = 5000
        fixed_edges = 5000

        dfs_times = []
        bfs_times = []
        range_labels = []

        for min_cap, max_cap in capacity_ranges:
            print(f"Testing capacities {min_cap}–{max_cap}")

            graph = self.generator.generate_random_graph(
                num_nodes=fixed_nodes,
                num_edges=fixed_edges,
                num_sources=1,
                num_sinks=1,
                min_capacity=min_cap,
                max_capacity=max_cap
            )

            source, sink = self._ensure_source_sink(graph)

            dfs_time = self._time_algorithm(DFSMaxFlow, graph, source, sink)
            bfs_time = self._time_algorithm(BFSMaxFlow, graph, source, sink)

            dfs_times.append(dfs_time)
            bfs_times.append(bfs_time)
            range_labels.append(f"{int(max_cap)}")

            print(f"Cap={min_cap}-{max_cap} | DFS={dfs_time:.3f}s | BFS={bfs_time:.3f}s")

            gc.collect()

        self._plot_results(
            x_values=range_labels,
            dfs_times=dfs_times,
            bfs_times=bfs_times,
            x_label="Max Capacity (Min=1)",
            title="Effect of Capacity Range (Fixed 5000 nodes/edges)",
            filename="output/capacity_range_test.png"
        )

        # Dodane: Generowanie wykresu liniowego
        line_filename = "output/capacity_range_test_line.png"
        self._plot_line_results(
            x_values=range_labels,
            dfs_times=dfs_times,
            bfs_times=bfs_times,
            x_label="Max Capacity (Min=1)",
            title="Effect of Capacity Range (Linear Scale)",
            filename=line_filename
        )

    def _get_active_subgraph(self, active_nodes, active_edges):
        sub = nx.DiGraph()
        for node in active_nodes:
            sub.add_node(node, **self.graph.nodes[node])
        for u, v in active_edges:
            if u in active_nodes and v in active_nodes:
                sub.add_edge(u, v, **self.graph[u][v])
        return sub

    def _ensure_source_sink(self, graph):
        nodes = list(graph.nodes())
        if len(nodes) < 2:
            raise ValueError("Not enough nodes for source/sink.")
        graph.nodes[nodes[0]]["type"] = "source"
        graph.nodes[nodes[1]]["type"] = "sink"
        return nodes[0], nodes[1]

    def _time_algorithm(self, algorithm_class, graph, source, sink):
        start = time.time()
        algorithm = algorithm_class(graph)
        algorithm.compute_max_flow(source, sink)
        return time.time() - start

    def _plot_results(self, x_values, dfs_times, bfs_times, x_label, title, filename):
        plt.figure(figsize=(12, 7))
        plt.plot(x_values, dfs_times, 's--', label="DFS", color='darkorange')
        plt.plot(x_values, bfs_times, 'o-', label="BFS", color='navy')
        plt.xlabel(x_label)
        plt.ylabel("Time (seconds)")
        plt.title(f"DFS then BFS Max Flow\n{title}")
        plt.legend()
        plt.grid(True, linestyle=':')
        plt.yscale('log')
        os.makedirs('output', exist_ok=True)
        plt.savefig(filename)
        plt.close()
        print(f"Saved plot: {filename}")

    def _plot_line_results(self, x_values, dfs_times, bfs_times, x_label, title, filename):
        """Nowa metoda do tworzenia wykresów liniowych z normalną skalą"""
        plt.figure(figsize=(12, 7))
        plt.plot(x_values, dfs_times, 's--', label="DFS", color='darkorange')
        plt.plot(x_values, bfs_times, 'o-', label="BFS", color='navy')
        plt.xlabel(x_label)
        plt.ylabel("Time (seconds)")
        plt.title(f"DFS vs BFS Max Flow Performance\n{title}")
        plt.legend()
        plt.grid(True, linestyle=':')

        # Formatowanie osi Y aby pokazywała sensowne wartości czasowe
        max_time = max(max(dfs_times), max(bfs_times))
        if max_time > 60:
            plt.ylabel("Time (minutes)")
            plt.yticks(
                [0, 15, 30, 45, 60, 120, 180],
                ["0", "0.25", "0.5", "0.75", "1", "2", "3"]
            )
        elif max_time > 10:
            plt.yticks(range(0, int(max_time) + 5, 5))

        os.makedirs('output', exist_ok=True)
        plt.savefig(filename)
        plt.close()
        print(f"Saved line plot: {filename}")


if __name__ == "__main__":
    tester = IncrementalFlowTester()
    tester.run_all_tests()