import math
import numpy as np
import sys
from decimal import Decimal
from shapely.strtree import STRtree
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree

class SlantedRowSolver:
    """
    Evolved Slanted Row Solver.
    Uses DNA to determine precise lattice and row jump vectors.
    """

    def __init__(self, dna=None):
        if dna is None:
            dna = {
                'u_dx': 0.355, 'u_dy': 0.805, 
                'v_dx': 0.71, 'v_dy': 0.0,
                'row_jump_x': 0.355, 'row_jump_y': 0.71
            }
        self.dna = dna

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        if num_trees == 1:
            t = ChristmasTree(0, 0, 44.9)
            return [t], self._get_side([t])

        placed_trees = []
        
        # Grid parameters from DNA
        u_dx, u_dy = self.dna['u_dx'], self.dna['u_dy']
        v_dx, v_dy = self.dna['v_dx'], self.dna['v_dy']
        rsx, rsy = self.dna['row_jump_x'], self.dna['row_jump_y']
        
        side_target = math.sqrt(num_trees * 0.35)
        # Use v_dx for column estimation
        cols = max(1, round(side_target / v_dx))
        
        for i in range(num_trees):
            brick_idx = i // 2
            is_inverted = (i % 2 == 1)
            
            row = brick_idx // cols
            col = brick_idx % cols
            
            bx = col * v_dx + row * rsx
            by = row * rsy
            
            if not is_inverted:
                tx, ty, rot = bx, by, 0
            else:
                tx, ty, rot = bx + u_dx, by + u_dy, 180
                
            tree = ChristmasTree(center_x=tx, center_y=ty, angle=rot)
            if self._has_overlap(tree, placed_trees):
                if stop_on_failure: 
                    print(f"Overlap at tree {i}, cancelling")
                    sys.exit(1)
                return [], float('inf')
            placed_trees.append(tree)

        return self._finalize(placed_trees)

    def _has_overlap(self, new_tree, existing):
        if not existing: return False
        new_poly = new_tree.get_polygon()
        for other in existing[-30:]:
            if new_poly.intersects(other.get_polygon()) and not new_poly.touches(other.get_polygon()):
                return True
        return False

    def _finalize(self, trees):
        if not trees: return [], float('inf')
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return trees, side

    def _get_side(self, trees):
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        return max(bounds[2]-bounds[0], bounds[3]-bounds[1])
