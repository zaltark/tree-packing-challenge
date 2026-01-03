import sys
from pathlib import Path
import pandas as pd
import math
import numpy as np
from shapely.affinity import rotate
from shapely.ops import unary_union

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from solver.engine import BrickTilerSolver
from solver.io import SubmissionFormatter
from solver.scoring import score, ParticipantVisibleError
from solver.strategies import get_seed_layout, get_odd_tree_rotation
from solver.geometry import ChristmasTree, SCALE_FACTOR

def optimize_rotation_for_trees(trees):
    """
    Rotates the entire cluster of trees to minimize the bounding square side.
    """
    if not trees: return trees
    
    all_polys = [t.get_polygon() for t in trees]
    union_poly = unary_union(all_polys)
    scaled_centroid = union_poly.centroid
    scx, scy = scaled_centroid.x, scaled_centroid.y
    
    initial_bounds = union_poly.bounds
    best_side = max(initial_bounds[2]-initial_bounds[0], initial_bounds[3]-initial_bounds[1])
    best_angle = 0
    
    for angle in range(0, 180, 1):
        rot_poly = rotate(union_poly, angle, origin=(scx, scy))
        b = rot_poly.bounds
        side = max(b[2]-b[0], b[3]-b[1])
        if side < best_side:
            best_side = side
            best_angle = angle
            
    if best_angle != 0:
        ucx = float(scx) / float(SCALE_FACTOR)
        ucy = float(scy) / float(SCALE_FACTOR)
        
        new_trees = []
        rad = math.radians(best_angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        
        for t in trees:
            new_angle = t.angle + best_angle
            dx = float(t.center_x) - ucx
            dy = float(t.center_y) - ucy
            new_x = ucx + dx * cos_a - dy * sin_a
            new_y = ucy + dx * sin_a + dy * cos_a
            new_trees.append(ChristmasTree(new_x, new_y, new_angle))
        return new_trees
    return trees

def main():
    MAX_N = 200
    all_results = {}
    solver = BrickTilerSolver()
    
    print(f"Generating optimized submission for N=1 to {MAX_N}...")
    
    for n in range(1, MAX_N + 1):
        # 1. Try Brick Tiler
        trees, side = solver.solve(n)
        
        # Apply Odd Tree Rotation if applicable
        if n % 2 != 0 and n > 1:
            opt_angle = get_odd_tree_rotation(n)
            if opt_angle != 0:
                new_trees = []
                for i, t in enumerate(trees):
                    if i == n - 1:
                        new_trees.append(ChristmasTree(t.center_x, t.center_y, opt_angle))
                    else:
                        new_trees.append(t)
                trees = new_trees
        
        # 2. Try Seed Layout
        seed_trees = get_seed_layout(n)
        if seed_trees:
            all_poly = [t.get_polygon() for t in seed_trees]
            bounds = unary_union(all_poly).bounds
            seed_side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
            
            if seed_side < side - 1e-9:
                final_trees = seed_trees
            else:
                final_trees = trees
        else:
            final_trees = trees
        
        # 3. Global Rotation
        final_trees = optimize_rotation_for_trees(final_trees)
            
        all_results[n] = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in final_trees])
        
        if n % 50 == 0:
            print(f"Processed N={n}...")

    output_path = PROJECT_ROOT / "output" / "submission.csv"
    SubmissionFormatter.create_submission_file(all_results, output_path)
    
    print("\nVerifying...")
    try:
        submission_df = pd.read_csv(output_path)
        final_score = score(pd.DataFrame(columns=['id']), submission_df, 'id')
        print(f"SUCCESS! Verified Score: {final_score}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    main()