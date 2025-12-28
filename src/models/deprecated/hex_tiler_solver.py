import math
import numpy as np
from decimal import Decimal
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree

class HexTilerSolver:
    """
    Hexagonal Tiler.
    Packs 3-tree triangles into a honeycomb grid.
    """

    def __init__(self, dna=None):
        # Lattice parameters for the 3-tree unit
        # Horizontal stride (u), Vertical stride (v)
        self.stride_x = 1.05 # Stride between trio centers
        self.stride_y = 0.90 # Height between trio rows
        
        # Internal trio offsets (derived from perfect_trio.png)
        self.trio_offsets = [
            (0, 0, 0),
            (0.35, 0.8, 180),
            (0.7, 0, 0)
        ]

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        
        placed_trees = []
        n_trios = (num_trees + 2) // 3
        
        # Spiral-out through hexagonal indices (q, r)
        # Using axial coordinates for the hex grid
        limit = int(math.sqrt(n_trios)) + 3
        coords = []
        for q in range(-limit, limit + 1):
            for r in range(-limit, limit + 1):
                # Distance to center in hex-space
                dist = (abs(q) + abs(q + r) + abs(r)) / 2
                coords.append((dist, q, r))
        coords.sort()

        for _, q, r in coords:
            # Convert Axial (q, r) to Cartesian (x, y)
            # x = stride_x * (q + r/2)
            # y = stride_y * r
            bx = self.stride_x * (q + r/2.0)
            by = self.stride_y * r
            
            # Place the 3-tree unit
            for dx, dy, rot in self.trio_offsets:
                if len(placed_trees) < num_trees:
                    placed_trees.append(ChristmasTree(bx + dx, by + dy, rot))
            
            if len(placed_trees) >= num_trees:
                break

        return self._finalize(placed_trees)

    def _finalize(self, trees):
        if not trees: return [], float('inf')
        all_polygons = [t.get_polygon() for t in trees]
        
        # Check for any overlaps (Strict)
        from shapely.strtree import STRtree
        tree_index = STRtree(all_polygons)
        for i in range(len(all_polygons)):
            possible = tree_index.query(all_polygons[i])
            for idx in possible:
                if idx > i:
                    if all_polygons[i].intersects(all_polygons[idx]) and \
                       not all_polygons[i].touches(all_polygons[idx]):
                        return trees, float('inf') # OVERLAP FAILURE

        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return trees, side
