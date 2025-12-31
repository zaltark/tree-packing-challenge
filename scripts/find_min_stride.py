import sys
from pathlib import Path
import pandas as pd
from shapely.ops import unary_union
from shapely.strtree import STRtree

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from src.models.tree_geometry import ChristmasTree

def check_overlap(trees):
    polygons = [t.get_polygon() for t in trees]
    r_tree = STRtree(polygons)
    for i, poly in enumerate(polygons):
        indices = r_tree.query(poly)
        for index in indices:
            if index == i: continue
            if poly.intersects(polygons[index]) and not poly.touches(polygons[index]):
                intersection = poly.intersection(polygons[index])
                if intersection.area > 1e-12:
                    return True
    return False

def test_stride_y(val):
    solver = BrickTilerSolver()
    solver.stride_y = val
    # Test a few critical N values
    for n in [2, 3, 5, 7, 10, 20, 50]:
        trees, _ = solver.solve(n)
        if check_overlap(trees):
            return False
    return True

def main():
    print(f"{ 'Stride Y':<20} | {'Status':<10}")
    print("-" * 35)
    
    # Test powers of 10 from 1e-1 to 1e-14
    best_safe = 1.02
    for k in range(1, 15):
        eps = 10**-k
        test_val = 1.0 + eps
        if test_stride_y(test_val):
            print(f"1.0 + 10^-{k:<2} ({test_val:.15f}) | SAFE")
            best_safe = test_val
        else:
            print(f"1.0 + 10^-{k:<2} ({test_val:.15f}) | OVERLAP")
            
    print(f"\nBest safe stride_y found: {best_safe:.15f}")

if __name__ == "__main__":
    main()
