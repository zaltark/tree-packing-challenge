import pandas as pd
from pathlib import Path

class SubmissionFormatter:
    """
    Handles formatting of tree placements into the specific string format
    required for the Santa 2025 Tree Packing Challenge.
    """
    
    @staticmethod
    def format_value(val):
        """Converts a float/Decimal to the required 's{value}' string format."""
        return f"s{val}"

    @staticmethod
    def create_submission_file(all_results, output_path):
        """
        Generates the submission CSV from a dictionary of results.
        
        Args:
            all_results (dict): A dictionary where keys are the number of trees (N)
                                and values are DataFrames containing columns ['x', 'y', 'angle']
                                for that N-tree solution.
                                Example: { 1: df_1_tree, 2: df_2_trees, ... }
            output_path (Path): Path to save the CSV.
        """
        submission_rows = []
        
        # Sort keys to ensure order 001, 002, 003...
        sorted_n = sorted(all_results.keys())
        
        for n in sorted_n:
            df = all_results[n]
            
            # Reset index to get tree_index (0 to n-1)
            # Assuming df is sorted or simple list of placements
            for tree_idx, row in df.reset_index(drop=True).iterrows():
                
                # Format ID: 001_0, 005_4, 150_22, etc.
                problem_id = f"{n:03d}"
                row_id = f"{problem_id}_{tree_idx}"
                
                submission_rows.append({
                    'id': row_id,
                    'x': SubmissionFormatter.format_value(row['x']),
                    'y': SubmissionFormatter.format_value(row['y']),
                    'deg': SubmissionFormatter.format_value(row['angle'])
                })
                
        submission_df = pd.DataFrame(submission_rows)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        submission_df.to_csv(output_path, index=False)
        print(f"Submission saved to {output_path}")
        return submission_df

if __name__ == "__main__":
    # Test with dummy data
    from decimal import Decimal
    
    # Mock result for N=2
    df_2 = pd.DataFrame([
        {'x': Decimal('0.0'), 'y': Decimal('0.0'), 'angle': Decimal('0.0')},
        {'x': Decimal('5.5'), 'y': Decimal('5.5'), 'angle': Decimal('90.0')}
    ])
    
    # Mock result for N=3
    df_3 = pd.DataFrame([
        {'x': 0, 'y': 0, 'angle': 0},
        {'x': 2, 'y': 2, 'angle': 45},
        {'x': -2, 'y': -2, 'angle': 180}
    ])
    
    results = {2: df_2, 3: df_3}
    
    # Save to a temp test file
    test_path = Path("results/test_submission.csv")
    SubmissionFormatter.create_submission_file(results, test_path)
