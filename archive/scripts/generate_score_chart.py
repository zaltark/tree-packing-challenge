import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from decimal import Decimal

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from src.models.tree_geometry import SCALE_FACTOR
from config.best_known import BEST_KNOWN_SIDES

def generate_chart():
    sizes = [1, 10, 25, 50, 100, 150, 200]
    solver = BrickTilerSolver()
    
    my_scores = []
    best_known_scores = []
    
    print(f"{ 'N':<5} | {'Side (Scaled)':<20} | {'Score':<10}")
    print("-" * 40)
    
    for n in sizes:
        # Run my solver
        trees, side_scaled = solver.solve(n)
        
        # Calculate Score
        # Score = (SideScaled^2) / (ScaleFactor^2) / N
        score_val = (Decimal(side_scaled) ** 2) / (SCALE_FACTOR ** 2) / Decimal(n)
        my_scores.append(float(score_val))
        
        print(f"{n:<5} | {side_scaled:<20.2f} | {score_val:.6f}")
        
        # Calculate Best Known Score if available
        if n in BEST_KNOWN_SIDES:
            # BEST_KNOWN_SIDES are typically unscaled side lengths (standard units)
            # based on how they were written in the file (e.g. 0.92, 10.51)
            # Let's verify: 
            # 200 trees -> side ~10.51. Area ~110. 110/200 = 0.55 per tree.
            # Yes, they are unscaled.
            bk_side = BEST_KNOWN_SIDES[n]
            bk_score = (bk_side ** 2) / n
            best_known_scores.append(bk_score)
        else:
            best_known_scores.append(None)

    # Plotting
    plt.figure(figsize=(10, 6))
    
    plt.plot(sizes, my_scores, marker='o', linestyle='-', label='Brick Tiler (Current)')
    
    # Filter None values for Best Known
    bk_sizes = [sizes[i] for i in range(len(sizes)) if best_known_scores[i] is not None]
    bk_vals = [s for s in best_known_scores if s is not None]
    
    if bk_vals:
        plt.plot(bk_sizes, bk_vals, marker='x', linestyle='--', color='red', label='Best Known Targets')
    
    plt.title('Tree Packing Score vs N (Lower is Better)')
    plt.xlabel('Number of Trees (N)')
    plt.ylabel('Score (Side^2 / N)')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.legend()
    
    output_path = PROJECT_ROOT / "results" / "plots" / "score_chart.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    print(f"\nChart saved to {output_path}")

if __name__ == "__main__":
    generate_chart()
