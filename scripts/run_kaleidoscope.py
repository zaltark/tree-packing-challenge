import sys
from pathlib import Path
import pandas as pd
import random
import copy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.kaleidoscope_solver import KaleidoscopeSolver
from scripts.visualize_results import plot_trees

def evolve_kaleidoscope(n_trees, generations=8):
    print(f"\n--- Evolving Kaleidoscope for N={n_trees} ---")
    population = []
    # Seed with angles around the theoretical optimal 20.4
    for _ in range(10):
        population.append({
            'global_tilt': random.uniform(0, 90),
            'step_size': 0.1 # Faster steps for evolution
        })

    best_dna, best_score = None, float('inf')

    for gen in range(generations):
        scored = []
        for dna in population:
            solver = KaleidoscopeSolver(dna)
            trees, side = solver.solve(n_trees)
            score = (side**2)/n_trees if side != float('inf') else 9999
            scored.append((score, dna))
            if score < best_score:
                best_score, best_dna = score, copy.deepcopy(dna)

        scored.sort(key=lambda x: x[0])
        print(f"Gen {gen}: Best Score = {scored[0][0]:.6f} (tilt={scored[0][1]['global_tilt']:.2f})")

        # Reproduce
        new_pop = [x[1] for x in scored[:3]]
        while len(new_pop) < len(population):
            parent = random.choice(scored[:5])[1]
            child = copy.deepcopy(parent)
            child['global_tilt'] += random.uniform(-2.0, 2.0)
            new_pop.append(child)
        population = new_pop

    return best_dna, best_score

def main():
    milestones = [1, 50, 100, 200]
    results = []
    for n in milestones:
        best_dna, score = evolve_kaleidoscope(n)
        # Final high-precision run
        best_dna['step_size'] = 0.05
        solver = KaleidoscopeSolver(best_dna)
        trees, _ = solver.solve(n, stop_on_failure=True)
        
        results.append({'N': n, 'Score': float(score)})
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
        plot_trees(df, output_path=PROJECT_ROOT / "results" / "plots" / f"kaleidoscope_{n:03d}.png")
    
    pd.DataFrame(results).to_csv(PROJECT_ROOT / "results" / "scores_kaleidoscope.csv", index=False)

if __name__ == "__main__":
    main()
