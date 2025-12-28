import math
import numpy as np
import sys
from decimal import Decimal
from shapely.strtree import STRtree
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree

class BrickStackerSolver:
    """
    Tiling/Stacking solver.
    Packs 'Slanted Bricks' (interlocked tree pairs) into a sheared lattice.
    """

    def __init__(self, dna=None):
        """
        dna dictionary contains:
        - block_dx, block_dy: Relative offset between Tree A and Tree B.
        - v1_x, v1_y: Horizontal lattice vector (row spacing).
        - v2_x, v2_y: Sheared vertical lattice vector (column spacing).
        """
        if dna is None:
            # High-performing defaults for interlocked pairs
            dna = {
                'block_dx': 0.35, 'block_dy': 0.8,
                'v1_x': 0.7, 'v1_y': 0.0,
                'v2_x': 0.175, 'v2_y': 0.8
            }
        self.dna = dna

    def solve(self, num_trees, stop_on_failure=False):
        placed_trees = []
        
        # Unit Cell offsets
        u_dx = float(self.dna['block_dx'])
        u_dy = float(self.dna['block_dy'])
        
        # Lattice Vectors
        v1 = (float(self.dna['v1_x']), float(self.dna['v1_y']))
        v2 = (float(self.dna['v2_x']), float(self.dna['v2_y']))
        
        # Estimate grid dimensions (we need num_trees/2 unit cells)
        n_cells = (num_trees + 1) // 2
        grid_dim = int(math.sqrt(n_cells)) + 2
        
        # Spiral-out coordinate indices (i, j) to grow from center
        indices = []
        for i in range(-grid_dim, grid_dim):
            for j in range(-grid_dim, grid_dim):
                indices.append((i**2 + j**2, i, j))
        indices.sort()
        
        for _, i, j in indices:
            # Base lattice point
            bx = i * v1[0] + j * v2[0]
            by = i * v1[1] + j * v2[1]
            
            # Place Tree A (Upright)
            if len(placed_trees) < num_trees:
                tree_a = ChristmasTree(center_x=bx, center_y=by, angle=0)
                if not self._check_validity(tree_a, placed_trees):
                    if stop_on_failure: 
                        print("Overlapping identified, cancelling model")
                        sys.exit(1)
                    return [], float('inf')
                placed_trees.append(tree_a)
                
            # Place Tree B (Inverted - The Interlock)
            if len(placed_trees) < num_trees:
                tree_b = ChristmasTree(center_x=bx + u_dx, center_y=by + u_dy, angle=180)
                if not self._check_validity(tree_b, placed_trees):
                    if stop_on_failure:
                        print("Overlapping identified, cancelling model")
                        sys.exit(1)
                    return [], float('inf')
                placed_trees.append(tree_b)
                
            if len(placed_trees) >= num_trees: break
            
        return self._finalize(placed_trees)

    def _check_validity(self, new_tree, existing):
        if not existing: return True
        new_poly = new_tree.get_polygon()
        # Fast neighbor check
        for other in existing[-20:]:
            if new_poly.intersects(other.get_polygon()) and not new_poly.touches(other.get_polygon()):
                return False
        return True

    def _finalize(self, trees):
        if not trees: return [], float('inf')
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return trees, side
