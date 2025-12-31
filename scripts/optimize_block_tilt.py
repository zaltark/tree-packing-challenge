import sys
from pathlib import Path
import pandas as pd
import math
import numpy as np
from shapely.affinity import rotate
from shapely.ops import unary_union
from shapely.strtree import STRtree

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

def optimize_global_rotation(trees, step=2):
    """Rotates the entire cluster to minimize bounding square."""
    if not trees: return trees, 0
    all_polys = [t.get_polygon() for t in trees]
    union_poly = unary_union(all_polys)
    scx, scy = union_poly.centroid.x, union_poly.centroid.y
    
    best_side = float('inf')
    best_angle = 0
    
    for angle in range(0, 180, step):
        rot_poly = rotate(union_poly, angle, origin=(scx, scy))
        b = rot_poly.bounds
        side = max(b[2]-b[0], b[3]-b[1])
        if side < best_side:
            best_side = side
            best_angle = angle
            
    return best_angle, best_side

def check_overlap(trees):
    polys = [t.get_polygon() for t in trees]
    tree = STRtree(polys)
    for i, poly in enumerate(polys):
        indices = tree.query(poly)
        for index in indices:
            if index == i: continue
            if poly.intersects(polys[index]) and not poly.touches(polys[index]):
                if poly.intersection(polys[index]).area > 1e-12:
                    return True
    return False

def main():
    solver = BrickTilerSolver()
    
    print(f"{'N':<4} | {'Base Side':<10} | {'Opt Side':<10} | {'Tilt':<6} | {'Odd Rot':<8} | {'Imp'}")
    print("-" * 70)
    
    # We'll sample specific N or a range
    target_ns = [7, 13, 25, 43, 71, 133] # Primes or specific odd targets
    
    for n in target_ns:
        base_trees, _ = solver.solve(n)
        _, base_side = optimize_global_rotation(base_trees)
        
        best_n_side = base_side
        best_tilt = 0
        best_odd_rot = 0
        
        # Search space
        for tilt in range(-45, 46, 15): # Tilt of the grid trees
            for odd_rot in range(0, 180, 15):
                
                modified_trees = []
                for i, t in enumerate(base_trees):
                    if i == n - 1: # Odd tree
                        modified_trees.append(ChristmasTree(t.center_x, t.center_y, odd_rot))
                    else: # Grid trees
                        # Base tree was either 0 or 180.
                        new_a = (float(t.angle) + tilt) % 360
                        modified_trees.append(ChristmasTree(t.center_x, t.center_y, new_a))
                
                if check_overlap(modified_trees):
                    continue
                    
                _, current_side = optimize_global_rotation(modified_trees, step=5)
                
                if current_side < best_n_side - 1e-7:
                    best_n_side = current_side
                    best_tilt = tilt
                    best_odd_rot = odd_rot
        
        imp = base_side - best_n_side
        print(f"{n:<4} | {base_side:<10.6f} | {best_n_side:<10.6f} | {best_tilt:<6} | {best_odd_rot:<8} | {imp:.6f}")

if __name__ == "__main__":
    main()
