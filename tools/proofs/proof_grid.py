import sys
from pathlib import Path
import numpy as np
from shapely.affinity import translate, rotate
from decimal import Decimal, getcontext

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from solver.geometry import ChristmasTree, SCALE_FACTOR

def optimize_grid_params():
    print("Exhaustive Search for Optimal Grid Stride...")
    
    t1 = ChristmasTree(0, 0, 0)
    
    best_area = float('inf')
    best_params = None
    
    # We search for dx, dy first
    # Then calculate min sx, sy for that brick.
    
    for dx in np.arange(0.30, 0.50, 0.01):
        # Binary search for min dy
        low = 0.0
        high = 1.2
        best_dy = 1.2
        for _ in range(20):
            mid = (low + high) / 2
            t2 = ChristmasTree(dx, mid, 180)
            if t1.intersects(t2): low = mid
            else: best_dy = mid; high = mid
            
        # For this dx, dy, find min sx
        sx = max(0.7, dx * 2) # Heuristic start
        while True:
            t3 = ChristmasTree(sx, 0, 0)
            t4 = ChristmasTree(sx + dx, best_dy, 180)
            if not (t3.intersects(t1) or t3.intersects(t2) or t4.intersects(t1) or t4.intersects(t2)):
                break
            sx += 0.01
            
        # Find min sy
        sy = max(1.0, best_dy)
        while True:
            t5 = ChristmasTree(0, sy, 0)
            t6 = ChristmasTree(dx, sy + best_dy, 180)
            if not (t5.intersects(t1) or t5.intersects(t2) or t6.intersects(t1) or t6.intersects(t2)):
                break
            sy += 0.01
            
        area = (sx * sy) / 2.0
        if area < best_area:
            best_area = area
            best_params = (dx, best_dy, sx, sy)
            print(f"New Best: dx={dx:.2f}, dy={best_dy:.3f} | sx={sx:.2f}, sy={sy:.2f} | Area/Tree={area:.6f}")

    print("\nFINAL OPTIMIZED GRID:")
    print(f"u_dx = {best_params[0]:.4f}")
    print(f"u_dy = {best_params[1]:.4f}")
    print(f"stride_x = {best_params[2]:.4f}")
    print(f"stride_y = {best_params[3]:.4f}")
    print(f"Efficiency: {best_area:.6f}")

if __name__ == "__main__":
    optimize_grid_params()
