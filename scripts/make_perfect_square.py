import sys
from pathlib import Path
import pandas as pd
from decimal import Decimal

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree
from scripts.visualize_results import plot_trees

def make_perfect_square():
    print("Building the fundamental interlocked square...")
    
    # Fundamental offsets discovered from tree geometry:
    # Upright Tree: Tip (0, 0.8), Corners (+/-0.35, 0)
    # Inverted Tree: Tip (0, 0), Corners (+/-0.35, 0.8)
    
    # 1. Base Upright
    t1 = ChristmasTree(0, 0, 0)
    
    # 2. Inverted Tree shifted so its Tip (0,0) touches T1's Tip (0,0.8) 
    # and its corner touches T1's corner.
    # Offset: dx=0.35, dy=0.8
    t2 = ChristmasTree(0.35, 0.8, 180)
    
    # 3. Next Upright Tree (Right)
    t3 = ChristmasTree(0.7, 0, 0)
    
    # 4. Next Inverted Tree (Right)
    t4 = ChristmasTree(1.05, 0.8, 180)
    
    trees = [t1, t2, t3, t4]
    
    data = []
    for t in trees:
        data.append({'x': t.center_x, 'y': t.center_y, 'angle': t.angle})
    df = pd.DataFrame(data)
    
    plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / "perfect_starting_square.png")
    print("Square patch saved to results/plots/perfect_starting_square.png")

if __name__ == "__main__":
    make_perfect_square()
