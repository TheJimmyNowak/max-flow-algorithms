import pytest
import networkx as nx
from src.graph.input_handler import GraphInputHandler
from src.graph.generator import GraphGenerator
from src.algorithms.bfs import BFSMaxFlow
from src.algorithms.dfs import DFSMaxFlow
from src.visualizer.animation_visualizer import AnimationGraphVisualizer


@pytest.fixture
def sample_graph():
    """Create a sample graph for testing."""
    handler = GraphInputHandler()

    # Create a simple graph with 4 nodes
    handler.add_node(0, "source")
    handler.add_node(1, "intermediate")
    handler.add_node(2, "intermediate")
    handler.add_node(3, "sink")

    # Add edges
    handler.add_edge(0, 1, 5.0)
    handler.add_edge(0, 2, 3.0)
    handler.add_edge(1, 2, 2.0)
    handler.add_edge(1, 3, 4.0)
    handler.add_edge(2, 3, 6.0)

    return handler.get_graph()


@pytest.fixture
def source_sink(sample_graph):
    """Get source and sink nodes from the graph."""
    sources = [node for node, data in sample_graph.nodes(data=True) if data.get("type") == "source"]
    sinks = [node for node, data in sample_graph.nodes(data=True) if data.get("type") == "sink"]
    return sources[0], sinks[0]


def test_graph_generation_to_algorithm(sample_graph, source_sink):
    """Test integration between graph generation and algorithm computation."""
    source, sink = source_sink

    # Test BFS
    bfs = BFSMaxFlow(sample_graph)
    max_flow_bfs, _, _ = bfs.compute_max_flow(source, sink)
    assert max_flow_bfs > 0

    # Test DFS
    dfs = DFSMaxFlow(sample_graph)
    max_flow_dfs, _, _ = dfs.compute_max_flow(source, sink)
    assert max_flow_dfs > 0

    # Both algorithms should give the same result
    assert abs(max_flow_bfs - max_flow_dfs) < 1e-10


def test_algorithm_to_visualization(sample_graph, source_sink):
    """Test integration between algorithm computation and visualization."""
    source, sink = source_sink

    # Run BFS algorithm
    bfs = BFSMaxFlow(sample_graph)
    max_flow, paths, residual_graphs = bfs.compute_max_flow(source, sink)

    # Create animator
    animator = AnimationGraphVisualizer(sample_graph)

    # Create animation
    animator.create_animation(paths, residual_graphs, title="Test Visualization")
    assert animator.animation is not None

    # Check that the number of frames matches the number of paths
    assert len(paths) == len(residual_graphs) - 1  # -1 because we include initial state

    # Check that the final flow matches the max flow
    assert abs(max_flow) > 0


def test_random_graph_generation_to_algorithm():
    """Test integration between random graph generation and algorithm computation."""
    # Generate random graph
    generator = GraphGenerator()
    graph = generator.generate_random_graph(
        num_nodes=5, num_edges=6, num_sources=1, num_sinks=1, min_capacity=1.0, max_capacity=10.0
    )

    # Validate graph
    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 6
    assert len(generator.get_sources()) == 1
    assert len(generator.get_sinks()) == 1

    # Get source and sink
    source = generator.get_sources()[0]
    sink = generator.get_sinks()[0]

    # Test BFS
    bfs = BFSMaxFlow(graph)
    max_flow_bfs, _, _ = bfs.compute_max_flow(source, sink)
    assert max_flow_bfs >= 0

    # Test DFS
    dfs = DFSMaxFlow(graph)
    max_flow_dfs, _, _ = dfs.compute_max_flow(source, sink)
    assert max_flow_dfs >= 0

    # Both algorithms should give the same result
    assert abs(max_flow_bfs - max_flow_dfs) < 1e-10


def test_end_to_end_flow():
    """Test the entire flow from graph creation to visualization."""
    # Create graph
    handler = GraphInputHandler()
    handler.add_node(0, "source")
    handler.add_node(1, "intermediate")
    handler.add_node(2, "sink")
    handler.add_edge(0, 1, 10.0)
    handler.add_edge(1, 2, 10.0)
    graph = handler.get_graph()

    # Validate graph
    assert handler.validate_graph()

    # Get source and sink
    source = handler.get_sources()[0]
    sink = handler.get_sinks()[0]

    # Run BFS algorithm
    bfs = BFSMaxFlow(graph)
    max_flow, paths, residual_graphs = bfs.compute_max_flow(source, sink)

    # Check results
    assert max_flow > 0
    assert len(paths) > 0
    assert len(residual_graphs) == len(paths) + 1

    # Create visualization
    animator = AnimationGraphVisualizer(graph)
    animator.create_animation(paths, residual_graphs, title="End to End Test")
    assert animator.animation is not None


def test_error_handling_integration():
    """Test error handling across module boundaries."""
    # Test invalid graph (no source)
    handler = GraphInputHandler()
    handler.add_node(0, "sink")
    handler.add_node(1, "intermediate")
    handler.add_edge(1, 0, 5.0)

    with pytest.raises(ValueError):
        handler.validate_graph()

    # Test invalid graph (no sink)
    handler = GraphInputHandler()
    handler.add_node(0, "source")
    handler.add_node(1, "intermediate")
    handler.add_edge(0, 1, 5.0)

    with pytest.raises(ValueError):
        handler.validate_graph()

    # Test invalid edge capacity
    handler = GraphInputHandler()
    handler.add_node(0, "source")
    handler.add_node(1, "sink")

    with pytest.raises(ValueError):
        handler.add_edge(0, 1, 0.0)

    with pytest.raises(ValueError):
        handler.add_edge(0, 1, -1.0)


def test_large_graph_integration():
    """Test integration with a larger graph."""
    # Generate a larger random graph
    generator = GraphGenerator()
    graph = generator.generate_random_graph(
        num_nodes=10, num_edges=15, num_sources=2, num_sinks=2, min_capacity=1.0, max_capacity=20.0
    )

    # Validate graph
    assert graph.number_of_nodes() == 10
    assert graph.number_of_edges() == 15
    assert len(generator.get_sources()) == 2
    assert len(generator.get_sinks()) == 2

    # Get source and sink
    source = generator.get_sources()[0]
    sink = generator.get_sinks()[0]

    # Run both algorithms
    bfs = BFSMaxFlow(graph)
    dfs = DFSMaxFlow(graph)

    max_flow_bfs, paths_bfs, residuals_bfs = bfs.compute_max_flow(source, sink)
    max_flow_dfs, paths_dfs, residuals_dfs = dfs.compute_max_flow(source, sink)

    # Check results
    assert max_flow_bfs >= 0
    assert max_flow_dfs >= 0
    assert abs(max_flow_bfs - max_flow_dfs) < 1e-10

    # Test visualization
    animator = AnimationGraphVisualizer(graph)
    animator.create_animation(paths_bfs, residuals_bfs, title="Large Graph Test")
    assert animator.animation is not None
