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

def get_bounds_side(trees):
    if not trees: return 0
    all_polys = [t.get_polygon() for t in trees]
    union_poly = unary_union(all_polys)
    b = union_poly.bounds
    return max(b[2]-b[0], b[3]-b[1])

def optimize_global_rotation(trees, step=1):
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
            
    if best_angle == 0:
        return trees, best_side
        
    ucx, ucy = float(scx)/float(SCALE_FACTOR), float(scy)/float(SCALE_FACTOR)
    rad = math.radians(best_angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    new_trees = []
    for t in trees:
        new_angle = float(t.angle) + best_angle
        dx, dy = float(t.center_x) - ucx, float(t.center_y) - ucy
        new_x = ucx + dx * cos_a - dy * sin_a
        new_y = ucy + dx * sin_a + dy * cos_a
        new_trees.append(ChristmasTree(new_x, new_y, new_angle))
    return new_trees, best_side

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
    results = []
    
    print(f"{'N':<4} | {'Base Side':<10} | {'Opt Side':<10} | {'Tree Angle':<10} | {'Improvement'}")
    print("-" * 65)
    
    for n in range(3, 201, 2):
        # 1. Base case
        base_trees, base_side = solver.solve(n)
        base_trees_rot, base_side_opt = optimize_global_rotation(base_trees)
        
        best_n_side = base_side_opt
        best_tree_angle = 0
        
        # 2. Try rotating the last tree
        # The last tree in BrickTiler is the one at the end of placed_trees
        for angle in range(0, 180, 5):
            if angle == 0: continue
            
            modified_trees = []
            for i, t in enumerate(base_trees):
                if i == n - 1:
                    modified_trees.append(ChristmasTree(t.center_x, t.center_y, angle))
                else:
                    modified_trees.append(t)
            
            if check_overlap(modified_trees):
                continue
                
            # Perform global rotation for this configuration
            _, current_side = optimize_global_rotation(modified_trees)
            
            if current_side < best_n_side - 1e-7:
                best_n_side = current_side
                best_tree_angle = angle
        
        improvement = base_side_opt - best_n_side
        results.append({
            'n': n,
            'base': base_side_opt,
            'opt': best_n_side,
            'angle': best_tree_angle,
            'imp': improvement
        })
        
        print(f"{n:<4} | {base_side_opt:<10.6f} | {best_n_side:<10.6f} | {best_tree_angle:<10} | {improvement:.6f}")

if __name__ == "__main__":
    main()
