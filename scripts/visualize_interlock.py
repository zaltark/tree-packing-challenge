import sys
from pathlib import Path
import matplotlib.pyplot as plt
from decimal import Decimal

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

def visualize_interlock(dx, dy):
    t1 = ChristmasTree(0, 0, 0)
    t2 = ChristmasTree(dx, dy, 180)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    for i, tree in enumerate([t1, t2]):
        poly = tree.get_polygon()
        x, y = poly.exterior.xy
        # Scale back coordinates for plotting
        x = [val / float(SCALE_FACTOR) for val in x]
        y = [val / float(SCALE_FACTOR) for val in y]
        color = 'green' if i == 0 else 'red'
        ax.fill(x, y, alpha=0.5, fc=color, ec='black', label=f'Tree {i+1}')
        
    # Calculate bounding box in original scale
    all_x = []
    all_y = []
    for tree in [t1, t2]:
        poly = tree.get_polygon()
        x, y = poly.exterior.xy
        all_x.extend([val / float(SCALE_FACTOR) for val in x])
        all_y.extend([val / float(SCALE_FACTOR) for val in y])
    
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    width = max_x - min_x
    height = max_y - min_y
    side = max(width, height)
    
    # Draw bounding square
    rect = plt.Rectangle((min_x, min_y), side, side, linewidth=2, edgecolor='blue', facecolor='none', linestyle='--', label='Bounding Square')
    ax.add_patch(rect)
    
    ax.set_aspect('equal')
    ax.legend()
    ax.set_title(f"Interlock: dx={dx}, dy={dy}\nSide={side:.4f}, Score={ (side**2)/2 :.4f}")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    output_path = Path("results/plots/perfect_interlock.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    print(f"Visualization saved to {output_path}")

if __name__ == "__main__":
    # Best values from optimize_pair.py
    best_dx, best_dy = 0.394118, 0.694118
    visualize_interlock(best_dx, best_dy)
