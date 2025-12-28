import math
import numpy as np
import sys
from decimal import Decimal
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree

class BrickTilerSolver:
    """
    Native Grid Brick Tiler.
    Ensures every tree, even the remainder in odd N, slots perfectly into the mathematical grid.
    """

    def __init__(self):
        # High-precision interlock offsets
        self.u_dx = 0.355
        self.u_dy = 0.805
        self.stride_x = 0.71
        self.stride_y = 1.01

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        if num_trees == 1:
            t = ChristmasTree(0, 0, 44.9)
            return [t], self._get_side([t])

        # 1. Determine how many brick slots we need
        # A brick slot has space for 2 trees.
        n_slots = (num_trees + 1) // 2
        
        # 2. Generate centered grid coordinates
        # Aspect ratio to keep it square-ish
        ratio = self.stride_y / self.stride_x
        est_rows = math.sqrt(n_slots / ratio)
        rows = max(1, round(est_rows))
        cols = max(1, round(n_slots / rows))
        while rows * cols < n_slots:
            if (cols * self.stride_x) < (rows * self.stride_y): cols += 1
            else: rows += 1
                
        grid_points = []
        offset_c, offset_r = (cols - 1) / 2.0, (rows - 1) / 2.0
        for r in range(rows):
            for c in range(cols):
                pos_x, pos_y = (c - offset_c) * self.stride_x, (r - offset_r) * self.stride_y
                # Sort by Chebyshev distance to fill square shells
                grid_points.append((max(abs(pos_x), abs(pos_y)), pos_x, pos_y))
        
        grid_points.sort()
        
        # 3. Fill the slots sequentially
        placed_trees = []
        for _, bx, by in grid_points:
            # Add Tree A (Up)
            if len(placed_trees) < num_trees:
                placed_trees.append(ChristmasTree(center_x=bx, center_y=by, angle=0))
            
            # Add Tree B (Down)
            if len(placed_trees) < num_trees:
                placed_trees.append(ChristmasTree(center_x=bx + self.u_dx, center_y=by + self.u_dy, angle=180))
            
            if len(placed_trees) >= num_trees:
                break

        return self._finalize(placed_trees)

    def _get_side(self, trees):
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        return max(bounds[2]-bounds[0], bounds[3]-bounds[1])

    def _finalize(self, trees):
        if not trees: return [], float('inf')
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return trees, side
