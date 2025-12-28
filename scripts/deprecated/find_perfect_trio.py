import sys
from pathlib import Path
import numpy as np
import pandas as pd
from decimal import Decimal
from shapely.ops import unary_union

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

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

def search_trio():
    print("Searching for the Perfect 3-Tree Triangle...")
    
    # Strategy: 120-degree symmetry
    # T1: (r, 0, 0)
    # T2: (r, 120, 120)
    # T3: (r, 240, 240)
    
    best_side = float('inf')
    best_trees = []
    
    # Search for the radius where they just touch
    for r in np.arange(0.1, 1.0, 0.01):
        trees = []
        for angle in [0, 120, 240]:
            rad = np.radians(angle)
            x = r * np.cos(rad)
            y = r * np.sin(rad)
            # Face outward or inward? Let's try facing center (angle - 90)
            trees.append(ChristmasTree(x, y, angle)) # Facing up/angled
            
        side = evaluate(trees)
        if side < best_side:
            best_side = side
            best_trees = trees

    print(f"Propeller Pattern Best Side: {best_side:.4f}")
    
    # Strategy 2: Nested Jigsaw (Brick + 1)
    # T1 (0,0,0), T2 (0.35, 0.8, 180)
    # Search for T3 around them
    t1 = ChristmasTree(0, 0, 0)
    t2 = ChristmasTree(0.35, 0.8, 180)
    for dx in np.arange(-1.0, 1.0, 0.05):
        for dy in np.arange(-1.0, 1.0, 0.05):
            for rot in [0, 180]:
                t3 = ChristmasTree(dx, dy, rot)
                side = evaluate([t1, t2, t3])
                if side < best_side:
                    best_side = side
                    best_trees = [t1, t2, t3]

    print(f"Overall Best Trio Side: {best_side:.4f}")
    
    # Save the best visual
    data = []
    for t in best_trees:
        data.append({'x': t.center_x, 'y': t.center_y, 'angle': t.angle})
    df = pd.DataFrame(data)
    plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / "perfect_trio.png")
    return best_trees

if __name__ == "__main__":
    search_trio()
