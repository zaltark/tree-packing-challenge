# Santa 2025: Tree Packing Challenge

Repository for the Santa 2025 Tree Packing Challenge. This project is structured to move beyond notebooks into a robust, local development pipeline.

## Core Modules

- **[src/models/tree_geometry.py](src/models/tree_geometry.py)**: **The Rules.** Contains the `ChristmasTree` class with precise polygon definitions. This is the source of truth for tree dimensions and rotations.
- **[src/models/engine.py](src/models/engine.py)**: **The Validator.** Implements efficient collision detection using `shapely.strtree.STRtree` and calculates the competition score.
- **[src/models/solver.py](src/models/solver.py)**: **The Brains.** Where the packing algorithms live. Currently implements a greedy "slide-in" heuristic with weighted axis-aligned rotations.
- **[src/submission/formatter.py](src/submission/formatter.py)**: **The Administrative.** Handles the conversion of coordinate data into the specific `s{value}` string format and `id` structure required for Kaggle submissions.

## Project Structure

- `data/`: Local storage for competition data (ignored by git).
- `scripts/`: Executable scripts for EDA, testing, and visualization.
- `results/`: Output directory for plots and submission files.
- `config/`: Centralized path management to ensure portability across environments.

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Geometry:**
   ```bash
   python scripts/test_tree.py
   ```

3. **Run Baseline Solver & Visualize:**
   ```bash
   python scripts/visualize_results.py
   ```

## References
- [COMPETITION_OVERVIEW.md](COMPETITION_OVERVIEW.md): Goals, evaluation metrics, and timeline.
- [TREE_SPECIFICATIONS.md](TREE_SPECIFICATIONS.md): Detailed vertex coordinates and geometric constraints.