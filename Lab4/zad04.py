from graph import load_graph_from_file

print("[ZADANIE 4]")

g = load_graph_from_file("siec_miast.txt", isDirected=False)

# a)
shortest_cycle, shortest_weight = g.shortest_hamiltonian_cycle()

print("Najkrótszy cykl:")
print(shortest_cycle)
print("Długość:", shortest_weight)

# b)
longest_cycle, longest_weight = g.longest_hamiltonian_cycle()

print("Najdłuższy cykl:")
print(longest_cycle)
print("Długość:", longest_weight)
