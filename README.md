# Santa 2025: Tree Packing Challenge

This repository contains a high-performance local pipeline for the Santa 2025 Tree Packing Challenge. The project focuses on mathematical tiling and automated optimization to solve 200 distinct geometry puzzles.

## The Mission: Total Score Optimization
The competition evaluates the **sum of scores** across 200 independent problems ($N=1$ to $N=200$). 
$$\text{Total Score} = \sum_{N=1}^{200} \frac{\max(\text{width}_N, \text{height}_N)^2}{N}$$

### Key Strategic Insight: The Stacking Unit
Our research has shown that the most efficient way to pack trees is by using a **"Slanted Brick"** unit:
- **Unit:** 2 trees interlocked (one at 0°, one at 180°).
- **Even N:** Fits perfectly into an $M \times M$ grid of bricks.
- **Odd N:** Requires a "Remainder Strategy"—placing the final single tree into the most efficient gap or corner of the existing brick grid without expanding the bounding box unnecessarily.

## Current Performance (Brick Tiler)
Our **Brick Tiler** model currently serves as the engine for all 200 problems.

| N | Model | Score | Improvement vs Baseline |
| :--- | :--- | :--- | :--- |
| **1** | Brick Tiler | 1.000 | (Baseline is better at N=1) |
| **50** | Brick Tiler | **0.528** | ~40% Better |
| **100** | Brick Tiler | **0.667** | ~25% Better |
| **200** | Brick Tiler | **0.519** | ~38% Better |

**Public Leaderboard Score:** `102.5445` (Initial robust submission).

## Project Structure
- `src/models/brick_tiler_solver.py`: The current champion. Uses mathematical stacking of interlocked tree pairs.
- `scripts/optimize_tiling.py`: Specialized tool for shrinking the spacing between bricks to find the "Stride of Perfection."
- `scripts/generate_submission.py`: Generates the 200-problem submission file in a single optimized pass.
- `config/magic_params.py`: Private competition constants (ignored by Git).

## Path Forward
1. **Precision Calibration:** Shrinking the `STRIDE_X` and `STRIDE_Y` values to the absolute physical limits.
2. **Odd-N Handling:** Optimizing the placement of the "lone tree" in odd-numbered configurations to prevent it from defining the bounding box.
3. **Corner Plugging:** Identifying if single trees can be used to fill the jagged "sawtooth" edges of the brick grid.
