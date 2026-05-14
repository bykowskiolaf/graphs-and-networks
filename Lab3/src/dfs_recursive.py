# Realizacja Zadania 1 oraz Zadania 6 (ograniczenie głębokości)

def dfs_recursive(graph, start=0, use_matrix=False, max_depth=float('inf'), backtracking=False):
    """
    Zadanie 1: DFS w wersji rekurencyjnej (obsługuje listę i macierz).
    Zadanie 6: Parametr max_depth ogranicza głębokość.
    """
    n = len(graph)
    visited = [False] * n
    pre = [0] * n
    post = [0] * n
    timer = [1]  # Używamy listy, by przekazywać referencję do licznika
    
    def search(v, depth):
        visited[v] = True
        pre[v] = timer[0]
        timer[0] += 1
        
        if depth < max_depth:
            # Określenie sąsiadów na podstawie reprezentacji
            neighbors = []
            if use_matrix:
                neighbors = [u for u in range(n) if graph[v][u] == 1]
            else:
                neighbors = graph[v]
                
            for u in neighbors:
                if not visited[u]:
                    search(u, depth + 1)
        
        post[v] = timer[0]
        timer[0] += 1
        
        # Zadanie 1: Wersja z nawracaniem (Backtracking)
        # Odznaczamy wierzchołek przy powrocie z rekurencji, by umożliwić
        # eksplorację innych ścieżek w specyficznych problemach.
        if backtracking:
            visited[v] = False

    search(start, 0)
    return pre, post