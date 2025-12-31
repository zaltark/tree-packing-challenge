import sys
from pathlib import Path
import math
import numpy as np
from shapely.affinity import rotate
from shapely.ops import unary_union

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from src.models.tree_geometry import ChristmasTree

def optimize_global_rotation():
    solver = BrickTilerSolver()
    
    # Test on a known inefficient case, e.g., N=5 (Side ~2.12)
    # Or N=10
    n = 10
    trees, side0 = solver.solve(n)
    
    print(f"N={n} Initial Side: {side0:.6f}")
    
    # Try rotating the whole cluster
    # We rotate all trees around the center of the cluster
    all_poly = [t.get_polygon() for t in trees]
    union_poly = unary_union(all_poly)
    centroid = union_poly.centroid
    cx, cy = centroid.x, centroid.y
    
    best_side = side0
    best_angle = 0
    
    # Coarse search
    for angle in np.arange(0, 90, 1):
        rotated_polys = [rotate(p, angle, origin=(cx, cy)) for p in all_poly]
        bounds = unary_union(rotated_polys).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        
        if side < best_side:
            best_side = side
            best_angle = angle
            
    print(f"Best Rotation: {best_angle} deg -> Side: {best_side:.6f}")
    
    # Check N=50
    n = 50
    trees, side0 = solver.solve(n)
    print(f"\nN={n} Initial Side: {side0:.6f}")
    
    all_poly = [t.get_polygon() for t in trees]
    union_poly = unary_union(all_poly)
    centroid = union_poly.centroid
    cx, cy = centroid.x, centroid.y
    
    best_side = side0
    best_angle = 0
    
    for angle in np.arange(0, 90, 0.5):
        rotated_polys = [rotate(p, angle, origin=(cx, cy)) for p in all_poly]
        bounds = unary_union(rotated_polys).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        
        if side < best_side:
            best_side = side
            best_angle = angle
            
    print(f"Best Rotation: {best_angle} deg -> Side: {best_side:.6f}")
    improvement = side0 - best_side
    print(f"Improvement: {improvement:.6f}")

if __name__ == "__main__":
    optimize_global_rotation()
