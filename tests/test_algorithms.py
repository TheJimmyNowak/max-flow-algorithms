import pytest
import networkx as nx
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow


def create_test_graph():
    """Create a test graph for algorithm testing."""
    G = nx.DiGraph()
    G.add_node(0, type="source")
    G.add_node(1, type="intermediate")
    G.add_node(2, type="intermediate")
    G.add_node(3, type="sink")

    # Add edges with capacities
    edges = [
        (0, 1, 10),  # Source to 1
        (0, 2, 5),   # Source to 2
        (1, 2, 2),   # 1 to 2
        (1, 3, 8),   # 1 to Sink
        (2, 3, 7),   # 2 to Sink
    ]
    for u, v, cap in edges:
        G.add_edge(u, v, capacity=cap)

    return G


def test_bfs_max_flow():
    """Test BFS implementation of max flow algorithm."""
    G = create_test_graph()
    bfs = BFSMaxFlow(G)
    max_flow, paths, residuals = bfs.compute_max_flow(0, 3)

    # Known max flow for this graph is 15
    # (10 units through node 1 and 5 units through node 2)
    assert max_flow == 15

    # Check metrics
    metrics = bfs.get_metrics()
    assert metrics.steps_count > 0
    assert metrics.paths_found > 0
    assert metrics.execution_time > 0


def test_dfs_max_flow():
    """Test DFS implementation of max flow algorithm."""
    G = create_test_graph()
    dfs = DFSMaxFlow(G)
    max_flow, paths, residuals = dfs.compute_max_flow(0, 3)

    # Known max flow for this graph is 15
    # (10 units through node 1 and 5 units through node 2)
    assert max_flow == 15

    # Check metrics
    metrics = dfs.get_metrics()
    assert metrics.steps_count > 0
    assert metrics.paths_found > 0
    assert metrics.execution_time > 0


def test_empty_graph():
    """Test algorithms with empty graph."""
    G = nx.DiGraph()
    G.add_node(0, type="source")
    G.add_node(1, type="sink")

    bfs = BFSMaxFlow(G)
    dfs = DFSMaxFlow(G)

    # No edges means no flow
    assert bfs.compute_max_flow(0, 1)[0] == 0
    assert dfs.compute_max_flow(0, 1)[0] == 0


def test_single_edge():
    """Test algorithms with graph containing single edge."""
    G = nx.DiGraph()
    G.add_node(0, type="source")
    G.add_node(1, type="sink")
    G.add_edge(0, 1, capacity=5)

    bfs = BFSMaxFlow(G)
    dfs = DFSMaxFlow(G)

    assert bfs.compute_max_flow(0, 1)[0] == 5
    assert dfs.compute_max_flow(0, 1)[0] == 5
