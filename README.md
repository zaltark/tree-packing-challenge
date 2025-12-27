# Santa 2025: Tree Packing Challenge

Repository for the Santa 2025 Tree Packing Challenge. This project has evolved from biological growth simulations to a high-performance mathematical tiling strategy.

## The Champion: Centric Crystal Growth
The current top-performing model utilizes **Centric Crystal Growth**. 

### Key Features:
- **Jigsaw Interlock:** Alternates trees between 0° and 180° rotations, allowing triangular tiers to nest perfectly into one another.
- **Centric Proactive Search:** Instead of a linear scan, the model searches for valid "rooting" spots starting from (0,0) and moving outwards using a Manhattan-distance priority ($max(|x|, |y|)$).
- **The "X Pattern":** This search strategy forces the trees into a dense, square-clump formation that expands symmetrically, often creating a visible "X" or diamond-like density pattern.
- **High Precision:** Uses a 0.05 unit step-size to find the absolute tightest safe fit without overlapping.

## Model Benchmarks (Final Scores)

| N | Greedy Baseline | Bio-Growth | Crystal Growth (Centric) | Winner |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **0.845** | 1.000 | 1.000 | Greedy |
| **50** | 0.822 | 0.904 | **0.732** | **Crystal** |
| **100** | 0.860 | 0.872 | **0.632** | **Crystal** |
| **250** | 0.846 | 0.864 | **0.552** | **Crystal** |

## Status Report
- **Greedy Baseline:** Replaced as the champion. Still useful for small N (N < 10) where local heuristics are fast.
- **Phyllotaxis (Bio-Growth):** Legacy experiment. Proved that "natural" growth is too circular for square-box competition scoring.
- **Centric Crystal:** **Current Champion.** Achieved a ~35% improvement over the baseline at N=250.

## Project Structure
- `src/models/tree_geometry.py`: Source of truth for tree dimensions and intersection rules.
- `src/models/crystal_growth_solver.py`: The winning interlocking scanline/centric model.
- `scripts/run_benchmark.py`: Comparative evaluation suite.
- `results/plots/`: Visual confirmation of valid, non-overlapping packings.
