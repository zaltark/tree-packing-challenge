import sys
from pathlib import Path
import numpy as np
from shapely.affinity import translate, rotate
from decimal import Decimal

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

def find_exact_contact():
    print("Calculating Exact Contact Offsets...")
    
    # We want to minimize (dx * dy) generally, or just tighten the fit.
    # Usually we lock dx (horizontal spacing) and minimize dy (vertical spacing) or vice versa.
    # In a grid, density ~ 1/(sx*sy).
    # sx depends on dx (width of pair). sy depends on dy (height of pair).
    
    # Let's fix dx at various points and find min dy. 
    
    t1 = ChristmasTree(0, 0, 0)
    poly1 = t1.get_polygon()
    
    # Current best
    # dx = 0.355, dy = 0.805
    
    best_config = None
    min_area = float('inf')
    
    # Search range
    # dx: 0.30 to 0.40
    # dy: 0.70 to 0.90
    
    # Coarse search to identify "valleys"
    print("Coarse Search...")
    for dx in np.arange(0.30, 0.40, 0.005):
        # Binary search for dy
        low = 0.70
        high = 0.90
        valid_dy = None
        
        for _ in range(20): # Precision
            mid = (low + high) / 2
            t2 = ChristmasTree(dx, mid, 180)
            if t1.intersects(t2):
                # Too close, need more dy
                low = mid
            else:
                # Valid (no overlap), try closer
                valid_dy = mid
                high = mid
        
        if valid_dy:
            # We have a tight dy for this dx.
            # Calculate grid stride implications.
            # Stride X approx 2*dx? No, stride x is width of the brick ~ dx + 0.35?
            # Actually stride_x in solver was 0.71 (approx 2*0.355).
            # Stride Y was 1.01 (approx dy + 0.2?)
            
            # Let's just metric: effective area of the pair bounding box
            # box width = (dx + 0.35) - (-0.35) = dx + 0.7
            # box height = (dy + 0.8) - (-0.2) = dy + 1.0
            
            # This is bounding box of the PAIR.
            # Grid density is better metric.
            
            area = (dx + 0.7) * (valid_dy + 1.0)
            # print(f"dx={dx:.4f}, dy={valid_dy:.4f}, box_area={area:.4f}")
            
            if area < min_area:
                min_area = area
                best_config = (dx, valid_dy)

    print(f"Best Coarse Config: dx={best_config[0]:.4f}, dy={best_config[1]:.4f}")
    
    # Fine optimization around best
    c_dx, c_dy = best_config
    print(f"Fine Tuning around dx={c_dx}...")
    
    final_best = None
    min_dy_found = float('inf')
    
    # Let's scan dx very finely
    for dx in np.arange(c_dx - 0.02, c_dx + 0.02, 0.0001):
        low = c_dy - 0.1
        high = c_dy + 0.1
        valid_dy = None
        
        for _ in range(30):
            mid = (low + high) / 2
            t2 = ChristmasTree(dx, mid, 180)
            if t1.intersects(t2):
                low = mid
            else:
                valid_dy = mid
                high = mid
                
        if valid_dy:
            # Check if this is a "deep" fit (local minimum of dy)
            if valid_dy < min_dy_found:
                min_dy_found = valid_dy
                final_best = (dx, valid_dy)
                
    print(f"\nExact Contact Limit:")
    print(f"dx = {final_best[0]:.6f}")
    print(f"dy = {final_best[1]:.6f}")
    
    # Verify with gap
    # Add small epsilon for safety
    safe_dx = final_best[0]
    safe_dy = final_best[1] + 0.000001
    print(f"Suggested Safe Params: dx={safe_dx:.6f}, dy={safe_dy:.6f}")
    print(f"Current Params:        dx=0.355000, dy=0.805000")

if __name__ == "__main__":
    find_exact_contact()
