import math


def max_degree(graph):
    """Δ(G) - maksymalny stopień wierzchołka."""
    return max(len(adj) for adj in graph)


def edge_count(graph):
    """Liczba krawędzi grafu."""
    return sum(len(adj) for adj in graph) // 2


def clique_number_greedy(graph):
    """ω(G) - przybliżenie liczby klikowej (heurystyka zachłanna).
    Dolne ograniczenie na ω(G).
    """
    n = len(graph)
    adj_sets = [set(graph[v]) for v in range(n)]
    best = 1
    for start in range(min(n, 50)):
        clique = {start}
        candidates = adj_sets[start].copy()
        while candidates:
            v = max(candidates, key=lambda x: len(adj_sets[x] & candidates))
            clique.add(v)
            candidates &= adj_sets[v]
        best = max(best, len(clique))
    return best


def chromatic_bounds(graph):
    """Wyznacza oszacowania liczby chromatycznej z zadania 3b).

    Dolne ograniczenia:
        ω(G) ≤ χ(G)
        n² / (n² - 2m) ≤ χ(G)

    Górne ograniczenia:
        χ(G) ≤ W_A(G)               (wynik algorytmu)
        χ(G) ≤ Δ(G) + 1             (tw. Brooksa)
        χ(G) ≤ P(G) + 1             (najdłuższa ścieżka + 1)
        χ(G) ≤ √(2m) + 1

    Zwraca słownik z wynikami.
    """
    n = len(graph)
    m = edge_count(graph)
    delta = max_degree(graph)
    omega = clique_number_greedy(graph)

    denom = n * n - 2 * m
    mycielski = (n * n) / denom if denom > 0 else float('inf')

    return {
        'n': n,
        'm': m,
        'delta': delta,
        'omega': omega,                         # ω(G)         — dolne
        'mycielski_bound': mycielski,            # n²/(n²-2m)   — dolne
        'delta_plus_1': delta + 1,               # Δ(G)+1       — górne
        'sqrt_2m_plus_1': math.sqrt(2 * m) + 1,  # √(2m)+1      — górne
    }
