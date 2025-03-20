import pytest
import networkx as nx
from src.graph.input_handler import GraphInputHandler
from src.graph.generator import GraphGenerator

# Test GraphInputHandler
def test_input_handler_initialization():
    handler = GraphInputHandler()
    assert isinstance(handler.graph, nx.DiGraph)
    assert handler.graph.number_of_nodes() == 0
    assert handler.graph.number_of_edges() == 0

def test_add_node():
    handler = GraphInputHandler()
    
    # Test adding intermediate node
    handler.add_node(0)
    assert handler.graph.has_node(0)
    assert handler.graph.nodes[0]['type'] == 'intermediate'
    
    # Test adding source node
    handler.add_node(1, 'source')
    assert handler.graph.has_node(1)
    assert handler.graph.nodes[1]['type'] == 'source'
    
    # Test adding sink node
    handler.add_node(2, 'sink')
    assert handler.graph.has_node(2)
    assert handler.graph.nodes[2]['type'] == 'sink'
    
    # Test invalid node type
    with pytest.raises(ValueError):
        handler.add_node(3, 'invalid_type')

def test_add_edge():
    handler = GraphInputHandler()
    
    # Add nodes first
    handler.add_node(0, 'source')
    handler.add_node(1, 'intermediate')
    handler.add_node(2, 'sink')
    
    # Test adding valid edge
    handler.add_edge(0, 1, 5.0)
    assert handler.graph.has_edge(0, 1)
    assert handler.graph[0][1]['capacity'] == 5.0
    
    # Test adding edge with non-existent nodes
    with pytest.raises(ValueError):
        handler.add_edge(3, 4, 5.0)
    
    # Test adding edge with non-positive capacity
    with pytest.raises(ValueError):
        handler.add_edge(0, 1, 0.0)
    with pytest.raises(ValueError):
        handler.add_edge(0, 1, -1.0)

def test_validate_graph():
    handler = GraphInputHandler()
    
    # Test empty graph
    with pytest.raises(ValueError):
        handler.validate_graph()
    
    # Test graph without source
    handler.add_node(0, 'sink')
    handler.add_node(1, 'intermediate')
    handler.add_edge(1, 0, 5.0)
    with pytest.raises(ValueError):
        handler.validate_graph()
    
    # Test graph without sink
    handler = GraphInputHandler()
    handler.add_node(0, 'source')
    handler.add_node(1, 'intermediate')
    handler.add_edge(0, 1, 5.0)
    with pytest.raises(ValueError):
        handler.validate_graph()
    
    # Test valid graph
    handler = GraphInputHandler()
    handler.add_node(0, 'source')
    handler.add_node(1, 'intermediate')
    handler.add_node(2, 'sink')
    handler.add_edge(0, 1, 5.0)
    handler.add_edge(1, 2, 5.0)
    assert handler.validate_graph() is True

def test_get_sources_and_sinks():
    handler = GraphInputHandler()
    
    # Add nodes
    handler.add_node(0, 'source')
    handler.add_node(1, 'intermediate')
    handler.add_node(2, 'sink')
    
    # Test getting sources
    sources = handler.get_sources()
    assert len(sources) == 1
    assert 0 in sources
    
    # Test getting sinks
    sinks = handler.get_sinks()
    assert len(sinks) == 1
    assert 2 in sinks

def test_get_edge_capacity():
    handler = GraphInputHandler()
    
    # Add nodes and edge
    handler.add_node(0, 'source')
    handler.add_node(1, 'sink')
    handler.add_edge(0, 1, 5.0)
    
    # Test getting capacity
    assert handler.get_edge_capacity(0, 1) == 5.0
    
    # Test getting capacity of non-existent edge
    with pytest.raises(KeyError):
        handler.get_edge_capacity(1, 0)

# Test GraphGenerator
def test_generator_initialization():
    generator = GraphGenerator()
    assert isinstance(generator.graph, nx.DiGraph)
    assert generator.graph.number_of_nodes() == 0
    assert generator.graph.number_of_edges() == 0

def test_generate_random_graph():
    generator = GraphGenerator()
    
    # Test generating a small graph
    graph = generator.generate_random_graph(
        num_nodes=5,
        num_edges=6,
        num_sources=1,
        num_sinks=1,
        min_capacity=1.0,
        max_capacity=10.0
    )
    
    # Check graph properties
    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 6
    assert len(generator.get_sources()) == 1
    assert len(generator.get_sinks()) == 1
    
    # Check edge capacities
    for u, v, data in graph.edges(data=True):
        assert 1.0 <= data['capacity'] <= 10.0
    
    # Check node types
    node_types = [data['type'] for _, data in graph.nodes(data=True)]
    assert node_types.count('source') == 1
    assert node_types.count('sink') == 1
    assert node_types.count('intermediate') == 3

def test_generate_random_graph_edge_cases():
    generator = GraphGenerator()
    
    # Test minimum possible graph
    graph = generator.generate_random_graph(
        num_nodes=2,
        num_edges=1,
        num_sources=1,
        num_sinks=1
    )
    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 1
    assert len(generator.get_sources()) == 1
    assert len(generator.get_sinks()) == 1
    
    # Test with equal number of sources and sinks to total nodes
    graph = generator.generate_random_graph(
        num_nodes=4,
        num_edges=4,
        num_sources=2,
        num_sinks=2
    )
    assert graph.number_of_nodes() == 4
    assert graph.number_of_edges() == 4
    assert len(generator.get_sources()) == 2
    assert len(generator.get_sinks()) == 2

def test_generator_get_sources_and_sinks():
    generator = GraphGenerator()
    
    # Generate a test graph
    graph = generator.generate_random_graph(
        num_nodes=5,
        num_edges=6,
        num_sources=2,
        num_sinks=1
    )
    
    # Test getting sources
    sources = generator.get_sources()
    assert len(sources) == 2
    
    # Test getting sinks
    sinks = generator.get_sinks()
    assert len(sinks) == 1

def test_generator_get_edge_capacity():
    generator = GraphGenerator()
    
    # Generate a test graph
    graph = generator.generate_random_graph(
        num_nodes=3,
        num_edges=2,
        num_sources=1,
        num_sinks=1
    )
    
    # Test getting capacity of existing edge
    for u, v, data in graph.edges(data=True):
        assert generator.get_edge_capacity(u, v) == data['capacity']
    
    # Find an edge that doesn't exist
    all_possible_edges = [(i, j) for i in range(3) for j in range(3) if i != j]
    existing_edges = list(graph.edges())
    non_existent_edge = next(edge for edge in all_possible_edges if edge not in existing_edges)
    
    # Test getting capacity of non-existent edge
    with pytest.raises(KeyError):
        generator.get_edge_capacity(non_existent_edge[0], non_existent_edge[1])
