import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from config.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, PROJECT_ROOT

def test_paths():
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Raw Data: {RAW_DATA_DIR}")
    print(f"Processed Data: {PROCESSED_DATA_DIR}")
    
    if PROJECT_ROOT.exists():
        print("SUCCESS: Project root exists.")
    else:
        print("ERROR: Project root not found.")

if __name__ == "__main__":
    test_paths()
