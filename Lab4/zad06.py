import argparse
from graph import load_graph_from_file

parser = argparse.ArgumentParser(description='Zadanie 6 - Metoda zachłanna dla TSP')
parser.add_argument('--start', type=str, default='Warszawa', help='Miasto początkowe (domyślnie: Warszawa)')
args = parser.parse_args()
start_city = args.start

print("=" * 60)
print(f"[ZADANIE 6] Metoda zachłanna TSP (Miasto startowe: {start_city})")
print("=" * 60)

g = load_graph_from_file("siec_miast.txt", isDirected=False)

if g and g.graph:
    if start_city not in g.graph:
        print(f"Błąd: Miasto '{start_city}' nie istnieje w wczytanym grafie.")
    else:
        # a) Ścieżka możliwie najkrótsza
        path_min, weight_min = g.greedy_tsp(start_city, maximize=False)
        print("\na) Ścieżka możliwie NAJKRÓTSZA (metoda zachłanna):")
        if path_min:
            print(f"   -> Trasa: {' -> '.join(path_min)}")
            print(f"   -> Dystans całkowity: {weight_min}")
        else:
            print("   -> Błąd: Nie udało się wyznaczyć cyklu.")

        # b) Ścieżka możliwie najdłuższa
        path_max, weight_max = g.greedy_tsp(start_city, maximize=True)
        print("\nb) Ścieżka możliwie NAJDŁUŻSZA (metoda zachłanna):")
        if path_max:
            print(f"   -> Trasa: {' -> '.join(path_max)}")
            print(f"   -> Dystans całkowity: {weight_max}")
        else:
            print("   -> Błąd: Nie udało się wyznaczyć cyklu.")