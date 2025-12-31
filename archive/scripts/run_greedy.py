import sys
from pathlib import Path
import pandas as pd
from decimal import Decimal

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.greedy_solver import SlideInSolver
from scripts.visualize_results import plot_trees

def main():
    milestones = [1, 50, 100, 200]
    solver = SlideInSolver()
    current_trees = []
    results = []

    print("--- Running Greedy Baseline ---")
    for n in range(1, max(milestones) + 1):
        current_trees, side = solver.solve_next(n, existing_trees=current_trees)
        if n in milestones:
            score = (side**2) / n
            print(f"N={n}: Score={score:.6f}")
            results.append({'N': n, 'Score': float(score)})
            df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in current_trees])
            plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"greedy_baseline_{n:03d}.png")

    pd.DataFrame(results).to_csv(PROJECT_ROOT / "results" / "scores_greedy.csv", index=False)

if __name__ == "__main__":
    main()
