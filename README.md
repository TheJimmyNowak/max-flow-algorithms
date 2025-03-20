# Graph Search Algorithm Visualizer

This project visualizes Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms on directed graphs. It provides interactive visualizations of the search process.

## Features

- Visualization of BFS and DFS search processes
- Support for networks with variable number of nodes and edges
- Edge weight visualization
- Node state highlighting (visited, current, unvisited)
- Step-by-step animation

## Requirements

- Python 3.7+
- NetworkX
- Matplotlib
- NumPy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/maksymalny-przeplyw.git
cd maksymalny-przeplyw
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main visualization script:
```bash
python max_flow_visualizer.py
```

This will generate two animation files:
- `bfs.mp4`: Shows the BFS algorithm visualization
- `dfs.mp4`: Shows the DFS algorithm visualization

## Customization

You can modify the following parameters in `max_flow_visualizer.py`:
- `num_nodes`: Number of nodes in the network
- `num_edges`: Number of edges in the network
- `cost_variance`: Range of edge weights (default: 1)

## Project Structure

- `max_flow_visualizer.py`: Main visualization script
- `requirements.txt`: Project dependencies
- `README.md`: This file

## License

This project is licensed under the MIT License - see the LICENSE file for details. 