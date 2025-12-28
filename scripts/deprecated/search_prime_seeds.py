import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import math
import numpy as np
import pandas as pd
from decimal import Decimal
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree
from scripts.visualize_results import plot_trees

def evaluate(trees):
    polys = [t.get_polygon() for t in trees]
    for i in range(len(polys)):
        for j in range(i+1, len(polys)):
            if polys[i].intersects(polys[j]) and not polys[i].touches(polys[j]):
                return float('inf')
    bounds = unary_union(polys).bounds
    return max(bounds[2]-bounds[0], bounds[3]-bounds[1])

def find_best_arrangement(n, iterations=2000):
    print(f"--- Searching for Optimal N={n} Arrangement ---")
    best_side = float('inf')
    best_trees = []

    # Strategy 1: Slanted Row (Duplicity)
    # We find a delta X, delta Y, and Delta Rot that can be repeated
    for dx in np.arange(0.3, 0.8, 0.05):
        for dy in np.arange(0.0, 0.8, 0.05):
            for dr in [0, 45, 90, 180]:
                trees = []
                for i in range(n):
                    # Repeat the transformation
                    trees.append(ChristmasTree(i*dx, i*dy, i*dr))
                
                side = evaluate(trees)
                if side < best_side:
                    best_side = side
                    best_trees = trees

    # Strategy 2: Pinwheel (Radial Duplicity)
    for r in np.arange(0.2, 1.0, 0.05):
        for tilt in np.arange(0, 90, 15):
            trees = []
            angle_step = 360 / n
            for i in range(n):
                angle = i * angle_step
                rad = math.radians(angle)
                trees.append(ChristmasTree(r*math.cos(rad), r*math.sin(rad), angle + tilt))
            
            side = evaluate(trees)
            if side < best_side:
                best_side = side
                best_trees = trees

    score = (best_side**2) / n
    print(f"Best found for N={n}: Side={best_side:.4f}, Score={score:.4f}")
    
    # Save visual
    data = [{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in best_trees]
    plot_trees(pd.DataFrame(data), output_path=PROJECT_ROOT / "results" / "plots" / f"prime_seed_{n:02d}.png")
    
    return best_trees, best_side

if __name__ == "__main__":
    for n in [3, 5, 7]:
        find_best_arrangement(n)
