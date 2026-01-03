import math
import numpy as np
import sys
from decimal import Decimal
from shapely.ops import unary_union
from solver.geometry import ChristmasTree, SAFE_TOUCH_BUFFER
from solver.targets import TargetLibrary

class BrickTilerSolver:
    """
    Native Grid Brick Tiler.
    Ensures every tree, even the remainder in odd N, slots perfectly into the mathematical grid.
    """

    def __init__(self):
        # High-precision interlock offsets (Exact Contact + Safety Epsilon)
        # Using SAFE_TOUCH_BUFFER as a "safe touch" buffer for float stability
        self.u_dx = 0.35 + SAFE_TOUCH_BUFFER
        self.u_dy = 0.80 + SAFE_TOUCH_BUFFER
        # Grid strides
        self.stride_x = 0.70 + (2 * SAFE_TOUCH_BUFFER)
        self.stride_y = 1.0 + (10 * SAFE_TOUCH_BUFFER)

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        if num_trees == 1:
            t = ChristmasTree(0, 0, 44.9) # Optimal single tree rotation
            return [t], self._get_side([t])

        # 1. Determine optimal grid dimensions from TargetLibrary
        target = TargetLibrary.get_target(num_trees)
        rows = target.rows
        cols = target.cols
        grid_points = []
        offset_c, offset_r = (cols - 1) / 2.0, (rows - 1) / 2.0
        for r in range(rows):
            for c in range(cols):
                pos_x, pos_y = (c - offset_c) * self.stride_x, (r - offset_r) * self.stride_y
                grid_points.append((max(abs(pos_x), abs(pos_y)), pos_x, pos_y))
        
        # Sort points to fill from center outward
        grid_points.sort()
        
        # 3. Fill the slots sequentially
        placed_trees = []
        for _, bx, by in grid_points:
            if len(placed_trees) >= num_trees: break
            
            # Add Tree A (Up)
            placed_trees.append(ChristmasTree(center_x=bx, center_y=by, angle=0))
            
            if len(placed_trees) >= num_trees: break
            
            # Add Tree B (Down)
            placed_trees.append(ChristmasTree(center_x=bx + self.u_dx, center_y=by + self.u_dy, angle=180))

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
