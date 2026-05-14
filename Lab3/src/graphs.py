# Moduł odpowiedzialny za reprezentacje grafów (Lista sąsiedztwa i Macierz sąsiedztwa)
# oraz wczytywanie danych.

def adj_list_to_matrix(adj_list):
    """Konwertuje listę sąsiedztwa na macierz sąsiedztwa."""
    n = len(adj_list)
    matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in adj_list[u]:
            matrix[u][v] = 1
    return matrix

def matrix_to_adj_list(matrix):
    """Konwertuje macierz sąsiedztwa na listę sąsiedztwa."""
    n = len(matrix)
    adj_list = [[] for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if matrix[u][v] == 1:
                adj_list[u].append(v)
    return adj_list

def generate_sample_graph():
    """
    Generuje prosty, nieskierowany graf z wykładu do testów (Zadanie 7a).
    Graf posiada cykle, co pozwoli przetestować algorytmy.
    """
    # 0: s, 1: z, 2: y, 3: x, 4: w, 5: v, 6: u, 7: t
    adj = [
        [1, 4],       # 0 (s) połączony z z(1), w(4)
        [0, 2, 4],    # 1 (z) połączony z s(0), y(2), w(4)
        [1, 3],       # 2 (y) połączony z z(1), x(3)
        [2, 4],       # 3 (x) połączony z y(2), w(4)
        [0, 1, 3, 5], # 4 (w) połączony z s(0), z(1), x(3), v(5)
        [4, 6, 7],    # 5 (v) połączony z w(4), u(6), t(7)
        [5, 7],       # 6 (u) połączony z v(5), t(7)
        [5, 6]        # 7 (t) połączony z v(5), u(6)
    ]
    return adj