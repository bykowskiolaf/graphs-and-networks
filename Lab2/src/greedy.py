# Klasyczny algorytm zachłanny kolorowania grafu.
# Zwraca listę kolorów (indeksy od 0) oraz liczbę użytych kolorów.
def greedy(G, pi=[]):
    max_colour = 0
    colors = [None] * len(G)
    if not pi:
        pi = range(len(G))
    for v in pi:
        nbr_colors = {colors[n] for n in G[v] if colors[n] is not None}
        k = 0
        while k in nbr_colors:
            k += 1
        colors[v] = k
        if k > max_colour:
            max_colour = k
    return colors, max_colour + 1
