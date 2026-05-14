import os
from src.graphs import generate_sample_graph, adj_list_to_matrix
from src.dfs_recursive import dfs_recursive
from src.dfs_iterative import dfs_iterative
from src.applications import is_tree, find_all_cycles
from src.viz import draw_intervals

def main():
    print("="*60)
    print(" GRIS: Laboratoria 9 - 11 (Przeszukiwanie i Backtracking)")
    print("="*60)
    
    # Inicjalizacja danych
    adj_list = generate_sample_graph()
    adj_matrix = adj_list_to_matrix(adj_list)
    names = ['s', 'z', 'y', 'x', 'w', 'v', 'u', 't']
    
    print("\n[Zadanie 1] DFS Rekurencyjny (Lista Sąsiedztwa)")
    pre_rec, post_rec = dfs_recursive(adj_list, start=0, use_matrix=False)
    for i in range(len(adj_list)):
        print(f"  {names[i]} -> pre: {pre_rec[i]:02d}, post: {post_rec[i]:02d}")

    print("\n[Zadanie 1] DFS Rekurencyjny (Macierz Sąsiedztwa)")
    pre_rec_m, post_rec_m = dfs_recursive(adj_matrix, start=0, use_matrix=True)
    print("  Wyniki identyczne z listą:", pre_rec == pre_rec_m and post_rec == post_rec_m)

    print("\n[Zadanie 6] DFS Rekurencyjny z max_depth = 2")
    pre_d, post_d = dfs_recursive(adj_list, start=0, max_depth=2)
    visited_nodes = [names[i] for i in range(len(adj_list)) if pre_d[i] > 0]
    print(f"  Odwiedzone węzły: {visited_nodes}")

    print("\n[Zadanie 2 & 5] DFS Iteracyjny z wizualizacją stosu ASCII")
    # Zmniejszamy graf dla czytelności stosu
    small_graph = [[1, 2], [0, 3], [0], [1]]
    dfs_iterative(small_graph, start=0, show_stack=True)

    print("\n[Zadanie 3] Czy graf jest drzewem?")
    # Graf testowy posiada cykle
    print("  Graf testowy (z wykładu):", "TAK" if is_tree(adj_list) else "NIE")
    tree_graph = [[1, 2], [0], [0, 3], [2]] # Proste drzewo (Gwiazda + 1)
    print("  Proste drzewo (0-1, 0-2, 2-3):", "TAK" if is_tree(tree_graph) else "NIE")

    print("\n[Zadanie 4] Detekcja cykli (Backtracking)")
    cycles = find_all_cycles(adj_list)
    print(f"  Znaleziono {len(cycles)} unikalnych cykli:")
    for c in cycles:
        cycle_names = [names[idx] for idx in c]
        print(f"  - {' -> '.join(cycle_names)} -> {cycle_names[0]}")

    print("\n[Zadanie 7] Wizualizacja przedziałów otwarcia (ASCII)")
    # Rysujemy przedziały dla rekurencyjnego DFS wywołanego na początku
    draw_intervals(pre_rec, post_rec, names)

if __name__ == "__main__":
    main()