import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.crystal_growth_solver import CrystalGrowthSolver
from src.submission.formatter import SubmissionFormatter

def main():
    MAX_N = 200
    all_results = {}
    
    solver = CrystalGrowthSolver()
    
    print(f"Generating full submission for N=1 to {MAX_N} in ONE PASS...")
    
    # Solve for the largest N
    final_trees, _ = solver.solve(MAX_N)
    
    # Save the first n trees for each problem n
    for n in range(1, MAX_N + 1):
        trees_subset = final_trees[:n]
        
        data = []
        for t in trees_subset:
            data.append({
                'x': t.center_x,
                'y': t.center_y,
                'angle': t.angle
            })
        
        all_results[n] = pd.DataFrame(data)
        
        if n % 50 == 0:
            print(f"Captured results for problem {n}...")

    # Save to final submission file
    output_path = PROJECT_ROOT / "results" / "submission.csv"
    SubmissionFormatter.create_submission_file(all_results, output_path)
    print(f"\nSUCCESS: Final submission generated at {output_path}")

if __name__ == "__main__":
    main()