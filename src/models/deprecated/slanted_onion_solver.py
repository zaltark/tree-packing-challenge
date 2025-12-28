import math
import numpy as np
import sys
from decimal import Decimal
from shapely.strtree import STRtree
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree

class SlantedOnionSolver:
    """
    Staggered Onion Solver with Safety Discovery.
    Finds the absolute minimum safe distances for checkerboard interlocking.
    """

    def __init__(self):
        # We find these values dynamically
        self.dx = 0.0
        self.dy = 0.0

    def _find_safe_strides(self):
        """Discovers the tightest safe checkerboard stride."""
        # 1. Horizontal Stride (dx)
        # Tree A(0,0,0) and Tree B(dx, 0, 180)
        dx = 0.35
        while True:
            t1 = ChristmasTree(0, 0, 0)
            t2 = ChristmasTree(dx, 0, 180)
            if not t1.intersects(t2):
                break
            dx += 0.005
            
        # 2. Vertical Stride (dy)
        # Tree A(0,0,0) and Tree C(0, dy, 180)
        dy = 0.40
        while True:
            t1 = ChristmasTree(0, 0, 0)
            t2 = ChristmasTree(0, dy, 180)
            if not t1.intersects(t2):
                break
            dy += 0.005
            
        return dx, dy

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        if num_trees == 1:
            t = ChristmasTree(0, 0, 44.9)
            return [t], self._get_side([t])

        # Calibrate Strides
        self.dx, self.dy = self._find_safe_strides()
        print(f"Calibration: DX={self.dx:.3f}, DY={self.dy:.3f}")

        # 1. Generate Centered Grid
        limit = int(math.sqrt(num_trees)) + 10
        grid_points = []
        for r in range(-limit, limit):
            for c in range(-limit, limit):
                pos_x = c * self.dx
                pos_y = r * self.dy
                angle = 0 if (c + r) % 2 == 0 else 180
                dist = max(abs(pos_x), abs(pos_y))
                grid_points.append((dist, pos_x, pos_y, angle))
        
        grid_points.sort(key=lambda x: x[0])
        
        # 2. Build Tree Pack
        placed_trees = []
        for _, x, y, rot in grid_points[:num_trees]:
            placed_trees.append(ChristmasTree(center_x=x, center_y=y, angle=rot))

        return self._finalize(placed_trees, stop_on_failure)

    def _get_side(self, trees):
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        return max(bounds[2]-bounds[0], bounds[3]-bounds[1])

    def _finalize(self, trees, stop_on_failure):
        if not trees: return [], float('inf')
        
        # Validation
        polys = [t.get_polygon() for t in trees]
        tree_index = STRtree(polys)
        for i in range(len(polys)):
            possible = tree_index.query(polys[i])
            for idx in possible:
                if idx > i:
                    if polys[i].intersects(polys[idx]) and not polys[i].touches(polys[idx]):
                        print(f"Overlapping identified, cancelling model")
                        if stop_on_failure: sys.exit(1)
                        return [], float('inf')

        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return trees, side