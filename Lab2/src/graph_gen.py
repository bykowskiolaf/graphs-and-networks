import random
import networkx as nx


def nx_to_adj(G_nx):
    """Konwertuje graf NetworkX na listę sąsiedztw."""
    n = G_nx.number_of_nodes()
    adj = [[] for _ in range(n)]
    for u, v in G_nx.edges():
        adj[u].append(v)
        adj[v].append(u)
    return adj


def generate_gnm_graph(n, m, seed=None):
    """Generuje graf G(n,m) jako listę sąsiedztw (bez pętli i multikrawędzi)."""
    return nx_to_adj(nx.gnm_random_graph(n, m, seed=seed))


def generate_collection(n, m, count=15):
    """Generuje kolekcję T(n,m) - `count` grafów z ±5% odchyleniem od m."""
    max_edges = n * (n - 1) // 2
    if m > max_edges:
        print(f"UWAGA: T({n},{m}) - max krawędzi to {max_edges}, pomijam.")
        return []
    deviation = int(m * 0.05)
    graphs = []
    for _ in range(count):
        m_actual = random.randint(max(0, m - deviation), min(max_edges, m + deviation))
        graphs.append(generate_gnm_graph(n, m_actual))
    return graphs


# Wszystkie kolekcje z treści zadania
COLLECTION_PARAMS = [
    (50, 100), (50, 500), (50, 800),
    (200, 1600), (200, 8000), (200, 12800),
    (500, 10000), (500, 50000), (500, 80000),
]


def generate_all_collections(count=15, seed=42):
    """Generuje wszystkie kolekcje T(n,m) z zadania 2b).
    Zwraca słownik: {(n,m): [lista grafów]}.
    """
    random.seed(seed)
    collections = {}
    for n, m in COLLECTION_PARAMS:
        print(f"  T({n},{m})...", end=" ", flush=True)
        collections[(n, m)] = generate_collection(n, m, count=count)
        print(f"OK ({len(collections[(n,m)])} grafów)")
    return collections
