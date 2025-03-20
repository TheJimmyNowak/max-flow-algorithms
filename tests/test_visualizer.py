import pytest
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from src.visualizer.animator import MaxFlowAnimator
from src.graph.input_handler import GraphInputHandler

@pytest.fixture
def sample_graph():
    """Create a sample graph for testing."""
    handler = GraphInputHandler()
    
    # Create a simple graph with 4 nodes
    handler.add_node(0, 'source')
    handler.add_node(1, 'intermediate')
    handler.add_node(2, 'intermediate')
    handler.add_node(3, 'sink')
    
    # Add edges
    handler.add_edge(0, 1, 5.0)
    handler.add_edge(0, 2, 3.0)
    handler.add_edge(1, 2, 2.0)
    handler.add_edge(1, 3, 4.0)
    handler.add_edge(2, 3, 6.0)
    
    return handler.get_graph()

@pytest.fixture
def animator(sample_graph):
    """Create a MaxFlowAnimator instance."""
    return MaxFlowAnimator(sample_graph)

def test_initialization(animator, sample_graph):
    """Test animator initialization."""
    assert isinstance(animator.graph, nx.DiGraph)
    assert isinstance(animator.fig, plt.Figure)
    assert isinstance(animator.ax, plt.Axes)
    assert animator.pos is not None
    assert len(animator.pos) == sample_graph.number_of_nodes()

def test_setup_plot(animator):
    """Test plot setup."""
    # Initial setup is done in __init__
    assert len(animator.ax.collections) > 0  # Should have nodes and edges drawn
    assert animator.ax.get_title() == "Maximum Flow Visualization"
    assert not animator.ax.axison  # Axes should be off

def test_update_edge_colors(animator):
    """Test edge color updates."""
    # Test without path
    animator.update_edge_colors()
    assert len(animator.edge_colors) == animator.graph.number_of_edges()
    assert all(color == 'gray' for color in animator.edge_colors)
    
    # Test with path
    path = [0, 1, 3]  # Source -> 1 -> Sink
    animator.update_edge_colors(path)
    assert len(animator.edge_colors) == animator.graph.number_of_edges()
    assert any(color == 'red' for color in animator.edge_colors)  # Path edges should be red

def test_update_node_colors(animator):
    """Test node color updates."""
    # Test without path
    animator.update_node_colors()
    assert len(animator.node_colors) == animator.graph.number_of_nodes()
    
    # Check source and sink colors
    node_types = nx.get_node_attributes(animator.graph, 'type')
    for i, color in enumerate(animator.node_colors):
        if node_types[i] == 'source':
            assert color == 'green'
        elif node_types[i] == 'sink':
            assert color == 'red'
        else:
            assert color == 'lightblue'
    
    # Test with path
    path = [0, 1, 3]  # Source -> 1 -> Sink
    animator.update_node_colors(path)
    assert len(animator.node_colors) == animator.graph.number_of_nodes()
    assert animator.node_colors[1] == 'red'  # Node 1 should be red (in path)

def test_update_edge_labels(animator, sample_graph):
    """Test edge label updates."""
    # Create a residual graph
    residual_graph = sample_graph.copy()
    # Simulate some flow
    residual_graph[0][1]['capacity'] = 3.0  # 2 units of flow used
    
    animator.update_edge_labels(residual_graph)
    assert len(animator.edge_labels) == animator.graph.number_of_edges()
    assert animator.edge_labels[(0, 1)] == '2.0/5.0'  # Flow/Capacity with decimal points

def test_create_animation(animator, sample_graph):
    """Test animation creation."""
    # Create sample data for animation
    paths = [[0, 1, 3], [0, 2, 3]]  # Two augmenting paths
    residual_graphs = [
        sample_graph.copy(),
        sample_graph.copy(),
        sample_graph.copy()
    ]
    metrics = [
        {'total_flow': 4.0, 'paths_found': 1},
        {'total_flow': 7.0, 'paths_found': 2}
    ]
    
    animation = animator.create_animation(paths, residual_graphs, metrics)
    assert isinstance(animation, FuncAnimation)
    # Store animation in a variable to prevent deletion warning
    plt.close()  # Close the figure to clean up

def test_show(animator, monkeypatch):
    """Test show method."""
    # Mock plt.show to avoid displaying the plot
    shown = False
    def mock_show():
        nonlocal shown
        shown = True
    
    monkeypatch.setattr(plt, 'show', mock_show)
    animator.show()
    assert shown  # Verify that show was called

def test_edge_case_empty_paths(animator):
    """Test animation with empty paths."""
    paths = []
    residual_graphs = [animator.graph.copy()]
    metrics = [{'total_flow': 0.0, 'paths_found': 0}]
    
    animation = animator.create_animation(paths, residual_graphs, metrics)
    assert isinstance(animation, FuncAnimation)
    plt.close()  # Close the figure to clean up

def test_edge_case_single_path(animator):
    """Test animation with a single path."""
    paths = [[0, 1, 3]]
    residual_graphs = [animator.graph.copy(), animator.graph.copy()]
    metrics = [{'total_flow': 4.0, 'paths_found': 1}]
    
    animation = animator.create_animation(paths, residual_graphs, metrics)
    assert isinstance(animation, FuncAnimation)
    plt.close()  # Close the figure to clean up
