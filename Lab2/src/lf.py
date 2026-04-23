import random
from src.greedy import greedy


def lf_ordering(graph, random_tiebreak=False):
    """Generuje uporządkowanie typu LF (Largest First).
    Wierzchołki sortowane malejąco wg stopnia w oryginalnym grafie G
    (Definicja 1.6 z wykładu: d_G(v_pi(i)) >= d_G(v_pi(i+1))).
    random_tiebreak: losowe rozstrzyganie remisów stopni
    (pozwala generować różne dopuszczalne uporządkowania LF).
    """
    n = len(graph)
    vertices = list(range(n))
    if random_tiebreak:
        # losowe przemieszanie, potem stabilny sort malejąco wg stopnia
        # -> wierzchołki o tym samym stopniu będą w losowej kolejności
        random.shuffle(vertices)
    vertices.sort(key=lambda v: len(graph[v]), reverse=True)
    return vertices


def LF(graph, random_tiebreak=False):
    """Algorytm Largest First.
    Zwraca listę kolorów oraz liczbę użytych kolorów.
    random_tiebreak=True -> losowe rozstrzyganie remisów stopni
    (przydatne do generowania wielu dopuszczalnych uporządkowań LF).
    """
    pi = lf_ordering(graph, random_tiebreak=random_tiebreak)
    return greedy(graph, pi)
