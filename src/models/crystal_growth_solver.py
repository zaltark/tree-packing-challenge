import math
import numpy as np
import sys
from decimal import Decimal
from shapely.strtree import STRtree
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree
from config.best_known import get_target_side

class CrystalGrowthSolver:
    """
    Centric Crystal Growth Solver.
    Grows from the center outward to maintain a square aspect ratio.
    """

    def __init__(self, dna=None):
        # High precision step for interlocking
        self.step_size = 0.05 

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        
        placed_trees = []
        target_side = get_target_side(num_trees)
        
        # Pre-calculate search grid points sorted by distance from origin
        # Search area: slightly larger than target square to find best fit
        search_limit = (target_side / 2.0) + 1.0
        grid_range = np.arange(-search_limit, search_limit, self.step_size)
        
        search_points = []
        for y in grid_range:
            for x in grid_range:
                # We sort by Manhattan distance or Euclidean to favor square/circle growth
                # Using max(abs(x), abs(y)) favors square growth!
                dist = max(abs(x), abs(y))
                search_points.append((dist, x, y))
        
        # Sort points: search closest to center first
        search_points.sort()

        for n_idx in range(num_trees):
            placed_polygons = [p.get_polygon() for p in placed_trees]
            tree_index = STRtree(placed_polygons) if placed_polygons else None
            
            # Alternating Jigsaw (Up/Down)
            angle = 0 if (n_idx % 2 == 0) else 180
            tree = ChristmasTree(angle=angle)
            found_spot = False
            
            # Search for the very first point where the tree fits
            for _, x, y in search_points:
                tree.center_x, tree.center_y = Decimal(str(x)), Decimal(str(y))
                tree._update_polygon()
                
                if not tree_index:
                    tree.center_x, tree.center_y = Decimal('0'), Decimal('0')
                    tree._update_polygon()
                    found_spot = True
                    break
                
                poly = tree.get_polygon()
                # Use query for speed
                possible = tree_index.query(poly)
                
                if not any(poly.intersects(placed_polygons[i]) and \
                           not poly.touches(placed_polygons[i]) \
                           for i in possible):
                    found_spot = True
                    break
            
            if found_spot:
                placed_trees.append(tree)
                # Optimization: Optional - remove points already covered by polygons? 
                # (Too complex for now, but sorting ensures we stay tight)
            else:
                print(f"FAILED: No spot found for tree {n_idx}")
                if stop_on_failure: sys.exit(1)
                return [], float('inf')

        return self._finalize(placed_trees)

    def _finalize(self, trees):
        if not trees: return [], float('inf')
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return trees, side
