import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR
from scripts.visualize_results import plot_trees

def verify_extreme_tight():
    # Experimental Point
    dx = 0.45
    dy = 0.25
    
    t1 = ChristmasTree(0, 0, 0)
    t2 = ChristmasTree(dx, dy, 180)
    
    print(f"Testing dx={dx}, dy={dy}...")
    print(f"Collision: {t1.intersects(t2)}")
    
    trees = [t1, t2]
    data = [{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees]
    df = pd.DataFrame(data)
    
    plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / "extreme_tight_test.png")

if __name__ == "__main__":
    verify_extreme_tight()
