import math
import numpy as np
import sys
from decimal import Decimal
from shapely.strtree import STRtree
from shapely.ops import unary_union
from src.models.tree_geometry import ChristmasTree
from config.best_known import get_target_side

class KaleidoscopeSolver:
    """
    Kaleidoscope Solver.
    Enforces 4-fold rotational symmetry to create a perfectly balanced X-pattern.
    """

    def __init__(self, dna=None):
        if dna is None:
            dna = {
                'global_tilt': 20.41, # Optimal tilt for a single tree
                'step_size': 0.05
            }
        self.dna = dna
        self.step_size = dna.get('step_size', 0.05)
        self.global_tilt = dna.get('global_tilt', 20.41)

    def solve(self, num_trees, stop_on_failure=False):
        if num_trees == 0: return [], 0
        
        placed_trees = []
        target_side = get_target_side(num_trees)
        search_limit = (target_side / 2.0) + 2.0
        
        # We only search the positive quadrant (x > 0, y >= 0)
        # The other 3 quadrants are filled by symmetry.
        grid_range = np.arange(0, search_limit, self.step_size)
        
        search_points = []
        for y in grid_range:
            for x in grid_range:
                # Priority: Manhattan distance to center
                dist = x + y
                search_points.append((dist, x, y))
        search_points.sort()

        # We add trees in groups of 4 to maintain symmetry
        # (Handling the remainder if num_trees is not a multiple of 4)
        
        while len(placed_trees) < num_trees:
            found_set = False
            is_odd_layer = (len(placed_trees) // 4) % 2 == 1
            
            for _, sx, sy in search_points:
                # Candidates for this set of 4
                # Rotation: global_tilt + symmetry rotations
                # We alternate the internal jigsaw flip (0 or 180) based on layers
                base_angle = self.global_tilt
                if is_odd_layer:
                    base_angle += 180
                
                # The 4 symmetric rotations
                candidates = []
                # (x, y, rot) -> (-y, x, rot+90) -> (-x, -y, rot+180) -> (y, -x, rot+270)
                candidates.append((sx, sy, base_angle))
                candidates.append((-sy, sx, base_angle + 90))
                candidates.append((-sx, -sy, base_angle + 180))
                candidates.append((sy, -sx, base_angle + 270))
                
                # Check if this whole set of 4 is valid
                temp_trees = []
                for cx, cy, crot in candidates:
                    temp_trees.append(ChristmasTree(center_x=cx, center_y=cy, angle=crot))
                
                if self._is_set_valid(temp_trees, placed_trees):
                    # Add as many as we need from this set
                    for t in temp_trees:
                        if len(placed_trees) < num_trees:
                            placed_trees.append(t)
                    found_set = True
                    break
            
            if not found_set:
                print("Kaleidoscope failed to find symmetric set.")
                if stop_on_failure: sys.exit(1)
                return [], float('inf')

        return self._finalize(placed_trees)

    def _is_set_valid(self, new_set, existing):
        # 1. Check set against existing
        all_existing_polys = [t.get_polygon() for t in existing]
        tree_index = STRtree(all_existing_polys) if all_existing_polys else None
        
        new_polys = [t.get_polygon() for t in new_set]
        
        for i, poly in enumerate(new_polys):
            # Check against already placed
            if tree_index:
                possible = tree_index.query(poly)
                if any(poly.intersects(all_existing_polys[idx]) and \
                       not poly.touches(all_existing_polys[idx]) for idx in possible):
                    return False
            
            # 2. Check against other trees in the same new set
            for j in range(i + 1, len(new_polys)):
                if poly.intersects(new_polys[j]) and not poly.touches(new_polys[j]):
                    return False
                    
        return True

    def _finalize(self, trees):
        if not trees: return [], float('inf')
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return trees, side
