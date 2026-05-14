# Realizacja Zadania 3 (Czy graf jest drzewem) i Zadania 4 (Cykle)

def is_tree(graph_list):
    """
    Zadanie 3: Sprawdza, czy graf jest drzewem.
    Graf nieskierowany jest drzewem, jeśli jest spójny i ma N-1 krawędzi,
    co jest równoważne z brakiem cykli (krawędzi powrotnych w DFS).
    """
    n = len(graph_list)
    visited = [False] * n
    
    def has_cycle(v, parent):
        visited[v] = True
        for u in graph_list[v]:
            if not visited[u]:
                if has_cycle(u, v):
                    return True
            elif u != parent:
                # Trafiliśmy na odwiedzony wierzchołek, który nie jest rodzicem -> cykl!
                return True
        return False

    # Sprawdzamy od wierzchołka 0
    if has_cycle(0, -1):
        return False
        
    # Sprawdzamy spójność (czy wszystkie wierzchołki zostały odwiedzone)
    if not all(visited):
        return False
        
    return True


def find_all_cycles(graph_list):
    """
    Zadanie 4: Znajduje wszystkie unikalne cykle przy użyciu Backtrackingu (DFS).
    """
    n = len(graph_list)
    visited = [False] * n
    path = []
    cycles = set()
    
    def dfs_backtrack(v, parent):
        visited[v] = True
        path.append(v)
        
        for u in graph_list[v]:
            if not visited[u]:
                dfs_backtrack(u, v)
            elif u != parent and u in path:
                # Cykl wykryty - wyciągamy odcinek ścieżki stanowiący cykl
                cycle_start_idx = path.index(u)
                cycle = path[cycle_start_idx:]
                
                # Normalizacja cyklu, by uniknąć duplikatów (np. 1-2-3 == 3-2-1 == 2-3-1)
                # Znajdujemy najmniejszy element, ustalamy kierunek
                min_idx = cycle.index(min(cycle))
                cycle_rotated = cycle[min_idx:] + cycle[:min_idx]
                if cycle_rotated[1] > cycle_rotated[-1]:
                    cycle_rotated = [cycle_rotated[0]] + cycle_rotated[1:][::-1]
                
                cycles.add(tuple(cycle_rotated))
                
        # Backtracking - cofamy stan
        path.pop()
        visited[v] = False

    # Uruchamiamy z każdego wierzchołka, by złapać izolowane komponenty
    for start_node in range(n):
        dfs_backtrack(start_node, -1)
        
    return list(cycles)