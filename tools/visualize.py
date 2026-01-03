import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from solver.geometry import ChristmasTree, SCALE_FACTOR

def plot_trees(placements_df, output_path=None):
    """
    Plots the placed trees using matplotlib, including bounding box and score square.
    """
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Track bounds
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    for _, row in placements_df.iterrows():
        tree = ChristmasTree(center_x=row['x'], center_y=row['y'], angle=row['angle'])
        poly = tree.get_polygon()
        
        # Scale back coordinates for plotting
        x, y = poly.exterior.xy
        x = [val / float(SCALE_FACTOR) for val in x]
        y = [val / float(SCALE_FACTOR) for val in y]
        
        # Update bounds
        min_x = min(min_x, min(x))
        min_y = min(min_y, min(y))
        max_x = max(max_x, max(x))
        max_y = max(max_y, max(y))
        
        ax.fill(x, y, alpha=0.5, fc='green', ec='darkgreen')

    # Calculate Dimensions
    width = max_x - min_x
    height = max_y - min_y
    side = max(width, height)
    
    # 1. Tight Bounding Box (Red Dashed)
    rect_bbox = Rectangle((min_x, min_y), width, height, 
                          linewidth=2, edgecolor='red', facecolor='none', linestyle='--', label='Tight Bounds')
    ax.add_patch(rect_bbox)
    
    # 2. Score Square (Blue Dotted) - Centered on the bounding box
    # The score is based on a square of size 'side'. 
    # Visually centering it makes sense.
    center_x = min_x + width / 2
    center_y = min_y + height / 2
    sq_x = center_x - side / 2
    sq_y = center_y - side / 2
    
    rect_score = Rectangle((sq_x, sq_y), side, side, 
                           linewidth=2, edgecolor='blue', facecolor='none', linestyle=':', label=f'Score Square (Side={side:.2f})')
    ax.add_patch(rect_score)

    ax.set_aspect('equal')
    ax.set_title(f"Tree Packing - {len(placements_df)} Trees\nScore Side: {side:.4f}")
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Adjust limits to show the square
    margin = side * 0.1
    ax.set_xlim(sq_x - margin, sq_x + side + margin)
    ax.set_ylim(sq_y - margin, sq_y + side + margin)
    
    if output_path:
        plt.savefig(output_path)
        print(f"Plot saved to {output_path}")
        plt.close(fig) # Close to free memory
    else:
        plt.show()

if __name__ == "__main__":
    from solver.engine import BrickTilerSolver
    
    # Run a small simulation and plot
    solver = BrickTilerSolver()
    trees, _ = solver.solve(num_trees=50)
    results = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
    
    output_dir = PROJECT_ROOT / "output" / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plot_trees(results, output_path=output_dir / "brick_tiler_50.png")
