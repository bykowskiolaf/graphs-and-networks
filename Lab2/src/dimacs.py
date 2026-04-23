# Odczyt grafu z formatu DIMACS do listy sąsiedztw.
def dimacs_to_adj(filepath):
    G = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('p'):
                parts = line.split()
                n = int(parts[2])
                G = [[] for _ in range(n)]
            elif line.startswith('e'):
                _, a, b = line.split()
                a, b = int(a) - 1, int(b) - 1
                G[a].append(b)
                G[b].append(a)
    return G
