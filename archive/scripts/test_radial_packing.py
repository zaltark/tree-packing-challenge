import sys
from pathlib import Path
import math
import pandas as pd
from shapely.ops import unary_union
from shapely.affinity import rotate

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR
from src.models.brick_tiler_solver import BrickTilerSolver
from scripts.generate_submission import optimize_rotation_for_trees
from scripts.visualize_results import plot_trees

def generate_radial_hex(n):
    """
    Generates a dense hexagonal/radial packing.
    """
    trees = []
    
    # Hexagonal Packing Constants
    # To fit trees (0.7 wide, 1.0 high), we need a specific lattice.
    # Vertical stride ~ 1.0 (tips touching bases)
    # Horizontal stride ~ 0.7?
    # Or tighter triangular interlock?
    # Our optimized brick stride was sx=0.71, sy=1.01.
    
    # Hex vectors:
    # v1 = (0.71, 0)
    # v2 = (0.355, 0.85)  <-- Triangle height sqrt(0.71^2 - 0.355^2)? No.
    # We want valid placements.
    # Let's use a "Spiral" placement on a valid triangular lattice.
    
    # Lattice Basis:
    dx = 0.71
    dy = 1.01 # Spacing for rows
    # Staggered rows:
    # Row 0: (0,0)
    # Row 1: (0.355, 1.01)
    
    # Spiral Generation
    # We generate points on this lattice spiral-fashion
    
    # Hand-coded rings for specific N
    
    if n == 7:
        # 1 Center + 6 Surround
        # Center
        trees.append(ChristmasTree(0, 0, 0))
        # Ring 1 (6 neighbors)
        # N1: Right
        trees.append(ChristmasTree(dx, 0, 0))
        # N2: Left
        trees.append(ChristmasTree(-dx, 0, 0))
        # N3: Top-Right
        trees.append(ChristmasTree(dx/2, dy, 180)) # Interlock?
        # N4: Top-Left
        trees.append(ChristmasTree(-dx/2, dy, 180))
        # N5: Bot-Right
        trees.append(ChristmasTree(dx/2, -dy, 180)) # Need to point down? 180 points down.
        # N6: Bot-Left
        trees.append(ChristmasTree(-dx/2, -dy, 180))
        
        # NOTE: 180 trees fit nicely "between" 0 trees vertically.
        
    elif n == 19:
        # 1 + 6 + 12
        # Center
        trees.append(ChristmasTree(0, 0, 0))
        
        # Inner Ring (6) - Mix of Up and Down
        trees.append(ChristmasTree(dx, 0, 0))
        trees.append(ChristmasTree(-dx, 0, 0))
        trees.append(ChristmasTree(dx/2, dy, 180))
        trees.append(ChristmasTree(-dx/2, dy, 180))
        trees.append(ChristmasTree(dx/2, -dy, 180))
        trees.append(ChristmasTree(-dx/2, -dy, 180))
        
        # Outer Ring (12)
        # Top-Top (Up)
        trees.append(ChristmasTree(0, dy*2, 0)) # Stacked on center?
        trees.append(ChristmasTree(dx, dy*2, 0))
        trees.append(ChristmasTree(-dx, dy*2, 0))
        
        # Bot-Bot (Up)
        trees.append(ChristmasTree(0, -dy*2, 0))
        trees.append(ChristmasTree(dx, -dy*2, 0))
        trees.append(ChristmasTree(-dx, -dy*2, 0))
        
        # Sides (Up)
        trees.append(ChristmasTree(dx*2, 0, 0))
        trees.append(ChristmasTree(-dx*2, 0, 0))
        
        # Side Interlocks (Down)
        trees.append(ChristmasTree(dx*1.5, dy, 180))
        trees.append(ChristmasTree(-dx*1.5, dy, 180))
        trees.append(ChristmasTree(dx*1.5, -dy, 180))
        trees.append(ChristmasTree(-dx*1.5, -dy, 180))
        
    else:
        return []
        
    return trees

def compare_layouts(n):
    print(f"\n--- Testing Radial Hex for N={n} ---")
    
    # 1. Brick Baseline (Optimized)
    solver = BrickTilerSolver()
    brick_trees, _ = solver.solve(n)
    brick_trees = optimize_rotation_for_trees(brick_trees)
    
    # Measure Brick
    all_poly = [t.get_polygon() for t in brick_trees]
    b = unary_union(all_poly).bounds
    brick_side = max(b[2]-b[0], b[3]-b[1])
    print(f"Brick Optimized Side: {brick_side/float(SCALE_FACTOR):.6f}")
    
    # 2. Hex Radial
    hex_trees = generate_radial_hex(n)
    if not hex_trees:
        print("No Hex layout defined.")
        return
        
    # Optimize Rotation
    hex_trees = optimize_rotation_for_trees(hex_trees)
    
    # Measure Hex
    all_poly = [t.get_polygon() for t in hex_trees]
    b = unary_union(all_poly).bounds
    hex_side = max(b[2]-b[0], b[3]-b[1])
    print(f"Hex Radial Optimized Side: {hex_side/float(SCALE_FACTOR):.6f}")
    
    if hex_side < brick_side:
        print(">>> WINNER: HEX RADIAL <<<")
        # Plot it
        data = [{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in hex_trees]
        df = pd.DataFrame(data)
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"hex_win_{n:03d}.png")
    else:
        print("Winner: Brick Grid")

if __name__ == "__main__":
    compare_layouts(7)
    compare_layouts(19)
