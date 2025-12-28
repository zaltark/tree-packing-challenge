import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.slanted_onion_solver import SlantedOnionSolver
from scripts.visualize_results import plot_trees

def main():
    milestones = [1, 50, 75, 100, 133, 152, 200]
    results = []
    
    print("--- Running Slanted Onion (Lattice Stacking) ---")
    for n in milestones:
        solver = SlantedOnionSolver()
        trees, side = solver.solve(n, stop_on_failure=True)
        
        score = (side**2)/n
        print(f"N={n}: Score={score:.6f}")
        results.append({'N': n, 'Score': float(score)})
        
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"slanted_onion_{n:03d}.png")

    pd.DataFrame(results).to_csv(PROJECT_ROOT / "results" / "scores_slanted_onion.csv", index=False)

if __name__ == "__main__":
    main()
