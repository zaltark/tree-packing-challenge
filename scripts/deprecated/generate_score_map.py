import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.greedy_solver import SlideInSolver
from src.models.brick_tiler_solver import BrickTilerSolver

def generate_map():
    MAX_N = 200
    map_data = []
    
    greedy_solver = SlideInSolver()
    brick_solver = BrickTilerSolver()
    
    print(f"Generating full score map for N=1 to {MAX_N}...")
    
    g_trees = []
    for n in range(1, MAX_N + 1):
        # Solve Greedy
        g_trees, g_side = greedy_solver.solve_next(n, existing_trees=g_trees)
        g_score = (g_side**2) / n
        
        # Solve Brick
        b_trees, b_side = brick_solver.solve(n)
        b_score = (b_side**2) / n
        
        best_score = float(min(g_score, b_score))
        winner = "Greedy" if g_score < b_score else "Brick"
        
        # Efficiency = (Sum of Tree Areas) / (Box Area)
        estimated_density = 0.28 / best_score if best_score > 0 else 0
        
        map_data.append({
            'N': n,
            'Greedy_Score': float(g_score),
            'Brick_Score': float(b_score),
            'Best_Score': float(best_score),
            'Winner': winner,
            'Density': float(estimated_density)
        })
        
        if n % 25 == 0:
            print(f"Mapped up to N={n}...")

    df = pd.DataFrame(map_data)
    df.to_csv(PROJECT_ROOT / "results" / "full_score_map.csv", index=False)
    
    # Visualization: Efficiency Dropoff
    plt.figure(figsize=(12, 6))
    plt.plot(df['N'], df['Best_Score'], label='Best Score')
    plt.axhline(y=df['Best_Score'].mean(), color='r', linestyle='--', label='Average')
    plt.title('Score Efficiency by Problem Size (Lower is Better)')
    plt.xlabel('N (Number of Trees)')
    plt.ylabel('Score (Side^2 / N)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(PROJECT_ROOT / "results" / "plots" / "score_efficiency_map.png")
    
    print(f"Score map saved to results/full_score_map.csv")
    print(f"Efficiency chart saved to results/plots/score_efficiency_map.png")
    
    # Final Total Score estimate
    print(f"\nESTIMATED TOTAL COMPETITION SCORE: {df['Best_Score'].sum():.4f}")

if __name__ == "__main__":
    generate_map()
