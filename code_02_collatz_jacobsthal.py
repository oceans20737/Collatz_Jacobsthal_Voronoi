# -*- coding: utf-8 -*-
"""code_02_collatz_jacobsthal.ipynb
"""

# ============================================================
# Collatz Jacobsthal Topology Visualizer (Stained Glass Edition)
# Author: Hiroshi Harada
# Date: May 23, 2026
# License: MIT License
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgba
import matplotlib.patheffects as path_effects

# Optional: text overlap avoidance (pip install adjustText)
try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False
    print("[Warning] 'adjustText' not found. Install it to reduce label overlap.")

# ============================================================
# CONFIGURATION
# ============================================================
TARGET_M = 1       # Root odd number M (e.g., 1, 5, 13, 17...)
N_DRAW = 2000      # Range of natural numbers to visualize
N_VORONOI = 5000   # Number of points used for Voronoi stabilization

# ============================================================
# Generalized Jacobsthal / Lucas Sequences
# ============================================================
def get_scaling_factor(m):
    """Empirical scaling factor based on inverse Collatz congruence conditions."""
    if m % 3 == 1:
        return m
    elif m % 3 == 2:
        return 2 * m
    else:
        return m  # Multiples of 3 are treated as auxiliary cases

A = get_scaling_factor(TARGET_M)

def gen_J(A, n):
    """Generalized Jacobsthal sequence J_n."""
    return int(round((A * (2**n) - (-1)**n) / 3))

def gen_3J(A, n):
    """Triple Jacobsthal sequence 3J_n."""
    return int(round(A * (2**n) - (-1)**n))

def gen_cJ(A, n):
    """Conjugate Jacobsthal (Lucas-type) sequence cJ_n."""
    return int(round(A * (2**n) + (-1)**n))

# ============================================================
# 2-adic Logarithmic Spiral Mapping
# ============================================================
def get_spiral_pos(n):
    """Map natural number n onto the 2-adic logarithmic spiral plane."""
    if n <= 0:
        return 0.0, 0.0
    r = np.log2(n)
    theta = 2 * np.pi * (r % 1)
    return r * np.cos(theta), r * np.sin(theta)

# ============================================================
# Main Visual Synthesis
# ============================================================
def create_mandala():
    print(f"[System] Voronoi tessellation for M={TARGET_M} (A={A})...")

    # Coordinates for Voronoi computation
    coords = np.array([get_spiral_pos(i) for i in range(1, N_VORONOI + 1)])
    max_r = np.log2(max(N_DRAW, N_VORONOI))

    # Outer dummy points to stabilize Voronoi boundaries
    theta_dummy = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    dummy = np.column_stack((max_r * 1.3 * np.cos(theta_dummy),
                             max_r * 1.3 * np.sin(theta_dummy)))

    all_coords = np.vstack((coords, dummy))
    vor = Voronoi(all_coords, qhull_options="QJ")

    # ========================================================
    # Sequence Extraction
    # ========================================================
    def seq_filter(values):
        return {v for v in values if 1 <= v <= N_DRAW}

    set_J_even  = seq_filter([gen_J(A, 2*n)     for n in range(40)])
    set_J_odd   = seq_filter([gen_J(A, 2*n+1)   for n in range(40)])
    set_3J_even = seq_filter([gen_3J(A, 2*n)    for n in range(40)])
    set_3J_odd  = seq_filter([gen_3J(A, 2*n+1)  for n in range(40)])
    set_cJ_even = seq_filter([gen_cJ(A, 2*n)    for n in range(40)])
    set_cJ_odd  = seq_filter([gen_cJ(A, 2*n+1)  for n in range(40)])
    set_2b      = seq_filter([TARGET_M * (2**b) for b in range(40)])

    all_seq_nums = (
        set_J_even | set_J_odd | set_3J_even | set_3J_odd |
        set_cJ_even | set_cJ_odd | set_2b
    )

    # ========================================================
    # Color Palette (Stained Glass)
    # ========================================================
    COLOR_J_EVEN  = '#00e5ff'
    COLOR_J_ODD   = '#0033ff'
    COLOR_3J_EVEN = '#ff00aa'
    COLOR_3J_ODD  = '#ff2200'
    COLOR_cJ_EVEN = '#00cc00'
    COLOR_cJ_ODD  = '#55ff00'
    COLOR_2b      = '#ffee00'

    seq_colors = {}

    for n in all_seq_nums:
        is_J  = (n in set_J_even) or (n in set_J_odd)
        is_3J = (n in set_3J_even) or (n in set_3J_odd)
        is_cJ = (n in set_cJ_even) or (n in set_cJ_odd)
        is_2b = (n in set_2b)

        # Rare triple intersection → white
        if is_J and is_3J and is_cJ:
            seq_colors[n] = '#ffffff'
        elif n == TARGET_M:
            seq_colors[n] = '#ffffff'
        elif is_J and is_3J:
            seq_colors[n] = '#9900ff'
        elif is_J and is_cJ:
            seq_colors[n] = '#00ffcc'
        elif is_cJ and is_2b:
            seq_colors[n] = '#ccff00'
        elif n in set_3J_odd:  seq_colors[n] = COLOR_3J_ODD
        elif n in set_3J_even: seq_colors[n] = COLOR_3J_EVEN
        elif n in set_2b:      seq_colors[n] = COLOR_2b
        elif n in set_cJ_odd:  seq_colors[n] = COLOR_cJ_ODD
        elif n in set_cJ_even: seq_colors[n] = COLOR_cJ_EVEN
        elif n in set_J_odd:   seq_colors[n] = COLOR_J_ODD
        elif n in set_J_even:  seq_colors[n] = COLOR_J_EVEN

    # ========================================================
    # Plot Setup
    # ========================================================
    fig, ax = plt.subplots(figsize=(16, 16), facecolor="#050508")
    ax.set_aspect("equal")
    ax.set_axis_off()

    limit = np.log2(N_DRAW) * 1.05
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    # ========================================================
    # Voronoi Polygons
    # ========================================================
    polys = []
    facecolors = []
    default_bg = to_rgba("#222222")

    for i in range(N_DRAW):
        n = i + 1
        region = vor.regions[vor.point_region[i]]
        if not region or -1 in region:
            polys.append(np.array([[0, 0]]))
        else:
            polys.append(vor.vertices[region])
        facecolors.append(to_rgba(seq_colors.get(n, default_bg)))

    poly_collection = PolyCollection(
        polys, facecolors=facecolors, edgecolors="#111111", linewidths=0.8
    )
    ax.add_collection(poly_collection)

    # ========================================================
    # Labels
    # ========================================================
    texts = []
    for n in range(1, N_DRAW + 1):
        if n not in seq_colors:
            continue

        x, y = get_spiral_pos(n)
        fs = 16 if n == TARGET_M else 9
        fw = 'heavy' if n == TARGET_M else 'bold'

        txt = ax.text(x, y, str(n), color="white", fontsize=fs,
                      ha="center", va="center", fontweight=fw, zorder=6)
        txt.set_path_effects([path_effects.withStroke(linewidth=2.5, foreground="black")])
        texts.append(txt)

    if HAS_ADJUST_TEXT and texts:
        print("[System] Adjusting text positions...")
        adjust_text(texts, ax=ax,
                    arrowprops=dict(arrowstyle="-", color='white', lw=0.5, alpha=0.5),
                    expand_points=(1.2, 1.2))

    # ========================================================
    # Save
    # ========================================================
    plt.tight_layout()
    filename = f"collatz_J-mandala_M{TARGET_M}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor="#050508")
    print(f"[Success] Image saved as: {filename}")
    plt.show()

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    create_mandala()

