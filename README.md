# Santa 2025: Tree Packing Challenge

This repository contains a high-performance local pipeline for the Santa 2025 Tree Packing Challenge.

## Installation & Usage

### 1. Set up Environment
The `venv` folder is not included in this repository. You must create your own virtual environment and install the dependencies.

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venc\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. Run the Solver
To generate the optimization, verification, and submission file in one go:

```bash
python main.py
```
This will:
1.  Solve all 200 configurations using the Ensemble + Global Rotation strategy.
2.  Save the submission to `output/submission.csv`.
3.  Verify the score against the official metric.

## Submissions
- **Submission File:** `output/submission.csv`
- **Verified Score:** **91.11704328246536** (Improved via Odd-Tree Rotation)
- **Latest Research:**
    - **Odd-Tree Individual Rotation:** Found that rotating the "remainder" tree in odd-N sets can significantly shrink the bounding box by allowing better corner fit.
        - **N=13, 25, 49, 71, 109, 141, 193:** Optimized rotations (up to 2.3% improvement)
- **Method:** Generated using `main.py`. 
- **Optimization Pipeline:**
    1. **Target Selection:** For each N, the script selects the best layout between a mathematically optimized **Brick Grid** (via `TargetLibrary`) and a manual **Prime Seed**.
    2. **Global Rotation:** The entire tree cluster is brute-force rotated (0-180°) to minimize the bounding square, effectively aligning jagged edges diagonally to save space.
- **Validation:** 100% overlap-free, verified using the official competition metric and `shapely` spatial indices.

## Technical Constraints & Constants

### Scale Factor & Coordinate System
The competition metric scales all coordinates by a factor of **$10^{18}$** (`SCALE_FACTOR`) to perform integer-like arithmetic on the grid.
- **Input:** Floating point values (e.g., `x=0.35`).
- **Metric Internal:** `Decimal(0.35) * 1e18 = 350,000,000,000,000,000`.

### "Safe Touch" Logic
While the problem statement allows trees to "touch" (share a boundary), floating-point instability in rotation (affine transformations) can cause microscopic overlaps that invalidate a solution.
To prevent this, a shared constant `SAFE_TOUCH_BUFFER` is enforced across all solvers:
- **Value:** `1e-14`
- **Usage:** Added to all contact offsets.
    - `u_dx` (Horizontal Interlock): $0.35 + 10^{-14}$
    - `u_dy` (Interlock Lift): $0.80 + 10^{-14}$
    - `stride_x` (Horizontal): $0.70 + 2 \times 10^{-14}$
    - `stride_y` (Vertical Row): $1.00 + 10^{-13}$
This ensures that `intersects()` checks return False while maintaining near-perfect packing density.

## Project Structure
- `main.py`: **Main Pipeline**. Runs the ensemble, optimizes rotation, generates the CSV, and verifies the score.
- `solver/`: Core logic package.
    - `engine.py`: High-precision mathematical tiling model (The Champion).
    - `strategies.py`: Manual optimization for small numbers and odd remainders.
    - `geometry.py`: Verified official tree specifications and $10^{18}$ scaling.
    - `scoring.py`: Official scoring logic (Side^2 / N).
    - `targets.py`: Heuristic for mathematically ideal grid aspect ratios.
    - `io.py`: Submission CSV formatting.
- `tools/`: Helper scripts.
    - `visualize.py`: Utility to plot packing configurations.
    - `plot_submission.py`: Generates visual confirmation of the submission.
    - `proofs/`: Scripts that mathematically derive the efficiency limits and constants.
- `output/`: Generated CSVs and plots.