import csv
import os
import random
import time
import numpy as np

from src.greedy import greedy
from src.sl import SL
from src.lf import LF
from src.dimacs import dimacs_to_adj
from src.graph_gen import generate_all_collections
from src.bounds import chromatic_bounds, edge_count

NUM_TRIALS_DIMACS = 30
NUM_TRIALS_COLLECTION = 10
NUM_TRIALS_LARGE = 3

ALGORITHMS = ['GREEDY', 'SL', 'LF']
OUT_DIR = 'out'
os.makedirs(OUT_DIR, exist_ok=True)


def run_experiment(graph, num_trials):
    n = len(graph)
    results = {alg: {'colors': [], 'time': 0.0} for alg in ALGORITHMS}

    for _ in range(num_trials):
        pi = list(range(n))
        random.shuffle(pi)
        t0 = time.time()
        _, gc = greedy(graph, pi)
        results['GREEDY']['time'] += time.time() - t0
        results['GREEDY']['colors'].append(gc)

        t0 = time.time()
        _, sc = SL(graph)
        results['SL']['time'] += time.time() - t0
        results['SL']['colors'].append(sc)

        t0 = time.time()
        _, lc = LF(graph, random_tiebreak=True)
        results['LF']['time'] += time.time() - t0
        results['LF']['colors'].append(lc)

    return results


def compute_stats(colors_list):
    return {
        'mean': np.mean(colors_list),
        'median': np.median(colors_list),
        'min': int(np.min(colors_list)),
        'max': int(np.max(colors_list)),
    }


def collection_label(n, m):
    """T_50_100 zamiast T(50,100) - bezpieczne dla CSV."""
    return f"T_{n}_{m}"


# ======================================================================
# WCZYTYWANIE GRAFÓW
# ======================================================================

print("Wczytywanie grafów DIMACS...")
dimacs_files = {
    'dsjc250_5':     'dimacs/dsjc250_5.col',
    'dsjr500_1c':    'dimacs/dsjr500_1c.col',
    'flat300_28_0': 'dimacs/flat300_28_0.col',
    'flat1000_50_0': 'dimacs/flat1000_50_0.col',
    'latin_square': 'dimacs/latin_square.col',
    'le450_25c':    'dimacs/le450_25c.col',
    'le450_25d':    'dimacs/le450_25d.col',
    'r250_5':       'dimacs/r250_5.col',
}

dimacs_graphs = {}
for name, filename in dimacs_files.items():
    try:
        g = dimacs_to_adj(filename)
        dimacs_graphs[name] = g
        print(f"  {name}: n={len(g)}, m={edge_count(g)}")
    except FileNotFoundError:
        print(f"  {name}: BRAK PLIKU")

print("\nGenerowanie kolekcji T(n,m)...")
collections = generate_all_collections(count=15, seed=42)


# ======================================================================
# ZADANIE 3a) - EKSPERYMENTY -> CSV
# ======================================================================

stats_rows = []

print(f"\nEksperymenty 3a)...")

for name, g in dimacs_graphs.items():
    n = len(g)
    m = edge_count(g)
    print(f"  {name}...", end=" ", flush=True)
    results = run_experiment(g, NUM_TRIALS_DIMACS)
    for alg in ALGORITHMS:
        s = compute_stats(results[alg]['colors'])
        stats_rows.append({
            'graph': name,
            'type': 'DIMACS',
            'n': n,
            'm': m,
            'algorithm': alg,
            'trials': NUM_TRIALS_DIMACS,
            'mean': round(s['mean'], 2),
            'median': round(s['median'], 2),
            'min': s['min'],
            'max': s['max'],
            'total_time_s': round(results[alg]['time'], 4),
        })
    print("OK")

for (n, m), graphs in collections.items():
    label = collection_label(n, m)
    print(f"  {label}...", end=" ", flush=True)
    merged = {alg: {'colors': [], 'time': 0.0} for alg in ALGORITHMS}
    trials = NUM_TRIALS_LARGE if n >= 500 else NUM_TRIALS_COLLECTION
    for g in graphs:
        r = run_experiment(g, trials)
        for alg in ALGORITHMS:
            merged[alg]['colors'].extend(r[alg]['colors'])
            merged[alg]['time'] += r[alg]['time']
    actual_m = int(np.mean([edge_count(g) for g in graphs]))
    for alg in ALGORITHMS:
        s = compute_stats(merged[alg]['colors'])
        stats_rows.append({
            'graph': label,
            'type': 'generated',
            'n': n,
            'm': actual_m,
            'algorithm': alg,
            'trials': trials * len(graphs),
            'mean': round(s['mean'], 2),
            'median': round(s['median'], 2),
            'min': s['min'],
            'max': s['max'],
            'total_time_s': round(merged[alg]['time'], 4),
        })
    print("OK")

stats_path = os.path.join(OUT_DIR, 'stats.csv')
fieldnames = ['graph', 'type', 'n', 'm', 'algorithm', 'trials',
              'mean', 'median', 'min', 'max', 'total_time_s']
with open(stats_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(stats_rows)
print(f"\nZapisano statystyki -> {stats_path}")


# ======================================================================
# ZADANIE 3b) - OSZACOWANIA -> CSV
# ======================================================================

bounds_rows = []

print("\nOszacowania 3b)...")

for name, g in dimacs_graphs.items():
    b = chromatic_bounds(g)
    best_wa = None
    for row in stats_rows:
        if row['graph'] == name:
            wa = row['max']
            if best_wa is None or wa < best_wa:
                best_wa = wa
    bounds_rows.append({
        'graph': name, 'type': 'DIMACS',
        'n': b['n'], 'm': b['m'],
        'omega': b['omega'],
        'mycielski_bound': round(b['mycielski_bound'], 2),
        'best_W_A': best_wa,
        'delta_plus_1': b['delta_plus_1'],
        'sqrt_2m_plus_1': round(b['sqrt_2m_plus_1'], 2),
    })

for (n, m), graphs in collections.items():
    label = collection_label(n, m)
    all_b = [chromatic_bounds(g) for g in graphs]
    avg = lambda key: round(np.mean([b[key] for b in all_b]), 2)
    best_wa = None
    for row in stats_rows:
        if row['graph'] == label:
            wa = row['max']
            if best_wa is None or wa < best_wa:
                best_wa = wa
    bounds_rows.append({
        'graph': label, 'type': 'generated',
        'n': n, 'm': int(np.mean([b['m'] for b in all_b])),
        'omega': int(np.mean([b['omega'] for b in all_b])),
        'mycielski_bound': avg('mycielski_bound'),
        'best_W_A': best_wa,
        'delta_plus_1': int(np.mean([b['delta_plus_1'] for b in all_b])),
        'sqrt_2m_plus_1': avg('sqrt_2m_plus_1'),
    })

bounds_path = os.path.join(OUT_DIR, 'bounds.csv')
bounds_fields = ['graph', 'type', 'n', 'm', 'omega', 'mycielski_bound',
                 'best_W_A', 'delta_plus_1', 'sqrt_2m_plus_1']
with open(bounds_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=bounds_fields)
    writer.writeheader()
    writer.writerows(bounds_rows)
print(f"Zapisano oszacowania -> {bounds_path}")

print("\nGotowe!")
