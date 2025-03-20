import pytest
import networkx as nx
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow

def create_test_graph():
    """Create a simple test graph with known max flow."""
    G = nx.DiGraph()
    G.add_node(0, type='source')
    G.add_node(1)
    G.add_node(2)
    G.add_node(3, type='sink')
    
    G.add_edge(0, 1, capacity=10)
    G.add_edge(0, 2, capacity=10)
    G.add_edge(1, 2, capacity=2)
    G.add_edge(1, 3, capacity=4)
    G.add_edge(2, 3, capacity=9)
    
    return G

def test_bfs_max_flow():
    """Test BFS implementation of max flow algorithm."""
    G = create_test_graph()
    bfs = BFSMaxFlow(G)
    max_flow = bfs.compute_max_flow(0, 3)
    
    # Known max flow for this graph is 13
    assert max_flow == 13
    
    # Check metrics
    metrics = bfs.get_metrics()
    assert metrics.steps_count > 0
    assert metrics.paths_found > 0
    assert metrics.execution_time > 0

def test_dfs_max_flow():
    """Test DFS implementation of max flow algorithm."""
    G = create_test_graph()
    dfs = DFSMaxFlow(G)
    max_flow = dfs.compute_max_flow(0, 3)
    
    # Known max flow for this graph is 13
    assert max_flow == 13
    
    # Check metrics
    metrics = dfs.get_metrics()
    assert metrics.steps_count > 0
    assert metrics.paths_found > 0
    assert metrics.execution_time > 0

def test_empty_graph():
    """Test algorithms with empty graph."""
    G = nx.DiGraph()
    bfs = BFSMaxFlow(G)
    dfs = DFSMaxFlow(G)
    
    with pytest.raises(KeyError):
        bfs.compute_max_flow(0, 1)
    
    with pytest.raises(KeyError):
        dfs.compute_max_flow(0, 1)

def test_single_edge():
    """Test algorithms with graph containing single edge."""
    G = nx.DiGraph()
    G.add_node(0, type='source')
    G.add_node(1, type='sink')
    G.add_edge(0, 1, capacity=5)
    
    bfs = BFSMaxFlow(G)
    dfs = DFSMaxFlow(G)
    
    assert bfs.compute_max_flow(0, 1) == 5
    assert dfs.compute_max_flow(0, 1) == 5
