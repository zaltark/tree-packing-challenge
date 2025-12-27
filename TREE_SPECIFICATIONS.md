# Santa 2025: Tree Packing Challenge - Tree Specifications

This document serves as the geometric reference for the Christmas Tree objects and the scoring logic required for the packing challenge.

## 1. Tree Geometry (Relative to Center 0,0)
The tree is a polygon defined by the following vertices (before rotation or translation).

| Part | X-Coordinate | Y-Coordinate |
| :--- | :--- | :--- |
| **Tip** | 0.0 | 0.8 |
| **R-Top Tier** | 0.125 | 0.5 |
| **R-Mid Tier** | 0.2 | 0.25 |
| **R-Base** | 0.35 | 0.0 |
| **R-Trunk** | 0.075 | 0.0 |
| **R-Trunk Bottom** | 0.075 | -0.2 |
| **L-Trunk Bottom** | -0.075 | -0.2 |
| **L-Trunk** | -0.075 | 0.0 |
| **L-Base** | -0.35 | 0.0 |
| **L-Mid Tier** | -0.2 | 0.25 |
| **L-Top Tier** | -0.125 | 0.5 |

### Dimensions Summary
- **Trunk Width:** 0.15
- **Trunk Height:** 0.2
- **Base Width:** 0.7
- **Middle Tier Width:** 0.4
- **Top Tier Width:** 0.25
- **Total Height:** 1.0 (from y=-0.2 to y=0.8)

---

## 2. Constraints & Scoring Logic

### Constraints
- **Coordinate Limits:** All points of the tree polygons must stay within the range `[-100, 100]` for both `x` and `y`.
- **No Overlap:** Trees are not allowed to intersect. They may touch at edges or vertices.
- **Rotation:** Trees can be rotated by an angle $\theta$.

### Scoring Formula
The goal is to minimize the final score:

$$Score = \frac{SideLength^2}{N}$$

Where:
- **SideLength:** The side length of the smallest axis-aligned bounding square that contains all placed trees.
- **N:** The total number of trees successfully packed.

---

## 3. Implementation Notes
- **Precision:** The challenge uses `Decimal` with 25-place precision.
- **Scaling:** A scale factor of $10^{18}$ is applied to coordinates during geometric operations to maintain precision.
- **Library:** `shapely` is the standard library for handling these polygons and checking for overlaps.
