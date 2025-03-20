import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from collections import deque
from matplotlib.animation import FuncAnimation


# Funkcja generująca losowy graf skierowany
def generate_random_graph(num_nodes, num_edges, cost_variance=1):
    """
    Generuje graf skierowany z losowymi łukami i kosztami.
    cost_variance – określa zakres losowanych kosztów: [1, 1+cost_variance].
    """
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))
    # Tworzymy listę możliwych krawędzi (bez pętli)
    possible_edges = [(u, v) for u in range(num_nodes) for v in range(num_nodes) if u != v]
    random.shuffle(possible_edges)
    for i in range(min(num_edges, len(possible_edges))):
        u, v = possible_edges[i]
        cost = random.uniform(1, 1 + cost_variance)  # koszt w zakresie [1, 1+cost_variance]
        G.add_edge(u, v, cost=cost)
    return G


# Implementacja DFS z rejestrowaniem kroków (użycie stosu)
def dfs_with_steps(G, start):
    """
    Przeszukiwanie grafu metodą DFS.
    Zwraca zbiór odwiedzonych wierzchołków oraz listę kroków (krotki: (aktualny_wierzchołek, lista_odwiedzonych)).
    """
    visited = set()
    stack = [start]
    steps = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            steps.append((node, list(visited)))
            # Aby zachować porządek DFS, sortujemy sąsiadów w kolejności odwrotnej
            neighbors = sorted(list(G.neighbors(node)), reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
    return visited, steps


# Implementacja BFS z rejestrowaniem kroków (użycie kolejki)
def bfs_with_steps(G, start):
    """
    Przeszukiwanie grafu metodą BFS.
    Zwraca zbiór odwiedzonych wierzchołków oraz listę kroków (krotki: (aktualny_wierzchołek, lista_odwiedzonych)).
    """
    visited = set()
    queue = deque([start])
    steps = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            steps.append((node, list(visited)))
            for neighbor in sorted(G.neighbors(node)):  # sortowanie dla spójności
                if neighbor not in visited:
                    queue.append(neighbor)
    return visited, steps


# Funkcja animująca przeszukiwanie (DFS lub BFS)
def animate_search(G, steps, algorithm_name="Search"):
    """
    Animuje proces przeszukiwania grafu.
    W kolejnych krokach aktualny wierzchołek jest zaznaczany na czerwono, odwiedzone na zielono,
    a nieodwiedzone pozostają jasnoniebieskie.
    """
    pos = nx.spring_layout(G, seed=42)  # Pozycjonowanie wierzchołków
    fig, ax = plt.subplots(figsize=(8, 6))

    def update(frame):
        ax.clear()
        current_node, visited_nodes = steps[frame]
        node_colors = []
        for node in G.nodes():
            if node in visited_nodes:
                # aktualny wierzchołek wyróżniamy kolorem czerwonym
                if node == current_node:
                    node_colors.append('red')
                else:
                    node_colors.append('green')
            else:
                node_colors.append('lightblue')
        nx.draw(G, pos, ax=ax, with_labels=True, node_color=node_colors, node_size=300)
        ax.set_title(f"{algorithm_name} - Krok {frame + 1}/{len(steps)} - Aktualnie: {current_node}")

    anim = FuncAnimation(fig, update, frames=len(steps), interval=500, repeat=False)
    plt.close(fig)  # Zamykamy figurę, aby nie wyświetlała się statycznie
    return anim


# Funkcje eksperymentów wydajnościowych

def experiment_fixed_nodes_variable_edges(num_nodes, edges_list, algorithm='DFS'):
    """
    Eksperyment: stała liczba wierzchołków, zmienna liczba łuków.
    Zwraca listę zmierzonych czasów wykonania dla poszczególnej liczby łuków.
    """
    times = []
    for num_edges in edges_list:
        G = generate_random_graph(num_nodes, num_edges)
        start = 0
        start_time = time.perf_counter()
        if algorithm.upper() == 'DFS':
            dfs_with_steps(G, start)
        else:
            bfs_with_steps(G, start)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    return times


def experiment_fixed_edges_variable_nodes(edges, nodes_list, algorithm='DFS'):
    """
    Eksperyment: stała liczba łuków, zmienna liczba wierzchołków.
    Zwraca listę czasów wykonania.
    """
    times = []
    for num_nodes in nodes_list:
        G = generate_random_graph(num_nodes, edges)
        start = 0
        start_time = time.perf_counter()
        if algorithm.upper() == 'DFS':
            dfs_with_steps(G, start)
        else:
            bfs_with_steps(G, start)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    return times


def experiment_cost_variance(num_nodes, num_edges, variances, algorithm='DFS'):
    """
    Eksperyment: wpływ wahań kosztów na czas wykonania.
    Dla danego grafu o stałej liczbie wierzchołków i łuków testujemy różne wartości cost_variance.
    """
    times = []
    for var in variances:
        G = generate_random_graph(num_nodes, num_edges, cost_variance=var)
        start = 0
        start_time = time.perf_counter()
        if algorithm.upper() == 'DFS':
            dfs_with_steps(G, start)
        else:
            bfs_with_steps(G, start)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    return times


def plot_experiment(x, times, xlabel, ylabel, title):
    """
    Rysuje wykres dla przeprowadzonego eksperymentu.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(x, times, marker='o')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()


# Przykładowe użycie
if __name__ == "__main__":
    # Przykładowy graf do animacji (dla mniejszej liczby wierzchołków)
    num_nodes_anim = 50
    num_edges_anim = 100
    G_anim = generate_random_graph(num_nodes_anim, num_edges_anim)

    # Animacja DFS
    visited_dfs, steps_dfs = dfs_with_steps(G_anim, start=0)
    anim_dfs = animate_search(G_anim, steps_dfs, algorithm_name="DFS")
    anim_dfs.save("dfs_animation.mp4", writer="ffmpeg")
    # Aby zapisać animację do pliku, można użyć np.:
    # anim_dfs.save("dfs_animation.mp4", writer="ffmpeg")
    # W środowiskach takich jak Jupyter Notebook można wyświetlić animację za pomocą HTML:
    # from IPython.display import HTML
    # HTML(anim_dfs.to_jshtml())

    # Animacja BFS
    visited_bfs, steps_bfs = bfs_with_steps(G_anim, start=0)
    anim_bfs = animate_search(G_anim, steps_bfs, algorithm_name="BFS")
    anim_bfs.save("bfs.mp4", writer="ffmpeg")
    # Analogicznie: zapisywanie lub wyświetlanie animacji

    # ------------------------------
    # Eksperymenty wydajnościowe
    # 1. Stała liczba wierzchołków, zmienna liczba łuków
    # edges_list = [50, 100, 200, 500, 1000]
    # times_dfs = experiment_fixed_nodes_variable_edges(num_nodes=1000, edges_list=edges_list, algorithm='DFS')
    # times_bfs = experiment_fixed_nodes_variable_edges(num_nodes=1000, edges_list=edges_list, algorithm='BFS')
    # plot_experiment(edges_list, times_dfs, xlabel="Liczba łuków", ylabel="Czas (s)",
    #                 title="DFS: Stała liczba wierzchołków, zmienna liczba łuków")
    # plot_experiment(edges_list, times_bfs, xlabel="Liczba łuków", ylabel="Czas (s)",
    #                 title="BFS: Stała liczba wierzchołków, zmienna liczba łuków")
    #
    # # 2. Stała liczba łuków, zmienna liczba wierzchołków
    # nodes_list = [500, 1000, 2000, 5000, 10000]
    # times_dfs_nodes = experiment_fixed_edges_variable_nodes(edges=500, nodes_list=nodes_list, algorithm='DFS')
    # times_bfs_nodes = experiment_fixed_edges_variable_nodes(edges=500, nodes_list=nodes_list, algorithm='BFS')
    # plot_experiment(nodes_list, times_dfs_nodes, xlabel="Liczba wierzchołków", ylabel="Czas (s)",
    #                 title="DFS: Stała liczba łuków, zmienna liczba wierzchołków")
    # plot_experiment(nodes_list, times_bfs_nodes, xlabel="Liczba wierzchołków", ylabel="Czas (s)",
    #                 title="BFS: Stała liczba łuków, zmienna liczba wierzchołków")
    #
    # # 3. Wpływ wahań kosztów na czas wykonania
    # variances = [1, 5, 10, 20]
    # times_dfs_var = experiment_cost_variance(num_nodes=1000, num_edges=500, variances=variances, algorithm='DFS')
    # times_bfs_var = experiment_cost_variance(num_nodes=1000, num_edges=500, variances=variances, algorithm='BFS')
    # plot_experiment(variances, times_dfs_var, xlabel="Wahania kosztów", ylabel="Czas (s)",
    #                 title="DFS: Wpływ wahań kosztów na czas")
    # plot_experiment(variances, times_bfs_var, xlabel="Wahania kosztów", ylabel="Czas (s)",
    #                 title="BFS: Wpływ wahań kosztów na czas")
