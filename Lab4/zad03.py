import argparse
from graph import load_graph_from_file

parser = argparse.ArgumentParser(description ='')
parser.add_argument('start', type = str)
parser.add_argument('finisz', type = str)

args = parser.parse_args()
start = args.start
finisz = args.finisz

g = load_graph_from_file("siec_miast.txt", isDirected=False)

if g and g.graph:
    miasta = sorted(list(g.graph.keys()))
    print(f"Załadowane miasta: {', '.join(miasta)}")
    print("-" * 60)

    print("[ZADANIE 3] Wyznaczanie tras między dwoma miastami:")

    if start not in g.graph or finisz not in g.graph:
        print("Błąd: Sprawdź pisownię. Podane miasta nie istnieją w pliku.")
    else:
        sk_l, d_sk_l = g.shortest_path_adj_list(start, finisz)
        sd_l, d_sd_l = g.longest_path_adj_list(start, finisz)

        sk_m, d_sk_m = g.shortest_path_adj_matrix(start, finisz)
        sd_m, d_sd_m = g.longest_path_adj_matrix(start, finisz)

        print("\nWyniki dla reprezentacji LISTY SĄSIEDZTWA:")
        print(f" -> Najkrótsza ścieżka: {' -> '.join(sk_l)} | Dystans: {d_sk_l}")
        print(f" -> Najdłuższa ścieżka: {' -> '.join(sd_l)} | Dystans: {d_sd_l}")

        print("\nWyniki dla reprezentacji MACIERZY SĄSIEDZTWA:")
        print(f" -> Najkrótsza ścieżka: {' -> '.join(sk_m)} | Dystans: {d_sk_m}")
        print(f" -> Najdłuższa ścieżka: {' -> '.join(sd_m)} | Dystans: {d_sd_m}")
