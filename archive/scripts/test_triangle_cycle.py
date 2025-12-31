import sys
from pathlib import Path
import math
from shapely.ops import unary_union
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR
from scripts.visualize_results import plot_trees

def test_triangle_cycle():
    print("Testing 3-Tree Cycle (Base-to-Base Triangle)...")
    
    # We want 3 trees forming a triangle.
    # Base of T1 -> Side of T2?
    # Or Bases forming a triangle hole in the middle?
    
    # Let's try equilateral triangle arrangement where trees point OUTWARD.
    # Bases form a small triangle in center.
    # Distance from center to base edge = r_base.
    # Base width = 0.7.
    # Side of inner triangle = 0.7?
    # r_base = 0.7 / (2 * tan(60/2)) = 0.7 / (2 * 0.577) = 0.606.
    
    # Tree geometry: Base is at y=0 relative to center.
    # So we place trees at radius r=0.202 (height of equilateral triangle with side 0.7 is 0.6).
    # Wait.
    # Triangle side s=0.7.
    # Height h = s * sqrt(3)/2 = 0.606.
    # Centroid to side distance (apothem) a = h/3 = 0.202.
    
    # So we place 3 trees at distance 0.202 from center, rotated 0, 120, 240.
    # BUT rotated such that Base faces center.
    # Tree 0 (Angle 0): Points Up. Base is at y=0.
    # If we want Base to be at y=0.202? No.
    # We want Base to be tangent to the inner circle?
    # Tree points OUT.
    # Angle 0: Points (1,0)? No, Angle 0 points (0,1).
    # Angle 0: Points Up.
    # Base is at y=0.
    # We want Base at y=0.202 (apothem).
    # So CenterY = 0.202.
    
    apothem = 0.7 / (2 * math.tan(math.pi/3)) # 0.202
    
    cycle_trees = []
    for i in range(3):
        angle = i * 120
        # Normal Angle 0 points North.
        # We want tree 0 to point North.
        # Center (0, apothem).
        
        # Rotate position (0, apothem) by angle
        rad = math.radians(angle)
        # x' = -y sin
        # y' = y cos
        cx = -apothem * math.sin(rad)
        cy = apothem * math.cos(rad)
        
        cycle_trees.append(ChristmasTree(cx, cy, angle))
        
    # Check collision
    collision = False
    for i in range(3):
        for j in range(i+1, 3):
            if cycle_trees[i].intersects(cycle_trees[j]):
                collision = True
                
    # Measure
    polys = [t.get_polygon() for t in cycle_trees]
    bounds = unary_union(polys).bounds
    side = max(bounds[2]-bounds[0], bounds[3]-bounds[1]) / float(SCALE_FACTOR)
    score = (side**2)/3
    
    print(f"\n--- 3-Tree Cycle (Outward) ---")
    print(f"Collision: {collision}")
    print(f"Side: {side:.4f}")
    print(f"Score: {score:.4f}")
    print(f"Brick Score Target: 0.66")
    
    if not collision:
         df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in cycle_trees])
         plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / "tri_cycle_out.png")

    # Try Inward?
    # Tips touching in center (we already did this, Tri-Star).
    # Score was 1.08.
    
    # Try "Cyclic Interlock" (Pinwheel)
    # T1 points Up.
    # T2 points Left.
    # T3 points Down-Right?
    # Like a Ninja Star.
    # 3 Trees.
    
    print("\n--- Testing Pinwheel ---")
    pinwheel = []
    # T1 at (0, r), angle 0
    # T2 at (r*cos(120), r*sin(120)), angle 120
    # ...
    # But shifted to interlock sides?
    # This is complex to guess. 
    # But usually "Brick" is just a flattened Pinwheel (2-fold symmetry).
    # 3-fold symmetry usually wastes space because the square bounding box kills it.
    
    # Square box around a triangle is inefficient. Area triangle = 0.43 * side^2.
    # Area square = side^2.
    # You lose 50% efficiency immediately by putting a triangle in a square.
    
    print("Skipping Pinwheel optimization (Geometric constraint: Triangle in Square < 0.5 efficiency)")

if __name__ == "__main__":
    test_triangle_cycle()
