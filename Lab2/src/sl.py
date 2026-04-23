from collections import defaultdict
from lib.greedy import greedy


class BucketsSL:
    """Struktura kubełkowa dla algorytmu Smallest Last.
    Pobiera wierzchołki o najmniejszym stopniu w aktualnym grafie.
    """

    def __init__(self, graph):
        self._graph = [adj[:] for adj in graph]
        self._buckets = defaultdict(list)
        for v in range(len(self._graph)):
            self._buckets[len(self._graph[v])].append(v)

    def pop(self):
        for deg in range(max(self._buckets.keys()) + 1):
            if self._buckets[deg]:
                v = self._buckets[deg].pop()
                for n in self._graph[v]:
                    old_deg = len(self._graph[n])
                    if old_deg > 0:
                        self._buckets[old_deg - 1].append(n)
                    self._buckets[old_deg].remove(n)
                    self._graph[n].remove(v)
                self._graph[v] = []
                return v
        return None

    def generate_order(self):
        pi = []
        while True:
            v = self.pop()
            if v is None:
                break
            pi.append(v)
        return pi


def SL(graph):
    """Algorytm Smallest Last.
    Zwraca listę kolorów oraz liczbę użytych kolorów.
    """
    b = BucketsSL(graph)
    pi = b.generate_order()
    return greedy(graph, pi)
