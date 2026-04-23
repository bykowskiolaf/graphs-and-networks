import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import re

matplotlib.rcParams['figure.dpi'] = 150
matplotlib.rcParams['font.size'] = 10

OUT_DIR = 'out'

stats = pd.read_csv(os.path.join(OUT_DIR, 'stats.csv'))
bounds = pd.read_csv(os.path.join(OUT_DIR, 'bounds.csv'))


def pretty_label(name):
    """T_50_100 -> T(50, 100) na wykresach."""
    m = re.match(r'T_(\d+)_(\d+)', name)
    if m:
        return f"T({m.group(1)}, {m.group(2)})"
    return name


# ======================================================================
# Wykres 1: Średnia liczba kolorów — kolekcje T(n,m)
# ======================================================================

gen = stats[stats['type'] == 'generated'].copy()
labels = gen['graph'].unique()
pretty = [pretty_label(l) for l in labels]

fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(labels))
width = 0.25

for i, alg in enumerate(['GREEDY', 'SL', 'LF']):
    means = [gen[(gen['graph'] == l) & (gen['algorithm'] == alg)]['mean'].values[0]
             for l in labels]
    ax.bar(x + i * width, means, width, label=alg)

ax.set_xlabel('Kolekcja')
ax.set_ylabel('Średnia liczba kolorów')
ax.set_title('Zadanie 3a) Średnia liczba kolorów — kolekcje T(n,m)')
ax.set_xticks(x + width)
ax.set_xticklabels(pretty, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_collections_mean.png'))
plt.close()
print("Zapisano: chart_collections_mean.png")


# ======================================================================
# Wykres 2: Min / Max / Średnia — grafy DIMACS
# ======================================================================

dim = stats[stats['type'] == 'DIMACS'].copy()
graphs = dim['graph'].unique()
algs = ['GREEDY', 'SL', 'LF']

fig, axes = plt.subplots(1, len(graphs), figsize=(5 * len(graphs), 5), sharey=False)
if len(graphs) == 1:
    axes = [axes]

for ax, gname in zip(axes, graphs):
    subset = dim[dim['graph'] == gname]
    x = np.arange(len(algs))
    mins  = [subset[subset['algorithm'] == a]['min'].values[0] for a in algs]
    means = [subset[subset['algorithm'] == a]['mean'].values[0] for a in algs]
    maxs  = [subset[subset['algorithm'] == a]['max'].values[0] for a in algs]

    ax.bar(x - 0.2, mins, 0.2, label='Min', color='#2ecc71')
    ax.bar(x,       means, 0.2, label='Średnia', color='#3498db')
    ax.bar(x + 0.2, maxs, 0.2, label='Max', color='#e74c3c')

    ax.set_xticks(x)
    ax.set_xticklabels(algs)
    ax.set_title(gname)
    ax.set_ylabel('Liczba kolorów')
    ax.legend(fontsize=8)
    ax.grid(axis='y', alpha=0.3)

plt.suptitle('Zadanie 3a) Min / Średnia / Max — grafy DIMACS', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_dimacs_stats.png'), bbox_inches='tight')
plt.close()
print("Zapisano: chart_dimacs_stats.png")


# ======================================================================
# Wykres 3: Czasy działania
# ======================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

for i, alg in enumerate(algs):
    sub = dim[dim['algorithm'] == alg]
    ax1.bar(np.arange(len(graphs)) + i * 0.25, sub['total_time_s'].values, 0.25, label=alg)
ax1.set_xticks(np.arange(len(graphs)) + 0.25)
ax1.set_xticklabels(graphs, rotation=30, ha='right')
ax1.set_ylabel('Czas [s]')
ax1.set_title('Czasy — DIMACS')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

labels_gen = gen['graph'].unique()
pretty_gen = [pretty_label(l) for l in labels_gen]
for i, alg in enumerate(algs):
    sub = gen[gen['algorithm'] == alg]
    ax2.bar(np.arange(len(labels_gen)) + i * 0.25, sub['total_time_s'].values, 0.25, label=alg)
ax2.set_xticks(np.arange(len(labels_gen)) + 0.25)
ax2.set_xticklabels(pretty_gen, rotation=45, ha='right')
ax2.set_ylabel('Czas [s]')
ax2.set_title('Czasy — kolekcje T(n,m)')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.suptitle('Czasy działania algorytmów', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_times.png'), bbox_inches='tight')
plt.close()
print("Zapisano: chart_times.png")


# ======================================================================
# Wykres 4: Oszacowania chromatyczne — DIMACS
# ======================================================================

dim_bounds = bounds[bounds['type'] == 'DIMACS']

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(dim_bounds))
names = dim_bounds['graph'].values

ax.scatter(x, dim_bounds['omega'], s=100, marker='v', zorder=5, label='ω(G) — dolne')
ax.scatter(x, dim_bounds['mycielski_bound'], s=100, marker='^', zorder=5, label='n²/(n²−2m) — dolne')
ax.scatter(x, dim_bounds['best_W_A'], s=120, marker='D', zorder=5, label='najlepszy W_A(G)')
ax.scatter(x, dim_bounds['delta_plus_1'], s=100, marker='s', zorder=5, label='Δ(G)+1 — górne')
ax.scatter(x, dim_bounds['sqrt_2m_plus_1'], s=100, marker='o', zorder=5, label='√(2m)+1 — górne')

ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylabel('Oszacowanie χ(G)')
ax.set_title('Zadanie 3b) Oszacowania liczby chromatycznej — DIMACS')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_bounds_dimacs.png'))
plt.close()
print("Zapisano: chart_bounds_dimacs.png")


# ======================================================================
# Wykres 5: Oszacowania chromatyczne — kolekcje T(n,m)
# ======================================================================

gen_bounds = bounds[bounds['type'] == 'generated']
pretty_bounds = [pretty_label(n) for n in gen_bounds['graph'].values]

fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(gen_bounds))

ax.plot(x, gen_bounds['omega'].values, 'v-', label='ω(G) — dolne', markersize=8)
ax.plot(x, gen_bounds['mycielski_bound'].values, '^-', label='n²/(n²−2m) — dolne', markersize=8)
ax.plot(x, gen_bounds['best_W_A'].values, 'D-', label='najlepszy W_A(G)', markersize=8)
ax.plot(x, gen_bounds['delta_plus_1'].values, 's-', label='Δ(G)+1 — górne', markersize=8)
ax.plot(x, gen_bounds['sqrt_2m_plus_1'].values, 'o-', label='√(2m)+1 — górne', markersize=8)

ax.set_xticks(x)
ax.set_xticklabels(pretty_bounds, rotation=45, ha='right')
ax.set_ylabel('Oszacowanie χ(G)')
ax.set_title('Zadanie 3b) Oszacowania liczby chromatycznej — kolekcje T(n,m)')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_bounds_collections.png'))
plt.close()
print("Zapisano: chart_bounds_collections.png")

print("\nWszystkie wykresy wygenerowane!")
