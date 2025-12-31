import sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from shapely.ops import unary_union

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree

def get_score_for_params(params, n):
    # params: [x1, y1, r1, x2, y2, r2, ...]
    trees = []
    for i in range(n):
        x = params[i*3]
        y = params[i*3 + 1]
        r = params[i*3 + 2]
        trees.append(ChristmasTree(x, y, r))
        
    # Check collisions
    for i in range(n):
        for j in range(i + 1, n):
            if trees[i].intersects(trees[j]):
                return 1000 + (n - i) # Penalty
                
    # Calculate Side
    all_poly = [t.get_polygon() for t in trees]
    bounds = unary_union(all_poly).bounds
    side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
    return float(side)

def optimize_n5():
    print("Optimizing N=5 for a perfect square...")
    
    # Initial guess: 3-2 staggered stack
    # Row 1: 3 trees (0, 180, 0)
    # Row 2: 2 trees (180, 180)? No.
    
    # Let's try 1-3-1 Diamond
    #   D
    #  U D U
    #   D
    
    initial_params = [
        0, 0, 0,        # Center (U)
        0.71, 0, 0,     # Right (U)
        -0.71, 0, 0,    # Left (U)
        0.355, 0.805, 180, # Top Gap (D)
        -0.355, 0.805, 180 # Top Gap (D)
    ]
    
    # We'll use a random search / local optimization hybrid
    best_side = 2.215 # Current
    best_params = initial_params
    
    for _ in range(100):
        # Random perturbation
        test_params = np.array(best_params) + np.random.normal(0, 0.1, len(best_params))
        # Snap rotations to 0 or 180 for now
        for i in range(5):
            test_params[i*3 + 2] = 0 if test_params[i*3 + 2] < 90 else 180
            
        res = minimize(get_score_for_params, test_params, args=(5,), method='Nelder-Mead', tol=1e-3)
        
        if res.fun < best_side:
            best_side = res.fun
            best_params = res.x
            print(f"New Best Side: {best_side:.4f}")

    print(f"\nFinal Best Side for N=5: {best_side:.4f}")

if __name__ == "__main__":
    # Just run a quick check of the "Manual Square" for N=5
    # 2 rows of interlocked trees.
    # Row 1: U, D, U. (3 trees)
    # Row 2: D, U? No.
    
    # Try 3 trees Row 1, 2 trees Row 2.
    # R1: (0,0,0), (0.355, 0.805, 180), (0.71, 0, 0)
    # R2: (0, 0.8, 180)? No, tip collision.
    # R2: (-0.355, 0.805, 180), (1.065, 0.805, 180)
    
    from src.models.tree_geometry import SCALE_FACTOR
    
    trees = [
        ChristmasTree(0, 0, 0),
        ChristmasTree(0.355, 0.805, 180),
        ChristmasTree(0.71, 0, 0),
        ChristmasTree(-0.355, 0.805, 180),
        ChristmasTree(1.065, 0.805, 180)
    ]
    
    all_poly = [t.get_polygon() for t in trees]
    # Check overlaps
    collision = False
    for i in range(5):
        for j in range(i+1, 5):
            if trees[i].intersects(trees[j]):
                print(f"Collision {i} and {j}")
                collision = True
    
    if not collision:
        bounds = unary_union(all_poly).bounds
        width = (bounds[2]-bounds[0])/float(SCALE_FACTOR)
        height = (bounds[3]-bounds[1])/float(SCALE_FACTOR)
        print(f"N=5 Manual Stack: Width {width:.4f}, Height {height:.4f}, Side {max(width, height):.4f}")
    else:
        print("Manual stack failed.")
