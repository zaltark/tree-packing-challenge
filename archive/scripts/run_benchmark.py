import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main():
    print("\n--- Aggregating Benchmark Results ---")
    
    brick_tiler_file = PROJECT_ROOT / "results" / "scores_brick_tiler.csv"
    prime_solver_file = PROJECT_ROOT / "results" / "scores_prime_solver.csv"
    
    files = [
        (brick_tiler_file, 'Brick Tiler'),
        (prime_solver_file, 'Prime Solver')
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