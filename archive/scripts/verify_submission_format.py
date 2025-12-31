import sys
from pathlib import Path
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.metric import score, ParticipantVisibleError

def verify_submission_format(submission_path):
    print(f"Verifying {submission_path}...")
    
    try:
        submission = pd.read_csv(submission_path)
    except Exception as e:
        print(f"FAILED: Could not read CSV. {e}")
        return

    # Check headers
    expected_headers = ['id', 'x', 'y', 'deg']
    if list(submission.columns) != expected_headers:
        print(f"FAILED: Headers do not match. Found {list(submission.columns)}, expected {expected_headers}")
        return

    # Create a dummy solution dataframe (metric requires it but doesn't strictly use it for scoring calculation logic unless validating IDs, but the provided metric snippet mostly uses submission)
    # The provided metric code:
    # def score(solution: pd.DataFrame, submission: pd.DataFrame, row_id_column_name: str) -> float:
    # It uses submission for everything. 'solution' is usually for ground truth in other Kaggle comps but here the 'truth' is geometric validity.
    
    # However, the metric function provided in the prompt uses `solution`?
    # Let's look at `src/models/metric.py` again.
    # It takes `solution` but I don't see it used in the snippet I wrote?
    # Ah, I wrote: `def score(solution: pd.DataFrame, submission: pd.DataFrame, row_id_column_name: str) -> float:`
    # And then I never used `solution` in the body.
    # This matches the Kaggle Metric template where `solution` is passed but for this specific problem (optimization), the score is derived solely from submission validity.
    
    solution = pd.DataFrame(columns=['id']) # Dummy
    
    try:
        calculated_score = score(solution, submission, 'id')
        print(f"SUCCESS: Submission format is valid. Calculated Score: {calculated_score}")
    except ParticipantVisibleError as e:
        print(f"FAILED: Metric Validation Error: {e}")
    except Exception as e:
        print(f"FAILED: Runtime Error: {e}")

if __name__ == "__main__":
    submission_file = PROJECT_ROOT / "results" / "brick_tiler_submission.csv"
    verify_submission_format(submission_file)
