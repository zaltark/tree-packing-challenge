import math
import numpy as np
import sys
from decimal import Decimal
from shapely.strtree import STRtree
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree

class CrystalGrowthSolver:
    """
    Centric Crystal Growth Solver optimized for fast nested solutions.
    """

    def __init__(self, dna=None):
        self.step_size = 0.05 

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        
        placed_trees = []
        
        # Fixed large search area to ensure consistency across N
        # N=200 needs a side of ~11, so a limit of 10.0 (covering -10 to 10) is safe.
        search_limit = 15.0 
        grid_range = np.arange(-search_limit, search_limit, self.step_size)
        
        # Pre-sort grid points by square-distance once
        search_points = []
        for y in grid_range:
            for x in grid_range:
                dist = max(abs(x), abs(y))
                search_points.append((dist, x, y))
        search_points.sort()

        for n_idx in range(num_trees):
            placed_polygons = [p.get_polygon() for p in placed_trees]
            tree_index = STRtree(placed_polygons) if placed_polygons else None
            
            angle = 0 if (n_idx % 2 == 0) else 180
            tree = ChristmasTree(angle=angle)
            found_spot = False
            
            for _, x, y in search_points:
                tree.center_x, tree.center_y = Decimal(str(round(x, 3))), Decimal(str(round(y, 3)))
                tree._update_polygon()
                
                if not tree_index:
                    tree.center_x, tree.center_y = Decimal('0'), Decimal('0')
                    tree._update_polygon()
                    found_spot = True
                    break
                
                poly = tree.get_polygon()
                possible = tree_index.query(poly)
                if not any(poly.intersects(placed_polygons[i]) and \
                           not poly.touches(placed_polygons[i]) \
                           for i in possible):
                    found_spot = True
                    break
            
            if found_spot:
                placed_trees.append(tree)
            else:
                print(f"FAILED: No spot found for tree {n_idx}")
                if stop_on_failure: sys.exit(1)
                return [], float('inf')

        all_polygons = [t.get_polygon() for t in placed_trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return placed_trees, side