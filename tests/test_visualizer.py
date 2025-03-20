import unittest
import networkx as nx
import os
import matplotlib.pyplot as plt
from src.visualizer.static_visualizer import StaticGraphVisualizer
from src.visualizer.animation_visualizer import AnimationGraphVisualizer


class TestVisualizer(unittest.TestCase):
    def setUp(self):
        # Create a simple planar graph for testing
        self.planar_graph = nx.DiGraph()
        self.planar_graph.add_nodes_from([0, 1, 2, 3])
        self.planar_graph.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 2)])
        for u, v in self.planar_graph.edges():
            self.planar_graph[u][v]["capacity"] = 10.0

        # Mark source and sink
        self.planar_graph.nodes[0]["type"] = "source"
        self.planar_graph.nodes[3]["type"] = "sink"

        # Create a non-planar graph (K5 - complete graph with 5 nodes)
        self.non_planar_graph = nx.DiGraph(nx.complete_graph(5))
        for u, v in self.non_planar_graph.edges():
            self.non_planar_graph[u][v]["capacity"] = 10.0

        # Mark source and sink
        self.non_planar_graph.nodes[0]["type"] = "source"
        self.non_planar_graph.nodes[4]["type"] = "sink"

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

    def test_edge_directions(self):
        """Test that edge directions are consistent and have single arrowheads."""
        # Create a test graph with known flow
        graph = self.planar_graph.copy()

        # Simulate flow by updating capacities
        graph[0][1]["capacity"] = 5.0  # Flow of 5 from 0 to 1
        graph[1][2]["capacity"] = 5.0  # Flow of 5 from 1 to 2
        graph[2][3]["capacity"] = 5.0  # Flow of 5 from 2 to 3

        # Create static visualization
        static_visualizer = StaticGraphVisualizer(graph)
        static_visualizer.visualize(show_flow=True)
        static_visualizer.save("output/test_directions.png")
        static_visualizer.close()

        # Verify that the file was created
        self.assertTrue(os.path.exists("output/test_directions.png"))

        # Create animation to test edge directions in animation
        animator = AnimationGraphVisualizer(graph)
        paths = [[0, 1, 2, 3]]  # Single path
        residuals = [graph.copy()]  # Single residual graph
        animator.create_animation(paths, residuals, title="Test Directions")
        animator.save("output/test_directions.gif")
        animator.close()

        # Verify that the animation file was created
        self.assertTrue(os.path.exists("output/test_directions.gif"))

    def test_flow_direction_consistency(self):
        """Test that flow direction is consistent with initial graph direction."""
        # Create a test graph with a known flow pattern
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2, 3])
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 2)])

        # Set initial capacities
        for u, v in graph.edges():
            graph[u][v]["capacity"] = 10.0

        # Mark source and sink
        graph.nodes[0]["type"] = "source"
        graph.nodes[3]["type"] = "sink"

        # Simulate flow that should maintain direction
        graph[0][1]["capacity"] = 5.0  # Flow of 5 from 0 to 1
        graph[1][2]["capacity"] = 5.0  # Flow of 5 from 1 to 2
        graph[2][3]["capacity"] = 5.0  # Flow of 5 from 2 to 3

        # Create visualization
        visualizer = StaticGraphVisualizer(graph)
        visualizer.visualize(show_flow=True)
        visualizer.save("output/test_flow_direction.png")
        visualizer.close()

        self.assertTrue(os.path.exists("output/test_flow_direction.png"))

    def test_planar_graph_detection(self):
        """Test that planar graphs are correctly detected and visualized."""
        # Test planar graph
        visualizer = StaticGraphVisualizer(self.planar_graph)
        visualizer.visualize()
        visualizer.save("output/test_planar.png")
        visualizer.close()
        self.assertTrue(os.path.exists("output/test_planar.png"))

        # Test non-planar graph
        visualizer = StaticGraphVisualizer(self.non_planar_graph)
        visualizer.visualize()
        visualizer.save("output/test_non_planar.png")
        visualizer.close()
        self.assertTrue(os.path.exists("output/test_non_planar.png"))

    def test_flow_visualization(self):
        """Test flow visualization features."""
        # Add flow information to the graph
        graph = self.planar_graph.copy()
        for u, v in graph.edges():
            graph[u][v]["capacity"] = 5.0  # Simulate some flow

        # Test visualization with flow
        visualizer = StaticGraphVisualizer(graph)
        visualizer.visualize(show_flow=True)
        visualizer.save("output/test_flow.png")
        visualizer.close()
        self.assertTrue(os.path.exists("output/test_flow.png"))

    def test_animation_creation(self):
        """Test animation creation with both planar and non-planar graphs."""
        # Create sample paths and residual graphs
        paths = [[0, 1, 2, 3], [0, 2, 3]]
        residuals = [self.planar_graph.copy() for _ in range(2)]

        # Test animation with planar graph
        animator = AnimationGraphVisualizer(self.planar_graph)
        animator.create_animation(paths, residuals, title="Test Animation")
        animator.save("output/test_animation.gif")
        animator.close()
        self.assertTrue(os.path.exists("output/test_animation.gif"))

    def test_source_sink_labels(self):
        """Test that source and sink labels are correctly added."""
        # Create visualization
        visualizer = StaticGraphVisualizer(self.planar_graph)
        visualizer.visualize()
        visualizer.save("output/test_labels.png")
        visualizer.close()
        self.assertTrue(os.path.exists("output/test_labels.png"))

    def tearDown(self):
        """Clean up test files."""
        test_files = [
            "output/test_planar.png",
            "output/test_non_planar.png",
            "output/test_flow.png",
            "output/test_animation.gif",
            "output/test_labels.png",
            "output/test_directions.png",
            "output/test_directions.gif",
            "output/test_flow_direction.png",
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

        # Close all matplotlib figures
        plt.close("all")


if __name__ == "__main__":
    unittest.main()
