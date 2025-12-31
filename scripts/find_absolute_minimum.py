import sys
from pathlib import Path
import numpy as np
from shapely.affinity import translate, rotate
from decimal import Decimal, getcontext

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

getcontext().prec = 25

def find_absolute_minimum():
    print("Finding Absolute Minimum (dx, dy) for Interlocking Pair...")
    
    t1 = ChristmasTree(0, 0, 0)
    
    # We want to minimize the 'Bounding Box Area' of the pair?
    # Or just find the "pareto front" of (dx, dy).
    
    # Let's fix dx and find the absolute min dy.
    # We'll test dx from 0.30 to 0.40.
    
    results = []
    
    for dx in np.linspace(0.30, 0.40, 101):
        # Binary search for min dy
        low = 0.70
        high = 0.90
        best_dy = high
        
        # High precision search
        for _ in range(40):
            mid = (low + high) / 2
            t2 = ChristmasTree(dx, mid, 180)
            if t1.intersects(t2):
                low = mid
            else:
                best_dy = mid
                high = mid
        
        # Efficiency Metric: 
        # Bounding box of pair:
        # width = (dx + 0.35) - (-0.35) = dx + 0.7
        # height = (best_dy + 0.2) - (-0.2) = best_dy + 0.4?
        # No. T1: [-0.2, 0.8]. T2: [dy-0.8, dy+0.2].
        # min_y = -0.2. max_y = dy+0.2.
        # height = dy + 0.4.
        
        # Grid Area per tree = (dx * dy)? No.
        # Grid Stride X = dx + epsilon? No. 
        # For a repeating grid, Stride X must be at least 0.7 (tree width).
        # So sx = 0.7.
        # Stride Y = dy + epsilon? No. Stride Y must be 1.0 (tree height).
        # Wait.
        
        area = (dx + 0.7) * (best_dy + 1.0) # Bounding Box of the pair
        results.append((area, dx, best_dy))

    results.sort()
    
    print(f"\nTop 5 Tightest Pairs (by Bounding Box Area):")
    for i in range(5):
        a, dx, dy = results[i]
        print(f"Area: {a:.6f} | dx: {dx:.6f}, dy: {dy:.6f}")

    best_area, best_dx, best_dy = results[0]
    
    # Let's check "Grid Efficiency"
    # If we repeat this unit:
    # sx = 0.71 (Locked by base width)
    # sy = 1.01 (Locked by tree height)
    # Then dx, dy don't change sx, sy. 
    # BUT! If dy is small enough, can we stack bricks tighter?
    # Brick 1: (0,0) and (dx, dy)
    # Brick 2: (0, sy) and (dx, sy+dy)
    # Sy is limited by T3 vs T1 (sy >= 1.0).
    # UNLESS T3 interlocks with T2?
    # T1(U), T2(D), T3(U), T4(D)...
    # This is exactly what BrickTiler does.
    
    print(f"\nRecommended Absolute Tightest Pair:")
    print(f"dx = {best_dx:.8f}")
    print(f"dy = {best_dy:.8f}")
    
    # Visualization of the contact
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 10))
    
    t1_poly = t1.get_polygon()
    t2_poly = ChristmasTree(best_dx, best_dy, 180).get_polygon()
    
    for p, c in [(t1_poly, 'green'), (t2_poly, 'lime')]:
        x, y = p.exterior.xy
        x = [val / float(SCALE_FACTOR) for val in x]
        y = [val / float(SCALE_FACTOR) for val in y]
        ax.fill(x, y, alpha=0.5, fc=c, ec='black')
        
    ax.set_aspect('equal')
    ax.set_title(f"Tightest Interlock (dx={best_dx:.4f}, dy={best_dy:.4f})")
    
    # Zoom in on the contact point (should be around dx/2, dy/2?)
    # Let's zoom on the overlap region
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 0.5)
    
    out_path = PROJECT_ROOT / "results" / "plots" / "absolute_tightest_pair.png"
    plt.savefig(out_path)
    print(f"Zoomed plot saved to {out_path}")

if __name__ == "__main__":
    find_absolute_minimum()
