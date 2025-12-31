import sys
from pathlib import Path
import numpy as np
from shapely.affinity import translate, rotate
from decimal import Decimal, getcontext

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

getcontext().prec = 50 # Extreme precision for this check

def measure_contact_precision():
    print("Measuring Contact Precision Limit...")
    
    # We want to find the exact dy where `intersects` becomes False.
    # Fixed dx = 0.35 (Safe tight fit)
    dx = 0.35
    
    # Binary Search
    t1 = ChristmasTree(0, 0, 0)
    
    low = 0.79
    high = 0.81
    
    for i in range(100): # 100 iterations gives huge precision
        mid = (low + high) / 2
        t2 = ChristmasTree(dx, mid, 180)
        
        # Check intersection
        # We need to distinguish between "intersects" and "touches"
        # The metric allows touching.
        # intersects() returns True if they share any interior point.
        # touches() returns True if they share boundary but no interior.
        # The collision check is: poly.intersects() AND NOT poly.touches()
        
        collision = t1.intersects(t2)
        
        if collision:
            # Overlap -> Need more separation (higher dy)
            low = mid
        else:
            # Valid (Touch or Apart) -> Try closer
            high = mid
            
    limit_dy = high
    print(f"Limit dy for dx={dx}: {limit_dy:.20f}")
    
    # Verify the limit point
    t_limit = ChristmasTree(dx, limit_dy, 180)
    print(f"Check at limit: Intersects? {t1.intersects(t_limit)}")
    
    # Add a safety margin (epsilon)
    # 1e-15?
    epsilon = 1e-12
    safe_dy = limit_dy + epsilon
    print(f"Safe dy: {safe_dy:.20f}")
    
    t_safe = ChristmasTree(dx, safe_dy, 180)
    print(f"Check at safe: Intersects? {t1.intersects(t_safe)}")

    # Now check dx limit for fixed dy=0.805 (Current Safe)
    fixed_dy = 0.805
    low = 0.30
    high = 0.40
    
    for i in range(100):
        mid = (low + high) / 2
        t2 = ChristmasTree(mid, fixed_dy, 180)
        if t1.intersects(t2):
            low = mid # Too close (horizontally? No, smaller dx means closer)
            # Actually, contact is complex.
            # If we reduce dx, we might collide.
            # So low = mid means "collided, need larger dx"?
            # Yes, for fixed dy, larger dx separates them.
        else:
            high = mid # Try tighter
            
    limit_dx = high # High is the valid bound (smallest valid dx)
    print(f"Limit dx for dy={fixed_dy}: {limit_dx:.20f}")

if __name__ == "__main__":
    measure_contact_precision()
