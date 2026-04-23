from collections import defaultdict
from src.greedy import greedy


class Buckets:
    # pole: lista list
    # dobre jest defaultdict, zeby nie trzeba bylo manualnie dodawac kubelkow
    _buckets = defaultdict(list)
    _graph = []

    # konstruktor na podstawie grafu
    # liczy stopnie i wrzuca indeksy wierzchołków do odpowiednich kubełków
    def __init__(self, graph):
        self._graph = [sublist[:] for sublist in graph]  # kopia grafu do wewnętrznej dla obiektu Buckets kopii grafu
        for v in range(len(self._graph)):  # iterujemy po indeksach wierzchołków
            degree = len(self._graph[v])  # w liście sąsiedztw stopień wierzchołka to długość listy jego sąsiadów
            self._buckets[degree].append(v)

    # funkcja do pobrania i usunięcia wierzchołka
    # znalezc sasiadow i zrzucic wszystkich kubelek nizej
    def pop(self):
        # iteracja od najniższego do najwyższego stopnia
        for bucket in range(0, max(self._buckets.keys())):
            if self._buckets[bucket]:  # jeżeli kubełek nie jest pusty...
                v = self._buckets[bucket].pop()  # ...zwraca i usuwa ostatni element kubełka
                # znalezc sasiadow wierzchołka v i zrzucic ich kubelek nizej (bo ich stopień zmniejszył się o 1)
                neighbours = self._graph[v]
                for n in neighbours:  # n to indeks wierzchołka w tablicy
                    degree = len(self._graph[n])  # liczymy stopień wierzchołka n, żeby wiedzieć, w którym kubełku się znajduje
                    if degree > 0:
                        self._buckets[degree - 1].append(n)  # dodanie n do niższego kubełka
                    self._buckets[degree].remove(n)  # usunięcie n ze starego kubełka
                    # usunięcie v z listy sąsiedztw n
                    self._graph[n].remove(v)
                # usunięcie wierzchołka z kopii grafu
                self._graph[v] = []  # dla zachowania porządku struktury: zastąpienie listy sąsiedztw wierzchołka v pustą listą
                return v
        return None  # jeśli cała struktura jest pusta

    def generateOrder(self):
        pi = []
        while True:  # dopóki kubełki zawierają jakieś wierzchołki
            popped = self.pop()
            if popped is None:
                break
            # print("Popped:", popped)
            # print("Internal graph:", self._graph)
            # print("Buckets:", self._buckets)
            pi.append(popped)
        return pi


# Algorytm Smallest Last
# Zwraca listę kolorów oraz liczbę użytych kolorów.
def SL(graph):
    # utworzyc bucket z grafu
    b = Buckets(graph)
    # wygenerować porządkowanie za pomocą pop w pętli dopoki wewnetrzny graf nie bedzie pusty
    pi = b.generateOrder()
    # uruchomic greedy na uporzadkowaniu
    return greedy(graph, pi)
