from graph import load_graph_from_file

print("=" * 60)
print("[ZADANIE 5] Ograniczenia dla problemu komiwojażera (TSP)")
print("=" * 60)

g = load_graph_from_file("siec_miast.txt", isDirected=False)

if g and g.graph:
    # a) Dolne ograniczenie dla problemu komiwojażera (Minimalne Drzewo Spinające - MST)
    mst_edges, mst_weight = g.kruskal_spanning_tree(maximize=False)
    print("\na) DOLNE OGRANICZENIE (wykorzystując Minimalne Drzewo Spinające):")
    print(f"   -> Waga minimalnego drzewa spinającego: {mst_weight}")
    
    # b) Górne ograniczenie dla problemu komiwojażera (Maksymalne Drzewo Spinające - MaxST)
    maxst_edges, maxst_weight = g.kruskal_spanning_tree(maximize=True)
    print("\nb) GÓRNE OGRANICZENIE (wykorzystując Maksymalne Drzewo Spinające):")
    print(f"   -> Waga maksymalnego drzewa spinającego: {maxst_weight}")