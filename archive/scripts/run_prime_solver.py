import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.prime_solver import PrimeSolver
from src.submission.formatter import SubmissionFormatter

from src.models.prime_solver import PrimeSolver
from src.submission.formatter import SubmissionFormatter
from src.utils.math_utils import get_primes
from src.models.prime_seeds import get_prime_seed
from scripts.visualize_results import plot_trees

def main():
    # Target all primes up to 30
    targets = get_primes(30)
    all_results = {}
    results = []
    # Geometric Jiggler uses iterations
    solver = PrimeSolver(iterations=10000)
    
    print(f"--- Running The Prime Solver for Primes up to 30 ---")
    for n in targets:
        # Load pattern seeds if available
        seeds = get_prime_seed(n)
        
        trees, side = solver.solve(n, seed_trees=seeds)
        
        # Check for Overlap Failure
        if side == float('inf'):
            print(f"CRITICAL FAILURE: Overlap detected for N={n}. Stopping generation.")
            # Still plot the failure state
            df_fail = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
            plot_trees(df_fail, output_path=PROJECT_ROOT / "results" / "plots" / f"prime_solver_FAILED_{n:03d}.png")
            break

        score = (side**2)/n
        print(f"N={n}: Score={score:.4f} (Side={side:.4f})")
        results.append({'N': n, 'Score': float(score)})
        
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
        all_results[n] = df
        
        # Visualization
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"prime_solver_{n:03d}.png")

    # Save scores for benchmarking
    pd.DataFrame(results).to_csv(PROJECT_ROOT / "results" / "scores_prime_solver.csv", index=False)

    output_path = PROJECT_ROOT / "results" / "prime_solver_small_n.csv"
    SubmissionFormatter.create_submission_file(all_results, output_path)
    print(f"\nPrime Solver results saved to {output_path}")

if __name__ == "__main__":
    main()

