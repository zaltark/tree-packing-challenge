import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from scripts.visualize_results import plot_trees

def visualize_specific_cases():
    cases = [75, 133, 152]
    solver = BrickTilerSolver()
    
    print("Generating visualizations for edge cases...")
    
    for n in cases:
        print(f"Solving for N={n}...")
        trees, side = solver.solve(n)
        
        data = []
        for t in trees:
            data.append({'x': t.center_x, 'y': t.center_y, 'angle': t.angle})
        df = pd.DataFrame(data)
        
        score = (side**2) / n
        filename = f"edge_case_{n:03d}_score_{score:.4f}.png"
        output_path = PROJECT_ROOT / "results" / "plots" / filename
        
        plot_trees(df, output_path=output_path)
        print(f"Saved: {filename}")

if __name__ == "__main__":
    visualize_specific_cases()
