import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.bio_optimizer import BioOptimizer
from src.models.bio_growth_solver import BioGrowthSolver
from scripts.visualize_results import plot_trees

def main():
    milestones = [1, 50, 100, 200]
    results = []

    print("--- Running Bio-Growth (Evolved) ---")
    for n in milestones:
        print(f"Optimizing for N={n}...")
        optimizer = BioOptimizer(population_size=10)
        best_dna, best_score = optimizer.evolve(num_trees=n, generations=5)
        
        solver = BioGrowthSolver(best_dna)
        trees, side = solver.solve(n)
        
        print(f"N={n}: Score={best_score:.6f}")
        results.append({'N': n, 'Score': float(best_score)})
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"bio_growth_{n:03d}.png")

    pd.DataFrame(results).to_csv(PROJECT_ROOT / "results" / "scores_bio_growth.csv", index=False)

if __name__ == "__main__":
    main()
