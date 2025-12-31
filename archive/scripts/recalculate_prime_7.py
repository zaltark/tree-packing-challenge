import sys
from pathlib import Path
import numpy as np
import pandas as pd
import math
from decimal import Decimal
from shapely.ops import unary_union
from shapely.strtree import STRtree

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree
from scripts.visualize_results import plot_trees

def get_perfect_trio(r, rot_offset=0):
    trees = []
    for angle_deg in [0, 120, 240]:
        rad = math.radians(angle_deg + rot_offset)
        x = r * math.cos(rad)
        y = r * math.sin(rad)
        trees.append(ChristmasTree(x, y, angle_deg + rot_offset))
    return trees

def evaluate(trees):
    polys = [t.get_polygon() for t in trees]
    tree_index = STRtree(polys)
    for i in range(len(polys)):
        possible = tree_index.query(polys[i])
        for idx in possible:
            if idx > i:
                if polys[i].intersects(polys[idx]) and not polys[i].touches(polys[idx]):
                    return float('inf')
    bounds = unary_union(polys).bounds
    return max(bounds[2]-bounds[0], bounds[3]-bounds[1])

def solve_n7_hex():
    print("--- Recalculating N=7 Hex-Monolith (2 Trios + 1) ---")
    best_side = float('inf')
    best_trees = []
    
    # 1. First, find the tightest TRIO radius
    best_trio_r = 0.5
    for r in np.arange(0.3, 0.7, 0.01):
        trio = get_perfect_trio(r)
        if evaluate(trio) != float('inf'):
            best_trio_r = r
    print(f"Tightest Trio Radius: {best_trio_r:.4f}")

    # 2. Try to pack 2 such trios + 1 center tree
    # Search for the distance 'D' between trio centers and their rotation
    for d in np.arange(0.5, 1.5, 0.05):
        dec_d = Decimal(str(d))
        for rot1 in [0, 30, 60, 90, 120, 180]:
            for rot2 in [0, 30, 60, 90, 120, 180]:
                trees = [ChristmasTree(0, 0, 0)] # Center
                
                # Trio 1
                t1_center_x, t1_center_y = dec_d, Decimal('0')
                for t in get_perfect_trio(best_trio_r, rot_offset=rot1):
                    trees.append(ChristmasTree(t.center_x + t1_center_x, t.center_y + t1_center_y, t.angle))
                
                # Trio 2
                t2_center_x, t2_center_y = -dec_d, Decimal('0')
                for t in get_perfect_trio(best_trio_r, rot_offset=rot2):
                    trees.append(ChristmasTree(t.center_x + t2_center_x, t.center_y + t2_center_y, t.angle))
                
                if len(trees) > 7: trees = trees[:7]
                
                side = evaluate(trees)
                if side < best_side:
                    best_side = side
                    best_trees = trees

    if best_trees:
        score = (best_side**2)/7
        print(f"SUCCESS: Found N=7 Hex Layout with Side={best_side:.4f}, Score={score:.4f}")
        data = [{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in best_trees]
        plot_trees(pd.DataFrame(data), output_path=PROJECT_ROOT / "results" / "plots" / "prime_7_hex_monolith.png")
    else:
        print("Failed to find valid hex-trio packing for N=7.")

if __name__ == "__main__":
    solve_n7_hex()