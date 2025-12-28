import sys
from pathlib import Path
import pandas as pd
import random
import copy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.slanted_row_solver import SlantedRowSolver
from scripts.visualize_results import plot_trees

def evolve_slanted_row(n_trees, generations=15):
    print(f"\n--- Evolving Slanted Row for N={n_trees} ---")
    population = []
    # Seed with safe starting guesses
    for _ in range(25):
        population.append({
            'u_dx': 0.355, 'u_dy': 0.805, # Fixed internal brick
            'v_dx': random.uniform(0.7, 0.8), # Width jump
            'v_dy': 0.0,
            'row_jump_x': random.uniform(0.3, 0.4), # Stagger
            'row_jump_y': random.uniform(0.7, 1.2)  # Vertical jump (Height)
        })

    best_dna, best_score = None, float('inf')

    for gen in range(generations):
        scored = []
        for dna in population:
            solver = SlantedRowSolver(dna)
            trees, side = solver.solve(n_trees)
            score = (side**2)/n_trees if side != float('inf') else 99999
            scored.append((score, dna))
            if score < best_score:
                best_score, best_dna = score, copy.deepcopy(dna)

        scored.sort(key=lambda x: x[0])
        print(f"Gen {gen}: Best Score = {scored[0][0] if scored[0][0] < 90000 else 'FAILED'}")

        # Reproduce
        new_pop = [x[1] for x in scored[:5]]
        while len(new_pop) < len(population):
            parent = random.choice(scored[:10])[1]
            child = copy.deepcopy(parent)
            # Tweak vectors
            child['row_jump_y'] += random.uniform(-0.02, 0.02)
            child['v_dx'] += random.uniform(-0.02, 0.02)
            new_pop.append(child)
        population = new_pop

    return best_dna, best_score

def main():
    milestones = [1, 50, 75, 100, 133, 152, 200]
    results = []
    for n in milestones:
        best_dna, score = evolve_slanted_row(n)
        solver = SlantedRowSolver(best_dna)
        trees, _ = solver.solve(n, stop_on_failure=True)
        results.append({'N': n, 'Score': float(score)})
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"slanted_row_{n:03d}.png")
    pd.DataFrame(results).to_csv(PROJECT_ROOT / "results" / "scores_slanted_row.csv", index=False)

if __name__ == "__main__":
    main()