import sys
from pathlib import Path
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from scripts.visualize_results import plot_trees

def regenerate_plots():
    submission_path = PROJECT_ROOT / "results" / "brick_tiler_submission.csv"
    if not submission_path.exists():
        print("Submission file not found!")
        return
        
    print(f"Loading submission from {submission_path}...")
    df = pd.read_csv(submission_path)
    
    # Clean data (remove 's' prefix)
    df['x'] = df['x'].astype(str).str.replace('s', '').astype(float)
    df['y'] = df['y'].astype(str).str.replace('s', '').astype(float)
    df['angle'] = df['deg'].astype(str).str.replace('s', '').astype(float)
    
    # Extract N from ID
    df['N_group'] = df['id'].str.split('_').str[0].astype(int)
    
    targets = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 50, 75, 100, 133, 152, 200]
    
    print(f"Regenerating plots for N={targets}...")
    
    output_dir = PROJECT_ROOT / "results" / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for n in targets:
        group_df = df[df['N_group'] == n]
        if group_df.empty:
            print(f"Warning: No data found for N={n}")
            continue
            
        plot_trees(group_df, output_path=output_dir / f"brick_tiler_{n:03d}.png")

if __name__ == "__main__":
    regenerate_plots()
