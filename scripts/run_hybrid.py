import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.hybrid_solver import HybridPhyllotaxisSolver
from scripts.visualize_results import plot_trees

def main():
    milestones = [1, 50, 100, 250]
    results = []
    
    # We can experiment with core_ratio. 
    # Let's use 0.7 (70% spiral, 30% corner fill)
    solver = HybridPhyllotaxisSolver(core_ratio=0.7, c_factor=0.35)

    print("--- Running Hybrid Sunflower-in-a-Pot ---")
    for n in milestones:
        trees, side = solver.solve(n)
        score = (side**2) / n
        print(f"N={n}: Score={score:.6f}")
        results.append({'N': n, 'Score': float(score)})
        
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"hybrid_sunflower_{n:03d}.png")

    pd.DataFrame(results).to_csv(PROJECT_ROOT / "results" / "scores_hybrid.csv", index=False)

if __name__ == "__main__":
    main()
