import numpy as np
from shapely import affinity
from shapely.geometry import Polygon
from scipy.optimize import minimize
from decimal import Decimal
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

def get_packing_efficiency(params):
    dx, dy, angle = params
    t1 = ChristmasTree(0, 0, 0)
    t2 = ChristmasTree(dx, dy, angle)
    
    if t1.intersects(t2):
        return 1e9 # Penalty for collision
    
    # We want to minimize the area of the rectangle that can contain this pair
    # AND be tiled. For a pair (T1, T2) to be a repeatable unit, 
    # we usually think of it as a cell of size W x H.
    
    poly1 = t1.get_polygon()
    poly2 = t2.get_polygon()
    
    # Combined bounds
    min_x = min(poly1.bounds[0], poly2.bounds[0])
    max_x = max(poly1.bounds[2], poly2.bounds[2])
    min_y = min(poly1.bounds[1], poly2.bounds[1])
    max_y = max(poly1.bounds[3], poly2.bounds[3])
    
    width = (max_x - min_x) / float(SCALE_FACTOR)
    height = (max_y - min_y) / float(SCALE_FACTOR)
    
    # We want to minimize the side of the square if we were packing just these two,
    # but for tiling, we might want to minimize width * height or max(width, height).
    # Since the final score is Side^2 / N, and we want to pack N trees into a square,
    # we essentially want to minimize the area per tree.
    area_per_tree = (width * height) / 2
    
    return max(width, height) # Minimize the side length of the bounding square for the pair

def find_best_pair():
    print("Optimizing two-tree unit cell...")
    best_score = 1e9
    best_params = None
    
    # Try different starting configurations
    # 1. Inverted (180 deg) - The "Jigsaw"
    # 2. Same orientation (0 deg)
    # 3. Side-by-side (90 or 270 deg)
    
    for start_angle in [0, 90, 180, 270]:
        res = minimize(
            get_packing_efficiency,
            x0=[0.4, 0.7, start_angle],
            bounds=[(-1, 1), (-1, 1), (0, 360)],
            method='Nelder-Mead',
            options={'xatol': 1e-4, 'fatol': 1e-4}
        )
        if res.fun < best_score:
            best_score = res.fun
            best_params = res.x
            
    dx, dy, angle = best_params
    print(f"Best Params: dx={dx:.6f}, dy={dy:.6f}, angle={angle:.6f}")
    print(f"Best Side Length for 2 trees: {best_score:.6f}")
    print(f"Score (Side^2 / 2): {(best_score**2)/2:.6f}")
    return best_params

if __name__ == "__main__":
    find_best_pair()
