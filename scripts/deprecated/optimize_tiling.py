import math
import sys
from pathlib import Path
import numpy as np
from decimal import Decimal
from shapely.strtree import STRtree
from shapely.ops import unary_union

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree

def validate_grid(sx, sy, u_dx, u_dy, n_bricks=100):
    m = int(math.ceil(math.sqrt(n_bricks)))
    trees = []
    for r in range(m):
        for c in range(m):
            bx, by = c * sx, r * sy
            trees.append(ChristmasTree(bx, by, 0))
            trees.append(ChristmasTree(bx + u_dx, by + u_dy, 180))
            
    polys = [t.get_polygon() for t in trees]
    tree_index = STRtree(polys)
    for i in range(len(polys)):
        possible = tree_index.query(polys[i])
        for idx in possible:
            if idx > i:
                if polys[i].intersects(polys[idx]) and not polys[i].touches(polys[idx]):
                    return False
    return True

import math

def optimize():
    print("--- Optimizing Tiling Spacing for N=200 ---")
    
    # Starting safe values
    u_dx, u_dy = 0.355, 0.805
    stride_x = 0.71
    stride_y = 1.01
    
    # 1. Optimize Internal Brick Interlock (u_dx, u_dy)
    print("Step 1: Tightening internal brick interlock...")
    for dy in np.arange(u_dy, 0.4, -0.001):
        t1 = ChristmasTree(0, 0, 0)
        t2 = ChristmasTree(0.35, dy, 180)
        if t1.intersects(t2) and not t1.touches(t2):
            u_dy = dy + 0.001
            break
    u_dx = 0.35 # Half-width is the theoretical ideal
    
    # 2. Optimize Grid Strides (stride_x, stride_y)
    print("Step 2: Tightening grid strides...")
    
    # Shrink Stride X
    for sx in np.arange(stride_x, 0.3, -0.001):
        if not validate_grid(sx, stride_y, u_dx, u_dy, 100):
            stride_x = sx + 0.001
            break
        stride_x = sx

    # Shrink Stride Y
    for sy in np.arange(stride_y, 0.3, -0.001):
        if not validate_grid(stride_x, sy, u_dx, u_dy, 100):
            stride_y = sy + 0.001
            break
        stride_y = sy

    print(f"\nOPTIMIZATION COMPLETE:")
    print(f"Jigsaw DX: {u_dx}")
    print(f"Jigsaw DY: {u_dy:.4f}")
    print(f"Stride X:  {stride_x:.4f}")
    print(f"Stride Y:  {stride_y:.4f}")
    
    # Calculate predicted score for N=200
    side = max(9 * stride_x + 0.7, 9 * stride_y + 1.0) # Approx
    score = (side**2) / 200
    print(f"Predicted Score for N=200: {score:.6f}")

    # Update magic_params.py
    params_path = PROJECT_ROOT / "config" / "magic_params.py"
    content = f"""# Optimized Tiling Parameters
from decimal import Decimal

TREE_COORDS = [
    (0.0, 0.8), (0.125, 0.5), (0.0625, 0.5), (0.2, 0.25), (0.1, 0.25),
    (0.35, 0.0), (0.075, 0.0), (0.075, -0.2), (-0.075, -0.2), (-0.075, 0.0),
    (-0.35, 0.0), (-0.1, 0.25), (-0.2, 0.25), (-0.0625, 0.5), (-0.125, 0.5)
]

SCALE_FACTOR = Decimal('1e18')

# Optimized for N=200 Square
JIGSAW_DX = {u_dx}
JIGSAW_DY = {u_dy:.4f}
STRIDE_X = {stride_x:.4f}
STRIDE_Y = {stride_y:.4f}

BEST_KNOWN_SIDES = {{
    1: 0.92,
    50: 6.05,
    100: 7.95,
    200: {side:.4f}
}}
"""
    with open(params_path, 'w') as f:
        f.write(content)
    print(f"\nMagic parameters updated in {params_path}")

if __name__ == "__main__":
    optimize()
