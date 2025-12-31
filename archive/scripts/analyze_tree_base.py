import sys
from pathlib import Path
import matplotlib.pyplot as plt
from shapely.geometry import box
from shapely.affinity import rotate, translate

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

def analyze_single_tree():
    # Create standard tree
    t = ChristmasTree(0, 0, 0)
    poly = t.get_polygon()
    
    # Get Bounds
    minx, miny, maxx, maxy = poly.bounds
    width = maxx - minx
    height = maxy - miny
    
    from decimal import Decimal
    
    print(f"Single Tree Bounds:")
    print(f"Min X: {Decimal(minx)/SCALE_FACTOR:.4f}, Max X: {Decimal(maxx)/SCALE_FACTOR:.4f}")
    print(f"Min Y: {Decimal(miny)/SCALE_FACTOR:.4f}, Max Y: {Decimal(maxy)/SCALE_FACTOR:.4f}")
    print(f"Width: {Decimal(width)/SCALE_FACTOR:.4f}")
    print(f"Height: {Decimal(height)/SCALE_FACTOR:.4f}")
    print(f"Bounding Box Area: {(Decimal(width)*Decimal(height))/(SCALE_FACTOR**2):.6f}")
    
    # Visualizing 'Touch' Border
    # In Shapely, touch means intersection of boundary but not interior.
    # Effectively buffer=0.
    
    # Let's plot the bounding box vs the tree
    fig, ax = plt.subplots(figsize=(6, 8))
    
    # Tree
    x, y = poly.exterior.xy
    x = [val / float(SCALE_FACTOR) for val in x]
    y = [val / float(SCALE_FACTOR) for val in y]
    ax.fill(x, y, alpha=0.5, fc='green', ec='black', label='Tree')
    
    # Bounding Box
    bbox = box(minx, miny, maxx, maxy)
    bx, by = bbox.exterior.xy
    bx = [val / float(SCALE_FACTOR) for val in bx]
    by = [val / float(SCALE_FACTOR) for val in by]
    ax.plot(bx, by, 'r--', label='Bounding Box')
    
    ax.set_aspect('equal')
    ax.legend()
    ax.set_title("Single Tree Bounding Box")
    
    out_path = PROJECT_ROOT / "results" / "plots" / "single_tree_analysis.png"
    plt.savefig(out_path)
    print(f"Plot saved to {out_path}")

if __name__ == "__main__":
    analyze_single_tree()
