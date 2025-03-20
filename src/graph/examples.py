#!/usr/bin/env python3

from .input_handler import GraphInputHandler
from .generator import GraphGenerator


def create_example_graph():
    """Create an example graph with known maximum flow."""
    handler = GraphInputHandler()

    # Add nodes
    handler.add_node(0, "source")
    handler.add_node(1, "intermediate")
    handler.add_node(2, "intermediate")
    handler.add_node(3, "intermediate")
    handler.add_node(4, "intermediate")
    handler.add_node(5, "intermediate")
    handler.add_node(6, "sink")

    # Add edges with capacities in a planar layout
    # Source edges
    handler.add_edge(0, 1, 15.0)  # source -> 1
    handler.add_edge(0, 2, 12.0)  # source -> 2
    handler.add_edge(0, 3, 10.0)  # source -> 3

    # Intermediate edges (arranged in a planar way)
    handler.add_edge(1, 2, 8.0)  # 1 -> 2
    handler.add_edge(2, 3, 5.0)  # 2 -> 3
    handler.add_edge(3, 4, 6.0)  # 3 -> 4
    handler.add_edge(4, 5, 3.0)  # 4 -> 5
    handler.add_edge(5, 2, 7.0)  # 5 -> 2
    handler.add_edge(1, 4, 10.0)  # 1 -> 4

    # Sink edges
    handler.add_edge(4, 6, 12.0)  # 4 -> sink
    handler.add_edge(5, 6, 15.0)  # 5 -> sink

    return handler.get_graph()


def create_random_graph():
    """Create a random graph for testing."""
    generator = GraphGenerator()
    return generator.generate_random_graph(
        num_nodes=6, num_edges=8, num_sources=1, num_sinks=1, min_capacity=1.0, max_capacity=10.0
    )
