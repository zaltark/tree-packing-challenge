from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data Directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Specification Files
COMPETITION_OVERVIEW_PATH = PROJECT_ROOT / "COMPETITION_OVERVIEW.md"
TREE_SPECIFICATIONS_PATH = PROJECT_ROOT / "TREE_SPECIFICATIONS.md"

# Models
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Output/Results
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
