import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main():
    print("\n--- Aggregating Benchmark Results ---")
    
    greedy_file = PROJECT_ROOT / "results" / "scores_greedy.csv"
    bio_file = PROJECT_ROOT / "results" / "scores_bio_growth.csv"
    hybrid_file = PROJECT_ROOT / "results" / "scores_hybrid.csv"
    crystal_file = PROJECT_ROOT / "results" / "scores_crystal.csv"
    brick_file = PROJECT_ROOT / "results" / "scores_brick.csv"
    brick_tiler_file = PROJECT_ROOT / "results" / "scores_brick_tiler.csv"
    kaleidoscope_file = PROJECT_ROOT / "results" / "scores_kaleidoscope.csv"
    
    files = [
        (greedy_file, 'Greedy Baseline'),
        (bio_file, 'Bio-Growth'),
        (hybrid_file, 'Hybrid Sunflower'),
        (crystal_file, 'Crystal Growth'),
        (brick_file, 'Brick Stacker'),
        (brick_tiler_file, 'Brick Tiler'),
        (kaleidoscope_file, 'Kaleidoscope')
    ]
    
    dfs = []
    for f, name in files:
        if f.exists():
            df = pd.read_csv(f)
            df['Model'] = name
            dfs.append(df)
            
    if not dfs:
        print("No score files found.")
        return

    combined = pd.concat(dfs)
    pivot = combined.pivot(index='N', columns='Model', values='Score')
    
    print(pivot)
    pivot.to_csv(PROJECT_ROOT / "results" / "final_benchmark.csv")

if __name__ == "__main__":
    main()