# Santa 2025: Tree Packing Challenge

This repository contains a high-performance local pipeline for the Santa 2025 Tree Packing Challenge.

## Current Strategy: The Duo
We use a two-pronged approach for optimal packing:
1. **The Architect (Brick Tiler):** Our primary high-N engine using a Slanted Brick tiling strategy.
2. **The Prime Solver (Annealer):** Our specialized model used for small N and complex odd/prime configurations where rigid grids are less efficient.

### Key Insights:
- **Jigsaw Interlocking:** Alternating trees (0° and 180°) allows triangular tiers to nest perfectly, eliminating internal gaps.
- **Native Grid Logic:** The Brick Tiler assigns trees to mathematical brick slots for uniform density.
- **Prime Optimization:** The Prime Solver uses simulated annealing to find organic, high-density clusters for edge cases.

## Model Benchmarks (Final Scores)

| N | Greedy Baseline | Bio-Growth | **Brick Tiler (Native)** | Winner |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 0.950 | 1.000 | **0.662** | **Brick** |
| **50** | 0.860 | 1.058 | **0.550** | **Brick** |
| **75** | - | - | **0.484** | **Brick** |
| **100** | 0.830 | 1.038 | **0.454** | **Brick** |
| **133** | - | - | **0.417** | **Brick** |
| **152** | - | - | **0.438** | **Brick** |
| **200** | 0.880 | 0.977 | **0.431** | **Brick** |

## Deprecated Models (Ended Tests)
The following strategies have been tested and moved to `src/models/deprecated/` as they were outperformed by the current duo:
- **Bio-Growth:** Biological spiral expansion.
- **Hybrid Sunflower:** Combined spiral and corner-fill.
- **Crystal Growth:** Seed-based expansion.
- **Kaleidoscope:** Radial symmetry packing.
- **Greedy / Slanted Row:** Simple heuristic baselines.

## Submissions
- **Submission File:** `results/final_ensemble_submission.csv`
- **Method:** Generated using the `ensemble_manager.py` which picks the best result between Brick Tiler and Prime Solver for each N.
- **Validation:** 100% overlap-free, verified with `shapely` spatial indices.

## Project Structure
- `src/models/brick_tiler_solver.py`: The primary mathematical tiling model.
- `src/models/prime_solver.py`: The annealing solver for prime/odd cases.
- `scripts/ensemble_manager.py`: Combines outputs from both solvers.
- `results/plots/`: Visual confirmation of the packing patterns.