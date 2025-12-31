import sys
from pathlib import Path
import numpy as np
from shapely.affinity import translate, rotate
from decimal import Decimal, getcontext
import matplotlib.pyplot as plt

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

getcontext().prec = 25

def find_absolute_limit():
    print("Scanning Interlock Efficiency (dx from 0 to 0.5)...")
    
    t1 = ChristmasTree(0, 0, 0)
    
    results = []
    
    # Range from 0 to 0.5
    for dx in np.linspace(0.0, 0.5, 201):
        low = 0.0
        high = 2.0
        best_dy = 2.0
        
        for _ in range(30):
            mid = (low + high) / 2
            t2 = ChristmasTree(dx, mid, 180)
            if t1.intersects(t2):
                low = mid
            else:
                best_dy = mid
                high = mid
        
        # Grid Area Metric:
        # In a grid, we repeat this brick.
        # Stride X (sx) is locked by tree width: sx = 0.7 (approx).
        # Stride Y (sy) is locked by tree height: sy = 1.0 (approx).
        # But dx, dy affects the bounding box of the final N-tree cluster.
        # Density ~ dx * dy is NOT the right metric.
        # Bounding box width ~ (C-1)*sx + dx + 0.7
        # Bounding box height ~ (R-1)*sy + dy + 1.0
        
        results.append((dx, best_dy))

    # Plot the Contact Curve
    dx_vals = [r[0] for r in results]
    dy_vals = [r[1] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(dx_vals, dy_vals, label='Min dy for dx')
    plt.xlabel('dx (Horizontal Offset)')
    plt.ylabel('dy (Vertical Offset)')
    plt.title('Interlock Contact Boundary')
    plt.grid(True)
    
    # Efficiency per tree (approx)
    # Area = (dx + 0.7) * (dy + 1.0) / 2
    eff = [((r[0]+0.7)*(r[1]+1.0))/2.0 for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(dx_vals, eff, label='Area/Tree (Pair BBox)')
    plt.xlabel('dx')
    plt.ylabel('Score Area Estimator')
    plt.title('Packing Efficiency vs Offset')
    plt.grid(True)
    
    # Find local minima
    best_idx = np.argmin(eff)
    best_dx, best_dy = results[best_idx]
    
    print(f"\nOptimal Point Found:")
    print(f"dx: {best_dx:.6f}")
    print(f"dy: {best_dy:.6f}")
    print(f"Area Estimator: {eff[best_idx]:.6f}")
    
    # Zoom in on the curve to see the 'teeth' of the tree
    plt.figure(figsize=(10, 6))
    plt.plot(dx_vals, dy_vals)
    plt.scatter([best_dx], [best_dy], color='red', label='Optimal')
    plt.title('Contact Boundary (Zoom)')
    plt.legend()
    
    plt.savefig(PROJECT_ROOT / "results" / "plots" / "interlock_analysis.png")
    print(f"Plot saved to results/plots/interlock_analysis.png")

if __name__ == "__main__":
    find_absolute_limit()
