import sys
from pathlib import Path
import pandas as pd
from decimal import Decimal
import matplotlib.pyplot as plt

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from src.models.tree_geometry import SCALE_FACTOR
from src.models.metric import score, ParticipantVisibleError
from scripts.visualize_results import plot_trees

def diagnose(n):
    print(f"\n--- DIAGNOSING CONFIGURATION N={n} ---")
    
    # 1. Run Solver
    solver = BrickTilerSolver()
    trees, side_scaled = solver.solve(n)
    
    # 2. Prepare Data
    data = []
    for t in trees:
        data.append({
            'x': t.center_x,
            'y': t.center_y,
            'angle': t.angle,
            'id': f"001_{len(data)}" # Dummy ID for metric
        })
    df = pd.DataFrame(data)
    
    # Format for Metric (Metric expects strings with 's' prefix for robustness, but our local score func handles it?)
    # Actually, looking at metric.py, it expects the 'submission' format (id, x, y, deg)
    # and it handles stripping 's'. It also checks constraints.
    # Let's create a "submission-like" dataframe.
    
    sub_df = df.copy()
    sub_df['x'] = sub_df['x'].apply(lambda v: f"s{v}")
    sub_df['y'] = sub_df['y'].apply(lambda v: f"s{v}")
    sub_df['deg'] = sub_df['angle'].apply(lambda v: f"s{v}")
    # metric.py uses 'id' to group. We can just set all to same group '001'
    sub_df['id'] = [f"001_{i}" for i in range(len(sub_df))]
    
    # 3. Calculate Score & Verify
    print("Verifying against official metric...")
    try:
        # Pass dummy solution (not used) and our submission df
        # The score function calculates (side^2)/N
        calc_score = score(pd.DataFrame(), sub_df, 'id')
        print(f"VERIFICATION PASSED.")
        print(f"Official Score: {calc_score:.12f}")
    except ParticipantVisibleError as e:
        print(f"VERIFICATION FAILED: {e}")
        calc_score = None
    except Exception as e:
        print(f"SYSTEM ERROR: {e}")
        calc_score = None
        
    # 4. Check Bounds Manually
    # Scaled side
    print(f"Solver Reported Scaled Side: {side_scaled}")
    
    # Unscaled dimensions
    unscaled_side = Decimal(side_scaled) / SCALE_FACTOR
    print(f"Unscaled Bounding Box Side: {unscaled_side:.6f}")
    
    # 5. Plot
    plot_path = PROJECT_ROOT / "results" / "plots" / f"diagnostic_{n}.png"
    print(f"Generating plot at {plot_path}...")
    plot_trees(df, output_path=plot_path)
    
    return calc_score

if __name__ == "__main__":
    # Default to 50 for quick check, or take arg
    target_n = 50
    if len(sys.argv) > 1:
        try:
            target_n = int(sys.argv[1])
        except ValueError:
            pass
            
    diagnose(target_n)
