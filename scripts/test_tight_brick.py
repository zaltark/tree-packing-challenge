import sys
from pathlib import Path
import pandas as pd
from shapely.ops import unary_union

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR
from scripts.visualize_results import plot_trees

def test_tight_brick_n3():
    print("Visualizing Tight Brick (0.32) for N=3...")
    
    # Tight Parameters
    u_dx = 0.320
    u_dy = 0.830
    stride_x = 0.71 # Safe
    stride_y = 1.01 # Safe
    
    # N=3 Layout: 2 Bricks (but only 3 trees filled)
    # Target Grid 2x1 (2 columns, 1 row).
    # Center offsets:
    # Cols: 2. offset_c = 0.5.
    # c=0: pos = -0.5 * 0.71 = -0.355
    # c=1: pos = 0.5 * 0.71 = 0.355
    
    # Points:
    # 1. (-0.355, 0)
    # 2. (0.355, 0)
    
    # Fill Order (Chebyshev):
    # 1. (-0.355, 0). Dist 0.355.
    # 2. (0.355, 0). Dist 0.355.
    
    # Trees:
    trees = []
    
    # Slot 1: (-0.355, 0)
    # T1 (Up)
    trees.append(ChristmasTree(-0.355, 0, 0))
    # T2 (Down)
    trees.append(ChristmasTree(-0.355 + u_dx, 0 + u_dy, 180))
    
    # Slot 2: (0.355, 0)
    # T3 (Up)
    trees.append(ChristmasTree(0.355, 0, 0))
    
    # Check Collisions
    collision = False
    for i in range(3):
        for j in range(i+1, 3):
            if trees[i].intersects(trees[j]):
                print(f"COLLISION: Tree {i} vs Tree {j}")
                collision = True
                
    # Visualize
    data = [{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees]
    df = pd.DataFrame(data)
    
    output_path = PROJECT_ROOT / "results" / "plots" / "debug_tight_n3.png"
    plot_trees(df, output_path=output_path)
    
    print(f"Collision: {collision}")
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    test_tight_brick_n3()
