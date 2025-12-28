import sys
from pathlib import Path
import pandas as pd
import random
import copy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.brick_stacker_solver import BrickStackerSolver
from scripts.visualize_results import plot_trees

def evolve_stacker(n_trees, generations=15):
    print(f"\n--- Evolving Brick Lattice for N={n_trees} ---")
    population = []
    # Seed with vectors near the theoretical interlock
    for _ in range(25):
        population.append({
            'block_dx': random.uniform(0.3, 0.4),
            'block_dy': random.uniform(0.7, 0.9),
            'v1_x': random.uniform(0.65, 0.8),
            'v1_y': random.uniform(-0.05, 0.05),
            'v2_x': random.uniform(0.1, 0.4),
            'v2_y': random.uniform(0.7, 0.9)
        })

    best_dna, best_score = None, float('inf')

    for gen in range(generations):
        scored = []
        for dna in population:
            solver = BrickStackerSolver(dna)
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
            for k in child: child[k] += random.uniform(-0.02, 0.02)
            new_pop.append(child)
        population = new_pop

    return best_dna, best_score

def main():
    milestones = [1, 50, 100, 200]
    results = []
    for n in milestones:
        best_dna, score = evolve_stacker(n)
        solver = BrickStackerSolver(best_dna)
        trees, _ = solver.solve(n, stop_on_failure=True)
        results.append({'N': n, 'Score': float(score)})
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"brick_stacker_{n:03d}.png")
    pd.DataFrame(results).to_csv(PROJECT_ROOT / "results" / "scores_brick.csv", index=False)

if __name__ == "__main__":
    main()
