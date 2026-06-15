import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import itertools

class Graph:
    def __init__(self, isDirected=False):
        self.graph = {}
        self.isDirected = isDirected

    def addVertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def addEdge(self, v, u, weight=1):
        self.addVertex(v)
        self.addVertex(u)

        self.graph[v].append((u, weight))

        if not self.isDirected and v != u:
            self.graph[u].append((v, weight))

    def __str__(self):
        result = ""
        for vertex in self.graph:
            result += f"{vertex} -> {self.graph[vertex]}\n"
        return result

    def to_adjacency_matrix(self):
        vertices = list(self.graph.keys())
        index = {v: i for i, v in enumerate(vertices)}
        matrix = np.zeros((len(vertices), len(vertices)), dtype=int)

        for v in vertices:
            for neighbor, weight in self.graph[v]:
                i = index[v]
                j = index[neighbor]
                matrix[i][j] = 1
        return matrix, vertices

    def to_adjacency_list(matrix, vertices=None, isDirected=False):
        n = matrix.shape[0]
        if vertices is None:
            vertices = list(range(n))
        g = Graph(isDirected)
        for v in vertices:
            g.addVertex(v)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    if not isDirected and j <= i:
                        continue
                    g.addEdge(vertices[i], vertices[j])
        return g

    def draw_graph(self, coloringMethod=None):
        G = nx.DiGraph() if self.isDirected else nx.Graph()
        for v in self.graph:
            G.add_node(v)
            for neighbor, weight in self.graph[v]:
                G.add_edge(v, neighbor, weight=weight)

        # Mapowanie kolorów (zostawione atrapy metod dla kompatybilności)
        color_map_dict = {v: 0 for v in self.graph}

        unique_colors = list(set(color_map_dict.values()))
        palette = list(mcolors.TABLEAU_COLORS.values())
        if len(unique_colors) > len(palette):
            palette = list(mcolors.CSS4_COLORS.values())

        node_colors = [
            palette[color_map_dict[v] % len(palette)] for v in G.nodes()
        ]

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=1000,
            font_size=9,
            font_weight="bold",
            edge_color="gray",
        )
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        plt.show()

    # Reprezentacja wagowa macierzy
    def to_adjacency_matrix_weighted(self):
        """Zwraca macierz sąsiedztwa z wagami oraz listę wierzchołków."""
        vertices = sorted(list(self.graph.keys()))
        n = len(vertices)
        index = {v: i for i, v in enumerate(vertices)}

        matrix = np.full((n, n), float("inf"))
        np.fill_diagonal(matrix, 0)

        for v in vertices:
            for neighbor, weight in self.graph[v]:
                matrix[index[v]][index[neighbor]] = weight

        return matrix, vertices

    # Pobranie wagi krawędzi
    def getWeight(self, v1, v2):
        for neighbor, weight in self.graph.get(v1, []):
            if neighbor == v2:
                return weight
        return None

    # =========================================================================
    # ZADANIE 1: NAJKRÓTSZA ŚCIEŻKA (ALGORYTM DIJKSTRY)
    # =========================================================================
    def shortest_path_adj_list(self, start, end):
        """Najkrótsza ścieżka - reprezentacja: LISTY SĄSIEDZTWA [cite: 11, 16]"""
        distances = {v: float("inf") for v in self.graph}
        previous = {v: None for v in self.graph}
        distances[start] = 0
        unvisited = set(self.graph.keys())

        while unvisited:
            current = min(unvisited, key=lambda v: distances[v])
            if distances[current] == float("inf") or current == end:
                break
            unvisited.remove(current)

            for neighbor, weight in self.graph[current]:
                if neighbor in unvisited:
                    new_dist = distances[current] + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        previous[neighbor] = current

        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()

        return (
            (path, distances[end])
            if distances[end] != float("inf")
            else ([], float("inf"))
        )

    def shortest_path_adj_matrix(self, start, end):
        """Najkrótsza ścieżka - reprezentacja: MACIERZ SĄSIEDZTWA [cite: 10, 16]"""
        matrix, vertices = self.to_adjacency_matrix_weighted()
        n = len(vertices)
        if start not in vertices or end not in vertices:
            return [], float("inf")

        start_idx, end_idx = vertices.index(start), vertices.index(end)

        distances = [float("inf")] * n
        previous = [None] * n
        distances[start_idx] = 0
        visited = [False] * n

        for _ in range(n):
            min_dist = float("inf")
            u = -1
            for v in range(n):
                if not visited[v] and distances[v] < min_dist:
                    min_dist = distances[v]
                    u = v

            if u == -1 or u == end_idx:
                break
            visited[u] = True

            for v in range(n):
                if not visited[v] and matrix[u][v] != float("inf"):
                    if distances[u] + matrix[u][v] < distances[v]:
                        distances[v] = distances[u] + matrix[u][v]
                        previous[v] = u

        path_idx = []
        curr = end_idx
        while curr is not None:
            path_idx.append(curr)
            curr = previous[curr]
        path_idx.reverse()

        path = [vertices[i] for i in path_idx]
        return (
            (path, distances[end_idx])
            if distances[end_idx] != float("inf")
            else ([], float("inf"))
        )

    # =========================================================================
    # ZADANIE 2: NAJDŁUŻSZA ŚCIEŻKA PROSTA (BACKTRACKING)
    # =========================================================================
    def longest_path_adj_list(self, start, end):
        """Najdłuższa ścieżka prosta - reprezentacja: LISTY SĄSIEDZTWA [cite: 14, 17]"""
        best_path = []
        max_weight = -float("inf")

        def dfs(current, visited, current_path, current_weight):
            nonlocal max_weight, best_path
            if current == end:
                if current_weight > max_weight:
                    max_weight = current_weight
                    best_path = list(current_path)
                return

            for neighbor, weight in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    current_path.append(neighbor)
                    dfs(neighbor, visited, current_path, current_weight + weight)
                    current_path.pop()
                    visited.remove(neighbor)

        dfs(start, {start}, [start], 0)
        return best_path, (max_weight if max_weight != -float("inf") else 0)

    def longest_path_adj_matrix(self, start, end):
        """Najdłuższa ścieżka prosta - reprezentacja: MACIERZ SĄSIEDZTWA [cite: 13, 17]"""
        matrix, vertices = self.to_adjacency_matrix_weighted()
        if start not in vertices or end not in vertices:
            return [], -float("inf")

        start_idx, end_idx = vertices.index(start), vertices.index(end)
        best_path_idx = []
        max_weight = -float("inf")
        n = len(vertices)

        def dfs_matrix(u, visited, current_path, current_weight):
            nonlocal max_weight, best_path_idx
            if u == end_idx:
                if current_weight > max_weight:
                    max_weight = current_weight
                    best_path_idx = list(current_path)
                return

            for v in range(n):
                if v != u and matrix[u][v] != float("inf") and v not in visited:
                    visited.add(v)
                    current_path.append(v)
                    dfs_matrix(
                        v, visited, current_path, current_weight + matrix[u][v]
                    )
                    current_path.pop()
                    visited.remove(v)

        dfs_matrix(start_idx, {start_idx}, [start_idx], 0)
        best_path = [vertices[i] for i in best_path_idx]
        return best_path, (max_weight if max_weight != -float("inf") else 0)

    # =========================================================================
    # ZADANIE 4: CYKLE HAMILTONA / PEŁNY PRZEGLĄD (TSP) [cite: 39]
    # =========================================================================
    def calculate_cycle_weight(self, cycle):
        total = 0
        for i in range(len(cycle) - 1):
            weight = self.getWeight(cycle[i], cycle[i + 1])
            if weight is None:
                return None
            total += weight
        return total

    def find_hamiltonian_cycles(self):
        vertices = list(self.graph.keys())
        if not vertices:
            return []
        start = vertices[0]
        all_cycles = []
        other_vertices = vertices[1:]

        for permutation in itertools.permutations(other_vertices):
            cycle = [start] + list(permutation) + [start]
            weight = self.calculate_cycle_weight(cycle)
            if weight is not None:
                all_cycles.append((cycle, weight))
        return all_cycles

    def shortest_hamiltonian_cycle(self):
        """Zadanie 4a [cite: 40]"""
        cycles = self.find_hamiltonian_cycles()
        return min(cycles, key=lambda x: x[1]) if cycles else ([], 0)

    def longest_hamiltonian_cycle(self):
        """Zadanie 4b [cite: 41]"""
        cycles = self.find_hamiltonian_cycles()
        return max(cycles, key=lambda x: x[1]) if cycles else ([], 0)
    
        # =========================================================================
    # POMOCNICZE: POBIERANIE WSZYSTKICH KRAWĘDZI
    # =========================================================================
    def get_all_edges(self):
        edges = []
        visited = set()
        for u in self.graph:
            for v, weight in self.graph[u]:
                if not self.isDirected:
                    # Sortowanie krotek, aby uniknąć duplikatów krawędzi w grafie nieskierowanym
                    edge = tuple(sorted([u, v]))
                    if edge not in visited:
                        edges.append((u, v, weight))
                        visited.add(edge)
                else:
                    edges.append((u, v, weight))
        return edges

    # =========================================================================
    # ZADANIE 5: DRZEWA SPINAJĄCE (ALGORYTM KRUSKALA)
    # =========================================================================
    def kruskal_spanning_tree(self, maximize=False):
        """Zwraca listę krawędzi oraz sumaryczną wagę drzewa spinającego."""
        edges = self.get_all_edges()
        # Sortujemy krawędzie rosnąco dla MST lub malejąco dla MaxST
        edges.sort(key=lambda x: x[2], reverse=maximize)

        parent = {v: v for v in self.graph}
        rank = {v: 0 for v in self.graph}

        def find(item):
            if parent[item] == item:
                return item
            else:
                parent[item] = find(parent[item])
                return parent[item]

        def union(set1, set2):
            root1 = find(set1)
            root2 = find(set2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1
                return True
            return False

        tree_edges = []
        tree_weight = 0

        for u, v, w in edges:
            if union(u, v):
                tree_edges.append((u, v, w))
                tree_weight += w

        return tree_edges, tree_weight

    # =========================================================================
    # ZADANIE 6: ZACHŁANNY PROBLEM KOMIWOJAŻERA (NEAREST NEIGHBOR)
    # =========================================================================
    def greedy_tsp(self, start_vertex, maximize=False):
        """Metoda zachłanna dla TSP: wybiera możliwie najkrótszą/najdłuższą krawędź."""
        vertices = list(self.graph.keys())
        if start_vertex not in vertices:
            return [], float('inf')

        current = start_vertex
        unvisited = set(vertices)
        unvisited.remove(current)

        path = [current]
        total_weight = 0

        while unvisited:
            next_vertex = None
            # Szukamy skrajnej wagi w zależności od celu (minimize / maximize)
            best_weight = -float('inf') if maximize else float('inf')

            for neighbor, weight in self.graph[current]:
                if neighbor in unvisited:
                    if (maximize and weight > best_weight) or (not maximize and weight < best_weight):
                        best_weight = weight
                        next_vertex = neighbor

            if next_vertex is None:
                return [], float('inf') # Brak przejścia (graf niespójny)

            path.append(next_vertex)
            total_weight += best_weight
            unvisited.remove(next_vertex)
            current = next_vertex

        # Powrót do miasta początkowego, zamykając cykl
        return_weight = self.getWeight(current, start_vertex)
        if return_weight is None:
            return [], float('inf')

        path.append(start_vertex)
        total_weight += return_weight

        return path, total_weight

def load_graph_from_file(filename, isDirected=False):
    g = Graph(isDirected=isDirected)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            raise ValueError("Plik jest pusty!")

        # Pomijamy pierwszą linię 'v e'
        for line in lines[1:]:
            parts = line.split()
            if len(parts) == 3:
                v_i, v_j, w_k = parts[0], parts[1], float(parts[2])
                g.addEdge(v_i, v_j, w_k)
        return g
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{filename}' w katalogu roboczym.")
        return None
