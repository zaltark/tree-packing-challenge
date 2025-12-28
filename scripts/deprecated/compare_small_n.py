import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.greedy_solver import SlideInSolver
from src.models.brick_tiler_solver import BrickTilerSolver

def compare():
    greedy = SlideInSolver()
    brick = BrickTilerSolver()
    
    data = []
    print("Comparing models for N=1 to 20...")
    
    g_trees = []
    for n in range(1, 21):
        # Greedy
        g_trees, g_side = greedy.solve_next(n, existing_trees=g_trees)
        g_score = (g_side**2) / n
        
        # Brick
        b_trees, b_side = brick.solve(n)
        b_score = (b_side**2) / n
        
        winner = "Greedy" if g_score < b_score else "Brick"
        print(f"N={n}: Greedy={g_score:.4f}, Brick={b_score:.4f} -> Winner: {winner}")
        
        data.append({
            'N': n,
            'Greedy': float(g_score),
            'Brick': float(b_score),
            'Winner': winner
        })
        
    df = pd.DataFrame(data)
    df.to_csv(PROJECT_ROOT / "results" / "small_n_comparison.csv", index=False)

if __name__ == "__main__":
    compare()
