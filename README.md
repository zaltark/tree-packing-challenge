# Santa 2025: Tree Packing Challenge

This repository contains a high-performance local pipeline for the Santa 2025 Tree Packing Challenge. The project evolved from biological growth simulations to a mathematically optimized tiling strategy that significantly outperforms standard greedy heuristics.

## The Strategy: Centric Crystal Growth
Our current champion model, **Centric Crystal Growth**, treats the tree packing problem as a tiling puzzle.

### Key Discoveries:
1.  **Jigsaw Interlocking:** By alternating trees between 0° and 180° rotations, the triangular tiers can "nest" into one another. This is the single most effective way to eliminate empty space.
2.  **Tiling beats Spiral:** While biological spirals (Phyllotaxis) are efficient for circular growth, they leave excessive gaps in the corners of the square bounding boxes required by the competition.
3.  **Centric Proactive Search:** By searching for valid "rooting" spots starting from (0,0) and expanding outwards using a Manhattan-distance priority ($max(|x|, |y|)$), the model naturally forms a dense, square-clump formation (the "X Pattern").
4.  **Nested Solutions:** Because the crystal growth is deterministic, a solution for $N=50$ is simply the first 50 trees of the $N=200$ solution. This allowed us to optimize submission generation to be nearly instantaneous.

## Model Benchmarks (Final Scores)

| N | Greedy Baseline | Bio-Growth | **Crystal Growth (Centric)** | Improvement vs Baseline |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **0.845** | 1.000 | 1.000 | - |
| **50** | 0.822 | 0.904 | **0.732** | **~11%** |
| **100** | 0.860 | 0.872 | **0.632** | **~26%** |
| **200** | 0.846 | 0.864 | **0.552** | **~35%** |

## Submissions
- **Current Submission:** `results/submission.csv`
- **Method:** Generated in a single pass using the Centric Crystal model for $N=1$ to $N=200$.
- **Validation:** 100% overlap-free, verified using `shapely.strtree.STRtree`.

## Project Structure
- `src/models/`: Modular solvers including `greedy`, `bio_growth`, and the winning `crystal_growth`.
- `scripts/`: Automated runners for benchmarking and submission generation.
- `results/plots/`: Visual confirmation of the "X Pattern" and dense interlocking.
- `config/`: Centralized targets and best-known scores.