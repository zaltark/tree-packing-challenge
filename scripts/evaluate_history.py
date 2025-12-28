import sys
from pathlib import Path
import pandas as pd
from decimal import Decimal

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.deprecated.greedy_solver import SlideInSolver
from src.models.deprecated.bio_growth_solver import BioGrowthSolver

def evaluate_greedy(n):
    solver = SlideInSolver()
    # Greedy has randomness, let's take best of 3
    best_score = float('inf')
    for _ in range(3):
        _, side = solver.solve_next(n)
        score = float(side**2) / n
        if score < best_score:
            best_score = score
    return best_score

def evaluate_bio(n):
    # Standard DNA roughly from previous runs
    dna = {
        'c_factor': 0.5,
        'golden_angle': 137.508,
        'square_factor': 0.8,
        'rot_mode': 'interlock',
        'seed_data': []
    }
    solver = BioGrowthSolver(dna)
    _, side = solver.solve(n)
    score = float(side**2) / n
    return score

def main():
    target_ns = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 75, 133, 152]
    
    results = []
    for n in target_ns:
        print(f"Evaluating N={n}...")
        g_score = evaluate_greedy(n)
        b_score = evaluate_bio(n)
        results.append({'N': n, 'Greedy': g_score, 'BioGrowth': b_score})
        
    df = pd.DataFrame(results)
    output_path = PROJECT_ROOT / "results" / "historical_scores_fill.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved results to {output_path}")

if __name__ == "__main__":
    main()
