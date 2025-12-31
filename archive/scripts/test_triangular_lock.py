import sys
from pathlib import Path
import math
from shapely.ops import unary_union

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR
from scripts.visualize_results import plot_trees
import pandas as pd

def test_radial_patterns():
    print("Testing Radial / Rotational Patterns...")
    
    # 1. Tri-Star (N=3, 120 deg)
    # Tips touching at (0,0)
    # Tree Tip is at (0, 0.8) relative to center.
    # So we need to translate tree by (0, -0.8) to put tip at (0,0)?
    # Then rotate.
    
    # Tree Geometry: Tip is at (0, 0.8).
    # To put tip at world (0,0), we place tree at (0, -0.8).
    
    offset_y = -0.8
    
    tri_star = []
    for i in range(3):
        angle = i * 120
        # Rotate the position (0, offset_y) by angle
        rad = math.radians(angle)
        # x' = x cos - y sin
        # y' = x sin + y cos
        # x=0, y=offset_y
        cx = -offset_y * math.sin(rad)
        cy = offset_y * math.cos(rad)
        
        tri_star.append(ChristmasTree(cx, cy, angle))
        
    # Check collision
    collision = False
    for i in range(3):
        for j in range(i+1, 3):
            if tri_star[i].intersects(tri_star[j]):
                collision = True
    
    # Measure
    polys = [t.get_polygon() for t in tri_star]
    bounds = unary_union(polys).bounds
    side = max(bounds[2]-bounds[0], bounds[3]-bounds[1]) / float(SCALE_FACTOR)
    score = (side**2)/3
    
    print(f"\n--- Tri-Star (N=3) ---")
    print(f"Collision: {collision}")
    print(f"Side: {side:.4f}")
    print(f"Score: {score:.4f}")
    print(f"Brick Score Target: 0.66")
    
    if not collision:
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in tri_star])
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / "tri_star_n3.png")

    # 2. Quad-Windmill (N=4, 90 deg)
    # Tips at center
    quad_mill = []
    for i in range(4):
        angle = i * 90
        rad = math.radians(angle)
        cx = -offset_y * math.sin(rad)
        cy = offset_y * math.cos(rad)
        quad_mill.append(ChristmasTree(cx, cy, angle))
        
    collision = False
    for i in range(4):
        for j in range(i+1, 4):
            if quad_mill[i].intersects(quad_mill[j]):
                collision = True
                
    polys = [t.get_polygon() for t in quad_mill]
    bounds = unary_union(polys).bounds
    side = max(bounds[2]-bounds[0], bounds[3]-bounds[1]) / float(SCALE_FACTOR)
    score = (side**2)/4
    
    print(f"\n--- Quad-Windmill (N=4) ---")
    print(f"Collision: {collision}")
    print(f"Side: {side:.4f}")
    print(f"Score: {score:.4f}")
    print(f"Brick Score Target: 0.50")

    if not collision:
         df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in quad_mill])
         plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / "quad_mill_n4.png")

if __name__ == "__main__":
    test_radial_patterns()
