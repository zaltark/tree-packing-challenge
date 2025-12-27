import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

def plot_trees(placements_df, output_path=None):
    """
    Plots the placed trees using matplotlib.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    for _, row in placements_df.iterrows():
        tree = ChristmasTree(center_x=row['x'], center_y=row['y'], angle=row['angle'])
        poly = tree.get_polygon()
        
        # Scale back coordinates for plotting
        x, y = poly.exterior.xy
        x = [val / float(SCALE_FACTOR) for val in x]
        y = [val / float(SCALE_FACTOR) for val in y]
        
        ax.fill(x, y, alpha=0.5, fc='green', ec='darkgreen')

    ax.set_aspect('equal')
    ax.set_title(f"Tree Packing - {len(placements_df)} Trees")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    if output_path:
        plt.savefig(output_path)
        print(f"Plot saved to {output_path}")
    else:
        plt.show()

if __name__ == "__main__":
    from src.models.solver import SlideInSolver
    
    # Run a small simulation and plot
    solver = SlideInSolver()
    results = solver.solve(num_trees=50)
    
    output_dir = PROJECT_ROOT / "results" / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plot_trees(results, output_path=output_dir / "baseline_packing.png")
