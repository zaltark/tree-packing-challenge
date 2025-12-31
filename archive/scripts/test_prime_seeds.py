import sys
from pathlib import Path
import pandas as pd
from decimal import Decimal

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.prime_seeds import get_prime_seed
from src.models.tree_geometry import SCALE_FACTOR
from src.models.metric import score, ParticipantVisibleError
from scripts.visualize_results import plot_trees

def evaluate_seeds():
    targets = [3, 5, 7]
    
    print(f"{'N':<5} | {'Score':<15} | {'Status':<10}")
    print("-" * 40)
    
    for n in targets:
        trees = get_prime_seed(n)
        
        # Prepare for scoring
        data = []
        for i, t in enumerate(trees):
            data.append({
                'id': f"{n:03d}_{i}",
                'x': f"s{t.center_x}",
                'y': f"s{t.center_y}",
                'deg': f"s{t.angle}",
                # numeric for plotting
                'num_x': t.center_x,
                'num_y': t.center_y,
                'num_angle': t.angle
            })
        
        df = pd.DataFrame(data)
        
        # Format for plotting
        plot_df = pd.DataFrame([{
            'x': row['num_x'], 
            'y': row['num_y'], 
            'angle': row['num_angle']
        } for _, row in df.iterrows()])
        
        # Score
        try:
            # We need to construct the submission df carefully for the metric
            sub_df = df[['id', 'x', 'y', 'deg']]
            final_score = score(pd.DataFrame(), sub_df, 'id')
            status = "VALID"
        except ParticipantVisibleError as e:
            final_score = 999.0
            status = f"FAIL: {e}"
        except Exception as e:
            final_score = 999.0
            status = f"ERR: {e}"
            
        print(f"{n:<5} | {final_score:<15.6f} | {status:<10}")
        
        if status == "VALID":
            plot_trees(plot_df, output_path=PROJECT_ROOT / "results" / "plots" / f"seed_test_{n:03d}.png")

if __name__ == "__main__":
    evaluate_seeds()
