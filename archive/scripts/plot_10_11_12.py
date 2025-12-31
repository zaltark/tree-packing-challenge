import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from scripts.visualize_results import plot_trees

def generate_specific_plots():
    submission_path = PROJECT_ROOT / "results" / "brick_tiler_submission.csv"
    df = pd.read_csv(submission_path)
    
    # Clean data
    df['x'] = df['x'].astype(str).str.replace('s', '').astype(float)
    df['y'] = df['y'].astype(str).str.replace('s', '').astype(float)
    df['angle'] = df['deg'].astype(str).str.replace('s', '').astype(float)
    df['N_group'] = df['id'].str.split('_').str[0].astype(int)
    
    targets = [10, 11, 12]
    output_dir = PROJECT_ROOT / "results" / "plots"
    
    for n in targets:
        group_df = df[df['N_group'] == n]
        plot_trees(group_df, output_path=output_dir / f"brick_tiler_{n:03d}.png")
        print(f"Generated plot for N={n}")

if __name__ == "__main__":
    generate_specific_plots()
