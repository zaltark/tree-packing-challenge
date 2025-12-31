import sys
from pathlib import Path
import pandas as pd
from decimal import Decimal

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from src.models.tree_geometry import SCALE_FACTOR

def log_all_scores():
    MAX_N = 200
    solver = BrickTilerSolver()
    scores = []
    
    print(f"Logging scores for N=1 to {MAX_N}...")
    for n in range(1, MAX_N + 1):
        _, side_scaled = solver.solve(n)
        score_val = (Decimal(side_scaled) ** 2) / (SCALE_FACTOR ** 2) / Decimal(n)
        scores.append({'N': n, 'Score': float(score_val)})
        
    df = pd.DataFrame(scores)
    output_path = PROJECT_ROOT / "results" / "scores_brick_tiler.csv"
    df.to_csv(output_path, index=False)
    print(f"Scores logged to {output_path}")

if __name__ == "__main__":
    log_all_scores()
