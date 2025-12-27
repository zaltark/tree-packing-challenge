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



## Model Benchmarks (Final Scores)







| N | Greedy Baseline | Bio-Growth (Evolved) | Hybrid Sunflower | Winner |



| :--- | :--- | :--- | :--- | :--- |



| **1** | **0.845** | 1.000 | 1.000 | Greedy |



| **50** | **0.822** | 0.904 | 1.623 | Greedy |



| **100** | **0.860** | 0.872 | 1.741 | Greedy |



| **250** | **0.846** | 0.864 | 2.351 | Greedy |







### Status Report



- **Greedy Baseline:** Most consistent performer across all scales. Its constructive "slide-in" mechanic handles local interlocking effectively.



- **Bio-Growth (Evolved):** Shows strong potential at scale (N=100+). The evolved square-aware spiral successfully minimizes global bounding boxes.



- **Hybrid Sunflower:** **FAILED.** The current implementation of switching to "corner filling" logic expanded the bounding box rather than compressing it. The model has been sidelined but preserved for post-mortem analysis.




