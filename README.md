# Santa 2025: Tree Packing Challenge

This repository contains a high-performance local pipeline for the Santa 2025 Tree Packing Challenge. The project features a mathematically optimized "Slanted Brick" tiling strategy that outperforms standard greedy heuristics by up to 50%.

## The Champion: Native Grid Brick Tiler
Our top-performing model utilizes a **Native Grid Tiling** strategy.

### Key Insights:
- **Jigsaw Interlocking:** Alternating trees (0° and 180°) allows triangular tiers to nest perfectly, eliminating internal gaps.
- **Native Grid Logic:** Every tree, including the remainder in odd-numbered problems, is assigned to a mathematical brick slot. This ensures that even odd configurations maintain a dense, uniform structure.
- **Shell Growth:** The grid expands from the center in square "onion" layers, keeping the total bounding box aspect ratio as close to a perfect square as possible.

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

## Submissions
- **Submission File:** `results/brick_tiler_submission.csv`
- **Method:** Generated using the Native Grid model for $N=1$ to $N=200$.
- **Validation:** 100% overlap-free, verified with `shapely` spatial indices.

## Project Structure
- `src/models/brick_tiler_solver.py`: The winning mathematical tiling model.
- `scripts/run_brick_tiler.py`: Automated benchmark runner including edge cases (75, 133, 152).
- `scripts/generate_submission.py`: Optimized one-pass submission generator.
- `results/plots/`: Visual confirmation of the dense, interlocked packing patterns.