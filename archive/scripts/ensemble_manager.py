import sys
from pathlib import Path
import pandas as pd
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

def get_exact_score(group_df):
    """Calculates the 100% accurate bounding box score for a set of trees."""
    trees = []
    for _, row in group_df.iterrows():
        x = float(row['x'].replace('s',''))
        y = float(row['y'].replace('s',''))
        a = float(row['deg'].replace('s',''))
        trees.append(ChristmasTree(x, y, a).get_polygon())
    
    bounds = unary_union(trees).bounds
    side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
    n = len(group_df)
    return (side**2) / n

def ensemble():
    brick_path = PROJECT_ROOT / "results" / "brick_tiler_submission.csv"
    prime_path = PROJECT_ROOT / "results" / "prime_solver_small_n.csv"
    output_path = PROJECT_ROOT / "results" / "final_ensemble_submission.csv"

    if not brick_path.exists() or not prime_path.exists():
        print("Error: Ensure both brick_tiler_submission.csv and prime_solver_small_n.csv exist.")
        return

    df_b = pd.read_csv(brick_path)
    df_p = pd.read_csv(prime_path)

    # Parse problem IDs
    df_b['n_id'] = df_b['id'].apply(lambda x: int(x.split('_')[0]))
    df_p['n_id'] = df_p['id'].apply(lambda x: int(x.split('_')[0]))

    final_rows = []
    print("--- Ensemble Manager Face-Off ---")
    
    total_score = 0
    for n in range(1, 201):
        # Filter groups
        group_b = df_b[df_b['n_id'] == n]
        group_p = df_p[df_p['n_id'] == n]

        if group_p.empty:
            winner = group_b
            score = get_exact_score(group_b)
            name = "Architect (Brick)"
        else:
            score_b = get_exact_score(group_b)
            score_p = get_exact_score(group_p)
            
            if score_b < score_p:
                winner = group_b
                score = score_b
                name = "Architect (Brick)"
            else:
                winner = group_p
                score = score_p
                name = "Prime Solver (Anneal)"

        if n <= 10 or n % 50 == 0:
            print(f"N={n:03d}: Winner={name} | Score={score:.4f}")
        
        total_score += score
        final_rows.append(winner[['id', 'x', 'y', 'deg']])

    result = pd.concat(final_rows)
    result.to_csv(output_path, index=False)
    print(f"\nEnsemble Complete!")
    print(f"Estimated Total Leaderboard Score: {total_score:.4f}")
    print(f"Final File: {output_path}")

if __name__ == "__main__":
    ensemble()
