import math
import numpy as np
import sys
from decimal import Decimal
from shapely.strtree import STRtree
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree

class BrickTilerSolver:
    """
    Robust Lattice Builder using Shell-based (Onion) growth.
    Maintains a square aspect ratio by calculating ideal row/column counts.
    """

    def __init__(self):
        # Discovered safe constants for the interlocked Jigsaw unit
        self.u_dx = 0.355  # Offset for the inverted tree
        self.u_dy = 0.805  # Offset for the inverted tree
        self.stride_x = 0.71  # Horizontal distance between bricks
        self.stride_y = 1.01  # Vertical distance between bricks

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        
        # 1. Each 'Brick' contains 2 trees.
        n_bricks = (num_trees + 1) // 2
        
        # 2. Generate the perfect lattice for bricks
        # Use the provided 'Layer by Layer' logic
        dx, dy = self.stride_x, self.stride_y
        ratio = dy / dx
        
        est_rows = math.sqrt(n_bricks / ratio)
        rows = max(1, round(est_rows))
        cols = max(1, round(n_bricks / rows))
        
        # Refine dimensions
        while rows * cols < n_bricks:
            if (cols * dx) < (rows * dy):
                cols += 1
            else:
                rows += 1
                
        # 3. Generate Centered Coordinates
        grid_points = []
        offset_c = (cols - 1) / 2.0
        offset_r = (rows - 1) / 2.0
        
        for r in range(rows):
            for c in range(cols):
                pos_x = (c - offset_c) * dx
                pos_y = (r - offset_r) * dy
                
                # Chebyshev distance for square growth
                dist = max(abs(pos_x), abs(pos_y))
                grid_points.append((dist, pos_x, pos_y))
        
        # 4. Sort by distance and pick top N bricks
        grid_points.sort(key=lambda x: x[0])
        brick_coords = grid_points[:n_bricks]
        
        # 5. Build the Tree List
        placed_trees = []
        for _, bx, by in brick_coords:
            # Tree A (Upright)
            if len(placed_trees) < num_trees:
                t_a = ChristmasTree(center_x=bx, center_y=by, angle=0)
                placed_trees.append(t_a)
            
            # Tree B (Inverted - Interlocked)
            if len(placed_trees) < num_trees:
                t_b = ChristmasTree(center_x=bx + self.u_dx, center_y=by + self.u_dy, angle=180)
                placed_trees.append(t_b)

        return self._finalize(placed_trees, stop_on_failure)

    def _finalize(self, trees, stop_on_failure):
        if not trees: return [], float('inf')
        
        # --- STRICT GLOBAL VALIDATION ---
        # We must verify before returning to ensure NO OVERLAPS
        polys = [t.get_polygon() for t in trees]
        tree_index = STRtree(polys)
        
        for i in range(len(polys)):
            possible = tree_index.query(polys[i])
            for idx in possible:
                if idx > i:
                    if polys[i].intersects(polys[idx]) and not polys[i].touches(polys[idx]):
                        print(f"Overlapping identified between tree {i} and {idx}, cancelling model")
                        if stop_on_failure: sys.exit(1)
                        return [], float('inf')

        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return trees, side
