# Realizacja Zadania 2 oraz Zadania 5 (wizualizacja stosu)
from src.viz import print_stack_state

def dfs_iterative(graph, start=0, use_matrix=False, show_stack=False):
    """
    Zadanie 2: DFS iteracyjnie ze stosem jawnym.
    Zadanie 5: Wyświetlanie stanu stosu w grafice ASCII.
    """
    n = len(graph)
    visited = [False] * n
    pre = [0] * n
    post = [0] * n
    timer = 1
    
    # Stos przechowuje krotki: (wierzchołek, czy_odwiedzony_wcześniej)
    # Flaga pozwala odróżnić moment wejścia (PRE) od wyjścia (POST)
    stack = [(start, False)]
    
    while stack:
        if show_stack:
            print_stack_state(stack)
            
        v, is_post = stack.pop()
        
        if is_post:
            # Moment zamknięcia wierzchołka
            post[v] = timer
            timer += 1
        else:
            if not visited[v]:
                visited[v] = True
                pre[v] = timer
                timer += 1
                
                # Zrzucamy na stos flagę POST, by oznaczyć zamknięcie gdy do niego wrócimy
                stack.append((v, True))
                
                neighbors = []
                if use_matrix:
                    neighbors = [u for u in range(n) if graph[v][u] == 1]
                else:
                    neighbors = graph[v]
                
                # Odwracamy kolejność, aby zachować identyczny z rekurencją
                # porządek odwiedzania (lewe gałęzie najpierw)
                for u in reversed(neighbors):
                    if not visited[u]:
                        stack.append((u, False))
                        
    return pre, post