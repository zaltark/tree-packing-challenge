# Santa 2025: Tree Packing Challenge

This repository contains a high-performance local pipeline for the Santa 2025 Tree Packing Challenge. The project utilizes modular solvers and automated benchmarking to optimize the packing of Christmas tree polygons into a minimal axis-aligned bounding square.

## Current Champion: Centric Crystal Growth
Our top-performing strategy is **Centric Crystal Growth**, which treats the problem as a jigsaw tiling puzzle.

### Key Insights:
- **Jigsaw Interlocking:** Alternating tree rotations (0° and 180°) allows the jagged triangular tiers to "nest" into one another, drastically increasing density.
- **Centric Proactive Search:** By searching for valid positions starting from the origin and expanding outwards (Manhattan-distance priority), the model forces trees into a dense, square clump (the "X Pattern").
- **Optimal Tilting:** The **Kaleidoscope** model discovered that a ~45° tilt for the initial trees can squeeze the bounding box below the standard $1.0 \times 1.0$ limit for single-tree problems.

## Model Benchmarks (Final Scores)

| N | Greedy Baseline | Bio-Growth | **Crystal Growth** | **Kaleidoscope** | Winner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | 0.936 | 1.000 | 1.000 | **0.662** | **Kaleidoscope** |
| **50** | 0.889 | 1.058 | **0.744** | 0.882 | **Crystal** |
| **100** | 0.898 | 1.038 | **0.632** | 0.820 | **Crystal** |
| **200** | 0.834 | 0.977 | **0.572** | 0.881 | **Crystal** |

## Project Features
- **Privacy First:** All official competition dimensions, vertex coordinates, and target scores are stored in `config/magic_params.py` (git-ignored) to comply with data restrictions.
- **Modular Solvers:** Separate implementations for Greedy, Phyllotaxis (Bio), Lattice (Crystal), and Symmetric (Kaleidoscope) strategies.
- **Automated Validation:** 100% overlap-free solutions verified using `shapely` spatial indices.

## Usage
1. **Setup:** `pip install -r requirements.txt`
2. **Benchmark:** `python scripts/run_benchmark.py`
3. **Generate Submission:** `python scripts/generate_submission.py`