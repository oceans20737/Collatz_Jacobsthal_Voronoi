# -*- coding: utf-8 -*-
"""code_01_collatz_voronoi.ipynb
"""

# ============================================================
# Collatz Orbit Prologue Visualizer (Voronoi + Trajectory Map)
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

# ============================================================
# CONFIGURATION
# ============================================================
ORBIT_START = 7     # Initial value for the Collatz odd orbit
N_DRAW = 500        # Range of natural numbers to visualize
N_VORONOI = 2000    # Number of points for Voronoi stabilization

# ============================================================
# Core Functions
# ============================================================
def get_odd_collatz_orbit(n):
    """Generate the odd Collatz orbit starting from n until reaching 1."""
    orbit = [n]
    while n != 1:
        n = 3 * n + 1
        while n % 2 == 0:
            n //= 2
        orbit.append(n)
    return orbit

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
def create_prologue_map():
    orbit = get_odd_collatz_orbit(ORBIT_START)
    print(f"[System] Odd Collatz Orbit for {ORBIT_START}: {orbit}")

    # --------------------------------------------------------
    # Voronoi Coordinates
    # --------------------------------------------------------
    coords = np.array([get_spiral_pos(i) for i in range(1, N_VORONOI + 1)])
    max_r = np.log2(max(N_DRAW, N_VORONOI))

    # Outer dummy points to stabilize Voronoi boundaries
    theta_dummy = np.linspace(0, 2 * np.pi, 120, endpoint=False)
    dummy = np.column_stack((max_r * 1.3 * np.cos(theta_dummy),
                             max_r * 1.3 * np.sin(theta_dummy)))

    all_coords = np.vstack((coords, dummy))
    vor = Voronoi(all_coords, qhull_options="QJ")

    # --------------------------------------------------------
    # Color Settings
    # --------------------------------------------------------
    ORBIT_COLOR = (0.0, 0.9, 1.0, 0.85)  # Cyan glow for orbit cells
    BG_COLOR = '#4a4a55'                # Background cell color
    EDGE_COLOR = '#222222'              # Voronoi boundary color

    fig, ax = plt.subplots(figsize=(12, 12), facecolor="#050508")
    ax.set_aspect("equal")
    ax.set_axis_off()

    limit = np.log2(N_DRAW) * 1.05
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    # --------------------------------------------------------
    # Voronoi Polygons
    # --------------------------------------------------------
    polys = []
    facecolors = []

    for i in range(N_DRAW):
        n = i + 1
        region = vor.regions[vor.point_region[i]]

        if not region or -1 in region:
            polys.append(np.array([[0, 0]]))
        else:
            polys.append(vor.vertices[region])

        if n in orbit:
            facecolors.append(to_rgba(ORBIT_COLOR))
        else:
            facecolors.append(to_rgba(BG_COLOR))

    poly_collection = PolyCollection(
        polys, facecolors=facecolors, edgecolors=EDGE_COLOR, linewidths=0.6
    )
    ax.add_collection(poly_collection)

    # --------------------------------------------------------
    # Trajectory Lines (simple straight connections)
    # --------------------------------------------------------
    for i in range(len(orbit) - 1):
        x1, y1 = get_spiral_pos(orbit[i])
        x2, y2 = get_spiral_pos(orbit[i + 1])
        ax.plot([x1, x2], [y1, y2], color="#ffffff", lw=2.2, alpha=0.9, zorder=4)

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------
    for n in range(1, N_DRAW + 1):
        x, y = get_spiral_pos(n)

        if n in orbit:
            # Highlight orbit numbers
            txt = ax.text(x, y, str(n), color="#ffffff", fontsize=16,
                          ha="center", va="center", fontweight='heavy', zorder=6)
            txt.set_path_effects([path_effects.withStroke(linewidth=4.0, foreground="#004466")])
        else:
            # Background numbers (small and subtle)
            txt = ax.text(x, y, str(n), color="#e0e0e0", fontsize=7,
                          ha="center", va="center", zorder=3)
            txt.set_path_effects([path_effects.withStroke(linewidth=1.0, foreground="#222222")])

    # --------------------------------------------------------
    # Save Image
    # --------------------------------------------------------
    plt.tight_layout()
    filename = f"collatz_prologue_orbit_{ORBIT_START}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor="#050508")
    print(f"[Success] Prologue Image saved as: {filename}")
    plt.show()

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    create_prologue_map()

