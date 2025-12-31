import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from shapely.affinity import translate, rotate
from src.models.tree_geometry import ChristmasTree

def plot_config(t1, t2, sx, sy, title, filename):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot a 3x3 grid to verify visually
    for row in range(3):
        for col in range(3):
            bx = col * sx
            by = row * sy
            
            # Tree 1
            p1 = translate(t1.get_polygon(), bx, by)
            x, y = p1.exterior.xy
            ax.fill(x, y, alpha=0.5, fc='green', ec='black')
            
            # Tree 2
            p2 = translate(t2.get_polygon(), bx, by)
            x, y = p2.exterior.xy
            ax.fill(x, y, alpha=0.5, fc='lime', ec='black')
        
    ax.set_aspect('equal')
    ax.set_title(title)
    
    out_path = PROJECT_ROOT / "results" / "plots" / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    print(f"Saved plot to {out_path}")
    plt.close()

def check_grid_validity(t1, t2, sx, sy):
    """
    Checks collision in a 2x2 grid context.
    If 2x2 works, 3x3 usually works for translation symmetry.
    We check the central brick against its neighbors.
    """
    # Neighbors: (1,0), (0,1), (1,1) relative to (0,0)
    # We only need to check if (0,0) collides with neighbors.
    
    # Brick 0: t1_0, t2_0
    
    neighbor_offsets = [
        (sx, 0),    # Right
        (0, sy),    # Top
        (sx, sy),   # Top-Right
        (-sx, 0),   # Left
        (0, -sy),   # Bottom
        (-sx, sy),  # Top-Left
        (sx, -sy),  # Bottom-Right
        (-sx, -sy)  # Bottom-Left
    ]
    
    for off_x, off_y in neighbor_offsets:
        # Translate T1 and T2 to neighbor position
        n_t1 = translate(t1.get_polygon(), off_x, off_y)
        n_t2 = translate(t2.get_polygon(), off_x, off_y)
        
        # Check vs Base T1
        if t1.get_polygon().intersects(n_t1) and not t1.get_polygon().touches(n_t1): return False
        if t1.get_polygon().intersects(n_t2) and not t1.get_polygon().touches(n_t2): return False
        
        # Check vs Base T2
        if t2.get_polygon().intersects(n_t1) and not t2.get_polygon().touches(n_t1): return False
        if t2.get_polygon().intersects(n_t2) and not t2.get_polygon().touches(n_t2): return False
        
    return True

def optimize_brick():
    print("Optimizing Brick Interlock with Rigorous Grid Check...")
    
    # Baseline
    base_dx = 0.355
    base_dy = 0.805
    base_sx = 0.71
    base_sy = 1.01
    base_area = (base_sx * base_sy) / 2.0
    print(f"Baseline Area/Tree: {base_area:.6f}")

    # Search
    best_area = base_area
    best_params = None
    
    # Finer grid search near the failing point to see if we can nudge it
    # We failed at 0.350, 0.800, 0.700, 1.000.
    # Let's search around that region but verify rigorously.
    
    dx_range = np.arange(0.350, 0.360, 0.001)
    dy_range = np.arange(0.800, 0.810, 0.001)
    
    t1 = ChristmasTree(0, 0, 0) # Fixed T1

    # Rotation: 180 seems best, but let's allow small wiggle if needed
    rot = 180 
    
    for dx in dx_range:
        for dy in dy_range:
            t2 = ChristmasTree(dx, dy, rot)
            
            # Check internal brick collision
            if t1.intersects(t2):
                continue
                
            # Now find tightest Stride X
            found_sx = None
            for sx in np.arange(0.700, 0.720, 0.001):
                # Basic check first
                if check_grid_validity(t1, t2, sx, 100): # Infinite Y
                     found_sx = sx
                     break
            
            if found_sx is None: continue
            
            # Find tightest Stride Y
            found_sy = None
            for sy in np.arange(1.000, 1.020, 0.001):
                if check_grid_validity(t1, t2, found_sx, sy):
                    found_sy = sy
                    break
                    
            if found_sy is None: continue
            
            current_area = (found_sx * found_sy) / 2.0
            
            if current_area < best_area:
                best_area = current_area
                best_params = (dx, dy, rot, found_sx, found_sy)
                print(f"New Best! Area: {best_area:.6f} | Params: dx={dx:.3f}, dy={dy:.3f}, sx={found_sx:.3f}, sy={found_sy:.3f}")
                
                # Save plot immediately
                filename = f"opt_candidate_{best_area:.5f}.png"
                plot_config(t1, t2, found_sx, found_sy, f"Candidate Area {best_area:.5f}", filename)

    if best_params:
        print(f"\nCONFIRMED IMPROVEMENT.")
        print(f"Old Area: {base_area:.6f} -> New Area: {best_area:.6f}")
        dx, dy, rot, sx, sy = best_params
        print(f"Parameters: u_dx={dx:.3f}, u_dy={dy:.3f}, stride_x={sx:.3f}, stride_y={sy:.3f}")
    else:
        print("\nNo improvement found over baseline with rigorous checks.")

if __name__ == "__main__":
    optimize_brick()
