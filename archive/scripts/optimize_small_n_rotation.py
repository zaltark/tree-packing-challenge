import sys
from pathlib import Path
import numpy as np
import pandas as pd
from shapely.affinity import rotate
from shapely.ops import unary_union
import matplotlib.pyplot as plt

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from src.models.prime_seeds import get_prime_seed
from src.models.tree_geometry import SCALE_FACTOR

def get_best_layout(n):
    # 1. Brick Tiler
    solver = BrickTilerSolver()
    brick_trees, _ = solver.solve(n)
    
    # 2. Prime Seed
    seed_trees = get_prime_seed(n)
    
    # Compare
    def get_side(trees):
        if not trees: return float('inf')
        polys = [t.get_polygon() for t in trees]
        bounds = unary_union(polys).bounds
        return max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        
    brick_side = get_side(brick_trees)
    seed_side = get_side(seed_trees)
    
    if seed_side < brick_side:
        return seed_trees, "Seed"
    return brick_trees, "Brick"

def optimize_rotation(n):
    print(f"\n--- Optimizing N={n} ---")
    
    base_trees, source = get_best_layout(n)
    print(f"Base Source: {source}")
    
    all_poly = [t.get_polygon() for t in base_trees]
    union_poly = unary_union(all_poly)
    centroid = union_poly.centroid
    cx, cy = centroid.x, centroid.y
    
    initial_bounds = union_poly.bounds
    initial_side = max(initial_bounds[2]-initial_bounds[0], initial_bounds[3]-initial_bounds[1])
    
    print(f"Initial Side: {initial_side/float(SCALE_FACTOR):.6f}")
    
    best_side = initial_side
    best_angle = 0
    
    # Fine search 0-180 (symmetry usually means we don't need 360)
    # Step 0.5 degrees
    angles = np.arange(0, 180, 0.5)
    
    for angle in angles:
        rotated_polys = [rotate(p, angle, origin=(cx, cy)) for p in all_poly]
        bounds = unary_union(rotated_polys).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        
        if side < best_side:
            best_side = side
            best_angle = angle
            
    print(f"Best Angle: {best_angle} deg")
    print(f"Optimized Side: {best_side/float(SCALE_FACTOR):.6f}")
    
    improvement = (initial_side - best_side) / float(SCALE_FACTOR)
    print(f"Improvement: {improvement:.6f}")
    
    # Plot Best
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Rotate original trees for plotting
    rotated_trees_polys = [rotate(p, best_angle, origin=(cx, cy)) for p in all_poly]
    
    for poly in rotated_trees_polys:
        x, y = poly.exterior.xy
        x = [val / float(SCALE_FACTOR) for val in x]
        y = [val / float(SCALE_FACTOR) for val in y]
        ax.fill(x, y, alpha=0.5, fc='green', ec='black')
        
    # Bounds
    minx, miny, maxx, maxy = unary_union(rotated_trees_polys).bounds
    w = maxx - minx
    h = maxy - miny
    side_len = max(w, h)
    
    # Convert to plot units
    px = minx / float(SCALE_FACTOR)
    py = miny / float(SCALE_FACTOR)
    pw = w / float(SCALE_FACTOR)
    ph = h / float(SCALE_FACTOR)
    pside = side_len / float(SCALE_FACTOR)
    
    rect = plt.Rectangle((px, py), pw, ph, edgecolor='red', facecolor='none', linestyle='--', label='Bounds')
    ax.add_patch(rect)
    
    # Score Square
    center_x = px + pw/2
    center_y = py + ph/2
    sq_x = center_x - pside/2
    sq_y = center_y - pside/2
    rect_sq = plt.Rectangle((sq_x, sq_y), pside, pside, edgecolor='blue', facecolor='none', linestyle=':', label='Score')
    ax.add_patch(rect_sq)
    
    ax.set_aspect('equal')
    ax.set_title(f"N={n} Rotated {best_angle} deg\nSide: {pside:.4f}")
    
    out_path = PROJECT_ROOT / "results" / "plots" / f"opt_rot_{n:03d}.png"
    plt.savefig(out_path)
    print(f"Plot saved to {out_path}")
    plt.close()

if __name__ == "__main__":
    targets = [1, 5, 7, 13]
    for n in targets:
        optimize_rotation(n)
