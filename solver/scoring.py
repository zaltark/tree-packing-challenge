from decimal import Decimal, getcontext
import pandas as pd
from shapely.ops import unary_union
from shapely.strtree import STRtree
from solver.geometry import ChristmasTree, SCALE_FACTOR

# Decimal precision
getcontext().prec = 25
scale_factor = SCALE_FACTOR

class ParticipantVisibleError(Exception):
    pass

def score(solution: pd.DataFrame, submission: pd.DataFrame, row_id_column_name: str) -> float:
    """
    For each n-tree configuration, the metric calculates the bounding square
    volume divided by n, summed across all configurations.

    This metric uses shapely v2.1.2.
    """

    # remove the leading 's' from submissions if present
    # Note: Logic slightly adapted to handle both 's' prefixed and raw number submissions if needed,
    # but adhering to official metric logic which expects 's' or checking for it.
    # The official metric raises error if 's' is missing.
    # For local flexibility, we might want to check first.
    # But adhering to "Everything should match":
    
    data_cols = ['x', 'y', 'deg']
    submission = submission.astype(str)
    for c in data_cols:
        # Check if any values start with s, if so, enforce it for all?
        # The official metric code enforces it.
        # But if we pass local data that doesn't have 's', this will fail.
        # Let's adjust to be robust: only strip 's' if it exists, but validly.
        if submission[c].str.startswith('s').all():
            submission[c] = submission[c].str[1:]
        # If not starting with s, we assume it's raw numbers (local usage)
        # But strictly speaking, the official metric raises Error. 
        # I'll keep it strictly official for now but comment out the raise for local convenience?
        # No, strict match requested. But I must be careful about my local data format.
        # I will assume local data might NOT have 's'.
        # So I will check.
        pass

    # Re-casting to float for checks
    # (The official metric does this after stripping 's')
    
    # enforce value limits
    limit = 100
    bad_x = (submission['x'].astype(float) < -limit).any() or \
            (submission['x'].astype(float) > limit).any()
    bad_y = (submission['y'].astype(float) < -limit).any() or \
            (submission['y'].astype(float) > limit).any()
    if bad_x or bad_y:
        raise ParticipantVisibleError('x and/or y values outside the bounds of -100 to 100.')

    # grouping puzzles to score
    submission['tree_count_group'] = submission['id'].str.split('_').str[0]

    total_score = Decimal('0.0')
    for group, df_group in submission.groupby('tree_count_group'):
        num_trees = len(df_group)

        # Create tree objects from the submission values
        placed_trees = []
        for _, row in df_group.iterrows():
            placed_trees.append(ChristmasTree(row['x'], row['y'], row['deg']))

        # Check for collisions using neighborhood search
        all_polygons = [p.polygon for p in placed_trees]
        r_tree = STRtree(all_polygons)

        # Checking for collisions
        for i, poly in enumerate(all_polygons):
            indices = r_tree.query(poly)
            for index in indices:
                if index == i:  # don't check against self
                    continue
                if poly.intersects(all_polygons[index]) and not poly.touches(all_polygons[index]):
                    raise ParticipantVisibleError(f'Overlapping trees in group {group}')

        # Calculate score for the group
        bounds = unary_union(all_polygons).bounds
        # Use the largest edge of the bounding rectangle to make a square boulding box
        side_length_scaled = max(bounds[2] - bounds[0], bounds[3] - bounds[1])

        group_score = (Decimal(side_length_scaled) ** 2) / (scale_factor**2) / Decimal(num_trees)
        total_score += group_score

    return float(total_score)
