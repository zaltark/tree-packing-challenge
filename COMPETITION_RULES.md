# Santa 2025: Official Competition Rules & Specifications

This document outlines the strict technical requirements and scoring mechanics for the Santa 2025 Tree Packing Challenge.

## 1. Exact Tree Geometry
The tree is a fixed-size polygon defined using the following parameters (relative to center 0,0).

### Dimensions
- **Trunk:** Width 0.15, Height 0.2 (Bottom Y: -0.2)
- **Top Tier Width:** 0.25 (at Y=0.5)
- **Middle Tier Width:** 0.4 (at Y=0.25)
- **Base Width:** 0.7 (at Y=0.0)
- **Tip Height:** 0.8

### Polygon Vertices (Clockwise from Tip)
1.  `(0.0, 0.8)` - Tip
2.  `(0.125, 0.5)` - Top Tier (Right Outer)
3.  `(0.0625, 0.5)` - Top Tier (Right Inner)
4.  `(0.2, 0.25)` - Middle Tier (Right Outer)
5.  `(0.1, 0.25)` - Middle Tier (Right Inner)
6.  `(0.35, 0.0)` - Bottom Tier (Right Outer)
7.  `(0.075, 0.0)` - Trunk (Right Top)
8.  `(0.075, -0.2)` - Trunk (Right Bottom)
9.  `(-0.075, -0.2)` - Trunk (Left Bottom)
10. `(-0.075, 0.0)` - Trunk (Left Top)
11. `(-0.35, 0.0)` - Bottom Tier (Left Outer)
12. `(-0.1, 0.25)` - Middle Tier (Left Inner)
13. `(-0.2, 0.25)` - Middle Tier (Left Outer)
14. `(-0.0625, 0.5)` - Top Tier (Left Inner)
15. `(-0.125, 0.5)` - Top Tier (Left Outer)

---

## 2. Submission & Formatting Rules
Submissions must strictly adhere to the following string-based format to prevent precision loss.

- **Header:** `id,x,y,deg`
- **Prefix Requirement:** All numeric values (`x`, `y`, `deg`) must be strings starting with the character 's'. 
  - *Example:* `s0.5`, `s-10.22`, `s90.0`.
- **Coordinate Bounds:** All points of all polygons must be within `[-100, 100]` for both X and Y.
- **ID Format:** `ProblemID_TreeIndex` (e.g., `002_0`, `002_1`).

---

## 3. Scoring & Technical Constraints
- **Precision:** Uses Python's `decimal` library with `getcontext().prec = 25`.
- **Scaling:** A scale factor of $1 \times 10^{18}$ is applied during geometry operations to ensure absolute precision.
- **Collisions:**
  - **Allowed:** Touching (Sharing a boundary/edge).
  - **Forbidden:** Overlapping (Sharing interior points).
- **Formula:**
  $$\text{Group Score} = \frac{\max(\text{width}, \text{height})^2}{N}$$
- **Final Score:** The sum of all Group Scores for $N=1$ to $N=200$.
